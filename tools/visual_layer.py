"""Nov 2026 visual layer: logo-curve motif, soft hero wash, duotone Unsplash photos (Unsplash licence, hotlinked),
mini flow diagrams on Services cards, faint grid on tinted bands. Run once, then tools/build_pages.py."""
import re, urllib.parse
p='index.html'; s=open(p,encoding='utf-8').read()

def curve_svg(op, w=5):
    svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none" stroke-linecap="round">'
         f'<defs><linearGradient id="a" x1="0" y1="0" x2="100" y2="100" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#33CCE0"/><stop offset="1" stop-color="#7A4CF0"/></linearGradient>'
         f'<linearGradient id="b" x1="100" y1="0" x2="0" y2="100" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#33CCE0"/><stop offset="1" stop-color="#7A4CF0"/></linearGradient></defs>'
         f'<g opacity="{op}"><path d="M12 20C52 20 48 80 88 80" stroke="url(#a)" stroke-width="{w}"/><path d="M12 80C52 80 48 20 88 20" stroke="url(#b)" stroke-width="{w}"/></g></svg>')
    return 'url("data:image/svg+xml,'+urllib.parse.quote(svg,safe='/:=" ')+'")'

def photo(id_, w=1600): return f'url("https://images.unsplash.com/{id_}?w={w}&q=60&auto=format&fit=crop&sat=-100")'
# Unsplash licence (free, no attribution required): laptop hBuwVLcYTnA, papers PUd6C90Isp0, server hall s0XabTAKvak, warehouse h3pVxOIpnzk
PH={'about':'photo-1499914485622-a88fac536970','industries':'photo-1631557776808-91908aba7ca0','security':'photo-1580106815433-a5b1d1d53d85','band':'photo-1644079446600-219068676743'}

CURVE_LIGHT=curve_svg(0.17); CURVE_NAVY=curve_svg(0.22)
fade='linear-gradient(90deg,var(--bg2) 0%,var(--bg2) 42%,rgba(243,240,251,.82) 62%,rgba(243,240,251,.35) 100%)'
tint='linear-gradient(rgba(106,59,228,.16),rgba(106,59,228,.16))'
css=f"""
/* ── Visual layer (Nov 2026): logo-curve motif, hero wash, duotone photos, grid texture ── */
.hero{{position:relative;overflow:hidden;background:
  radial-gradient(ellipse 55% 60% at 88% 18%,rgba(51,204,224,.10),transparent 70%),
  radial-gradient(ellipse 50% 55% at 70% 85%,rgba(122,76,240,.08),transparent 70%),var(--bg)}}
.hero::after{{content:'';position:absolute;width:720px;height:720px;right:-260px;top:-140px;background:{CURVE_LIGHT} no-repeat center/contain;pointer-events:none}}
.hero .container{{position:relative;z-index:1}}
.page-hero{{position:relative;overflow:hidden}}
.page-hero::after{{content:'';position:absolute;width:520px;height:520px;right:-140px;top:-90px;background:{CURVE_LIGHT} no-repeat center/contain;pointer-events:none}}
.cta-band{{position:relative;overflow:hidden}}
.cta-band::after{{content:'';position:absolute;width:560px;height:560px;left:-200px;bottom:-260px;background:{CURVE_NAVY} no-repeat center/contain;pointer-events:none}}
.section-alt{{background-color:var(--bg2);background-image:linear-gradient(rgba(106,59,228,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(106,59,228,.045) 1px,transparent 1px);background-size:32px 32px}}
body[data-page=about] .page-hero{{background:{fade},{tint},{photo(PH['about'])} right center/cover no-repeat}}
body[data-page=industries] .page-hero{{background:{fade},{tint},{photo(PH['industries'])} right center/cover no-repeat}}
body[data-page=security] .page-hero{{background:{fade},{tint},{photo(PH['security'])} right center/cover no-repeat}}
body[data-page=about] .page-hero::after,body[data-page=industries] .page-hero::after,body[data-page=security] .page-hero::after{{display:none}}
@media(max-width:768px){{body[data-page=about] .page-hero{{background:linear-gradient(rgba(243,240,251,.86),rgba(243,240,251,.86)),{photo(PH['about'],900)} center/cover no-repeat}}body[data-page=industries] .page-hero{{background:linear-gradient(rgba(243,240,251,.86),rgba(243,240,251,.86)),{photo(PH['industries'],900)} center/cover no-repeat}}body[data-page=security] .page-hero{{background:linear-gradient(rgba(243,240,251,.86),rgba(243,240,251,.86)),{photo(PH['security'],900)} center/cover no-repeat}}}}
.photo-band{{position:relative;background:linear-gradient(90deg,rgba(20,24,51,.94) 0%,rgba(20,24,51,.86) 45%,rgba(20,24,51,.55) 100%),linear-gradient(rgba(106,59,228,.25),rgba(106,59,228,.25)),{photo(PH['band'])} center/cover no-repeat;color:#fff}}
.photo-band .container{{padding-top:96px;padding-bottom:96px}}
.photo-band h2{{font-size:clamp(1.7rem,3vw,2.4rem);color:#fff;max-width:34rem;line-height:1.15}}
.photo-band p{{color:#C9CCE0;max-width:34rem;margin-top:14px;font-size:1.05rem}}
.photo-band .mono{{color:#8FE3EE}}
.mflow{{display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-bottom:18px}}
.mflow span{{font:500 11.5px 'IBM Plex Mono',monospace;padding:5px 9px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--ink2)}}
.mflow span.k{{border-color:var(--accent);color:var(--accent)}}
.mflow i{{font-style:normal;color:var(--accent);font-size:13px}}
@media(prefers-reduced-motion:reduce){{.hero::after{{display:none}}}}
"""
s=s.replace('</style>',css+'</style>',1)

# body data-page for page-specific photos
s=s.replace("initReveal();if(p==='home')initHome();","initReveal();document.body.dataset.page=p;if(p==='home')initHome();",1)

# mini flow diagrams on Services cards
MINI=r"""
const MINI_FLOW={'System Integration':['CRM','⇄','ERP','⇄','Bank'],'Workflow Automation':['Invoice','→','Approve','→','Post'],'Data Migration & Sync':['Old ERP','→','Validate','→','New ERP'],'ERP Integration Projects':['Your systems','→','*Layer','→','ERP'],'Managed Support':['Monitor','→','Alert','→','Fix']};
function miniFlow(t){const f=MINI_FLOW[t];return f?`<div class="mflow" aria-hidden="true">${f.map(x=>x==='→'||x==='⇄'?`<i>${x}</i>`:x[0]==='*'?`<span class="k">${x.slice(1)}</span>`:`<span>${x}</span>`).join('')}</div>`:''}
"""
s=s.replace("function render(p){",MINI+"function render(p){",1)
old='<div class="card reveal"><div class="card-icon">${ic(icon,22)}</div><h3>${title}</h3>'
assert old in s
s=s.replace(old,'<div class="card reveal">${miniFlow(title)}<h3>${title}</h3>',1)

# home photo band, between "Sound Familiar?" and "How We Work"
anchor='<section class="section section-alt">\n  <div class="container">\n    <div class="sh l"><h2 class="st">How We Work</h2>'
assert anchor in s
band='<section class="photo-band"><div class="container"><span class="mono">WHERE THE WORK HAPPENS</span><h2>Built inside your environment, owned by your team</h2><p>Integrations run in your systems, under your security controls, and are documented so they keep working long after handover.</p></div></section>\n'
s=s.replace(anchor,band+anchor,1)
open(p,'w',encoding='utf-8').write(s); print('visual layer ok')
