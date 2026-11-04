"""Nov 2026: one type scale. Body sizes snap to 12/14/16/18/20px; card/section/page headings use fixed tokens.
Technical graphics (mono), logo wordmark and badge letters are left as designed."""
import re
p='index.html'; s=open(p,encoding='utf-8').read()
STEPS=[(14.6,'var(--fs-sm)'),(17.0,'var(--fs-base)'),(19.0,'var(--fs-lg)'),(21.0,'var(--fs-xl)')]
def snap(v,unit):
    px=float(v)*(16 if unit=='rem' or unit=='em' else 1)
    if px<9 or px>21: return None
    if px<13: return 'var(--fs-xs)'
    for lim,tok in STEPS:
        if px<lim: return tok
EXCL=re.compile(r'imap|\.kv|mflow|ptl-chip|fx-|\.mono|wordmark|pf-badge-txt|hc-meter|\.fl\b|fx-ms|ls-track|hc-next span|\.n\b|ptl|code|pre|\.itag|\bh1\b|\bh2\b|\.st\b|\.hero h1')
def fix_decls(sel,body):
    if EXCL.search(sel): return body
    return re.sub(r'font-size:\s*([0-9.]+)(rem|px|em)(?=[;}\s!]|$)',lambda m:('font-size:'+snap(m.group(1),m.group(2))) if snap(m.group(1),m.group(2)) else m.group(0),body)
a=s.index('<style>');b=s.index('</style>',a)
css=s[a:b]
css=re.sub(r'([^{}]+)\{([^{}]*)\}',lambda m:m.group(1)+'{'+fix_decls(m.group(1),m.group(2))+'}',css)
s=s[:a]+css+s[b:]
# inline styles in templates
i=s.index('<script>',b)
tail=re.sub(r'style="([^"]*)"',lambda m:'style="'+re.sub(r'font-size:\s*([0-9.]+)(rem|px|em)',lambda k:('font-size:'+snap(k.group(1),k.group(2))) if snap(k.group(1),k.group(2)) else k.group(0),m.group(1))+'"',s[i:])
s=s[:i]+tail
TOK=''':root{--fs-xs:.75rem;--fs-sm:.875rem;--fs-base:1rem;--fs-lg:1.125rem;--fs-xl:1.25rem;--fs-h3:1.125rem;--fs-h2:clamp(1.75rem,3vw,2.375rem);--fs-h1:clamp(2rem,4vw,3rem);--fs-hero:clamp(2.5rem,4.6vw,3.75rem)}
'''
LAYER='''
/* ── Type scale (Nov 2026): 12 / 14 / 16 / 18 / 20 body, fixed heading tokens ── */
body{font-size:var(--fs-base)}
p{font-size:inherit}
.sd,.hero-sub,.page-hero p,.photo-band p{font-size:var(--fs-lg)}
.card p,.bcard p,.tile p,.why-card p,.num-card p,.outcome-card p,.glass-card p,.plist-item p,.phase p,.qrow-item p,.step-body p,.hc-why,.contact-item-text a,.feature-list li{font-size:var(--fs-base)}
.nav-link,.dropdown a,.footer-col a,.footer-bottom,.form-note,.chip,.platform-tag,.inote,.hc-next p,.hp-item,.fx-tip,.expect-item{font-size:var(--fs-sm)}
.eyebrow,.hc-split>div>.mono,.ls-label,.photo-band .mono,.footer-col h4,label{font-size:var(--fs-xs)}
.btn{font-size:var(--fs-base)}.btn-lg{font-size:var(--fs-base)}.nav .btn,.nav-cta .btn{font-size:var(--fs-sm)}
.hc-opt,input,select,textarea{font-size:var(--fs-base)}
h3,.card h3,.bcard h3,.tile h3,.why-card h3,.num-card h3,.outcome-card h3,.glass-card h3,.plist-item h3,.phase h3,.qrow-item h3,.step-body h3,.inode h3,.hc-body h3,.contact-info-card h3,.ck-item strong{font-size:var(--fs-h3);line-height:1.35}
h2.st,.photo-band h2,.cta-inner h2{font-size:var(--fs-h2)}
.page-hero h1{font-size:var(--fs-h1)}
.hero h1{font-size:var(--fs-hero)}
.hc-head b{font-size:var(--fs-base)}
@media(max-width:768px){.hero h1{font-size:2.25rem}h2.st{font-size:1.75rem}}
'''
s=s.replace('<style>','<style>\n'+TOK,1)
s=s.replace('</style>',LAYER+'</style>',1)
open(p,'w',encoding='utf-8').write(s);print('ok')
