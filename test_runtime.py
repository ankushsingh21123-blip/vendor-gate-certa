"""Disposable local production-process replacement acceptance. Not Docker/host proof."""
import json, os, pathlib, signal, socket, subprocess, tempfile, time, unittest
from urllib.request import Request, urlopen

ROOT = pathlib.Path(__file__).resolve().parent

class RuntimeTest(unittest.TestCase):
    def test_production_launcher_and_restart_persistence(self):
        with tempfile.TemporaryDirectory(prefix='vendor-runtime-') as folder:
            with socket.socket() as sock:
                sock.bind(('127.0.0.1', 0)); port = sock.getsockname()[1]
            base = f'http://127.0.0.1:{port}'
            env = dict(os.environ, PORT=str(port), VENDOR_DB_PATH=str(pathlib.Path(folder)/'demo.sqlite3'))
            def call(path, method='GET', payload=None, token=None):
                headers = {'Content-Type':'application/json'}
                if token: headers['X-Workspace'] = token
                data = json.dumps(payload).encode() if payload is not None else None
                with urlopen(Request(base+path, data=data, method=method, headers=headers), timeout=4) as r:
                    raw = r.read()
                    return json.loads(raw) if 'json' in r.headers.get('Content-Type','') else raw.decode()
            def start():
                p = subprocess.Popen(['sh','start.sh'], cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True)
                for _ in range(100):
                    if p.poll() is not None: self.fail(p.stdout.read().decode())
                    try:
                        if call('/api/health')['ok']: return p
                    except (OSError, ValueError): time.sleep(.05)
                stop(p); self.fail('Server failed readiness')
            def stop(p):
                if p.poll() is None:
                    os.killpg(p.pid, signal.SIGTERM)
                    try: p.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        os.killpg(p.pid, signal.SIGKILL); p.wait(timeout=5)
                p.stdout.close()
            p = start()
            try:
                self.assertIn('<div id="root">', call('/'))
                token = call('/api/workspaces','POST',{},None)['workspace']
                v = call('/api/vendors','POST',{'name':'Runtime synthetic vendor','category':'Software','country':'India','amount':5000,'data_access':'none'},token)['vendor']
                vid = v['id']
                v = call('/api/vendors/'+vid,'PATCH',{'action':'evidence','version':v['version'],'kind':'business','reference':'Synthetic registry 123'},token)['vendor']
                self.assertEqual(v['missing'],[])
            finally: stop(p)
            p = start()
            try:
                saved = call('/api/vendors/'+vid, token=token)['vendor']
                self.assertEqual(saved['name'],'Runtime synthetic vendor')
                self.assertEqual(saved['version'],v['version'])
                self.assertEqual(len(saved['audit']),2)
                self.assertEqual(saved['evidence'][0]['reference'],'Synthetic registry 123')
            finally: stop(p)

if __name__ == '__main__': unittest.main(verbosity=2)
