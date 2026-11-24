// Original Vendor Gate adapter for Workers + D1. Local-only until live verification.
export const requirements={low:['business'],medium:['business','privacy'],high:['business','privacy','security','financial']};
export function riskFor(amount,data,country){const n=(amount>=100000?2:amount>=20000?1:0)+(data==='sensitive'?2:data==='personal'?1:0)+(['India','United Kingdom','United States','Singapore'].includes(country)?0:1);return n>=3?'high':n>=1?'medium':'low'}
const stamp=()=>new Date().toISOString();
const id=(n=16)=>{const b=new Uint8Array(n);crypto.getRandomValues(b);return [...b].map(x=>x.toString(16).padStart(2,'0')).join('')};
const result=(body,status=200)=>new Response(JSON.stringify(body),{status,headers:{'Content-Type':'application/json','Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'same-origin'}});
const all=async(db,sql,...args)=>(await db.prepare(sql).bind(...args).all()).results;
const first=async(db,sql,...args)=>db.prepare(sql).bind(...args).first();
const statement=(db,sql,...args)=>db.prepare(sql).bind(...args);
const audit=(db,vid,action,detail)=>statement(db,'INSERT INTO audit(vendor,action,detail,created) VALUES(?,?,?,?)',vid,action,detail,stamp());
async function detail(db,v){const evidence=await all(db,'SELECT kind,reference,created FROM evidence WHERE vendor=? ORDER BY kind',v.id);return {...v,evidence,required:requirements[v.risk],missing:requirements[v.risk].filter(k=>!evidence.some(e=>e.kind===k)),audit:await all(db,'SELECT action,detail,created FROM audit WHERE vendor=? ORDER BY id DESC',v.id)}}
export default {async fetch(request,env){try{return await handle(request,env)}catch(e){console.error('Vendor Gate API failure',e.name);return result({error:'The workspace could not be loaded. Try again.'},500)}}};
export async function handle(request,env){
 const url=new URL(request.url),path=url.pathname,method=request.method,db=env.DB;
 if(!path.startsWith('/api/'))return env.ASSETS.fetch(request);
 if(['POST','PUT','PATCH','DELETE'].includes(method)){
  if(request.headers.get('Origin')&&new URL(request.headers.get('Origin')).origin!==url.origin)return result({error:'Cross-origin writes are not allowed.'},403);
  const body=await request.clone().text();if(new TextEncoder().encode(body).length>32768)return result({error:'Request too large.'},413);
 }
 if(path==='/api/health'&&method==='GET'){await first(db,'SELECT 1 AS ok');return result({ok:true,project:'vendor-gate',storage:'d1',synthetic:true})}
 let workspace=request.headers.get('X-Workspace')||'';
 if(path!=='/api/workspaces'){
  if(!/^[a-f0-9]{32}$/.test(workspace)||!await first(db,'SELECT id FROM workspaces WHERE id=?',workspace))return result({error:'This demo session has expired. Start a new workspace.'},401);
 }
 if(path==='/api/workspaces'&&method==='POST'){
  const cutoff=new Date(Date.now()-7*86400000).toISOString();
  await db.batch([
   statement(db,'DELETE FROM audit WHERE vendor IN (SELECT id FROM vendors WHERE workspace IN (SELECT id FROM workspaces WHERE created<?))',cutoff),
   statement(db,'DELETE FROM evidence WHERE vendor IN (SELECT id FROM vendors WHERE workspace IN (SELECT id FROM workspaces WHERE created<?))',cutoff),
   statement(db,'DELETE FROM vendors WHERE workspace IN (SELECT id FROM workspaces WHERE created<?)',cutoff),
   statement(db,'DELETE FROM workspaces WHERE created<?',cutoff)]);
  if((await first(db,'SELECT count(*) AS n FROM workspaces')).n>=100)return result({error:'This demo is at capacity. Try again after workspace expiry.'},503);
  workspace=id();const statements=[statement(db,'INSERT INTO workspaces VALUES(?,?)',workspace,stamp())];
  for(const [name,category,country,amount,data]of[['Northstar Cloud','Software','India',35000,'personal'],['Maple Office','Facilities','United Kingdom',8500,'none'],['Harbor Analytics','Data services','Singapore',120000,'sensitive']]){const vid=id(8);statements.push(statement(db,'INSERT INTO vendors VALUES(?,?,?,?,?,?,?,?,?,?,?)',vid,workspace,name,category,country,amount,data,riskFor(amount,data,country),'draft',1,stamp()),audit(db,vid,'created','Synthetic seed vendor created'))}
  await db.batch(statements);return result({workspace},201);
 }
 if(path==='/api/vendors'&&method==='GET'){const rows=await all(db,'SELECT * FROM vendors WHERE workspace=? ORDER BY created DESC',workspace);return result({vendors:await Promise.all(rows.map(v=>detail(db,v)))})}
 let data={};if(['POST','PATCH'].includes(method)){try{data=await request.json()}catch{return result({error:'Expected a JSON object.'},400)}if(!data||Array.isArray(data)||typeof data!=='object')return result({error:'Expected a JSON object.'},400)}
 if(path==='/api/vendors'&&method==='POST'){
  if((await first(db,'SELECT count(*) AS n FROM vendors WHERE workspace=?',workspace)).n>=40)return result({error:'Demo limit: 40 vendors per workspace.'},429);
  const name=String(data.name||'').trim(),category=String(data.category||'').trim(),country=String(data.country||'').trim(),access=data.data_access,amount=typeof data.amount==='number'?data.amount:Number(data.amount),fields={};
  if(name.length<2||name.length>80)fields.name='Enter 2-80 characters.';
  if(!['Software','Facilities','Data services','Consulting'].includes(category))fields.category='Choose a valid category.';
  if(!['India','United Kingdom','United States','Singapore','Other'].includes(country))fields.country='Choose a country.';
  if(!Number.isInteger(amount)||amount<0||amount>10000000||data.amount===undefined||data.amount===null||data.amount==='')fields.amount='Enter an annual amount between 0 and 10,000,000.';
  if(!['none','personal','sensitive'].includes(access))fields.data_access='Choose a data access level.';
  if(await first(db,'SELECT id FROM vendors WHERE workspace=? AND lower(name)=lower(?)',workspace,name))fields.name='A vendor with this name already exists.';
  if(Object.keys(fields).length)return result({error:'Check the highlighted fields.',fields},422);
  const vid=id(8),risk=riskFor(amount,access,country);await db.batch([statement(db,'INSERT INTO vendors VALUES(?,?,?,?,?,?,?,?,?,?,?)',vid,workspace,name,category,country,amount,access,risk,'draft',1,stamp()),audit(db,vid,'created',`Risk calculated: ${risk}`)]);return result({vendor:await detail(db,await first(db,'SELECT * FROM vendors WHERE id=?',vid))},201);
 }
 const match=path.match(/^\/api\/vendors\/([a-f0-9]{16})$/);
 if(match&&['GET','PATCH'].includes(method)){
  const vid=match[1],row=await first(db,'SELECT * FROM vendors WHERE id=? AND workspace=?',vid,workspace);if(!row)return result({error:'Vendor not found in this workspace.'},404);
  if(method==='GET')return result({vendor:await detail(db,row)});
  if(data.version!==row.version)return result({error:'Another change was saved. Refresh this vendor before continuing.',conflict:true},409);
  // D1 batch is transactional. Version guard is checked again by SQL before writes.
  let writes=[];
  if(data.action==='evidence'){
   const kind=data.kind,reference=String(data.reference||'').trim();if(!requirements[row.risk].includes(kind))return result({error:'Evidence type is not required for this risk level.'},422);if(reference.length<5||reference.length>180)return result({error:'Evidence reference must be 5-180 characters.'},422);if(row.status==='approved')return result({error:'Approved vendors are locked. Reopen review first.'},409);
   writes=[statement(db,'INSERT INTO evidence(id,vendor,kind,reference,created) SELECT ?,?,?,?,? WHERE EXISTS(SELECT 1 FROM vendors WHERE id=? AND version=?) ON CONFLICT(vendor,kind) DO UPDATE SET reference=excluded.reference,created=excluded.created',id(8),vid,kind,reference,stamp(),vid,row.version)];
   writes.push(statement(db,'INSERT INTO audit(vendor,action,detail,created) SELECT ?,?,?,? WHERE EXISTS(SELECT 1 FROM vendors WHERE id=? AND version=?)',vid,'evidence',`${kind}: ${reference}`,stamp(),vid,row.version));
  }else if(data.action==='transition'){
   const target=data.status,allowed={draft:['review'],review:['approved','draft'],approved:['review']};if(!allowed[row.status].includes(target))return result({error:'This status transition is not allowed.'},422);
   const current=await detail(db,row);if(target==='approved'&&current.missing.length)return result({error:'Approval blocked: missing '+current.missing.join(', '),missing:current.missing},422);
   writes=[statement(db,'UPDATE vendors SET status=? WHERE id=? AND version=?',target,vid,row.version),statement(db,'INSERT INTO audit(vendor,action,detail,created) SELECT ?,?,?,? WHERE EXISTS(SELECT 1 FROM vendors WHERE id=? AND version=?)',vid,'status',`${row.status} to ${target}`,stamp(),vid,row.version)];
  }else return result({error:'Unknown update action.'},422);
  writes.push(statement(db,'UPDATE vendors SET version=version+1 WHERE id=? AND version=?',vid,row.version));
  const outputs=await db.batch(writes);if(outputs.at(-1).meta.changes===0)return result({error:'Another change was saved. Refresh this vendor before continuing.',conflict:true},409);
  return result({vendor:await detail(db,await first(db,'SELECT * FROM vendors WHERE id=?',vid))});
 }
 return result({error:'Route not found.'},404);
}
