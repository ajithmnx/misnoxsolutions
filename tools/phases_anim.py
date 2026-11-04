"""Nov 2026: animated 'How We Work' timeline on home (icons, progress line, travelling dot, per-step artefact chips)."""
p='index.html'; s=open(p,encoding='utf-8').read()
old="<div class=\"phases\">${PHASES.map(([n,t,d])=>`<div class=\"phase\"><span class=\"n\">${n}</span><h3>${t}</h3><p>${d}</p></div>`).join('')}</div>"
new=("<div class=\"phases ptl\" id=\"ptl\"><div class=\"ptl-track\" aria-hidden=\"true\"><span class=\"ptl-fill\"></span><span class=\"ptl-dot\"></span></div>"
     "${PHASES.map(([n,t,d],i)=>`<div class=\"phase\" style=\"--i:${i}\"><span class=\"ptl-node\" aria-hidden=\"true\">${PH_ICON[i]}</span><span class=\"n\">${n}</span><h3>${t}</h3><p>${d}</p><span class=\"ptl-chip\" aria-hidden=\"true\">${PH_CHIP[i]}</span></div>`).join('')}</div>")
assert old in s; s=s.replace(old,new,1)
JS=r'''
const PH_ICON=[
 '<svg viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="6"/><path d="m15 15 5 5"/><path d="M8 10.5h5M10.5 8v5" opacity=".5"/></svg>',
 '<svg viewBox="0 0 24 24"><rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/></svg>',
 '<svg viewBox="0 0 24 24"><path d="M8 7 3 12l5 5M16 7l5 5-5 5M13.5 5l-3 14"/></svg>',
 '<svg viewBox="0 0 24 24"><path d="M3 12h4l3-7 4 14 3-7h4"/></svg>'];
const PH_CHIP=['findings report','design spec · signed off ✓','tests passed · rollback ready','monitoring on · alerts → your team'];
function initPhases(){const el=document.getElementById('ptl');if(!el)return;
  if(!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion: reduce)').matches){el.classList.add('run','done');return}
  const o=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){el.classList.add('run');setTimeout(()=>el.classList.add('done'),2600);o.disconnect()}})},{threshold:.35});o.observe(el)}
'''
s=s.replace("const HOME_TILES={",JS+"\nconst HOME_TILES={",1)
s=s.replace("if(p==='home'){initHome();initImap()}","if(p==='home'){initHome();initImap();initPhases()}",1)
CSS='''
/* ── Animated How We Work timeline (Nov 2026) ── */
.ptl{position:relative;padding-top:8px}
.ptl .phase{border-top:0;padding-top:0;position:relative}
.ptl-track{position:absolute;left:22px;right:calc(25% - 2px);top:30px;height:2px;background:#D9D3EE;border-radius:2px;overflow:visible}
.ptl-fill{position:absolute;inset:0;width:0;background:linear-gradient(90deg,#33CCE0,#6A3BE4);border-radius:2px;transition:width 2.4s cubic-bezier(.4,0,.2,1)}
.ptl.run .ptl-fill{width:100%}
.ptl-dot{position:absolute;top:-4px;left:0;width:10px;height:10px;border-radius:50%;background:#33CCE0;box-shadow:0 0 0 4px rgba(51,204,224,.18);opacity:0}
.ptl.done .ptl-dot{opacity:1;animation:ptlDot 6s ease-in-out infinite}
@keyframes ptlDot{0%{left:0;opacity:0}8%{opacity:1}92%{opacity:1}100%{left:calc(100% - 10px);opacity:0}}
.ptl-node{position:relative;z-index:1;display:flex;align-items:center;justify-content:center;width:46px;height:46px;border-radius:12px;background:var(--surface);border:1.5px solid #D9D3EE;color:#9A9DB2;margin-bottom:14px;transition:border-color .4s,color .4s,box-shadow .4s;transition-delay:calc(var(--i)*.6s)}
.ptl-node svg{width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.ptl.run .ptl-node{border-color:var(--accent);color:var(--accent);box-shadow:0 6px 18px -8px rgba(106,59,228,.45)}
.ptl .phase>.n,.ptl .phase>h3,.ptl .phase>p,.ptl-chip{opacity:.35;transform:translateY(6px);transition:opacity .5s,transform .5s;transition-delay:calc(var(--i)*.6s + .15s)}
.ptl.run .phase>.n,.ptl.run .phase>h3,.ptl.run .phase>p,.ptl.run .ptl-chip{opacity:1;transform:none}
.ptl-chip{display:inline-flex;align-self:start;justify-self:start;margin-top:4px;font:500 11.5px 'IBM Plex Mono',monospace;color:var(--accent2);background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:4px 9px}
@media(max-width:960px){.ptl-track{display:none}}
@media(prefers-reduced-motion:reduce){.ptl-fill,.ptl-node,.ptl .phase>*{transition:none}.ptl-dot{display:none}}
'''
s=s.replace('</style>',CSS+'</style>',1)
open(p,'w',encoding='utf-8').write(s);print('ok')
