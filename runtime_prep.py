"""Reviewed portable runtime supplement. Extract only into an owned repo checkout."""
import pathlib
FILES = {'.dockerignore': '.git\n'
                  'node_modules\n'
                  'web/node_modules\n'
                  '.venv\n'
                  '__pycache__\n'
                  '.pytest_cache\n'
                  '*.sqlite*\n'
                  '.env*\n'
                  'static\n'
                  'playwright-report\n'
                  'test-results\n'
                  'source_bundle.py\n',
 '.gitignore': 'node_modules/\n'
               'static/\n'
               '.env*\n'
               '!.env.example\n'
               '*.sqlite*\n'
               '__pycache__/\n'
               '.pytest_cache/\n'
               '\n'
               '.venv/\n',
 'DEPLOYMENT.md': '# Persistent-disk deployment preparation\n'
                  '\n'
                  'This recipe is unhosted. No provider account, terms, payment, database or remote '
                  "resources have been created by adding it. A provider's free offer and writable persistent "
                  'mount still need verification before deployment.\n'
                  '\n'
                  '## Container contract\n'
                  '\n'
                  '- Build with `docker build -t vendor-gate .`.\n'
                  '- Mount a NEW dedicated writable volume at `/data`.\n'
                  "- Set `VENDOR_DB_PATH=/data/vendor-gate.sqlite3` and `PORT` to the platform's assigned "
                  'port.\n'
                  '- Start the image normally. Gunicorn binds `0.0.0.0:$PORT` with one worker, appropriate '
                  'for this bounded SQLite demo.\n'
                  '- Read `/api/health` to check process and database access. Open `/` to check the built '
                  'frontend.\n'
                  '- Create a synthetic workspace and vendor, replace the container on the same volume, and '
                  'verify the saved vendor and audit history from the same workspace.\n'
                  '- Do not use serverless ephemeral `/tmp` as durable storage, repurpose an existing '
                  'database, or scale replicas independently against separate SQLite files.\n'
                  '\n'
                  '`python test_runtime.py` checks the production launcher on a disposable local database '
                  'and nondefault port. It creates a vendor, stops and replaces the process with the same '
                  'database, and verifies vendor/audit persistence. This is a LOCAL PROCESS test, not a '
                  'Docker or hosting test. Container and selected-provider acceptance remain separate work.\n'
                  '\n'
                  'No secrets, personal data or customer data belong in this synthetic portfolio demo. '
                  'Workspace tokens are bearer credentials, not real account authentication. Existing '
                  'seven-day cleanup and demo caps still apply.\n',
 'Dockerfile': 'FROM node:22-slim AS frontend\n'
               'WORKDIR /app\n'
               'COPY package.json package-lock.json vite.config.ts ./\n'
               'COPY web ./web\n'
               'RUN npm ci --ignore-scripts && npm run build\n'
               '\n'
               'FROM python:3.12-slim\n'
               'ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=4178 '
               'VENDOR_DB_PATH=/data/vendor-gate.sqlite3\n'
               'WORKDIR /app\n'
               'COPY requirements.txt ./\n'
               'RUN pip install --no-cache-dir -r requirements.txt && groupadd -g 10001 demo && useradd -u '
               '10001 -g demo -M demo && mkdir /data && chown demo:demo /data\n'
               'COPY api ./api\n'
               'COPY start.sh ./\n'
               'COPY --from=frontend /app/static ./static\n'
               'USER demo\n'
               'EXPOSE 4178\n'
               'CMD ["sh","start.sh"]\n',
 'README.md': '# Vendor Gate\n'
              '\n'
              'An original, AI-assisted synthetic vendor due-diligence workspace built for a frontend '
              'engineering portfolio. Not affiliated with Certa. Not an employer assessment, production '
              'compliance system, real-customer project or claim of unaided authorship.\n'
              '\n'
              '## Current status\n'
              '\n'
              'Local implementation and tests complete. **Not deployed yet.** No hosted persistence claim. A '
              'SQLite file in a serverless `/tmp` directory is not durable storage, and is not a supported '
              'production deployment for this project.\n'
              '\n'
              '## Role-specific implementation\n'
              '\n'
              '- React/TypeScript interface with nested protected routes and URL-backed register filters.\n'
              '- Original vendor schema, risk rules, evidence checklist, approval state machine and '
              'server-recorded audit trail.\n'
              '- Client loading, offline, validation, missing-vendor and expired-session states.\n'
              '- Approval blocked server-side until risk-dependent evidence is recorded. Approved vendors '
              'lock evidence until review is reopened.\n'
              '- Every change carries an optimistic version. Stale tabs receive 409 instead of overwriting '
              'another change.\n'
              '- Isolated random demo workspace tokens, seven-day cleanup, 100-workspace and 40-vendor caps, '
              'same-origin writes and parameterized SQL.\n'
              '- Desktop table becomes stacked cards on mobile. Keyboard focus, labels, live status and '
              'inert text rendering.\n'
              '\n'
              '## Stack\n'
              '\n'
              'React, TypeScript, React Router and Vite frontend; Python Flask HTTP API; SQLite persistence. '
              'The workspace token is a bearer credential stored in sessionStorage, not a real user '
              'authentication system. Synthetic data only. Do not enter customer, personal or confidential '
              'information. There is no document authenticity check, sanctions screening or AI risk '
              'prediction.\n'
              '\n'
              '## Run locally\n'
              '\n'
              'Use Node 22+ and Python 3.10+.\n'
              '\n'
              '```\n'
              'npm ci\n'
              'python -m pip install -r requirements.txt\n'
              'npm run build\n'
              'python api/index.py\n'
              '```\n'
              '\n'
              'Open http://127.0.0.1:4178. `VENDOR_DB_PATH` chooses the SQLite database file, default '
              '`/tmp/vendor-gate.sqlite3`. For persistent hosting it MUST point to a supported persistent '
              'disk. Back up demo data only if needed; it is disposable and expires after seven days. '
              '`SESSION_SECRET` is optional in the current bearer-session design, reserved for future '
              'signed-session work. Never commit secrets.\n'
              '\n'
              '## Verify\n'
              '\n'
              '```\n'
              'python -m unittest test_api -v\n'
              'npm test\n'
              'npx playwright install chromium\n'
              'npx playwright test\n'
              '```\n'
              '\n'
              'Playwright starts the Flask server automatically. Set `VENDOR_TEST_SERVER` only if a custom '
              'virtual-environment command is needed. No credentials are required.\n'
              '\n'
              '24 November 2026 local evidence: 15 API tests, 11 component/model tests and 3 browser '
              'scenarios passed. Browser scenarios exercise validation, evidence-gated approval, reload '
              'persistence, re-open review, filters, expired sessions and offline errors. Responsive '
              'screenshots at 320, 390 and 1280 pixels were inspected. `npm audit` reported zero known '
              'advisories at that check. These are local results, not hosted acceptance or a security '
              'certification.\n'
              '\n'
              '## State ownership\n'
              '\n'
              'URL search parameters own filters. Browser sessionStorage owns only the isolated workspace '
              'identifier. The server owns vendor state, risk, evidence, version and audit events. Risk '
              'rules and evidence gates cannot be bypassed by changing browser controls.\n'
              '\n'
              '## Risk rules\n'
              '\n'
              'Annual USD amount: <20k = 0, 20k–99,999 = 1, >=100k = 2. Data: none = 0, personal = 1, '
              'sensitive = 2. Country: India/UK/US/Singapore = 0, other = 1. Score 0 is low, 1–2 medium, 3+ '
              'high. Low requires business evidence, medium adds privacy, high adds security and financial. '
              'These arbitrary demo rules are transparent, not legal or compliance recommendations.\n'
              '\n'
              '## Limitations\n'
              '\n'
              'No real login, role-based authorization, signed audit export, malware/file scanning or '
              'production anti-abuse controls. A workspace bearer token must not be used for private '
              'records. SQLite serializes writes and suits this bounded single-worker demo, not a scaled '
              'multi-instance service. Public anonymous workspace creation can exhaust the cap. Add shared '
              'edge throttling before open production use. No paid host, card, trial or automatic upgrade is '
              'part of this source.\n'
              '\n'
              'MIT-licensed project code. React/React Router/Vite/Vitest/Flask and other dependencies retain '
              'their own licences. Substantial AI assistance was used for implementation, debugging and '
              'tests.\n'
              '\n'
              '## Alternative hosting adapter, prepared locally\n'
              '\n'
              '`worker/` contains an original Workers/D1 adapter with 15 SQLite-backed contract tests and 3 '
              'passing browser scenarios. No Cloudflare Worker or D1 database exists yet. These are local '
              'simulations, not production runtime or remote durability proof. See `worker/README.md` for '
              'the held prerequisites. The example configuration intentionally has no real database ID.\n'
              '\n'
              '## Portable deployment preparation, 25 November\n'
              '\n'
              '`start.sh` uses Gunicorn, one worker and the assigned `PORT`, binding all interfaces. '
              '`Dockerfile` and `.dockerignore` prepare a non-root image and dedicated persistent `/data` '
              'mount. Local acceptance of production-process replacement passed: frontend, database health, '
              'evidence/audit persistence on a nondefault port. This is not a Docker run or a provider '
              'deployment. See `DEPLOYMENT.md`; the account, final free offer and supported storage must '
              'still be checked.\n',
 'api/index.py': '"""Original synthetic vendor due-diligence API. Not Certa software."""\n'
                 'import os, sqlite3, json, secrets, datetime, re\n'
                 'from urllib.parse import urlparse\n'
                 'from contextlib import contextmanager\n'
                 'from flask import Flask, request, jsonify, send_from_directory\n'
                 '\n'
                 "app = Flask(__name__, static_folder='../static')\n"
                 "app.config.update(MAX_CONTENT_LENGTH=32768,SECRET_KEY=os.environ.get('SESSION_SECRET') or "
                 'secrets.token_hex(32))\n'
                 "DB = os.environ.get('VENDOR_DB_PATH','/tmp/vendor-gate.sqlite3')\n"
                 "REQUIREMENTS = {'low':['business'], 'medium':['business','privacy'], "
                 "'high':['business','privacy','security','financial']}\n"
                 '\n'
                 'def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()\n'
                 '@contextmanager\n'
                 'def db():\n'
                 '    c=sqlite3.connect(DB);c.row_factory=sqlite3.Row\n'
                 "    c.execute('PRAGMA foreign_keys=ON');c.execute('PRAGMA journal_mode=WAL')\n"
                 '    try: yield c; c.commit()\n'
                 '    except: c.rollback(); raise\n'
                 '    finally: c.close()\n'
                 '\n'
                 'def init_db():\n'
                 '    with db() as c:\n'
                 "        c.executescript('''CREATE TABLE IF NOT EXISTS workspaces(id TEXT PRIMARY "
                 'KEY,created TEXT NOT NULL);\n'
                 'CREATE TABLE IF NOT EXISTS vendors(id TEXT PRIMARY KEY,workspace TEXT NOT NULL REFERENCES '
                 'workspaces(id),name TEXT NOT NULL,category TEXT NOT NULL,country TEXT NOT NULL,amount '
                 'INTEGER NOT NULL CHECK(amount>=0),data_access TEXT NOT NULL,risk TEXT NOT NULL,status TEXT '
                 'NOT NULL,version INTEGER NOT NULL DEFAULT 1,created TEXT NOT NULL);\n'
                 'CREATE TABLE IF NOT EXISTS evidence(id TEXT PRIMARY KEY,vendor TEXT NOT NULL REFERENCES '
                 'vendors(id),kind TEXT NOT NULL,reference TEXT NOT NULL,created TEXT NOT '
                 'NULL,UNIQUE(vendor,kind));\n'
                 'CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY AUTOINCREMENT,vendor TEXT NOT NULL '
                 'REFERENCES vendors(id),action TEXT NOT NULL,detail TEXT NOT NULL,created TEXT NOT NULL);\n'
                 "CREATE INDEX IF NOT EXISTS vendor_workspace ON vendors(workspace);''')\n"
                 '\n'
                 'def risk_for(amount, data, country):\n'
                 "    score=(2 if amount>=100000 else 1 if amount>=20000 else 0)+(2 if data=='sensitive' "
                 "else 1 if data=='personal' else 0)+(1 if country not in ['India','United Kingdom','United "
                 "States','Singapore'] else 0)\n"
                 "    return 'high' if score>=3 else 'medium' if score>=1 else 'low'\n"
                 '\n'
                 "def record(c,vid,action,detail): c.execute('INSERT INTO "
                 "audit(vendor,action,detail,created) VALUES(?,?,?,?)',(vid,action,detail,now()))\n"
                 'def workspace():\n'
                 "    token=request.headers.get('X-Workspace','')\n"
                 "    if not re.fullmatch('[a-f0-9]{32}', token): return None\n"
                 "    with db() as c:return token if c.execute('SELECT 1 FROM workspaces WHERE "
                 "id=?',(token,)).fetchone() else None\n"
                 '\n'
                 'def detail(c,row):\n'
                 "    v=dict(row);v['evidence']=[dict(x) for x in c.execute('SELECT kind,reference,created "
                 "FROM evidence WHERE vendor=? ORDER BY kind',(v['id'],))]\n"
                 "    v['required']=REQUIREMENTS[v['risk']];v['missing']=[r for r in v['required'] if r not "
                 "in [e['kind'] for e in v['evidence']]]\n"
                 "    v['audit']=[dict(x) for x in c.execute('SELECT action,detail,created FROM audit WHERE "
                 "vendor=? ORDER BY id DESC',(v['id'],))]\n"
                 '    return v\n'
                 '@app.before_request\n'
                 'def auth():\n'
                 "    if request.method in ['POST','PATCH','DELETE','PUT'] and "
                 "request.path.startswith('/api/'):\n"
                 "        origin=request.headers.get('Origin')\n"
                 '        if origin and urlparse(origin).netloc!=request.host:return '
                 "jsonify(error='Cross-origin writes are not allowed.'),403\n"
                 "    if request.path.startswith('/api/') and request.path not in "
                 "['/api/health','/api/workspaces']:\n"
                 '        request.workspace=workspace()\n'
                 "        if not request.workspace:return jsonify(error='This demo session has expired. "
                 "Start a new workspace.'),401\n"
                 '@app.after_request\n'
                 'def headers(r):\n'
                 '    '
                 "r.headers['Cache-Control']='no-store';r.headers['X-Content-Type-Options']='nosniff';r.headers['Referrer-Policy']='same-origin';return "
                 'r\n'
                 '@app.errorhandler(413)\n'
                 "def large(e): return jsonify(error='Request too large.'),413\n"
                 "@app.route('/api/health')\n"
                 'def health():\n'
                 "    with db() as c:c.execute('SELECT 1').fetchone()\n"
                 "    return jsonify(ok=True,project='vendor-gate',storage='sqlite',synthetic=True)\n"
                 "@app.post('/api/workspaces')\n"
                 'def create_workspace():\n'
                 '    token=secrets.token_hex(16)\n'
                 '    with db() as c:\n'
                 '        '
                 'cutoff=(datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(days=7)).isoformat()\n'
                 "        expired=[r['id'] for r in c.execute('SELECT id FROM workspaces WHERE "
                 "created<?',(cutoff,))]\n"
                 '        for old in expired:\n'
                 "            c.execute('DELETE FROM audit WHERE vendor IN (SELECT id FROM vendors WHERE "
                 "workspace=?)',(old,))\n"
                 "            c.execute('DELETE FROM evidence WHERE vendor IN (SELECT id FROM vendors WHERE "
                 "workspace=?)',(old,))\n"
                 "            c.execute('DELETE FROM vendors WHERE workspace=?',(old,));c.execute('DELETE "
                 "FROM workspaces WHERE id=?',(old,))\n"
                 "        if c.execute('SELECT count(*) FROM workspaces').fetchone()[0]>=100:return "
                 "jsonify(error='This demo is at capacity. Try again after workspace expiry.'),503\n"
                 "        c.execute('INSERT INTO workspaces VALUES(?,?)',(token,now()))\n"
                 "        for name,cat,country,amount,data in [('Northstar "
                 "Cloud','Software','India',35000,'personal'),('Maple Office','Facilities','United "
                 "Kingdom',8500,'none'),('Harbor Analytics','Data "
                 "services','Singapore',120000,'sensitive')]:\n"
                 '            vid=secrets.token_hex(8);risk=risk_for(amount,data,country)\n'
                 "            c.execute('INSERT INTO vendors "
                 "VALUES(?,?,?,?,?,?,?,?,?,?,?)',(vid,token,name,cat,country,amount,data,risk,'draft',1,now()))\n"
                 "            record(c,vid,'created','Synthetic seed vendor created')\n"
                 '    return jsonify(workspace=token),201\n'
                 "@app.route('/api/vendors', methods=['GET','POST'])\n"
                 'def vendors():\n'
                 '    with db() as c:\n'
                 "        if request.method=='GET':return jsonify(vendors=[detail(c,x) for x in "
                 "c.execute('SELECT * FROM vendors WHERE workspace=? ORDER BY created "
                 "DESC',(request.workspace,))])\n"
                 '        data=request.get_json(silent=True) or {}\n'
                 "        if c.execute('SELECT count(*) FROM vendors WHERE "
                 "workspace=?',(request.workspace,)).fetchone()[0]>=40:return jsonify(error='Demo limit: 40 "
                 "vendors per workspace.'),429\n"
                 '        '
                 "name=str(data.get('name','')).strip();cat=str(data.get('category','')).strip();country=str(data.get('country','')).strip();access=data.get('data_access')\n"
                 "        try: amount=int(data.get('amount',-1))\n"
                 '        except (ValueError,TypeError):amount=-1\n'
                 '        errors={}\n'
                 "        if not 2<=len(name)<=80:errors['name']='Enter 2–80 characters.'\n"
                 "        if cat not in ['Software','Facilities','Data "
                 "services','Consulting']:errors['category']='Choose a valid category.'\n"
                 "        if country not in ['India','United Kingdom','United "
                 "States','Singapore','Other']:errors['country']='Choose a country.'\n"
                 "        if not 0<=amount<=10000000:errors['amount']='Enter an annual amount between 0 and "
                 "10,000,000.'\n"
                 "        if access not in ['none','personal','sensitive']:errors['data_access']='Choose a "
                 "data access level.'\n"
                 "        if c.execute('SELECT 1 FROM vendors WHERE workspace=? AND "
                 "lower(name)=lower(?)',(request.workspace,name)).fetchone():errors['name']='A vendor with "
                 "this name already exists.'\n"
                 "        if errors:return jsonify(error='Check the highlighted fields.',fields=errors),422\n"
                 '        vid=secrets.token_hex(8);risk=risk_for(amount,access,country)\n'
                 "        c.execute('INSERT INTO vendors "
                 "VALUES(?,?,?,?,?,?,?,?,?,?,?)',(vid,request.workspace,name,cat,country,amount,access,risk,'draft',1,now()))\n"
                 "        record(c,vid,'created',f'Risk calculated: {risk}')\n"
                 "        return jsonify(vendor=detail(c,c.execute('SELECT * FROM vendors WHERE "
                 "id=?',(vid,)).fetchone())),201\n"
                 "@app.route('/api/vendors/<vid>',methods=['GET','PATCH'])\n"
                 'def vendor(vid):\n'
                 '    with db() as c:\n'
                 "        row=c.execute('SELECT * FROM vendors WHERE id=? AND "
                 "workspace=?',(vid,request.workspace)).fetchone()\n"
                 "        if not row:return jsonify(error='Vendor not found in this workspace.'),404\n"
                 "        if request.method=='GET':return jsonify(vendor=detail(c,row))\n"
                 '        d=request.get_json(silent=True) or {}\n'
                 "        if d.get('version')!=row['version']:return jsonify(error='Another change was "
                 "saved. Refresh this vendor before continuing.',conflict=True),409\n"
                 "        action=d.get('action')\n"
                 "        if action=='evidence':\n"
                 "            kind=d.get('kind');reference=str(d.get('reference','')).strip()\n"
                 "            if kind not in REQUIREMENTS[row['risk']]:return jsonify(error='Evidence type "
                 "is not required for this risk level.'),422\n"
                 "            if not 5<=len(reference)<=180:return jsonify(error='Evidence reference must be "
                 "5–180 characters.'),422\n"
                 "            if row['status']=='approved':return jsonify(error='Approved vendors are "
                 "locked. Reopen review first.'),409\n"
                 "            c.execute('INSERT INTO evidence VALUES(?,?,?,?,?) ON CONFLICT(vendor,kind) DO "
                 'UPDATE SET '
                 "reference=excluded.reference,created=excluded.created',(secrets.token_hex(8),vid,kind,reference,now()))\n"
                 "            record(c,vid,'evidence',f'{kind}: {reference}')\n"
                 "        elif action=='transition':\n"
                 '            '
                 "target=d.get('status');allowed={'draft':['review'],'review':['approved','draft'],'approved':['review']}\n"
                 "            if target not in allowed[row['status']]:return jsonify(error='This status "
                 "transition is not allowed.'),422\n"
                 '            v=detail(c,row)\n'
                 "            if target=='approved' and v['missing']:return jsonify(error='Approval blocked: "
                 "missing '+', '.join(v['missing']),missing=v['missing']),422\n"
                 "            c.execute('UPDATE vendors SET status=? WHERE "
                 'id=?\',(target,vid));record(c,vid,\'status\',f\'{row["status"]} → {target}\')\n'
                 "        else:return jsonify(error='Unknown update action.'),422\n"
                 "        c.execute('UPDATE vendors SET version=version+1 WHERE id=?',(vid,))\n"
                 "        return jsonify(vendor=detail(c,c.execute('SELECT * FROM vendors WHERE "
                 "id=?',(vid,)).fetchone()))\n"
                 "@app.route('/',defaults={'path':''})\n"
                 "@app.route('/<path:path>')\n"
                 'def serve_app(path):\n'
                 '    folder=os.path.abspath(app.static_folder)\n'
                 '    return send_from_directory(folder,path if path and '
                 "os.path.isfile(os.path.join(folder,path)) else 'index.html')\n"
                 'init_db()\n'
                 "if __name__=='__main__':app.run(host='0.0.0.0',port=int(os.environ.get('PORT','4178')))\n",
 'requirements.txt': 'Flask==3.1.2\npsycopg[binary]==3.2.13\ngunicorn==23.0.0\n',
 'start.sh': '#!/bin/sh\n'
             'set -eu\n'
             'exec gunicorn --bind "0.0.0.0:${PORT:-4178}" --workers 1 --threads 4 --access-logfile - '
             '--error-logfile - api.index:app\n',
 'test_runtime.py': '"""Disposable local production-process replacement acceptance. Not Docker/host '
                    'proof."""\n'
                    'import json, os, pathlib, signal, socket, subprocess, tempfile, time, unittest\n'
                    'from urllib.request import Request, urlopen\n'
                    '\n'
                    'ROOT = pathlib.Path(__file__).resolve().parent\n'
                    '\n'
                    'class RuntimeTest(unittest.TestCase):\n'
                    '    def test_production_launcher_and_restart_persistence(self):\n'
                    "        with tempfile.TemporaryDirectory(prefix='vendor-runtime-') as folder:\n"
                    '            with socket.socket() as sock:\n'
                    "                sock.bind(('127.0.0.1', 0)); port = sock.getsockname()[1]\n"
                    "            base = f'http://127.0.0.1:{port}'\n"
                    '            env = dict(os.environ, PORT=str(port), '
                    "VENDOR_DB_PATH=str(pathlib.Path(folder)/'demo.sqlite3'))\n"
                    "            def call(path, method='GET', payload=None, token=None):\n"
                    "                headers = {'Content-Type':'application/json'}\n"
                    "                if token: headers['X-Workspace'] = token\n"
                    '                data = json.dumps(payload).encode() if payload is not None else None\n'
                    '                with urlopen(Request(base+path, data=data, method=method, '
                    'headers=headers), timeout=4) as r:\n'
                    '                    raw = r.read()\n'
                    "                    return json.loads(raw) if 'json' in "
                    "r.headers.get('Content-Type','') else raw.decode()\n"
                    '            def start():\n'
                    "                p = subprocess.Popen(['sh','start.sh'], cwd=ROOT, env=env, "
                    'stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True)\n'
                    '                for _ in range(100):\n'
                    '                    if p.poll() is not None: self.fail(p.stdout.read().decode())\n'
                    '                    try:\n'
                    "                        if call('/api/health')['ok']: return p\n"
                    '                    except (OSError, ValueError): time.sleep(.05)\n'
                    "                stop(p); self.fail('Server failed readiness')\n"
                    '            def stop(p):\n'
                    '                if p.poll() is None:\n'
                    '                    os.killpg(p.pid, signal.SIGTERM)\n'
                    '                    try: p.wait(timeout=5)\n'
                    '                    except subprocess.TimeoutExpired:\n'
                    '                        os.killpg(p.pid, signal.SIGKILL); p.wait(timeout=5)\n'
                    '                p.stdout.close()\n'
                    '            p = start()\n'
                    '            try:\n'
                    '                self.assertIn(\'<div id="root">\', call(\'/\'))\n'
                    "                token = call('/api/workspaces','POST',{},None)['workspace']\n"
                    "                v = call('/api/vendors','POST',{'name':'Runtime synthetic "
                    "vendor','category':'Software','country':'India','amount':5000,'data_access':'none'},token)['vendor']\n"
                    "                vid = v['id']\n"
                    '                v = '
                    "call('/api/vendors/'+vid,'PATCH',{'action':'evidence','version':v['version'],'kind':'business','reference':'Synthetic "
                    "registry 123'},token)['vendor']\n"
                    "                self.assertEqual(v['missing'],[])\n"
                    '            finally: stop(p)\n'
                    '            p = start()\n'
                    '            try:\n'
                    "                saved = call('/api/vendors/'+vid, token=token)['vendor']\n"
                    "                self.assertEqual(saved['name'],'Runtime synthetic vendor')\n"
                    "                self.assertEqual(saved['version'],v['version'])\n"
                    "                self.assertEqual(len(saved['audit']),2)\n"
                    "                self.assertEqual(saved['evidence'][0]['reference'],'Synthetic registry "
                    "123')\n"
                    '            finally: stop(p)\n'
                    '\n'
                    "if __name__ == '__main__': unittest.main(verbosity=2)\n"}
if __name__ == "__main__":
    for name, text in FILES.items():
        p=pathlib.Path(name)
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(text)
    print("Updated",len(FILES),"portable runtime source files")
