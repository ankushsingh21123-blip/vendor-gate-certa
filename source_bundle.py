#!/usr/bin/env python3
"""Complete original AI-assisted Vendor Gate source. Extract with --extract DEST.
No download, dependency installation or execution occurs during extraction.
"""
import pathlib,argparse
FILES = {'README.md': '# Vendor Gate\n'
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
              'tests.\n',
 'LICENSE': 'MIT License\n'
            '\n'
            'Copyright (c) 2026 Ankush Singh\n'
            '\n'
            'Permission is hereby granted, free of charge, to any person obtaining a copy of this software '
            'and associated documentation files (the "Software"), to deal in the Software without '
            'restriction, including without limitation the rights to use, copy, modify, merge, publish, '
            'distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the '
            'Software is furnished to do so, subject to the following conditions:\n'
            'The above copyright notice and this permission notice shall be included in all copies or '
            'substantial portions of the Software.\n'
            'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING '
            'BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND '
            'NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, '
            'DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, '
            'OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n',
 'PLAN.md': '# Vendor Gate, new Certa-role portfolio build\n'
            'Started 24 November 2026. No Certa affiliation, customer data or employer assessment. Synthetic '
            'vendor risk and evidence workflow, built with AI assistance. Original source, not a fork or '
            'renamed prior demo.\n'
            '\n'
            'Role mapping: React/TypeScript interactive components; nested protected routes; query filters; '
            'API request states and conflict handling; accessible responsive design; validated forms; '
            'backend/database persistence; component and API tests. No invented independent authorship or '
            'production customer claim.\n'
            '\n'
            'Workflow: create vendor, assign risk from country/data access/contract amount; record required '
            'evidence; transition draft -> review -> approved only when evidence gates pass. High risk needs '
            'security+privacy+financial evidence. Audit trail records changes. Optimistic version checks '
            'prevent overwrites. Isolated demo workspace and explicit synthetic-data notice.\n'
            '\n'
            'Delivery gates: local API tests and browser scenarios, responsive actual-pixel inspection, '
            'clean secret-free repository, zero-cost deployment and production persistence verification. No '
            'application until all pass. Existing hosting or old portfolio links do not satisfy this '
            'build.\n',
 'package.json': '{"name":"vendor-gate","private":true,"version":"1.0.0","scripts":{"build":"vite build '
                 '--outDir ../static","test":"vitest run","dev":"vite --host '
                 '127.0.0.1"},"dependencies":{"react":"^19.3.1","react-dom":"^19.3.1","react-router-dom":"^7.18.6"},"devDependencies":{"@playwright/test":"^1.65.1","@testing-library/jest-dom":"6.9.1","@testing-library/react":"16.3.0","@types/react":"19.2.2","@types/react-dom":"19.2.2","jsdom":"26.1.0","typescript":"5.9.3","vite":"^8.3.8","vitest":"^5.1.1"},"type":"module"}',
 'requirements.txt': 'Flask==3.1.2\npsycopg[binary]==3.2.13\n',
 'vite.config.ts': "import {defineConfig} from 'vite';\n"
                   'export default '
                   "defineConfig({root:'web',server:{proxy:{'/api':'http://127.0.0.1:4178'}},test:{environment:'jsdom',include:['**/*.test.tsx']}});\n",
 'playwright.config.ts': "import{defineConfig}from'@playwright/test';\n"
                         'export default '
                         "defineConfig({testDir:'.',testMatch:'browser.spec.ts',workers:1,use:{baseURL:'http://127.0.0.1:4178',headless:true},webServer:{command:(process.env.VENDOR_TEST_SERVER||'python "
                         "api/index.py'),url:'http://127.0.0.1:4178/api/health',reuseExistingServer:true}})\n",
 'test_api.py': 'import os, tempfile, unittest, importlib\n'
                "os.environ['VENDOR_DB_PATH']=tempfile.mktemp(suffix='.sqlite')\n"
                'from api.index import app,risk_for\n'
                'class ApiTest(unittest.TestCase):\n'
                ' def setUp(self):\n'
                '  '
                "self.c=app.test_client();self.token=self.c.post('/api/workspaces').json['workspace'];self.h={'X-Workspace':self.token};self.v=self.c.get('/api/vendors',headers=self.h).json['vendors'][0]\n"
                ' def patch(self,v,body):return '
                "self.c.patch('/api/vendors/'+v['id'],headers=self.h,json={'version':v['version'],**body})\n"
                ' def '
                "test_session_required(self):self.assertEqual(self.c.get('/api/vendors').status_code,401)\n"
                ' def test_isolation(self):\n'
                '  '
                "t=self.c.post('/api/workspaces').json['workspace'];r=self.c.get('/api/vendors/'+self.v['id'],headers={'X-Workspace':t});self.assertEqual(r.status_code,404)\n"
                ' def test_risk_boundaries(self):\n'
                '  '
                "self.assertEqual(risk_for(19999,'none','India'),'low');self.assertEqual(risk_for(20000,'none','India'),'medium');self.assertEqual(risk_for(100000,'personal','India'),'high');self.assertEqual(risk_for(1,'sensitive','Other'),'high')\n"
                ' def test_validation(self):\n'
                '  '
                "r=self.c.post('/api/vendors',headers=self.h,json={'name':'x','amount':-1});self.assertEqual(r.status_code,422);self.assertIn('name',r.json['fields'])\n"
                ' def test_duplicate(self):\n'
                '  '
                "r=self.c.post('/api/vendors',headers=self.h,json={**self.v,'name':self.v['name'].upper()});self.assertEqual(r.status_code,422)\n"
                ' def test_create_persists(self):\n'
                "  r=self.c.post('/api/vendors',headers=self.h,json={'name':'Cedar "
                "Test','category':'Software','country':'India','amount':150000,'data_access':'sensitive'});self.assertEqual(r.status_code,201);self.assertEqual(r.json['vendor']['risk'],'high');self.assertEqual(self.c.get('/api/vendors/'+r.json['vendor']['id'],headers=self.h).json['vendor']['name'],'Cedar "
                "Test')\n"
                ' def '
                "test_invalid_transition(self):self.assertEqual(self.patch(self.v,{'action':'transition','status':'approved'}).status_code,422)\n"
                ' def test_approval_blocked(self):\n'
                '  '
                "v=self.patch(self.v,{'action':'transition','status':'review'}).json['vendor'];r=self.patch(v,{'action':'transition','status':'approved'});self.assertEqual(r.status_code,422);self.assertTrue(r.json['missing'])\n"
                ' def test_full_workflow(self):\n'
                '  v=self.v\n'
                '  for kind in '
                "v['required']:v=self.patch(v,{'action':'evidence','kind':kind,'reference':'Demo reference "
                "checked'}).json['vendor']\n"
                '  '
                "v=self.patch(v,{'action':'transition','status':'review'}).json['vendor'];v=self.patch(v,{'action':'transition','status':'approved'}).json['vendor'];self.assertEqual(v['status'],'approved');self.assertGreater(len(v['audit']),3)\n"
                "  self.assertEqual(self.patch(v,{'action':'evidence','kind':'business','reference':'Changed "
                "note'}).status_code,409)\n"
                '  '
                "self.assertEqual(self.patch(v,{'action':'transition','status':'review'}).json['vendor']['status'],'review')\n"
                ' def test_stale_write(self):\n'
                '  '
                "self.patch(self.v,{'action':'transition','status':'review'});self.assertEqual(self.patch(self.v,{'action':'transition','status':'review'}).status_code,409)\n"
                ' def '
                "test_unknown_evidence(self):self.assertEqual(self.patch(self.v,{'action':'evidence','kind':'bad','reference':'something'}).status_code,422)\n"
                ' def '
                "test_reference_validation(self):self.assertEqual(self.patch(self.v,{'action':'evidence','kind':'business','reference':'x'}).status_code,422)\n"
                ' def test_no_html_execution(self):\n'
                '  '
                "r=self.c.post('/api/vendors',headers=self.h,json={'name':'<script>alert(1)</script>','category':'Software','country':'India','amount':0,'data_access':'none'});self.assertEqual(r.status_code,201);self.assertIn('<script>',r.json['vendor']['name'])\n"
                ' def test_origin_protection(self):\n'
                '  '
                "self.assertEqual(self.c.post('/api/workspaces',headers={'Origin':'https://evil.invalid'}).status_code,403)\n"
                ' def '
                "test_invalid_json(self):self.assertEqual(self.c.post('/api/vendors',headers=self.h,data='[',content_type='application/json').status_code,422)\n"
                "if __name__=='__main__':unittest.main(verbosity=2)\n",
 'browser.spec.ts': "import{test,expect}from'@playwright/test';\n"
                    "test('full onboarding evidence and approval flow survives reload',async({page})=>{const "
                    "errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));await "
                    "page.goto('/app/vendors');await expect(page.getByRole('button',{name:/Open a "
                    "private/})).toBeVisible();await page.getByRole('button',{name:/Open a "
                    'private/}).click();await '
                    "expect(page.getByRole('heading',{name:'Overview',exact:true})).toBeVisible();await "
                    "page.getByRole('link',{name:'+ Add vendor'}).click();await "
                    "page.getByRole('button',{name:'Create vendor →'}).click();await "
                    "expect(page.getByRole('alert')).toContainText('Check');await page.getByLabel('Vendor "
                    "name').fill('Cedar Proof '+Date.now());await page.getByLabel('Annual contract "
                    "value').fill('150000');await page.getByLabel('Data "
                    "access').selectOption('sensitive');await page.getByRole('button',{name:'Create vendor "
                    "→'}).click();await expect(page.getByRole('heading',{name:'Evidence "
                    "checklist'})).toBeVisible();await expect(page.getByText('4 evidence items still "
                    "needed')).toBeVisible();await page.getByRole('button',{name:'Start review "
                    "→'}).click();await expect(page.getByRole('button',{name:'Approve vendor "
                    "✓'})).toBeDisabled();for(const kind of "
                    "['business','privacy','security','financial']){await page.getByLabel('Evidence "
                    "type').selectOption(kind);await page.getByLabel('Review reference').fill('Synthetic "
                    "reference '+kind+' checked');await page.getByRole('button',{name:'Save "
                    "evidence'}).click();await expect(page.getByLabel('Review "
                    "reference')).toHaveValue('')}await expect(page.getByRole('button',{name:'Approve vendor "
                    "✓'})).toBeEnabled();await page.getByRole('button',{name:'Approve vendor "
                    "✓'}).click();await expect(page.getByText('Approved profile is "
                    "locked.')).toBeVisible();await page.reload();await expect(page.getByText('Approved "
                    "profile is locked.')).toBeVisible();await page.getByRole('button',{name:'Reopen "
                    "review'}).click();await expect(page.getByLabel('Review reference')).toBeVisible();await "
                    "page.getByRole('link',{name:/Vendor register/}).first().click();await "
                    "page.getByRole('searchbox').fill('does-not-exist');await "
                    "expect(page.getByRole('heading',{name:'No vendors match'})).toBeVisible();await "
                    "page.getByRole('button',{name:'Reset filters'}).click();await "
                    "expect(page.getByRole('table')).toBeVisible();expect(errors).toEqual([])});\n"
                    "test('actual responsive views and no overflow',async({page})=>{await "
                    "page.goto('/');await page.getByRole('button',{name:/Open a private/}).click();await "
                    "expect(page.getByRole('heading',{name:'Overview',exact:true})).toBeVisible();for(const "
                    'width of [1280,390,320]){await page.setViewportSize({width,height:900});await '
                    'page.screenshot({path:`evidence/overview-${width}.png`,fullPage:true});expect(await '
                    'page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBeTruthy()}await '
                    "page.getByRole('link',{name:'+ Add vendor'}).click();await "
                    "page.screenshot({path:'evidence/new-vendor-320.png',fullPage:true});expect(await "
                    'page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBeTruthy()});\n'
                    "test('expired sessions recover safely and offline errors are "
                    "visible',async({page})=>{await page.goto('/');await "
                    "page.evaluate(()=>sessionStorage.setItem('vendor-gate-session','a'.repeat(32)));await "
                    "page.goto('/app');await expect(page.getByRole('button',{name:/Open a "
                    "private/})).toBeVisible();await page.route('**/api/workspaces',r=>r.abort());await "
                    "page.getByRole('button',{name:/Open a private/}).click();await "
                    "expect(page.getByRole('alert')).toContainText('Connection lost')});\n",
 '.gitignore': 'node_modules/\nstatic/\n.env*\n!.env.example\n*.sqlite*\n__pycache__/\n.pytest_cache/\n',
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
                 "if __name__=='__main__':app.run(port=4178)\n",
 'web/model.ts': "export type Risk='low'|'medium'|'high';\n"
                 'export type '
                 "Vendor={id:string;name:string;category:string;country:string;amount:number;data_access:string;risk:Risk;status:'draft'|'review'|'approved';version:number;evidence:{kind:string;reference:string;created:string}[];required:string[];missing:string[];audit:{action:string;detail:string;created:string}[]};\n"
                 "export const riskLabel={low:'Low risk',medium:'Medium risk',high:'High risk'};\n"
                 'export function summarize(v:Vendor[]){return '
                 "{total:v.length,review:v.filter(x=>x.status==='review').length,high:v.filter(x=>x.risk==='high').length,approved:v.filter(x=>x.status==='approved').length}}\n"
                 'export function filterVendors(v:Vendor[],query:string,status:string,risk:string){const '
                 'q=query.trim().toLowerCase();return v.filter(x=>(!q||`${x.name} ${x.category} '
                 '${x.country}`.toLowerCase().includes(q))&&(!status||x.status===status)&&(!risk||x.risk===risk))}\n'
                 'export function currency(n:number){return new '
                 "Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0}).format(n)}\n",
 'web/model.test.tsx': "import{describe,it,expect}from'vitest';\n"
                       "import{filterVendors,summarize,currency,Vendor}from'./model';\n"
                       "const vendors=[{name:'Cedar "
                       "Cloud',category:'Software',country:'India',risk:'high',status:'review'},{name:'Maple "
                       "Desk',category:'Facilities',country:'Singapore',risk:'low',status:'approved'}] as "
                       'Vendor[];\n'
                       "describe('vendor view model',()=>{it('matches case-insensitive "
                       "names',()=>expect(filterVendors(vendors,'CEDAR','','')).toHaveLength(1));it('matches "
                       'country and '
                       "category',()=>expect(filterVendors(vendors,'singapore','','')).toHaveLength(1));it('combines "
                       "filters',()=>expect(filterVendors(vendors,'','review','low')).toHaveLength(0));it('keeps "
                       'input '
                       "immutable',()=>{filterVendors(vendors,'cedar','','');expect(vendors).toHaveLength(2)});it('summarizes "
                       'operational '
                       "states',()=>expect(summarize(vendors)).toEqual({total:2,review:1,high:1,approved:1}));it('handles "
                       "an empty workspace',()=>expect(summarize([]).total).toBe(0));it('formats annual "
                       "value without fractional noise',()=>expect(currency(24000)).toBe('$24,000'))});\n",
 'web/main.tsx': "import React,{useState,useEffect,useCallback,createContext,useContext} from 'react';\n"
                 "import{createRoot}from'react-dom/client';\n"
                 "import{BrowserRouter,Routes,Route,Navigate,Link,NavLink,useNavigate,useParams,useSearchParams,Outlet}from'react-router-dom';\n"
                 "import{Vendor,riskLabel,summarize,filterVendors,currency}from'./model';\n"
                 "import'./style.css';\n"
                 "import{Badge,EvidenceGate}from'./components';\n"
                 "const Session=createContext<{token:string;logout:()=>void}>({token:'',logout:()=>{}});\n"
                 'export class ApiError extends Error{constructor(message:string,public status:number,public '
                 'fields:Record<string,string>={}){super(message)}}\n'
                 'async function api(path:string,token:string,options:RequestInit={}){let '
                 'response;try{response=await '
                 "fetch('/api'+path,{...options,headers:{'Content-Type':'application/json','X-Workspace':token,...options.headers}})}catch{throw "
                 "new ApiError('Connection lost. Your saved data is safe. Please try again.',0)}const "
                 "body=await response.json().catch(()=>({error:'The server returned an unexpected "
                 "response.'}));if(!response.ok)throw new ApiError(body.error||'Request "
                 "failed.',response.status,body.fields);return body}\n"
                 '\n'
                 'function '
                 "Login({onLogin}:{onLogin:(s:string)=>void}){const[busy,setBusy]=useState(false),[error,setError]=useState('');async "
                 "function start(){setBusy(true);setError('');try{const d=await "
                 "api('/workspaces','',{method:'POST',body:'{}'});onLogin(d.workspace)}catch(e){setError((e "
                 'as Error).message)}finally{setBusy(false)}}return <main className="welcome"><div '
                 'className="brand"><span className="brand-icon">V</span> Vendor Gate</div><div '
                 'className="eyebrow">A SYNTHETIC DUE-DILIGENCE WORKSPACE</div><h1>Better vendor '
                 'decisions.<br/><span>A clear trail behind each one.</span></h1><p>Review risk, collect '
                 'evidence and move vendors through approval, without losing the context.</p><button '
                 "onClick={start} disabled={busy}>{busy?'Creating workspace…':'Open a private demo workspace "
                 '→\'}</button>{error&&<div role="alert" className="alert">{error}</div>}<p '
                 'className="small">Synthetic data only. Not a real compliance tool. Each session gets a '
                 'separate workspace. Do not enter personal, customer or confidential information.</p><div '
                 'className="welcome-grid"><section><b>01 / Assess</b><p>Explainable risk rules, not a '
                 'black-box score.</p></section><section><b>02 / Verify</b><p>Evidence requirements adapt to '
                 'the vendor.</p></section><section><b>03 / Decide</b><p>Approval gates and version-safe '
                 'changes.</p></section></div><footer>Original AI-assisted portfolio project · Built for '
                 'frontend engineering practice · Not affiliated with Certa.</footer></main>}\n'
                 'function Shell(){const{logout}=useContext(Session);return <div '
                 'className="app-shell"><aside><Link to="/app" className="brand"><span '
                 'className="brand-icon">V</span> Vendor Gate</Link><div className="workspace-label"><i/> '
                 'DEMO WORKSPACE</div><nav aria-label="Main"><NavLink to="/app" end>▦ '
                 '<span>Overview</span></NavLink><NavLink to="/app/vendors">▤ <span>Vendor '
                 'register</span></NavLink><NavLink to="/app/method">◎ <span>Risk '
                 'methodology</span></NavLink></nav><div className="sidebar-note">Evidence before '
                 'approval.<br/>Context before decisions.</div><button className="subtle" '
                 'onClick={logout}>Leave workspace</button></aside><div className="main-area"><header '
                 'className="topbar"><span>Third-party operations <span className="muted">/ '
                 'Workspace</span></span><span className="demo-tag">SYNTHETIC DATA ONLY</span></header><div '
                 'className="content"><Outlet/></div><footer className="app-footer">AI-assisted portfolio '
                 'build · No real vendors or compliance advice · No Certa affiliation</footer></div></div>}\n'
                 'function '
                 "useVendors(){const{token,logout}=useContext(Session),[vendors,setVendors]=useState<Vendor[]>([]),[loading,setLoading]=useState(true),[error,setError]=useState('');const "
                 "load=useCallback(async()=>{setLoading(true);setError('');try{setVendors((await "
                 "api('/vendors',token)).vendors)}catch(e){if((e as ApiError).status===401)logout();else "
                 'setError((e as '
                 'Error).message)}finally{setLoading(false)}},[token]);useEffect(()=>{load()},[load]);return{vendors,loading,error,load}}\n'
                 'function '
                 'State({loading,error,retry}:{loading:boolean;error:string;retry:()=>void}){if(loading)return '
                 '<div role="status" className="loading"><div className="skeleton"/><div '
                 'className="skeleton"/><div className="skeleton"/>Loading saved '
                 'workspace…</div>;if(error)return <div className="alert" role="alert"><b>Couldn\'t load the '
                 'workspace.</b><p>{error}</p><button className="secondary" onClick={retry}>Try '
                 'again</button></div>;return null}\n'
                 'function '
                 'Title({eyebrow,title,description,action}:{eyebrow:string;title:string;description:string;action?:React.ReactNode}){return '
                 '<div className="title-row"><div><div className="eyebrow">{eyebrow}</div><h1>{title}</h1><p '
                 'className="muted">{description}</p></div>{action}</div>}\n'
                 'function VendorTable({vendors}:{vendors:Vendor[]}){return <div '
                 'className="table-wrap"><table><thead><tr><th scope="col">Vendor / category</th><th '
                 'scope="col">Risk</th><th scope="col">Review status</th><th scope="col">Evidence</th><th '
                 'scope="col">Annual value</th></tr></thead><tbody>{vendors.map(v=><tr key={v.id}><td><Link '
                 'className="vendor-link" to={\'/app/vendors/\'+v.id}>{v.name} '
                 '<span>↗</span></Link><small>{v.category} · {v.country}</small></td><td '
                 'data-label="Risk"><Badge kind={v.risk}>{riskLabel[v.risk]}</Badge></td><td '
                 'data-label="Status"><Badge kind={v.status}>{v.status===\'draft\'?\'Not '
                 "started':v.status==='review'?'In review':'Approved'}</Badge></td><td "
                 'data-label="Evidence"><span '
                 "className={v.missing.length?'muted':'complete'}>{v.required.length-v.missing.length}/{v.required.length} "
                 'verified</span><div className="progress" aria-hidden="true"><span '
                 "style={{width:((v.required.length-v.missing.length)/v.required.length*100)+'%'}}/></div></td><td "
                 'data-label="Annual value" '
                 'className="amount">{currency(v.amount)}</td></tr>)}</tbody></table></div>}\n'
                 'function Dashboard(){const{vendors,loading,error,load}=useVendors();const '
                 'stats=summarize(vendors);return <><Title eyebrow="YOUR OPERATIONS AT A GLANCE" '
                 'title="Overview" description="A focused view of what needs a decision next." action={<Link '
                 'className="button" to="/app/vendors/new">+ Add vendor</Link>}/><State loading={loading} '
                 'error={error} retry={load}/>{!loading&&!error&&<><div className="stats">{[[\'Vendors '
                 "tracked',stats.total,'Across your isolated workspace'],['In review',stats.review,'Ready "
                 "for the next decision'],['High risk',stats.high,'Extra evidence "
                 "required'],['Approved',stats.approved,'All required evidence "
                 'verified\']].map(([label,note,sub])=><section className="stat" '
                 'key={label}><span>{label}</span><strong>{note}</strong><small>{sub}</small></section>)}</div><div '
                 'className="section-heading"><div><h2>Vendor register</h2><p className="muted">Every '
                 'relationship. One review trail.</p></div><Link to="/app/vendors">View all vendors '
                 '→</Link></div><VendorTable vendors={vendors.slice(0,5)}/><section className="insight"><div '
                 'className="insight-mark">◎</div><div><h2>Risk changes the review, not the '
                 'standard.</h2><p>High-risk vendors need business, privacy, security and financial '
                 'evidence. No vendor can be approved with missing evidence.</p><Link '
                 'to="/app/method">Understand the rules →</Link></div></section></>}</>}\n'
                 'function '
                 'Register(){const{vendors,loading,error,load}=useVendors(),[params,setParams]=useSearchParams();const '
                 "q=params.get('q')||'',status=params.get('status')||'',risk=params.get('risk')||'';const "
                 'filtered=filterVendors(vendors,q,status,risk);function set(key:string,value:string){const '
                 'p=new '
                 'URLSearchParams(params);value?p.set(key,value):p.delete(key);setParams(p,{replace:true})}return '
                 '<><Title eyebrow="THIRD-PARTY RELATIONSHIPS" title="Vendor register" description="Search '
                 'the details. Keep the context." action={<Link className="button" to="new">+ Add '
                 'vendor</Link>}/><div className="filters"><label className="search">Search vendors<input '
                 'type="search" placeholder="Name, category or country" value={q} '
                 "onChange={e=>set('q',e.target.value)}/></label><label>Status<select value={status} "
                 'onChange={e=>set(\'status\',e.target.value)}><option value="">All statuses</option><option '
                 'value="draft">Not started</option><option value="review">In review</option><option '
                 'value="approved">Approved</option></select></label><label>Risk level<select value={risk} '
                 'onChange={e=>set(\'risk\',e.target.value)}><option value="">All '
                 "risks</option>{['low','medium','high'].map(r=><option key={r} value={r}>{riskLabel[r as "
                 'keyof typeof riskLabel]}</option>)}</select></label></div><State loading={loading} '
                 'error={error} retry={load}/>{!loading&&!error&&<><p className="result-count" '
                 'role="status">{filtered.length} of {vendors.length} '
                 'vendors</p>{filtered.length?<VendorTable vendors={filtered}/>:<section '
                 'className="empty"><h2>No vendors match these filters</h2><p>Try a different name or reset '
                 'your filters.</p><button className="secondary" onClick={()=>setParams({})}>Reset '
                 'filters</button></section>}</>}</>}\n'
                 "const initial={name:'',category:'Software',country:'India',amount:'',data_access:'none'};\n"
                 'function '
                 "NewVendor(){const{token,logout}=useContext(Session),nav=useNavigate(),[form,setForm]=useState(initial),[busy,setBusy]=useState(false),[error,setError]=useState(''),[fields,setFields]=useState<Record<string,string>>({});async "
                 'function '
                 "submit(e:React.FormEvent){e.preventDefault();setError('');setFields({});setBusy(true);try{const "
                 'd=await '
                 "api('/vendors',token,{method:'POST',body:JSON.stringify({...form,amount:form.amount===''?-1:Number(form.amount)})});nav('/app/vendors/'+d.vendor.id)}catch(e){const "
                 'a=e as '
                 'ApiError;if(a.status===401)logout();setError(a.message);setFields(a.fields||{})}finally{setBusy(false)}}function '
                 'field(key:keyof typeof initial,label:string,children:React.ReactElement){return '
                 '<label>{label}{React.cloneElement(children as '
                 "React.ReactElement<any>,{id:key,name:key,value:form[key],onChange:(e:React.ChangeEvent<HTMLInputElement>)=>setForm({...form,[key]:e.target.value}),'aria-invalid':!!fields[key],'aria-describedby':fields[key]?key+'-error':undefined})}{fields[key]&&<span "
                 'className="field-error" id={key+\'-error\'}>{fields[key]}</span>}</label>}return <><Link '
                 'className="back" to="/app/vendors">← Vendor register</Link><Title eyebrow="START A NEW '
                 'RELATIONSHIP" title="Add a vendor" description="A few details determine the evidence this '
                 'vendor needs."/><div className="form-grid"><form onSubmit={submit} className="panel" '
                 'noValidate>{error&&<div className="alert" role="alert">{error}</div>}<h2>Vendor '
                 'profile</h2><p className="muted">Use fictional information only. All fields are '
                 'required.</p>{field(\'name\',\'Vendor name\',<input autoComplete="off" maxLength={80} '
                 'required placeholder="e.g. Cedar Cloud Services"/>)}<div '
                 'className="two-col">{field(\'category\',\'Category\',<select>{[\'Software\',\'Facilities\',\'Data '
                 "services','Consulting'].map(x=><option "
                 "key={x}>{x}</option>)}</select>)}{field('country','Operating "
                 "country',<select>{['India','United Kingdom','United "
                 "States','Singapore','Other'].map(x=><option "
                 "key={x}>{x}</option>)}</select>)}</div>{field('amount','Annual contract value "
                 '(USD)\',<input type="number" min="0" max="10000000" required placeholder="e.g. '
                 '25000"/>)}{field(\'data_access\',\'Data access\',<select><option value="none">No personal '
                 'data</option><option value="personal">Personal data</option><option '
                 'value="sensitive">Sensitive personal data</option></select>)}<div '
                 'className="form-actions"><Link to="/app/vendors" className="button '
                 'secondary">Cancel</Link><button disabled={busy}>{busy?\'Saving vendor…\':\'Create vendor '
                 '→\'}</button></div></form><section className="aside-card"><span className="eyebrow">HOW '
                 'THIS WORKS</span><h2>A review plan,<br/>built from context.</h2><p>Contract value, data '
                 'access and operating country feed an explicit risk rule.</p><ol><li>Create the vendor '
                 'profile</li><li>Add the required evidence references</li><li>Move to review, then '
                 'approve</li></ol><p className="small">Demo rules are illustrative. They are not legal, '
                 'financial or compliance advice.</p></section></div></>}\n'
                 'function '
                 "VendorDetail(){const{id}=useParams(),{token,logout}=useContext(Session),[v,setV]=useState<Vendor|null>(null),[loading,setLoading]=useState(true),[error,setError]=useState(''),[busy,setBusy]=useState(false),[kind,setKind]=useState('business'),[reference,setReference]=useState(''),[notice,setNotice]=useState('');const "
                 "load=useCallback(async()=>{setLoading(true);setError('');try{setV((await "
                 "api('/vendors/'+id,token)).vendor)}catch(e){if((e as ApiError).status===401)logout();else "
                 'setError((e as '
                 'Error).message)}finally{setLoading(false)}},[id,token]);useEffect(()=>{load()},[load]);async '
                 'function '
                 "update(body:object){if(!v)return;setBusy(true);setError('');setNotice('');try{const "
                 'd=await '
                 "api('/vendors/'+id,token,{method:'PATCH',body:JSON.stringify({...body,version:v.version})});setV(d.vendor);setReference('');setNotice('Change "
                 "saved to the review trail.')}catch(e){if((e as ApiError).status===401)logout();else "
                 'setError((e as Error).message)}finally{setBusy(false)}}if(loading)return <State loading '
                 'error="" retry={load}/>;if(!v)return <><Link to="/app/vendors">← Vendor '
                 'register</Link><State loading={false} error={error} retry={load}/></>;return <><Link '
                 'className="back" to="/app/vendors">← Vendor register</Link><Title eyebrow={\'VENDOR '
                 "PROFILE · VERSION '+v.version} title={v.name} description={v.category+' · '+v.country+' · "
                 "'+currency(v.amount)+' annual value'} action={<Badge "
                 'kind={v.risk}>{riskLabel[v.risk]}</Badge>}/>{error&&<div role="alert" '
                 'className="alert">{error} <button className="text-button" onClick={load}>Refresh saved '
                 'version</button></div>}{notice&&<div role="status" className="success">{notice}</div>}<div '
                 'className="detail-grid"><section className="panel"><div '
                 'className="section-heading"><h2>Evidence checklist</h2><span '
                 'className="muted">{v.required.length-v.missing.length}/{v.required.length} '
                 'complete</span></div><p className="muted">References are demo review notes, not document '
                 'uploads.</p><ul className="evidence-list">{v.required.map(r=>{const '
                 "e=v.evidence.find(x=>x.kind===r);return <li key={r}><span className={e?'check "
                 "done':'check'}>{e?'✓':'○'}</span><div><strong>{r[0].toUpperCase()+r.slice(1)} "
                 "verification</strong><p>{e?e.reference:'Evidence not yet recorded'}</p></div><Badge "
                 "kind={e?'approved':'draft'}>{e?'Verified':'Missing'}</Badge></li>})}</ul>{v.status!=='approved'?<form "
                 "onSubmit={e=>{e.preventDefault();update({action:'evidence',kind,reference})}} "
                 'className="evidence-form"><h3>Record evidence</h3><label>Evidence type<select value={kind} '
                 'onChange={e=>setKind(e.target.value)}>{v.required.map(r=><option key={r} '
                 'value={r}>{r[0].toUpperCase()+r.slice(1)}</option>)}</select></label><label>Review '
                 'reference<input value={reference} onChange={e=>setReference(e.target.value)} '
                 'placeholder="e.g. Synthetic review SEC-024, checked" minLength={5} maxLength={180} '
                 "required/></label><button disabled={busy}>{busy?'Saving…':'Save "
                 'evidence\'}</button></form>:<p className="success">Approved profile is locked. Reopen '
                 'review to change evidence.</p>}</section><section className="panel decision"><span '
                 'className="eyebrow">DECISION GATE</span><h2>Review status</h2><Badge '
                 "kind={v.status}>{v.status==='draft'?'Not started':v.status==='review'?'In "
                 "review':'Approved'}</Badge><p>{v.status==='approved'?'All required evidence was recorded "
                 "before approval.':v.missing.length?`${v.missing.length} evidence "
                 "item${v.missing.length>1?'s':''} still needed before approval.`:'All evidence is ready. "
                 "Move this vendor through review.'}</p>{v.status==='draft'&&<button disabled={busy} "
                 "onClick={()=>update({action:'transition',status:'review'})}>Start review "
                 "→</button>}{v.status==='review'&&<><EvidenceGate missing={v.missing.length} busy={busy} "
                 "onApprove={()=>update({action:'transition',status:'approved'})}/><button "
                 'className="secondary" disabled={busy} '
                 "onClick={()=>update({action:'transition',status:'draft'})}>Return to "
                 'draft</button></>}{v.status===\'approved\'&&<button className="secondary" disabled={busy} '
                 "onClick={()=>update({action:'transition',status:'review'})}>Reopen "
                 'review</button>}<hr/><h3>Risk factors</h3><dl><dt>Annual '
                 'value</dt><dd>{currency(v.amount)}</dd><dt>Data '
                 'access</dt><dd>{v.data_access}</dd><dt>Country</dt><dd>{v.country}</dd></dl><Link '
                 'to="/app/method">How risk is calculated →</Link></section></div><section className="panel '
                 'audit"><h2>Review trail</h2><p className="muted">Server-recorded events, newest '
                 'first.</p><ol>{v.audit.map((a,i)=><li key={i}><span '
                 'className="timeline-dot"/><div><b>{a.detail}</b><small>{new '
                 'Date(a.created).toLocaleString()} · {a.action}</small></div></li>)}</ol></section></>}\n'
                 'function Method(){return <><Title eyebrow="EXPLAINABLE BY DESIGN" title="Risk methodology" '
                 'description="Illustrative rules for a synthetic workflow, not real compliance '
                 'advice."/><section className="panel method"><h2>Three inputs. One consistent '
                 'review.</h2><p>The API, not the browser, calculates risk and enforces the evidence '
                 'gates.</p><table><thead><tr><th>Input</th><th>Points</th></tr></thead><tbody><tr><td>Annual '
                 'contract value</td><td>Under $20,000: 0 · $20,000–99,999: 1 · $100,000+: '
                 '2</td></tr><tr><td>Data access</td><td>None: 0 · Personal: 1 · Sensitive: '
                 '2</td></tr><tr><td>Operating country</td><td>India, UK, US, Singapore: 0 · Other: '
                 '1</td></tr></tbody></table><p>0 points = low risk. 1–2 = medium risk. 3+ = high '
                 'risk.</p><h3>Evidence requirements</h3><ul><li>Low: business verification</li><li>Medium: '
                 'business and privacy</li><li>High: business, privacy, security and '
                 'financial</li></ul><h3>What this project does not do</h3><p>No sanctions screening, '
                 'real-document verification, AI risk prediction, legal assessment or customer data '
                 'processing. A saved reference records a demo review decision, not proof that a real '
                 'document is genuine.</p><h3>State and API decisions</h3><p>URL query parameters own '
                 'register filters. The session owns an isolated workspace token. The server owns vendor '
                 'status, risk, version and audit events. Each update carries a version so a stale tab '
                 'cannot silently overwrite a newer decision.</p></section></>}\n'
                 'function '
                 "App(){const[token,setToken]=useState(()=>sessionStorage.getItem('vendor-gate-session')||'');function "
                 "login(t:string){sessionStorage.setItem('vendor-gate-session',t);setToken(t)}function "
                 "logout(){sessionStorage.removeItem('vendor-gate-session');setToken('')}return "
                 '<Session.Provider value={{token,logout}}><BrowserRouter><Routes><Route path="/" '
                 'element={token?<Navigate to="/app" replace/>:<Login onLogin={login}/>}/><Route path="/app" '
                 'element={token?<Shell/>:<Navigate to="/" replace/>}><Route index '
                 'element={<Dashboard/>}/><Route path="vendors" element={<Register/>}/><Route '
                 'path="vendors/new" element={<NewVendor/>}/><Route path="vendors/:id" '
                 'element={<VendorDetail/>}/><Route path="method" element={<Method/>}/></Route><Route '
                 'path="*" element={<main className="welcome"><h1>This page isn\'t here.</h1><Link '
                 'to="/">Return to workspace '
                 '→</Link></main>}/></Routes></BrowserRouter></Session.Provider>}\n'
                 "createRoot(document.getElementById('root')!).render(<App/>);\n",
 'web/components.test.tsx': 'import React '
                            "from'react';import{describe,it,expect,vi,afterEach}from'vitest';import{render,screen,fireEvent,cleanup}from'@testing-library/react';import{Badge,EvidenceGate}from'./components';\n"
                            'afterEach(cleanup);\n'
                            "describe('actual evidence approval component',()=>{it('blocks incomplete "
                            "evidence',()=>{const click=vi.fn();render(<EvidenceGate missing={2} "
                            "busy={false} onApprove={click}/>);const b=screen.getByRole('button');expect((b "
                            'as '
                            "HTMLButtonElement).disabled).toBe(true);fireEvent.click(b);expect(click).not.toHaveBeenCalled()});it('dispatches "
                            "approval only when ready',()=>{const click=vi.fn();render(<EvidenceGate "
                            'missing={0} busy={false} '
                            "onApprove={click}/>);fireEvent.click(screen.getByRole('button'));expect(click).toHaveBeenCalledOnce()});it('prevents "
                            "repeat submission while busy',()=>{render(<EvidenceGate missing={0} busy={true} "
                            "onApprove={()=>{}}/>);expect((screen.getByRole('button')as "
                            "HTMLButtonElement).disabled).toBe(true)});it('renders text rather than "
                            "HTML',()=>{render(<Badge "
                            'kind="high">{\'<script>test</script>\'}</Badge>);expect(screen.getByText(\'<script>test</script>\')).toBeTruthy();expect(document.querySelector(\'script\')).toBeNull()})});\n',
 'web/index.html': '<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" '
                   'content="width=device-width,initial-scale=1"><title>Vendor Gate | Synthetic diligence '
                   'workspace</title></head><body><div id="root"></div><script type="module" '
                   'src="/main.tsx"></script></body></html>\n',
 'web/components.tsx': "import React from'react';\n"
                       'export function Badge({kind,children}:{kind:string;children:React.ReactNode}){return '
                       "<span className={'badge '+kind}>{children}</span>}\n"
                       'export function '
                       'EvidenceGate({missing,busy,onApprove}:{missing:number;busy:boolean;onApprove:()=>void}){return '
                       '<button disabled={busy||missing>0} onClick={onApprove} title={missing?`${missing} '
                       "evidence items required`:'All evidence recorded'}>Approve vendor ✓</button>}\n",
 'web/style.css': '@import '
                  "url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');\n"
                  ":root{font-family:'DM "
                  "Sans',sans-serif;color:#183132;background:#f4f6f4;font-synthesis:none;font-size:14px;line-height:1.5;--green:#17614d;--muted:#6b7b77;--border:#dfe6e0}*{box-sizing:border-box}body{margin:0}a{color:var(--green);text-decoration:none}a:hover{text-decoration:underline}button,.button{font:inherit;background:var(--green);color:white;border:1px "
                  'solid var(--green);border-radius:7px;padding:10px '
                  '16px;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;gap:7px;font-weight:600;min-height:42px}button:hover,.button:hover{background:#114b3b;text-decoration:none}button:disabled{opacity:.5;cursor:not-allowed}.secondary{background:white;color:#244c40;border-color:#cbd7cf}.secondary:hover{background:#edf3ef}.subtle{background:transparent;border:1px '
                  'solid '
                  '#47645b;color:#d2e1d8}.text-button{background:transparent;color:inherit;border:0;text-decoration:underline;padding:4px;min-height:30px}button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible{outline:3px '
                  'solid #dfaa51;outline-offset:3px}input,select{font:inherit;width:100%;padding:11px '
                  '12px;border:1px solid '
                  '#cdd7cf;border-radius:6px;background:white;color:#183132;min-height:43px}input[aria-invalid=true]{border-color:#af4939}label{display:flex;flex-direction:column;gap:6px;font-size:13px;font-weight:600;margin:16px '
                  '0}label input,label '
                  "select{font-weight:400}.muted{color:var(--muted)}.small,small{font-size:12px;color:var(--muted)}h1,h2,h3,.brand{font-family:'Manrope',sans-serif}h1{font-size:32px;line-height:1.2;letter-spacing:-1.1px;margin:10px "
                  '0}h2{font-size:18px;letter-spacing:-.35px;margin:0 0 7px}h3{font-size:14px;margin:16px 0 '
                  '7px}p{margin:7px 0 '
                  '16px}.eyebrow{font-size:10px;letter-spacing:1.6px;color:#6d8576;font-weight:700}.brand{display:flex;align-items:center;gap:11px;font-size:20px;font-weight:800;letter-spacing:-.6px;color:inherit}.brand-icon{display:inline-flex;width:32px;height:32px;border:1px '
                  'solid '
                  '#a9c4b3;border-radius:8px;align-items:center;justify-content:center;font-size:21px;background:#d6e8ce;color:#214e3c}.app-shell{display:flex;min-height:100vh}aside{width:227px;position:fixed;height:100vh;background:#18392f;color:#f2f7f0;padding:29px '
                  '21px;display:flex;flex-direction:column}.workspace-label{border:1px solid '
                  '#3e5a4f;border-radius:6px;font-size:10px;letter-spacing:1px;padding:10px;margin:34px 0 '
                  '20px;color:#bfd2c3}.workspace-label '
                  'i{display:inline-block;width:6px;height:6px;border-radius:50%;background:#a2c68d;margin-right:7px}nav{display:grid;gap:6px}nav '
                  'a{color:#aec3b6;font-size:18px;padding:10px '
                  '12px;border-radius:6px;display:flex;gap:12px;align-items:center}nav a '
                  'span{font-size:13px}nav a.active{background:#345547;color:#f6faf4}nav '
                  'a:hover{background:#2a4c3e;text-decoration:none}.sidebar-note{margin-top:auto;color:#a0b9a9;font-size:12px;line-height:1.8;padding:20px '
                  '6px}aside '
                  '.subtle{font-size:12px;justify-content:flex-start}.main-area{margin-left:227px;width:calc(100% '
                  '- '
                  '227px);display:flex;flex-direction:column;min-height:100vh}.topbar{height:70px;background:#fff;border-bottom:1px '
                  'solid var(--border);padding:0 '
                  '37px;display:flex;justify-content:space-between;align-items:center;font-size:12px}.demo-tag{color:#66846e;background:#eff4eb;font-size:9px;letter-spacing:1.1px;padding:6px '
                  '9px;border-radius:4px;font-weight:700}.content{padding:35px '
                  '38px;max-width:1500px;width:100%;margin:0 '
                  'auto;flex:1}.title-row{display:flex;align-items:center;justify-content:space-between;gap:20px;margin-bottom:28px}.title-row '
                  'p{margin-bottom:0;font-size:13px}.title-row '
                  '.badge{font-size:12px}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:10px '
                  '0 35px}.stat{background:#fff;border:1px solid '
                  'var(--border);border-radius:9px;padding:19px '
                  '20px;display:flex;flex-direction:column}.stat>span{font-size:12px;color:#5e7366}.stat '
                  'strong{font-family:Manrope,sans-serif;font-size:34px;font-weight:600;letter-spacing:-1px;margin:8px '
                  '0}.stat '
                  'small{font-size:10px}.section-heading{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:16px}.section-heading '
                  'p{font-size:12px;margin:0}.section-heading>a{font-size:12px;font-weight:600}.table-wrap{background:white;border:1px '
                  'solid '
                  'var(--border);border-radius:9px;overflow:auto}table{width:100%;border-collapse:collapse;text-align:left}th{font-size:10px;color:#6d8076;font-weight:600;letter-spacing:.3px;background:#f8faf7;white-space:nowrap}th,td{padding:16px '
                  '19px;border-bottom:1px solid #e9eee9}tbody tr:last-child '
                  'td{border-bottom:0}td{font-size:12px}.vendor-link{font-weight:700;color:#203c30;display:block;white-space:nowrap}.vendor-link '
                  'span{font-weight:400;color:#7c9787;margin-left:6px}td '
                  'small{display:block;margin-top:4px;font-size:10px}.amount{white-space:nowrap}.badge{display:inline-block;font-size:10px;padding:4px '
                  '8px;border-radius:5px;white-space:nowrap;font-weight:600}.badge.low,.badge.approved{background:#e7f2e5;color:#2d643e}.badge.medium,.badge.review{background:#fcf1d8;color:#826015}.badge.high{background:#f8e6df;color:#a04729}.badge.draft{background:#edf0ed;color:#687b6e}.progress{width:74px;height:3px;background:#e7ece5;border-radius:4px;margin-top:6px}.progress '
                  'span{display:block;height:3px;background:#448b63;border-radius:4px}.complete{color:#2d794c}.insight{display:flex;gap:20px;padding:25px '
                  '28px;border:1px solid '
                  '#d5dfce;background:#eaf1e4;border-radius:9px;margin-top:28px}.insight-mark{font-size:33px;color:#52714c}.insight '
                  'h2{font-size:16px}.insight p{font-size:12px;max-width:650px;color:#62775e}.insight '
                  'a{font-size:12px;font-weight:600}.app-footer{border-top:1px solid '
                  'var(--border);font-size:10px;color:#7b8a7b;padding:16px '
                  '38px}.filters{display:flex;gap:14px;padding:4px 0 8px}.filters '
                  'label{margin:0;width:170px;font-size:11px}.filters '
                  '.search{width:auto;flex:1}.result-count{font-size:11px;color:#7c8b7f;margin:11px '
                  '0}.panel{background:white;border:1px solid '
                  'var(--border);border-radius:9px;padding:26px}.form-grid{display:grid;grid-template-columns:minmax(0,1.8fr) '
                  '1fr;gap:23px;max-width:1000px}.two-col{display:grid;grid-template-columns:1fr '
                  '1fr;gap:18px}.form-actions{display:flex;justify-content:space-between;gap:10px;border-top:1px '
                  'solid var(--border);padding-top:21px;margin-top:25px}.aside-card{border:1px solid '
                  '#d4dfce;border-radius:9px;background:#e9f0e2;padding:28px;align-self:start}.aside-card '
                  'h2{font-size:23px;line-height:1.4;margin:16px 0}.aside-card p,.aside-card '
                  'li{font-size:12px;color:#52684c}.aside-card '
                  'ol{padding-left:18px;line-height:2.5}.back{display:inline-block;font-size:12px;margin:0 0 '
                  '23px}.alert{border:1px solid #e8b8a4;border-left:3px solid '
                  '#bd6c4e;background:#fff2e9;padding:14px '
                  '16px;border-radius:6px;color:#8b442c;margin-bottom:18px;font-size:13px}.success{background:#e9f4e7;border:1px '
                  'solid #cbdcbe;padding:12px '
                  '15px;border-radius:6px;color:#3c6a39;font-size:12px;margin-bottom:18px}.field-error{font-size:11px;color:#a2442e;font-weight:400}.detail-grid{display:grid;grid-template-columns:minmax(0,1.7fr) '
                  '1fr;gap:22px}.evidence-list{padding:0;list-style:none;margin:16px 0 23px}.evidence-list '
                  'li{display:flex;align-items:center;gap:11px;border-top:1px solid '
                  'var(--border);padding:15px 0}.evidence-list li>div{flex:1;min-width:0}.evidence-list '
                  'strong{font-size:12px}.evidence-list p{font-size:11px;color:#7c8d7c;margin:3px '
                  '0;overflow-wrap:anywhere}.check{font-size:21px;color:#aab8a7}.check.done{color:#387948}.evidence-form{border-top:1px '
                  'solid var(--border);padding-top:8px}.decision{align-self:start}.decision '
                  'h2{margin-top:10px}.decision p{font-size:12px;color:#73826e;margin:19px 0}.decision '
                  'button{width:100%;margin-bottom:9px}.decision hr{border:0;border-top:1px solid '
                  'var(--border);margin:23px 0}.decision a{font-size:11px}.decision '
                  'dl{display:grid;grid-template-columns:1fr 1fr;font-size:12px;gap:10px}.decision '
                  'dt{color:#84917c}.decision dd{margin:0;text-align:right}.audit{margin-top:23px}.audit '
                  'ol{list-style:none;padding:0}.audit '
                  'li{display:flex;gap:13px;align-items:start;border-bottom:1px solid #eef1e9;padding:16px '
                  '0}.audit li:last-child{border:0}.audit '
                  'b{font-size:12px;font-weight:500;overflow-wrap:anywhere}.audit '
                  'small{display:block;font-size:10px;margin-top:4px}.timeline-dot{display:block;width:8px;height:8px;border-radius:50%;background:#8ca37c;margin-top:5px}.method{max-width:940px}.method '
                  'p,.method li{font-size:13px;color:#62725c}.method table{margin:22px 0}.method '
                  'h3{margin-top:28px}.empty{text-align:center;padding:55px 20px;border:1px dashed '
                  '#b8c8b4;border-radius:9px}.empty p{color:#798b70;font-size:12px}.loading{padding:28px '
                  '0;color:#7c8b70;font-size:12px}.skeleton{height:44px;border-radius:7px;background:linear-gradient(90deg,#e6ece1,#f0f4ec,#e6ece1);margin-bottom:12px;animation:pulse '
                  '1s infinite alternate}@keyframes '
                  'pulse{to{opacity:.5}}.welcome{max-width:1000px;margin:auto;padding:55px '
                  '42px}.welcome>.brand{margin-bottom:67px}.welcome '
                  'h1{font-size:48px;line-height:1.22;letter-spacing:-2px;margin:22px 0}.welcome h1 '
                  'span{color:#73936b}.welcome>p:not(.small){max-width:570px;font-size:16px;color:#75866c}.welcome>button{margin:14px '
                  '0 '
                  '10px}.welcome>.small{max-width:570px;line-height:1.7}.welcome-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:30px;border-top:1px '
                  'solid #dce5d5;padding-top:28px;margin-top:55px}.welcome-grid '
                  'b{font-size:12px;color:#345c2f}.welcome-grid '
                  'p{font-size:12px;color:#819174;margin-top:9px}.welcome '
                  'footer{font-size:10px;color:#8c9980;padding-top:34px}\n'
                  '@media(min-width:1500px){.content{padding-top:45px}.title-row{margin-bottom:36px}}\n'
                  '@media(max-width:1050px){aside{width:190px;padding:25px '
                  '15px}.main-area{margin-left:190px;width:calc(100% - 190px)}.content{padding:28px '
                  '25px}.stats{gap:10px}.stat{padding:16px 12px}.stat small{font-size:9px}th,td{padding:14px '
                  '12px}.topbar{padding:0 25px}.detail-grid{grid-template-columns:minmax(0,1.5fr) '
                  '1fr}.panel{padding:20px}.form-grid{grid-template-columns:1.6fr 1fr}}\n'
                  '@media(max-width:760px){aside{position:static;width:100%;height:auto;padding:17px '
                  '18px;gap:14px}.app-shell{display:block}.main-area{margin:0;width:100%}aside '
                  '.brand{font-size:19px}.workspace-label,.sidebar-note,aside>.subtle{display:none}nav{display:flex;justify-content:space-between;gap:5px}nav '
                  'a{padding:8px 10px;gap:6px;font-size:16px}nav a '
                  'span{font-size:10px}.topbar{height:46px;padding:0 '
                  '20px;font-size:10px}.demo-tag{font-size:8px;padding:5px}.content{padding:28px '
                  '20px}.title-row{align-items:flex-start;gap:12px;margin-bottom:25px}.title-row '
                  'h1{font-size:27px}.title-row .button{font-size:11px;padding:9px '
                  '10px;white-space:nowrap}.title-row '
                  '.muted{font-size:12px}.stats{grid-template-columns:repeat(2,1fr);gap:11px;margin-bottom:29px}.stat{padding:18px}.stat '
                  'small{font-size:10px}.stat strong{font-size:32px;margin:5px '
                  '0}.section-heading>a{white-space:nowrap;font-size:10px}.section-heading '
                  'h2{font-size:16px}.table-wrap '
                  'table{min-width:650px}.table-wrap{position:relative}.insight{padding:20px '
                  '17px;gap:12px}.insight '
                  'h2{font-size:15px}.insight-mark{font-size:27px}.app-footer{padding:16px '
                  '20px;font-size:9px}.filters{flex-wrap:wrap;gap:10px}.filters '
                  '.search{flex-basis:100%}.filters '
                  'label{flex:1;width:auto}.form-grid,.detail-grid{grid-template-columns:1fr}.form-grid '
                  '.aside-card{order:-1}.aside-card{padding:18px}.aside-card '
                  'h2{font-size:18px;line-height:1.3;margin:8px 0}.aside-card h2 br{display:none}.aside-card '
                  'ol,.aside-card>.small{display:none}.aside-card '
                  'p{margin-bottom:0}.two-col{gap:12px}.panel{padding:20px 17px}.evidence-list '
                  '.badge{font-size:9px}.evidence-list{margin-bottom:15px}.evidence-list '
                  'strong{font-size:11px}.evidence-list p{font-size:10px}.decision '
                  'dl{grid-template-columns:1fr 1fr}.method{overflow:auto}.method '
                  'table{min-width:500px}.welcome{padding:30px '
                  '23px}.welcome>.brand{margin-bottom:50px}.welcome '
                  'h1{font-size:35px;letter-spacing:-1.3px}.welcome>p:not(.small){font-size:14px}.welcome-grid{grid-template-columns:1fr;gap:13px;margin-top:40px}.welcome-grid '
                  'p{margin-bottom:7px}.welcome footer{font-size:9px}}\n'
                  '@media(prefers-reduced-motion:reduce){.skeleton{animation:none}}\n'
                  '\n'
                  '@media(max-width:760px){.table-wrap{background:transparent;border:0;overflow:visible}.table-wrap '
                  'table{min-width:0;display:block}.table-wrap thead{display:none}.table-wrap '
                  'tbody{display:grid;gap:12px}.table-wrap tr{display:block;background:white;border:1px '
                  'solid var(--border);border-radius:8px;padding:15px}.table-wrap '
                  'td{display:flex;align-items:center;justify-content:space-between;border:0;padding:7px '
                  '0;gap:12px}.table-wrap td:first-child{display:block;border-bottom:1px solid '
                  '#edf0e9;padding:0 0 12px;margin-bottom:5px}.table-wrap '
                  'td[data-label]::before{content:attr(data-label);color:#7c8b76;font-size:11px}.table-wrap '
                  'td[data-label="Evidence"]{flex-wrap:wrap}.table-wrap td '
                  '.progress{display:none}.table-wrap td '
                  'small{margin-top:4px}.vendor-link{font-size:14px}}\n'}
if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--extract',required=True);args=parser.parse_args()
    root=pathlib.Path(args.extract)
    if root.exists() and any(root.iterdir()):raise SystemExit('Refusing nonempty destination')
    root.mkdir(parents=True,exist_ok=True)
    for name,content in FILES.items():
        path=root/name
        if root.resolve() not in path.resolve().parents:raise SystemExit('Invalid path')
        path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
    print('Extracted',len(FILES),'reviewable source files to',root)
