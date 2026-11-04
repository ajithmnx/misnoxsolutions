"""Nov 2026 home v4 (learned from Shinetech): stat bar under hero, 'What we do' accordion on photo,
'Why choose us' numbered split, trust stat cards, consistent section labels, wider 1360px container, larger footer."""
import re
p='index.html'; s=open(p,encoding='utf-8').read()
sc=s.index('<script>',s.index('</style>')); head,tail=s[:sc],s[sc:]
def U(id_,w=1800): return f'https://images.unsplash.com/{id_}?w={w}&q=65&auto=format&fit=crop'
def rep(t,a,b):
    assert t.count(a)>=1,a[:70]; return t.replace(a,b,1)
reg=tail.index("register('home'")
H,T=tail[:reg],tail[reg:]
# 1 stat bar after hero
T=rep(T,'''  <span class="hero-mark hm1" aria-hidden="true"></span><span class="hero-mark hm2" aria-hidden="true"></span>
</section>''','''  <span class="hero-mark hm1" aria-hidden="true"></span><span class="hero-mark hm2" aria-hidden="true"></span>
</section>
<div class="statbar"><div class="container statbar-in">${[['15+','platforms we connect'],['6','major ERP families covered'],['4','clear steps, every project'],['1','accountable team, start to finish']].map(([n,t])=>`<div class="stat"><b>${n}</b><span>${t}</span></div>`).join('')}</div></div>''')
# 2 What we do accordion after health check section (before invoice section)
T=rep(T,'''<section class="section">
  <div class="container">
    <div class="sh l"><h2 class="st">One Supplier Invoice, Start to Finish</h2>''','''<section class="wwd">
  <div class="container wwd-in">
    <div class="wwd-head"><p class="eyebrow">What we do</p><h2 class="st">Built around the systems you already run</h2><p class="sd">From a single connection to a full ERP programme, every engagement is shaped to your environment.</p></div>
    <div class="acc" id="acc">${SERVICES.map(([t,icon,d,page],i)=>`<div class="acc-item${i===0?' open':''}"><button class="acc-btn" type="button" aria-expanded="${i===0}"><span class="acc-ic">${ic(icon,18)}</span><span class="acc-t">${t}</span><span class="acc-pm" aria-hidden="true"></span></button><div class="acc-body"><p>${d}</p><a class="card-link" href="/${page||'services'}/">${page?'Learn more':'See all services'} <span class="arrow">→</span></a></div></div>`).join('')}</div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="sh l"><p class="eyebrow">See it in action</p><h2 class="st">One Supplier Invoice, Start to Finish</h2>''')
# 3 labels on other sections
T=rep(T,'<div class="sh l"><h2 class="st">Find Your Starting Point</h2>','<div class="sh l"><p class="eyebrow">Explore</p><h2 class="st">Find Your Starting Point</h2>')
T=rep(T,'<div class="sh l"><h2 class="st">Sound Familiar?</h2>','<div class="sh l"><p class="eyebrow">Common starting points</p><h2 class="st">Sound Familiar?</h2>')
T=rep(T,'<div class="sh l"><h2 class="st">How We Work</h2>','<div class="sh l"><p class="eyebrow">The process</p><h2 class="st">How We Work</h2>')
# 4 replace photo band with Why choose us split
a=T.index('<section class="photo-band">'); b=T.index('</section>',a)+len('</section>')
WHY='''<section class="why">
  <div class="why-photo" role="img" aria-label="Warehouse aisles with stocked shelves"></div>
  <div class="why-body"><p class="eyebrow">Why organisations choose us</p><h2 class="st">Built to keep working long after go-live</h2>
    <ol class="why-list">${[['No lock-in','Built on each platform\\'s own APIs and standard tools, with nothing proprietary of ours in the middle.'],['Controls built in','Approval limits, segregation of duties and audit trails are part of the design, not added later.'],['You own it','Code, configuration and documentation are handed over in full. Another team could run it tomorrow.'],['One accountable team','The people who design your solution stay with it through build, go-live and support.']].map(([t,d],i)=>`<li><span class="why-n">0${i+1}</span><div><h3>${t}</h3><p>${d}</p></div></li>`).join('')}</ol>
  </div>
</section>'''
T=T[:a]+WHY+T[b:]
# 5 replace "What You Can Count On" with trust section
a=T.index('<section class="section">\n  <div class="container">\n    <div class="sh l"><h2 class="st">What You Can Count On</h2>')
b=T.index('</section>',a)+len('</section>')
TRUST='''<section class="section">
  <div class="container">
    <div class="trust">
      <div class="trust-main"><p class="eyebrow">Security &amp; trust</p><h2 class="st">Your data, protected from day one</h2><p class="sd">We work inside your environment, under your security controls. Access is named, limited and removed when the work is done.</p><a class="card-link" href="/security/">How we handle access and data <span class="arrow">→</span></a></div>
      <div class="trust-stats">${[['0','copies of your financial data kept by us'],['Never','credentials stored outside your environment'],['100%','code and documentation handed over to you'],['Written','quote and design signed off before any build']].map(([n,t])=>`<div class="tstat"><b>${n}</b><span>${t}</span></div>`).join('')}</div>
    </div>
  </div>
</section>'''
T=T[:a]+TRUST+T[b:]
tail=H+T
# accordion JS hook
tail=rep(tail,"if(p==='home'){initHome();initImap();initPhases();initFlow()}","if(p==='home'){initHome();initImap();initPhases();initFlow();initAcc()}")
tail=rep(tail,"const HOME_TILES={","""function initAcc(){const acc=document.getElementById('acc');if(!acc)return;acc.querySelectorAll('.acc-btn').forEach(b=>b.onclick=()=>{const it=b.parentElement,open=it.classList.contains('open');acc.querySelectorAll('.acc-item').forEach(x=>{x.classList.remove('open');x.querySelector('.acc-btn').setAttribute('aria-expanded','false')});if(!open){it.classList.add('open');b.setAttribute('aria-expanded','true')}})}
const HOME_TILES={""")
# footer
fa=head.index('<footer id="site-footer">'); fb=head.index('</footer>',fa)+len('</footer>')
old=head[fa:fb]
brand=old[old.index('<div class="footer-brand">'):old.index('<div class="footer-col">')]
FOOT=f'''<footer id="site-footer">
  <div class="container">
    <div class="footer-grid fg5">
      {brand.strip()}
      <div class="footer-col"><h4>Services</h4><a href="/services/">System Integration</a><a href="/services/">Workflow Automation</a><a href="/services/">Data Migration &amp; Sync</a><a href="/erp/">ERP Integration Projects</a><a href="/services/">Managed Support</a></div>
      <div class="footer-col"><h4>Systems</h4><a href="/erp/">Microsoft Dynamics 365</a><a href="/erp/">Oracle NetSuite</a><a href="/erp/">SAP</a><a href="/erp/">TechnologyOne</a><a href="/erp/">Xero</a><a href="/erp/">MYOB</a></div>
      <div class="footer-col"><h4>Company</h4><a href="/about/">About Us</a><a href="/industries/">Who We Help</a><a href="/delivery/">How We Work</a><a href="/security/">Security &amp; Data</a><a href="/faq/">FAQ</a><a href="/contact/">Contact</a></div>
      <div class="footer-col"><h4>Get in touch</h4><div class="footer-contact-item"><a href="mailto:contact@misnox.com.au">contact@misnox.com.au</a></div><div class="footer-contact-item">Sydney, Australia</div><button class="btn btn-primary footer-book" type="button" data-cta="footer" onclick="bookCall()">Book an Intro Call <span class="arrow">→</span></button></div>
    </div>
    <div class="footer-bottom">
      <span style="color:var(--muted)">© <span id="yr">2026</span> MISNOX Solutions. All rights reserved.</span>
      <div class="footer-bottom-links"><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a><a href="/faq/">FAQ</a></div>
    </div>
  </div>
</footer>'''
head=head[:fa]+FOOT+head[fb:]
head=head.replace('max-width:1280px','max-width:1360px').replace('100vw - 1280px','100vw - 1360px')
CSS=f'''
/* ── Home v4 (Nov 2026) ── */
.eyebrow{{display:flex;align-items:center;gap:10px;margin-bottom:12px}}
.eyebrow::before{{content:'';width:22px;height:2px;background:var(--accent);flex:none}}
.page-hero .eyebrow::before{{background:var(--accent2)}}
.statbar{{background:var(--navy);color:#fff;position:relative;z-index:2;margin-top:-56px}}
.statbar-in{{display:grid;grid-template-columns:repeat(4,1fr);padding-top:26px;padding-bottom:26px}}
.stat{{display:grid;gap:4px;padding:0 24px;border-left:1px solid #2E345C}}.stat:first-child{{border-left:0;padding-left:0}}
.stat b{{font:700 2rem/1 'Sora',sans-serif;color:#fff}}.stat span{{font-size:var(--fs-sm);color:#BFC3DA}}
.hero.hero-photo{{clip-path:none}}
.wwd{{position:relative;color:#fff;background:linear-gradient(90deg,rgba(14,17,38,.94) 0%,rgba(14,17,38,.85) 45%,rgba(14,17,38,.55) 100%),url("{U('photo-1686100511314-7d4a52987f2f')}") center/cover no-repeat}}
.wwd-in{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:56px;align-items:start;padding-top:96px;padding-bottom:96px}}
.wwd .st{{color:#fff}}.wwd .sd{{color:#C9CCE0}}.wwd .eyebrow{{color:#8FE3EE}}.wwd .eyebrow::before{{background:#8FE3EE}}
.acc{{background:rgba(20,24,51,.72);backdrop-filter:blur(6px);border:1px solid #2E345C;border-radius:12px;overflow:hidden}}
.acc-item+.acc-item{{border-top:1px solid #2E345C}}
.acc-btn{{display:flex;align-items:center;gap:14px;width:100%;background:none;border:0;color:#fff;padding:18px 22px;cursor:pointer;text-align:left;font:600 var(--fs-lg) 'Sora',sans-serif}}
.acc-ic{{display:inline-flex;width:34px;height:34px;border-radius:9px;align-items:center;justify-content:center;background:rgba(106,59,228,.25);color:#B9A4FF;flex:none}}
.acc-item.open .acc-ic{{background:var(--accent);color:#fff}}
.acc-t{{flex:1}}
.acc-pm::before{{content:'+';font:400 22px/1 'Sora',sans-serif;color:#8FE3EE}}.acc-item.open .acc-pm::before{{content:'−'}}
.acc-body{{display:grid;grid-template-rows:0fr;transition:grid-template-rows .35s ease;padding:0 22px 0 70px}}
.acc-body>*{{overflow:hidden}}
.acc-item.open .acc-body{{grid-template-rows:1fr;padding-bottom:18px}}
.acc-body{{grid-template-columns:1fr}}
.acc-body p{{color:#C9CCE0;margin:0 0 10px}}.acc-body .card-link{{color:#8FE3EE}}
.acc-item:not(.open) .acc-body .card-link{{display:none}}
.why{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);background:var(--navy);color:#fff}}
.why-photo{{min-height:520px;background:linear-gradient(rgba(106,59,228,.18),rgba(106,59,228,.18)),url("{U('photo-1644079446600-219068676743',1400)}") center/cover no-repeat}}
.why-body{{padding:88px max(24px,calc((100vw - 1360px)/2 + 24px)) 88px 64px}}
.why .st{{color:#fff}}.why .eyebrow{{color:#8FE3EE}}.why .eyebrow::before{{background:#8FE3EE}}
.why-list{{list-style:none;margin-top:28px;display:grid}}
.why-list li{{display:flex;gap:22px;padding:20px 0;border-top:1px solid #2E345C}}
.why-n{{font:300 2.25rem/1 'Sora',sans-serif;color:#6E7396;min-width:52px}}
.why-list h3{{color:#fff;margin-bottom:6px}}.why-list p{{color:#BFC3DA}}
.trust{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);border:1px solid var(--line);border-radius:14px;background:var(--surface);overflow:hidden}}
.trust-main{{padding:44px}}.trust-main .sd{{margin-bottom:18px}}
.trust-stats{{display:grid;grid-template-columns:1fr 1fr;border-left:1px solid var(--line);background:var(--bg)}}
.tstat{{padding:32px 30px;display:grid;gap:8px;align-content:start}}
.tstat:nth-child(odd){{border-right:1px solid var(--line)}}.tstat:nth-child(-n+2){{border-bottom:1px solid var(--line)}}
.tstat b{{font:700 2.25rem/1 'Sora',sans-serif;color:var(--accent)}}.tstat span{{font-size:var(--fs-base);color:var(--ink2)}}
.fg5{{grid-template-columns:1.6fr 1fr 1fr 1fr 1.2fr}}
.footer-book{{margin-top:14px;font-size:var(--fs-sm);padding:11px 18px}}
@media(max-width:1024px){{.fg5{{grid-template-columns:1fr 1fr}}.footer-brand{{grid-column:1/-1}}}}
@media(max-width:960px){{.statbar{{margin-top:0}}.statbar-in{{grid-template-columns:1fr 1fr;gap:18px 0}}.stat:nth-child(3){{border-left:0;padding-left:0}}.wwd-in,.why,.trust{{grid-template-columns:1fr}}.why-photo{{min-height:260px}}.why-body{{padding:56px 20px}}.trust-stats{{border-left:0;border-top:1px solid var(--line)}}.trust-main{{padding:28px}}}}
@media(max-width:560px){{.fg5{{grid-template-columns:1fr}}.tstat{{padding:22px 18px}}.tstat b{{font-size:1.75rem}}.acc-body{{padding-left:22px}}}}
'''
head=head.replace('</style>',CSS+'</style>',1)
open(p,'w',encoding='utf-8').write(head+tail);print('ok')
