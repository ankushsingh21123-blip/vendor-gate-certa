"""Original synthetic vendor due-diligence API. Not Certa software."""
import os, sqlite3, json, secrets, datetime, re
from urllib.parse import urlparse
from contextlib import contextmanager
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='../static')
app.config.update(MAX_CONTENT_LENGTH=32768,SECRET_KEY=os.environ.get('SESSION_SECRET') or secrets.token_hex(32))
DB = os.environ.get('VENDOR_DB_PATH','/tmp/vendor-gate.sqlite3')
REQUIREMENTS = {'low':['business'], 'medium':['business','privacy'], 'high':['business','privacy','security','financial']}

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
@contextmanager
def db():
    c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
    c.execute('PRAGMA foreign_keys=ON');c.execute('PRAGMA journal_mode=WAL')
    try: yield c; c.commit()
    except: c.rollback(); raise
    finally: c.close()

def init_db():
    with db() as c:
        c.executescript('''CREATE TABLE IF NOT EXISTS workspaces(id TEXT PRIMARY KEY,created TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS vendors(id TEXT PRIMARY KEY,workspace TEXT NOT NULL REFERENCES workspaces(id),name TEXT NOT NULL,category TEXT NOT NULL,country TEXT NOT NULL,amount INTEGER NOT NULL CHECK(amount>=0),data_access TEXT NOT NULL,risk TEXT NOT NULL,status TEXT NOT NULL,version INTEGER NOT NULL DEFAULT 1,created TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS evidence(id TEXT PRIMARY KEY,vendor TEXT NOT NULL REFERENCES vendors(id),kind TEXT NOT NULL,reference TEXT NOT NULL,created TEXT NOT NULL,UNIQUE(vendor,kind));
CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY AUTOINCREMENT,vendor TEXT NOT NULL REFERENCES vendors(id),action TEXT NOT NULL,detail TEXT NOT NULL,created TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS vendor_workspace ON vendors(workspace);''')

def risk_for(amount, data, country):
    score=(2 if amount>=100000 else 1 if amount>=20000 else 0)+(2 if data=='sensitive' else 1 if data=='personal' else 0)+(1 if country not in ['India','United Kingdom','United States','Singapore'] else 0)
    return 'high' if score>=3 else 'medium' if score>=1 else 'low'

def record(c,vid,action,detail): c.execute('INSERT INTO audit(vendor,action,detail,created) VALUES(?,?,?,?)',(vid,action,detail,now()))
def workspace():
    token=request.headers.get('X-Workspace','')
    if not re.fullmatch('[a-f0-9]{32}', token): return None
    with db() as c:return token if c.execute('SELECT 1 FROM workspaces WHERE id=?',(token,)).fetchone() else None

def detail(c,row):
    v=dict(row);v['evidence']=[dict(x) for x in c.execute('SELECT kind,reference,created FROM evidence WHERE vendor=? ORDER BY kind',(v['id'],))]
    v['required']=REQUIREMENTS[v['risk']];v['missing']=[r for r in v['required'] if r not in [e['kind'] for e in v['evidence']]]
    v['audit']=[dict(x) for x in c.execute('SELECT action,detail,created FROM audit WHERE vendor=? ORDER BY id DESC',(v['id'],))]
    return v
@app.before_request
def auth():
    if request.method in ['POST','PATCH','DELETE','PUT'] and request.path.startswith('/api/'):
        origin=request.headers.get('Origin')
        if origin and urlparse(origin).netloc!=request.host:return jsonify(error='Cross-origin writes are not allowed.'),403
    if request.path.startswith('/api/') and request.path not in ['/api/health','/api/workspaces']:
        request.workspace=workspace()
        if not request.workspace:return jsonify(error='This demo session has expired. Start a new workspace.'),401
@app.after_request
def headers(r):
    r.headers['Cache-Control']='no-store';r.headers['X-Content-Type-Options']='nosniff';r.headers['Referrer-Policy']='same-origin';return r
@app.errorhandler(413)
def large(e): return jsonify(error='Request too large.'),413
@app.route('/api/health')
def health():
    with db() as c:c.execute('SELECT 1').fetchone()
    return jsonify(ok=True,project='vendor-gate',storage='sqlite',synthetic=True)
@app.post('/api/workspaces')
def create_workspace():
    token=secrets.token_hex(16)
    with db() as c:
        cutoff=(datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(days=7)).isoformat()
        expired=[r['id'] for r in c.execute('SELECT id FROM workspaces WHERE created<?',(cutoff,))]
        for old in expired:
            c.execute('DELETE FROM audit WHERE vendor IN (SELECT id FROM vendors WHERE workspace=?)',(old,))
            c.execute('DELETE FROM evidence WHERE vendor IN (SELECT id FROM vendors WHERE workspace=?)',(old,))
            c.execute('DELETE FROM vendors WHERE workspace=?',(old,));c.execute('DELETE FROM workspaces WHERE id=?',(old,))
        if c.execute('SELECT count(*) FROM workspaces').fetchone()[0]>=100:return jsonify(error='This demo is at capacity. Try again after workspace expiry.'),503
        c.execute('INSERT INTO workspaces VALUES(?,?)',(token,now()))
        for name,cat,country,amount,data in [('Northstar Cloud','Software','India',35000,'personal'),('Maple Office','Facilities','United Kingdom',8500,'none'),('Harbor Analytics','Data services','Singapore',120000,'sensitive')]:
            vid=secrets.token_hex(8);risk=risk_for(amount,data,country)
            c.execute('INSERT INTO vendors VALUES(?,?,?,?,?,?,?,?,?,?,?)',(vid,token,name,cat,country,amount,data,risk,'draft',1,now()))
            record(c,vid,'created','Synthetic seed vendor created')
    return jsonify(workspace=token),201
@app.route('/api/vendors', methods=['GET','POST'])
def vendors():
    with db() as c:
        if request.method=='GET':return jsonify(vendors=[detail(c,x) for x in c.execute('SELECT * FROM vendors WHERE workspace=? ORDER BY created DESC',(request.workspace,))])
        data=request.get_json(silent=True) or {}
        if c.execute('SELECT count(*) FROM vendors WHERE workspace=?',(request.workspace,)).fetchone()[0]>=40:return jsonify(error='Demo limit: 40 vendors per workspace.'),429
        name=str(data.get('name','')).strip();cat=str(data.get('category','')).strip();country=str(data.get('country','')).strip();access=data.get('data_access')
        try: amount=int(data.get('amount',-1))
        except (ValueError,TypeError):amount=-1
        errors={}
        if not 2<=len(name)<=80:errors['name']='Enter 2–80 characters.'
        if cat not in ['Software','Facilities','Data services','Consulting']:errors['category']='Choose a valid category.'
        if country not in ['India','United Kingdom','United States','Singapore','Other']:errors['country']='Choose a country.'
        if not 0<=amount<=10000000:errors['amount']='Enter an annual amount between 0 and 10,000,000.'
        if access not in ['none','personal','sensitive']:errors['data_access']='Choose a data access level.'
        if c.execute('SELECT 1 FROM vendors WHERE workspace=? AND lower(name)=lower(?)',(request.workspace,name)).fetchone():errors['name']='A vendor with this name already exists.'
        if errors:return jsonify(error='Check the highlighted fields.',fields=errors),422
        vid=secrets.token_hex(8);risk=risk_for(amount,access,country)
        c.execute('INSERT INTO vendors VALUES(?,?,?,?,?,?,?,?,?,?,?)',(vid,request.workspace,name,cat,country,amount,access,risk,'draft',1,now()))
        record(c,vid,'created',f'Risk calculated: {risk}')
        return jsonify(vendor=detail(c,c.execute('SELECT * FROM vendors WHERE id=?',(vid,)).fetchone())),201
@app.route('/api/vendors/<vid>',methods=['GET','PATCH'])
def vendor(vid):
    with db() as c:
        row=c.execute('SELECT * FROM vendors WHERE id=? AND workspace=?',(vid,request.workspace)).fetchone()
        if not row:return jsonify(error='Vendor not found in this workspace.'),404
        if request.method=='GET':return jsonify(vendor=detail(c,row))
        d=request.get_json(silent=True) or {}
        if d.get('version')!=row['version']:return jsonify(error='Another change was saved. Refresh this vendor before continuing.',conflict=True),409
        action=d.get('action')
        if action=='evidence':
            kind=d.get('kind');reference=str(d.get('reference','')).strip()
            if kind not in REQUIREMENTS[row['risk']]:return jsonify(error='Evidence type is not required for this risk level.'),422
            if not 5<=len(reference)<=180:return jsonify(error='Evidence reference must be 5–180 characters.'),422
            if row['status']=='approved':return jsonify(error='Approved vendors are locked. Reopen review first.'),409
            c.execute('INSERT INTO evidence VALUES(?,?,?,?,?) ON CONFLICT(vendor,kind) DO UPDATE SET reference=excluded.reference,created=excluded.created',(secrets.token_hex(8),vid,kind,reference,now()))
            record(c,vid,'evidence',f'{kind}: {reference}')
        elif action=='transition':
            target=d.get('status');allowed={'draft':['review'],'review':['approved','draft'],'approved':['review']}
            if target not in allowed[row['status']]:return jsonify(error='This status transition is not allowed.'),422
            v=detail(c,row)
            if target=='approved' and v['missing']:return jsonify(error='Approval blocked: missing '+', '.join(v['missing']),missing=v['missing']),422
            c.execute('UPDATE vendors SET status=? WHERE id=?',(target,vid));record(c,vid,'status',f'{row["status"]} → {target}')
        else:return jsonify(error='Unknown update action.'),422
        c.execute('UPDATE vendors SET version=version+1 WHERE id=?',(vid,))
        return jsonify(vendor=detail(c,c.execute('SELECT * FROM vendors WHERE id=?',(vid,)).fetchone()))
@app.route('/',defaults={'path':''})
@app.route('/<path:path>')
def serve_app(path):
    folder=os.path.abspath(app.static_folder)
    return send_from_directory(folder,path if path and os.path.isfile(os.path.join(folder,path)) else 'index.html')
init_db()
if __name__=='__main__':app.run(port=4178)
