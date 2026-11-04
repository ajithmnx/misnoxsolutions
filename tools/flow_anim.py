"""Nov 2026: scroll-triggered, hover-inspectable invoice flow (capture → rules → post) on home."""
p='index.html'; s=open(p,encoding='utf-8').read()
reg=s.index("register('home'")
a=s.index('<div class="iflow" role="img"',reg); b=s.index('<p class="inote">',a)
NEW=r'''<div class="fx" id="fx">
      <div class="fx-bar"><span class="mono">PIPELINE</span><span class="fx-run" id="fx-run">idle</span><span class="fx-prog"><i id="fx-prog"></i></span><button class="fx-replay" type="button" id="fx-replay" aria-label="Replay the example">↻ Replay</button></div>
      <div class="iflow fx-row">
        <div class="inode fx-node" data-s="0" tabindex="0">
          <span class="mono">1 · CAPTURE</span><h3>Supplier invoice</h3>
          <div class="fx-doc" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><span class="fx-scan"></span></div>
          <div class="kv"><span>source</span><b>AP inbox (PDF)</b><span>supplier</span><b data-v="Northwind Freight (sample)">—</b><span>invoice</span><b data-v="INV-20418">—</b><span>amount</span><b data-v="$18,640.00">—</b></div>
          <div class="fx-foot"><span class="itag" data-done="Extracted ✓">Incoming</span><span class="fx-ms" data-v="OCR · 312 ms"></span></div>
        </div>
        <div class="fx-wire" aria-hidden="true"><svg viewBox="0 0 60 12" preserveAspectRatio="none"><path d="M0 6h54M49 1l5 5-5 5"/></svg><span class="fx-pkt">INV</span></div>
        <div class="inode core fx-node" data-s="1" tabindex="0">
          <span class="mono">2 · VALIDATE · MAP · ROUTE</span><h3><svg viewBox="0 0 100 100" width="18" height="18" aria-hidden="true"><use href="#mx-mark"/></svg>Your rules, enforced</h3>
          <div class="ichecks fx-checks">
            <span data-tip="Invoice lines agree with purchase order PO-7713 within tolerance">Matched to PO-7713</span>
            <span data-tip="GL 5120 Freight and cost centre FIN-02 exist and are open for posting">GL 5120 · cost centre FIN-02 valid</span>
            <span data-tip="Amount above $10,000 threshold: routed to a second approver before posting">Over $10k: second approver asked</span>
            <span data-tip="Every check, value and approver recorded against the invoice">Audit trail written</span>
          </div>
          <div class="fx-tip" id="fx-tip">Hover a check to see the rule.</div>
          <div class="fx-foot"><span class="itag" data-done="4/4 rules passed">Waiting</span><span class="fx-ms" data-v="rules · 41 ms"></span></div>
        </div>
        <div class="fx-wire" aria-hidden="true"><svg viewBox="0 0 60 12" preserveAspectRatio="none"><path d="M0 6h54M49 1l5 5-5 5"/></svg><span class="fx-pkt">PI</span></div>
        <div class="inode fx-node" data-s="2" tabindex="0">
          <span class="mono">3 · POST</span><h3><svg width="16" height="16" aria-hidden="true"><use href="#lg-ms"/></svg>Business Central</h3>
          <div class="kv"><span>journal</span><b>Purchase invoice</b><span>doc no.</span><b data-v="PI-104382">—</b><span>status</span><b class="fx-status">Waiting</b></div>
          <code class="fx-api">POST /purchaseInvoices → <em>201 Created</em></code>
          <div class="fx-foot"><span class="itag" data-done="✓ Complete">Pending</span><span class="fx-ms" data-v="API · 188 ms"></span></div>
        </div>
      </div>
      <div class="fx-insp" aria-live="polite"><div class="fx-insp-h"><span class="mono" id="fx-insp-t">PAYLOAD · CAPTURE</span><span class="mono fx-hint">hover a step to inspect</span></div><pre id="fx-json"></pre></div>
    </div>
    '''
s=s[:a]+NEW+s[b:]
JS=r'''
const FX_JSON=[
`{
  "source": "ap-inbox",
  "file": "INV-20418.pdf",
  "supplier": { "name": "Northwind Freight", "abn": "•• ••• ••• •••" },
  "invoiceNo": "INV-20418",
  "poRef": "PO-7713",
  "lines": 3,
  "total": 18640.00,
  "currency": "AUD",
  "confidence": 0.98
}`,
`{
  "rules": [
    { "id": "po_match", "po": "PO-7713", "tolerance": "0.5%", "result": "pass" },
    { "id": "gl_valid", "account": "5120", "costCentre": "FIN-02", "result": "pass" },
    { "id": "approval_limit", "threshold": 10000, "route": "second_approver", "result": "pass" },
    { "id": "audit", "written": true }
  ],
  "decision": "post"
}`,
`POST /api/v2.0/companies({id})/purchaseInvoices
{
  "vendorNumber": "V-0091",
  "vendorInvoiceNumber": "INV-20418",
  "postingDate": "2026-11-04",
  "totalAmountIncludingTax": 18640.00
}
→ 201 Created  { "number": "PI-104382", "status": "Open" }`];
const FX_T=['PAYLOAD · CAPTURE','RULES · EVALUATION','API · BUSINESS CENTRAL'];
function initFlow(){const fx=document.getElementById('fx');if(!fx)return;
  const nodes=[...fx.querySelectorAll('.fx-node')],wires=[...fx.querySelectorAll('.fx-wire')],pre=document.getElementById('fx-json'),tt=document.getElementById('fx-insp-t'),run=document.getElementById('fx-run'),prog=document.getElementById('fx-prog'),tip=document.getElementById('fx-tip');
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;let timers=[],hover=false;
  const show=i=>{pre.textContent=FX_JSON[i];tt.textContent=FX_T[i];nodes.forEach((n,k)=>n.classList.toggle('insp',k===i))};
  const at=(ms,f)=>timers.push(setTimeout(f,ms));
  const finish=n=>{n.querySelectorAll('[data-v]').forEach(e=>e.textContent=e.dataset.v);const t=n.querySelector('.itag');if(t)t.textContent=t.dataset.done;n.classList.add('done')};
  function reset(){timers.forEach(clearTimeout);timers=[];fx.classList.remove('live');nodes.forEach(n=>{n.classList.remove('done','act');n.querySelectorAll('b[data-v]').forEach(e=>e.textContent='—');n.querySelectorAll('.fx-ms').forEach(e=>e.textContent='');const t=n.querySelector('.itag');t.textContent=['Incoming','Waiting','Pending'][+n.dataset.s]});fx.querySelectorAll('.fx-checks span').forEach(c=>c.classList.remove('ok'));wires.forEach(w=>w.classList.remove('go'));fx.querySelector('.fx-status').textContent='Waiting';prog.style.width='0';run.textContent='idle';show(0)}
  function type(el,ms){const v=el.dataset.v;let i=0;const t=setInterval(()=>{el.textContent=v.slice(0,++i);if(i>=v.length)clearInterval(t)},ms);timers.push(t)}
  function play(){reset();fx.classList.add('live');run.textContent='running';
    if(reduce){nodes.forEach(finish);fx.querySelectorAll('.fx-checks span').forEach(c=>c.classList.add('ok'));fx.querySelector('.fx-status').textContent='Approved, posted';prog.style.width='100%';run.textContent='completed';return}
    nodes[0].classList.add('act');if(!hover)show(0);
    nodes[0].querySelectorAll('b[data-v]').forEach((e,k)=>at(500+k*380,()=>type(e,22)));
    at(1900,()=>{finish(nodes[0]);nodes[0].classList.remove('act');prog.style.width='33%';wires[0].classList.add('go')});
    at(2700,()=>{nodes[1].classList.add('act');if(!hover)show(1)});
    [...fx.querySelectorAll('.fx-checks span')].forEach((c,k)=>at(3000+k*450,()=>c.classList.add('ok')));
    at(4900,()=>{finish(nodes[1]);nodes[1].classList.remove('act');prog.style.width='66%';wires[1].classList.add('go')});
    at(5700,()=>{nodes[2].classList.add('act');if(!hover)show(2);fx.querySelector('.fx-status').textContent='Posting…'});
    at(6600,()=>{finish(nodes[2]);nodes[2].classList.remove('act');fx.querySelector('.fx-status').textContent='Approved, posted';prog.style.width='100%';run.textContent='completed · 7.1 s'});}
  nodes.forEach((n,i)=>{const on=()=>{hover=true;show(i)},off=()=>{hover=false};n.addEventListener('mouseenter',on);n.addEventListener('focus',on);n.addEventListener('mouseleave',off);n.addEventListener('blur',off)});
  fx.querySelectorAll('.fx-checks span').forEach(c=>{c.addEventListener('mouseenter',()=>tip.textContent=c.dataset.tip);c.addEventListener('mouseleave',()=>tip.textContent='Hover a check to see the rule.')});
  document.getElementById('fx-replay').onclick=play;
  reset();
  if('IntersectionObserver' in window){let seen=false;new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting&&!seen){seen=true;play()}else if(!e.isIntersecting&&e.boundingClientRect.top>0){seen=false}}),{threshold:.45}).observe(fx)}else play();
  const row=fx.querySelector('.fx-row');window.addEventListener('scroll',()=>{const r=fx.getBoundingClientRect(),v=Math.max(-1,Math.min(1,(r.top+r.height/2-innerHeight/2)/innerHeight));row.style.setProperty('--tilt',v)},{passive:true});
}
'''
s=s.replace("const HOME_TILES={",JS+"\nconst HOME_TILES={",1)
s=s.replace("if(p==='home'){initHome();initImap();initPhases()}","if(p==='home'){initHome();initImap();initPhases();initFlow()}",1)
CSS='''
/* ── Interactive invoice pipeline (Nov 2026) ── */
.fx{position:relative}
.fx-bar{display:flex;align-items:center;gap:14px;margin-bottom:14px;font:500 12px 'IBM Plex Mono',monospace;color:var(--muted)}
.fx-run{color:var(--accent2)}.fx-run::before{content:'';display:inline-block;width:7px;height:7px;border-radius:50%;background:#B9B4CC;margin-right:7px;vertical-align:1px}
.fx.live .fx-run::before{background:var(--green);animation:imapPulse 1.2s infinite}
.fx-prog{flex:1;height:3px;background:var(--line);border-radius:2px;overflow:hidden}.fx-prog i{display:block;height:100%;width:0;background:linear-gradient(90deg,#33CCE0,#6A3BE4);transition:width .7s ease}
.fx-replay{background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:5px 10px;font:500 12px 'IBM Plex Mono',monospace;color:var(--ink2);cursor:pointer}.fx-replay:hover{border-color:var(--accent);color:var(--accent)}
.fx-row{grid-template-columns:1fr 64px 1.25fr 64px 1fr;transform:perspective(1400px) rotateX(calc(var(--tilt,0)*4deg));transition:transform .2s linear}
.fx-node{transition:transform .35s cubic-bezier(.2,.8,.2,1),box-shadow .35s,border-color .35s;cursor:default;outline:none}
.fx-node:hover,.fx-node:focus-visible,.fx-node.insp{transform:translateY(-4px);box-shadow:0 18px 36px -20px rgba(20,24,51,.35);border-color:#B9A9EE}
.fx-node.act{border-color:var(--accent);box-shadow:0 0 0 4px rgba(106,59,228,.10),0 18px 36px -20px rgba(106,59,228,.45)}
.fx-node.done .itag{background:#E5F4EC;color:var(--green)}
.fx-foot{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-top:2px}
.fx-ms{font:500 11px 'IBM Plex Mono',monospace;color:#9A9DB2}
.fx-doc{position:relative;height:54px;border:1px solid var(--line);border-radius:6px;background:var(--bg);padding:8px 10px;display:grid;gap:5px;overflow:hidden}
.fx-doc i{display:block;height:4px;border-radius:2px;background:#DDD8EC}.fx-doc i:nth-child(1){width:45%;background:#C9BEF0}.fx-doc i:nth-child(3){width:70%}.fx-doc i:nth-child(5){width:35%;justify-self:end;background:#C9BEF0}
.fx-scan{position:absolute;left:0;right:0;top:-30%;height:30%;background:linear-gradient(180deg,transparent,rgba(51,204,224,.35),transparent);opacity:0}
.fx-node.act .fx-scan{opacity:1;animation:fxScan 1.1s linear infinite}
@keyframes fxScan{to{top:100%}}
.fx-wire{position:relative;display:flex;align-items:center;color:#CFC6EE}
.fx-wire svg{width:100%;height:12px;fill:none;stroke:currentColor;stroke-width:1.6}
.fx-pkt{position:absolute;left:0;top:50%;transform:translate(-50%,-50%) scale(.6);font:600 9.5px 'IBM Plex Mono',monospace;color:#fff;background:var(--accent);border-radius:999px;padding:3px 8px;opacity:0}
.fx-wire.go{color:var(--accent)}.fx-wire.go .fx-pkt{animation:fxPkt .8s cubic-bezier(.5,0,.3,1) forwards}
@keyframes fxPkt{0%{left:0;opacity:0;transform:translate(-50%,-50%) scale(.6)}20%{opacity:1;transform:translate(-50%,-50%) scale(1)}80%{opacity:1}100%{left:100%;opacity:0;transform:translate(-50%,-50%) scale(.6)}}
.fx-checks span{position:relative;transition:color .3s;color:#9A9DB2;cursor:help}
.fx-checks span::before{content:'';display:inline-block;width:12px;height:12px;border:2px solid #CFC6EE;border-top-color:var(--accent);border-radius:50%;margin-right:9px;vertical-align:-2px;animation:fxSpin .8s linear infinite}
.fx-checks span.ok{color:var(--ink2)}.fx-checks span.ok::before{content:'✓';border:0;animation:none;width:auto;height:auto;color:var(--green);font-weight:700;vertical-align:0}
.fx-checks span:hover{color:var(--accent)}
@keyframes fxSpin{to{transform:rotate(360deg)}}
.fx:not(.live) .fx-checks span::before{animation:none;border-top-color:#CFC6EE}
.fx-tip{font-size:.8rem;color:var(--muted);background:var(--bg);border:1px dashed var(--line);border-radius:6px;padding:7px 10px;min-height:2.6em}
.fx-api{font:500 11.5px 'IBM Plex Mono',monospace;color:var(--muted);background:var(--bg);border:1px solid var(--line);border-radius:6px;padding:6px 9px;opacity:.35;transition:opacity .4s}
.fx-api em{font-style:normal;color:var(--green)}.fx-node.done .fx-api{opacity:1}
.fx-insp{margin-top:18px;border:1px solid #2A2F55;border-radius:10px;background:#141833;overflow:hidden}
.fx-insp-h{display:flex;justify-content:space-between;padding:9px 14px;border-bottom:1px solid #2A2F55}.fx-insp-h .mono{color:#8FE3EE}.fx-insp-h .fx-hint{color:#6E7396}
.fx-insp pre{margin:0;padding:14px 16px;font:500 12.5px/1.6 'IBM Plex Mono',monospace;color:#D5D8EA;white-space:pre-wrap;overflow-wrap:anywhere;min-height:13em}
@media(max-width:960px){.fx-row{grid-template-columns:1fr;transform:none}.fx-wire{height:40px;width:12px;margin:0 auto}.fx-wire svg{transform:rotate(90deg);width:40px}.fx-pkt{display:none}.fx-hint{display:none}}
@media(prefers-reduced-motion:reduce){.fx-row{transform:none!important}.fx-scan,.fx-pkt{display:none}.fx-checks span::before{animation:none}}
'''
s=s.replace('</style>',CSS+'</style>',1)
open(p,'w',encoding='utf-8').write(s);print('ok')
