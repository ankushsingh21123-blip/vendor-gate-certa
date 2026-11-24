export type Risk='low'|'medium'|'high';
export type Vendor={id:string;name:string;category:string;country:string;amount:number;data_access:string;risk:Risk;status:'draft'|'review'|'approved';version:number;evidence:{kind:string;reference:string;created:string}[];required:string[];missing:string[];audit:{action:string;detail:string;created:string}[]};
export const riskLabel={low:'Low risk',medium:'Medium risk',high:'High risk'};
export function summarize(v:Vendor[]){return {total:v.length,review:v.filter(x=>x.status==='review').length,high:v.filter(x=>x.risk==='high').length,approved:v.filter(x=>x.status==='approved').length}}
export function filterVendors(v:Vendor[],query:string,status:string,risk:string){const q=query.trim().toLowerCase();return v.filter(x=>(!q||`${x.name} ${x.category} ${x.country}`.toLowerCase().includes(q))&&(!status||x.status===status)&&(!risk||x.risk===risk))}
export function currency(n:number){return new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0}).format(n)}
