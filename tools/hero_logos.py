"""Nov 2026: Leverage-style photo hero, health check moved below hero, moving real-logo strip,
warm photos (Sound Familiar split, CTA band Sydney harbour, About boardroom). Run once, then build_pages."""
import re
p='index.html'; s=open(p,encoding='utf-8').read()
SP='/tmp/claude-0/-home-claude/affd0311-3ba6-5c2a-b5bc-b87b6c18853a/scratchpad/'
def U(id_,w=1800,extra=''): return f'https://images.unsplash.com/{id_}?w={w}&q=65&auto=format&fit=crop{extra}'
HERO='photo-1690378820474-b468b8ee64d3'; DESK='photo-1551434678-e076c223a692'; HARBOUR='photo-1512477525059-e0b091e0a9ba'; ROOM='photo-1431540015161-0bf868a2d407'
reg=s.index("register('home',()=>`")

# 1. hero: photo hero, then health-check section, then logo marquee
a=s.index('<section class="hero">',reg); b=s.index('<section class="section">',a)
new=r'''<section class="hero hero-photo">
  <div class="container">
    <div class="hero-copy">
      <h1>Your systems, <em>connected</em>. Your controls, enforced.<span class="sr-only"> — ERP and finance system integration</span></h1>
      <p class="hero-sub">We connect your ERP, finance and procurement systems so data moves on its own and your approval rules are enforced, not just written down.</p>
      <div class="hero-actions">
        <button class="btn btn-primary btn-lg" data-cta="hero-primary" onclick="bookCall()">Book an Intro Call <span class="arrow">→</span></button>
        <button class="btn btn-outline btn-lg" data-cta="hero-secondary" onclick="navigate('services')">See Our Services</button>
      </div>
      <div class="hero-promises">${['You own everything we build','No vendor lock-in'].map(t=>`<span class="hp-item">${t}</span>`).join('')}</div>
    </div>
  </div>
  <span class="hero-mark hm1" aria-hidden="true"></span><span class="hero-mark hm2" aria-hidden="true"></span>
</section>
<div class="logo-strip" aria-label="Systems we connect"><span class="mono ls-label">SYSTEMS WE CONNECT</span><div class="ls-viewport"><ul class="ls-track">${LOGOS}${LOGOS.replaceAll('<li ','<li aria-hidden="true" ')}</ul></div></div>
<section class="section hc-section">
  <div class="container hc-split">
    <div><span class="mono">INTEGRATION HEALTH CHECK</span><h2 class="st">How healthy are your integrations?</h2><p class="sd">Four quick questions about how your systems connect today. You get a short read-out of what we would look at first.</p></div>
    <div class="hc" aria-live="polite">
      <div class="hc-head"><b>Integration Health Check</b><span class="mono" id="hc-count">QUESTION 1 OF 4</span></div>
      <div class="hc-steps" id="hc-steps"><i class="on"></i><i></i><i></i><i></i></div>
      <div id="hc-body"></div>
    </div>
  </div>
</section>
'''
s=s[:a]+new+s[b:]

# 2. Sound Familiar -> split with photo
old='<div class="sh l"><h2 class="st">Sound Familiar?</h2></div>\n    <div class="plist" style="margin:0">'
k=s.index(old,reg)
s=s[:k]+'<div class="sf-split"><div class="sf-photo" role="img" aria-label="Someone working at a desk with two screens"></div><div><div class="sh l"><h2 class="st">Sound Familiar?</h2></div>\n    <div class="plist sf-list" style="margin:0">'+s[k+len(old):]
# close the extra wrappers after plist closes: find end of that plist block
k2=s.index('</div>\n  </div>\n</section>',k)
s=s[:k2]+'</div></div></div>\n  </div>\n</section>'+s[k2+len('</div>\n  </div>\n</section>'):]

# 3. logos const
s=s.replace("const HOME_TILES={",open(SP+'logos.js').read()+"\nconst HOME_TILES={",1)

CSS=f'''
/* ── Photo hero, logo marquee, warm photos (Nov 2026) ── */
.hero.hero-photo{{min-height:0;display:block;padding-top:74px;position:relative;overflow:hidden;color:#fff;
  background:linear-gradient(90deg,rgba(14,17,38,.92) 0%,rgba(14,17,38,.80) 38%,rgba(14,17,38,.35) 70%,rgba(14,17,38,.15) 100%),url("{U(HERO)}") 70% 40%/cover no-repeat;
  clip-path:polygon(0 0,100% 0,100% 100%,0 calc(100% - 56px))}}
.hero.hero-photo::after{{display:none}}
.hero-copy{{max-width:620px;padding:110px 0 150px;position:relative;z-index:1}}
.hero-photo h1{{color:#fff}}
.hero-photo h1 em{{color:#6A3BE4}}
.hero-photo .hero-sub{{color:#D5D8EA;max-width:520px}}
.hero-photo .btn-outline{{color:#fff;border-color:rgba(255,255,255,.55)}}
.hero-photo .btn-outline:hover{{border-color:#fff;background:rgba(255,255,255,.06)}}
.hero-photo .hp-item{{color:#D5D8EA}}.hero-photo .hp-item::before{{color:#7FE0B4}}
.hero-mark{{position:absolute;pointer-events:none;background:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22 fill=%22none%22 stroke-linecap=%22round%22%3E%3Cpath d=%22M12 20C52 20 48 80 88 80%22 stroke=%22%2333CCE0%22 stroke-width=%2210%22/%3E%3Cpath d=%22M12 80C52 80 48 20 88 20%22 stroke=%22%237A4CF0%22 stroke-width=%2210%22/%3E%3C/svg%3E") no-repeat center/contain;opacity:.9}}
.hm1{{width:110px;height:110px;right:9%;top:22%}}
.hm2{{width:64px;height:64px;right:38%;bottom:18%;opacity:.7}}
.logo-strip{{display:flex;align-items:center;gap:28px;padding:26px 0 26px max(24px,calc((100vw - 1160px)/2 + 24px));background:var(--surface);border-bottom:1px solid var(--line);overflow:hidden}}
.ls-label{{flex:none}}
.ls-viewport{{overflow:hidden;flex:1;min-width:0;-webkit-mask-image:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent);mask-image:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent)}}
.ls-track{{display:flex;gap:56px;list-style:none;width:max-content;animation:lsScroll 45s linear infinite}}
.ls-track:hover{{animation-play-state:paused}}
.ls-track li{{display:flex;align-items:center;gap:9px;height:34px;flex:none;font:600 15px 'Sora',sans-serif;color:var(--ink2);white-space:nowrap}}
.ls-track svg{{height:26px;width:auto;display:block}}
@keyframes lsScroll{{to{{transform:translateX(-50%)}}}}
.ls-track li[title*="Oracle"] svg{{height:15px}}.ls-track li[title="Xero"] svg,.ls-track li[title="HubSpot"] svg{{height:30px}}
@media(prefers-reduced-motion:reduce){{.ls-track{{animation:none;flex-wrap:wrap}}}}
.hc-section{{padding-top:72px}}
.hc-split{{display:grid;grid-template-columns:minmax(0,.85fr) minmax(0,1fr);gap:56px;align-items:center}}
.hc-split .st{{margin-top:10px}}
.sf-split{{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:56px;align-items:stretch}}
.sf-photo{{border-radius:12px;min-height:420px;background:linear-gradient(rgba(106,59,228,.08),rgba(106,59,228,.08)),url("{U(DESK,1000)}") center/cover no-repeat}}
.sf-list{{grid-template-columns:1fr!important}}
.cta-band{{background:linear-gradient(rgba(14,17,38,.86),rgba(14,17,38,.90)),url("{U(HARBOUR)}") center 60%/cover no-repeat}}
body[data-page=about] .page-hero{{background:linear-gradient(90deg,var(--bg2) 0%,var(--bg2) 42%,rgba(243,240,251,.80) 62%,rgba(243,240,251,.25) 100%),url("{U(ROOM,1600)}") right center/cover no-repeat}}
@media(max-width:960px){{.hc-split,.sf-split{{grid-template-columns:1fr;gap:32px}}.sf-photo{{min-height:240px}}.hero.hero-photo{{background:linear-gradient(rgba(14,17,38,.82),rgba(14,17,38,.88)),url("{U(HERO,1100)}") center/cover no-repeat}}.hero-mark{{display:none}}.hero-copy{{padding:72px 0 110px}}.logo-strip{{flex-direction:column;align-items:flex-start;gap:12px;padding-left:20px}}.ls-viewport{{width:100%}}}}
@media(max-width:768px){{body[data-page=about] .page-hero{{background:linear-gradient(rgba(243,240,251,.86),rgba(243,240,251,.86)),url("{U(ROOM,900)}") center/cover no-repeat}}}}
'''
s=s.replace('</style>',CSS+'</style>',1)
open(p,'w',encoding='utf-8').write(s); print('ok')
