// Local harness only. Exercises the Worker request handler with real SQLite.
// Not proof of Cloudflare runtime or remote D1 behavior.
import http from 'node:http';
import {DatabaseSync} from 'node:sqlite';
import {readFileSync,existsSync,statSync} from 'node:fs';
import {resolve,extname} from 'node:path';
import handler from './index.mjs';
const sql=new DatabaseSync(process.env.VENDOR_WORKER_DB||'/tmp/vendor-gate-worker-local.sqlite');
sql.exec(readFileSync(new URL('./schema.sql',import.meta.url),'utf8'));
const prepare=q=>({bind(...args){return {query:q,args,async all(){return {results:sql.prepare(q).all(...args)}},async first(){return sql.prepare(q).get(...args)||null}}},async first(){return sql.prepare(q).get()||null}});
const batch=async(statements)=>{sql.exec('BEGIN');try{const results=statements.map(s=>({meta:{changes:Number(sql.prepare(s.query).run(...s.args).changes)}}));sql.exec('COMMIT');return results}catch(e){sql.exec('ROLLBACK');throw e}};
const root=resolve(new URL('../static/',import.meta.url).pathname);
const types={'.html':'text/html','.js':'text/javascript','.css':'text/css','.svg':'image/svg+xml'};
const env={DB:{prepare,batch},ASSETS:{async fetch(request){const u=new URL(request.url);let path=resolve(root,'.'+u.pathname);if(!path.startsWith(root+'/')||!existsSync(path)||!statSync(path).isFile())path=root+'/index.html';return new Response(readFileSync(path),{headers:{'Content-Type':types[extname(path)]||'application/octet-stream'}})}}};
http.createServer(async(req,res)=>{try{const chunks=[];for await(const c of req)chunks.push(c);const body=Buffer.concat(chunks);const request=new Request('http://'+req.headers.host+req.url,{method:req.method,headers:req.headers,...(body.length?{body}:{} )});const response=await handler.fetch(request,env);res.writeHead(response.status,Object.fromEntries(response.headers));res.end(Buffer.from(await response.arrayBuffer()))}catch(e){console.error(e);res.writeHead(500);res.end('Local harness error')}}).listen(4178,'127.0.0.1',()=>console.log('Local Worker adapter on 4178, SQLite simulation only'));
