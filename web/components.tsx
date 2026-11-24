import React from'react';
export function Badge({kind,children}:{kind:string;children:React.ReactNode}){return <span className={'badge '+kind}>{children}</span>}
export function EvidenceGate({missing,busy,onApprove}:{missing:number;busy:boolean;onApprove:()=>void}){return <button disabled={busy||missing>0} onClick={onApprove} title={missing?`${missing} evidence items required`:'All evidence recorded'}>Approve vendor ✓</button>}
