import os, tempfile, unittest, importlib
os.environ['VENDOR_DB_PATH']=tempfile.mktemp(suffix='.sqlite')
from api.index import app,risk_for
class ApiTest(unittest.TestCase):
 def setUp(self):
  self.c=app.test_client();self.token=self.c.post('/api/workspaces').json['workspace'];self.h={'X-Workspace':self.token};self.v=self.c.get('/api/vendors',headers=self.h).json['vendors'][0]
 def patch(self,v,body):return self.c.patch('/api/vendors/'+v['id'],headers=self.h,json={'version':v['version'],**body})
 def test_session_required(self):self.assertEqual(self.c.get('/api/vendors').status_code,401)
 def test_isolation(self):
  t=self.c.post('/api/workspaces').json['workspace'];r=self.c.get('/api/vendors/'+self.v['id'],headers={'X-Workspace':t});self.assertEqual(r.status_code,404)
 def test_risk_boundaries(self):
  self.assertEqual(risk_for(19999,'none','India'),'low');self.assertEqual(risk_for(20000,'none','India'),'medium');self.assertEqual(risk_for(100000,'personal','India'),'high');self.assertEqual(risk_for(1,'sensitive','Other'),'high')
 def test_validation(self):
  r=self.c.post('/api/vendors',headers=self.h,json={'name':'x','amount':-1});self.assertEqual(r.status_code,422);self.assertIn('name',r.json['fields'])
 def test_duplicate(self):
  r=self.c.post('/api/vendors',headers=self.h,json={**self.v,'name':self.v['name'].upper()});self.assertEqual(r.status_code,422)
 def test_create_persists(self):
  r=self.c.post('/api/vendors',headers=self.h,json={'name':'Cedar Test','category':'Software','country':'India','amount':150000,'data_access':'sensitive'});self.assertEqual(r.status_code,201);self.assertEqual(r.json['vendor']['risk'],'high');self.assertEqual(self.c.get('/api/vendors/'+r.json['vendor']['id'],headers=self.h).json['vendor']['name'],'Cedar Test')
 def test_invalid_transition(self):self.assertEqual(self.patch(self.v,{'action':'transition','status':'approved'}).status_code,422)
 def test_approval_blocked(self):
  v=self.patch(self.v,{'action':'transition','status':'review'}).json['vendor'];r=self.patch(v,{'action':'transition','status':'approved'});self.assertEqual(r.status_code,422);self.assertTrue(r.json['missing'])
 def test_full_workflow(self):
  v=self.v
  for kind in v['required']:v=self.patch(v,{'action':'evidence','kind':kind,'reference':'Demo reference checked'}).json['vendor']
  v=self.patch(v,{'action':'transition','status':'review'}).json['vendor'];v=self.patch(v,{'action':'transition','status':'approved'}).json['vendor'];self.assertEqual(v['status'],'approved');self.assertGreater(len(v['audit']),3)
  self.assertEqual(self.patch(v,{'action':'evidence','kind':'business','reference':'Changed note'}).status_code,409)
  self.assertEqual(self.patch(v,{'action':'transition','status':'review'}).json['vendor']['status'],'review')
 def test_stale_write(self):
  self.patch(self.v,{'action':'transition','status':'review'});self.assertEqual(self.patch(self.v,{'action':'transition','status':'review'}).status_code,409)
 def test_unknown_evidence(self):self.assertEqual(self.patch(self.v,{'action':'evidence','kind':'bad','reference':'something'}).status_code,422)
 def test_reference_validation(self):self.assertEqual(self.patch(self.v,{'action':'evidence','kind':'business','reference':'x'}).status_code,422)
 def test_no_html_execution(self):
  r=self.c.post('/api/vendors',headers=self.h,json={'name':'<script>alert(1)</script>','category':'Software','country':'India','amount':0,'data_access':'none'});self.assertEqual(r.status_code,201);self.assertIn('<script>',r.json['vendor']['name'])
 def test_origin_protection(self):
  self.assertEqual(self.c.post('/api/workspaces',headers={'Origin':'https://evil.invalid'}).status_code,403)
 def test_invalid_json(self):self.assertEqual(self.c.post('/api/vendors',headers=self.h,data='[',content_type='application/json').status_code,422)
if __name__=='__main__':unittest.main(verbosity=2)
