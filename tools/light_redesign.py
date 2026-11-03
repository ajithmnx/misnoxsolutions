"""Nov 2026 light redesign: convert dark-theme colours to light tokens and append the light style layer.
Run once from repo root, then python3 tools/build_pages.py."""
import re
p='index.html'; s=open(p,encoding='utf-8').read()

# 1. tokens
s=s.replace("--bg:#121828;--bg2:#171e31;--bg3:#1d2539;","--bg:#FBFAFD;--bg2:#F3F0FB;--bg3:#FFFFFF;--surface:#FFFFFF;--ink:#141833;--ink2:#2E3352;--line:#E5E2EE;",1)
s=s.replace("--accent:#9B7BFF;--accent2:#33CCE0;--teal:#7A4CF0;","--accent:#6A3BE4;--accent2:#0B7F96;--teal:#6A3BE4;",1)
s=s.replace("--green:#34d399;--navy:#111a2e;--navy2:#16213a;","--green:#17784C;--navy:#141833;--navy2:#22274A;",1)
s=s.replace("--muted:#9aa7bf;","--muted:#585D77;",1)
s=s.replace('<meta name="theme-color" content="#121828"/>','<meta name="theme-color" content="#FBFAFD"/>')
s=s.replace('family=Sora:wght@600;700;800&amp;display=swap"','family=Sora:wght@600;700;800&amp;family=IBM+Plex+Sans:wght@400;500;600&amp;family=IBM+Plex+Mono:wght@500&amp;display=swap"')

# 2. white literals -> light tokens (CSS + inline markup)
W=r'rgba\(255,\s*255,\s*255,\s*([0-9.]+)\)'
s=re.sub(r'(?<![-\w])color:\s*'+W, lambda m:'color:'+('var(--ink2)' if float(m.group(1))>=0.75 else 'var(--muted)'), s)
s=re.sub(r'(border[\w-]*:[^;"}]*?)'+W, lambda m:m.group(1)+'var(--line)', s)
s=re.sub(r'(background[\w-]*:[^;"}]*?)'+W, lambda m:m.group(1)+'var(--surface)', s)
s=re.sub(W, 'rgba(20,24,51,0.08)', s)
s=s.replace('#f0f6ff','var(--ink)').replace('#c8d8e8','var(--ink2)')
s=re.sub(r'(?<![-\w])color:#fff(?=[;"}])','color:var(--ink)',s)

# 3. light style layer (later rules win)
LAYER=r'''
/* ── Light redesign (Nov 2026): calm light base, navy ink, logo violet for the main action only ── */
body{font-family:'IBM Plex Sans',-apple-system,'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--ink)}
.reveal,.hero-left>*,.flow-stack{opacity:1!important;transform:none!important;animation:none!important;transition:none!important}
.hero-glow,.hero-glow-2,.page-hero::before,.cta-band::before,.section-light::before{display:none!important}
.eyebrow{color:var(--accent2);font-family:'IBM Plex Mono',ui-monospace,monospace;font-weight:500;letter-spacing:.04em;text-transform:none;font-size:.8rem}
.btn{border-radius:8px}
.btn-lg{border-radius:8px;padding:14px 26px}
.btn-primary,.btn-primary:hover{background:var(--accent);color:#fff;box-shadow:none;transform:none}
.btn-primary:hover{background:#4E25C2}
.btn-ghost,.btn-outline{background:transparent;color:var(--ink);border:1px solid var(--line)}
.btn-ghost:hover,.btn-outline:hover{background:transparent;border-color:var(--ink)}
:focus-visible{outline-color:var(--accent)}
#main-nav{background:rgba(251,250,253,.94);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
#main-nav.scrolled{background:rgba(251,250,253,.97);box-shadow:none}
.wordmark{color:var(--ink)}.wordmark-sub{color:var(--muted)}
.nav-link{color:var(--ink2)}.nav-link:hover,.nav-link.active{color:var(--ink);background:var(--bg2)}
.dropdown{background:var(--surface);border:1px solid var(--line);box-shadow:0 12px 32px -12px rgba(20,24,51,.25)}
.dropdown a{color:var(--ink2)}.dropdown a:hover{background:var(--bg2);color:var(--ink)}
.mobile-toggle{color:var(--ink)}
.mobile-menu{background:var(--surface);border-top:1px solid var(--line)}
.mobile-menu a{color:var(--ink2);border-bottom-color:var(--line)}
h2.st{color:var(--ink)}.sd{color:var(--muted)}
.sh.c::before{display:none}
.section-alt{background:var(--bg2)}
.section-light{background:var(--bg2);border:0}
.section-light .why-card{background:var(--surface);border:1px solid var(--line)}
.section-light .sd,.section-light .why-card p{color:var(--muted)}
.bcard,.why-card,.card,.num-card,.outcome-card,.glass-card{background:var(--surface);border:1px solid var(--line);border-radius:10px}
.bcard:hover,.why-card:hover,.card:hover,.num-card:hover,.outcome-card:hover,.glass-card:hover{transform:none;background:var(--surface);border-color:#CFC8E6;box-shadow:none}
.glass-card h3{color:var(--ink)}.glass-card p{color:var(--muted)}
.bcard-icon,.card-icon{background:var(--bg2);border:0;color:var(--accent)}
.chip,.platform-tag{background:var(--surface);border:1px solid var(--line);color:var(--ink2)}
.chip::before{background:var(--accent2)}
.ps-num{color:var(--accent);font-weight:500;font-family:'IBM Plex Mono',monospace}
.step-num{background:var(--surface);border:1px solid var(--line);color:var(--ink)}
.page-hero{background:var(--bg2);border-bottom:1px solid var(--line);padding:132px 0 64px}
.page-hero .eyebrow{color:var(--accent2)}
.page-hero h1{color:var(--ink)}.page-hero p{color:var(--muted)}
.section-dark{background:var(--bg2);color:var(--ink)}
.cta-band{background:var(--navy);border:0}
.cta-inner h2{color:#fff}.cta-inner p{color:#BFC3DA}
.cta-band .btn-ghost,.cta-band .btn-outline{color:#fff;border-color:#3B4066}
.cta-band .btn-ghost:hover,.cta-band .btn-outline:hover{border-color:#fff}
.contact-info-card{background:var(--surface);border:1px solid var(--line)}
.contact-info-card h3{color:var(--ink)}
.contact-item-icon{background:var(--bg2)}
.expect-item::before{color:var(--green)}
label{color:var(--ink2)}
input,select,textarea{color:var(--ink);background:var(--surface);border:1px solid #D6D2E2}
input:hover,select:hover,textarea:hover{background:var(--surface);border-color:#B9B3CF}
input:focus,select:focus,textarea:focus{background:var(--surface);box-shadow:0 0 0 3px rgba(106,59,228,.14)}
input::placeholder,textarea::placeholder{color:#9A9DB2}
select option{background:#fff;color:var(--ink)}
footer{background:var(--surface);color:var(--muted);border-top:1px solid var(--line)}
.footer-col h4{color:var(--ink)}.footer-col a,.footer-bottom-links a{color:var(--muted)}
.footer-col a:hover,.footer-bottom-links a:hover{color:var(--accent)}
.pf-badge{background:var(--surface);border:1px solid var(--line)}
.hub-node{background:var(--surface);border:1px solid var(--line);color:var(--ink)}
.hub-wire{background:#CFC8E6}.hub-wire::after{display:none}
.hub-core{background:var(--surface);border:1.5px solid var(--accent);box-shadow:none}
.hub-core strong{color:var(--ink)}.hub-core small{color:var(--muted)}
.plist-num{display:none}
.plist-item{border-top-color:var(--line)}
details{background:var(--surface)!important;border-color:var(--line)!important}
/* home: hero, health check, flow, explorer */
.hero{min-height:0;background:var(--bg);padding-top:74px;display:block}
.hero-split{padding:72px 0 64px;gap:56px}
.hero h1{color:var(--ink);font-weight:700}
.hero h1 em{font-style:normal;color:var(--accent)}
.hero-sub{color:var(--muted);font-size:1.1rem}
.hp-item{color:var(--muted)}
.hp-item::before{content:'✓';background:none;border:0;color:var(--green);font-weight:700;width:auto;height:auto}
.hc{background:var(--surface);border:1px solid var(--line);border-radius:12px;box-shadow:0 18px 40px -24px rgba(20,24,51,.25);overflow:hidden}
.hc-head{display:flex;justify-content:space-between;align-items:center;padding:18px 22px;border-bottom:1px solid var(--line)}
.hc-head b{font:600 15px 'Sora',sans-serif;color:var(--ink)}
.mono{font:500 12px/1.4 'IBM Plex Mono',ui-monospace,monospace;color:var(--muted);letter-spacing:.02em}
.hc-steps{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;padding:14px 22px 0}
.hc-steps i{height:3px;border-radius:2px;background:var(--line)}.hc-steps i.on{background:var(--accent)}
.hc-body{padding:20px 22px 22px;display:grid;gap:14px}
.hc-body h3{font-size:1.12rem;line-height:1.35;color:var(--ink)}
.hc-why{color:var(--muted);font-size:.9rem}
.hc-opts{display:grid;gap:8px}
.hc-opt{display:flex;align-items:center;gap:12px;width:100%;text-align:left;font:500 .95rem 'IBM Plex Sans',sans-serif;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:12px 14px;cursor:pointer}
.hc-opt:hover{border-color:var(--accent);background:var(--bg2)}
.hc-opt::before{content:'';width:14px;height:14px;border-radius:50%;border:1.5px solid #B9B4CC;flex:none}
.hc-next{border-top:1px solid var(--line);padding:14px 22px 18px;display:grid;gap:6px;background:var(--bg)}
.hc-next p{font-size:.85rem;color:var(--muted)}.hc-next span{font-family:'IBM Plex Mono',monospace;color:var(--accent);margin-right:8px}
.hc-meter{display:flex;gap:4px}.hc-meter i{flex:1;height:8px;border-radius:2px;background:var(--line)}.hc-meter i.on{background:#A8551B}
.hc-body ul{padding-left:18px;display:grid;gap:6px;color:var(--muted);font-size:.9rem}
.hc-row{display:flex;gap:14px;flex-wrap:wrap;align-items:center;margin-top:4px}
.hc-link{background:none;border:0;color:var(--accent);font:500 .9rem 'IBM Plex Sans',sans-serif;cursor:pointer;padding:0}
.sys-strip{border-top:1px solid var(--line);border-bottom:1px solid var(--line);background:var(--surface)}
.sys-strip .container{display:flex;flex-wrap:wrap;align-items:center;gap:10px 30px;padding-top:22px;padding-bottom:22px}
.sys-strip b{font:600 15px 'Sora',sans-serif;color:var(--ink2)}
.iflow{display:grid;grid-template-columns:1fr 44px 1.25fr 44px 1fr;align-items:stretch}
.inode{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:20px;display:grid;gap:10px;align-content:start;min-width:0}
.inode.core{border:1.5px solid var(--accent)}
.inode h3{font-size:1rem;color:var(--ink);display:flex;align-items:center;gap:7px}
.kv{display:grid;grid-template-columns:auto 1fr;gap:4px 12px;font:500 12.5px/1.5 'IBM Plex Mono',monospace;color:var(--muted)}
.kv b{color:var(--ink);font-weight:500;overflow-wrap:anywhere}
.ichecks{display:grid;gap:7px;font-size:.9rem;color:var(--ink2)}
.ichecks span::before{content:'✓';color:var(--green);font-weight:700;margin-right:9px}
.iarrow{display:flex;align-items:center;justify-content:center;color:var(--accent)}
.itag{justify-self:start;font:500 11.5px 'IBM Plex Mono',monospace;padding:3px 8px;border-radius:4px;background:var(--bg2);color:var(--accent)}
.itag.ok{background:#E5F4EC;color:var(--green)}
.inote{margin-top:14px;font-size:.82rem;color:var(--muted)}
.tabs{display:flex;flex-wrap:wrap;border-bottom:1px solid var(--line);margin-bottom:28px}
.tabs button{background:none;border:0;border-bottom:2px solid transparent;margin:0 22px -1px 0;padding:10px 2px;font:600 .95rem 'IBM Plex Sans',sans-serif;color:var(--muted);cursor:pointer}
.tabs button[aria-selected="true"]{color:var(--ink);border-bottom-color:var(--accent)}
.tgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.tile{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:22px;display:grid;gap:10px;align-content:start}
.tile h3{font-size:1.02rem;color:var(--ink)}.tile p{color:var(--muted);font-size:.9rem}
.tile .fl{font:500 12.5px/1.7 'IBM Plex Mono',monospace;color:var(--accent2)}
.phases{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:24px}
.phase{border-top:2px solid var(--ink);padding-top:18px;display:grid;gap:8px;align-content:start}
.phase .n{font:500 13px 'IBM Plex Mono',monospace;color:var(--accent)}
.phase h3{font-size:1.05rem;color:var(--ink)}.phase p{color:var(--muted);font-size:.9rem}
.qrow-item .card-icon{display:none}
.sh.l{text-align:left;align-items:flex-start;max-width:44rem}
@media(max-width:960px){.iflow{grid-template-columns:1fr}.iarrow{height:36px;transform:rotate(90deg)}.tgrid,.phases{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:600px){.tgrid,.phases{grid-template-columns:1fr}}
'''
s=s.replace('</style>',LAYER+'</style>',1)
open(p,'w',encoding='utf-8').write(s)
print('ok')

# 4. tone down violet-tinted panels (inline styles)
s=open(p,encoding='utf-8').read()
s=re.sub(r'(background:)\s*rgba\(122,\s*76,\s*240,\s*0?\.(0\d|1\d?)\d*\)',r'\1var(--surface)',s)
s=re.sub(r'(border(?:-color)?:[^;"]*?)rgba\(122,\s*76,\s*240,\s*0?\.[0-3]\d*\)',r'\1var(--line)',s)
open(p,'w',encoding='utf-8').write(s)
