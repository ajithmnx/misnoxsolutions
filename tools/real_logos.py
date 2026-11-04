"""Nov 2026: one global logo sprite (Iconify logos / Simple Icons, open-source) used by the integration map,
platform badges (Services, ERP pages) and home 'By system' tiles. Run once, then build_pages."""
import json,re
SI='/tmp/claude-0/-home-claude/affd0311-3ba6-5c2a-b5bc-b87b6c18853a/scratchpad/si/'
p='index.html'; s=open(p,encoding='utf-8').read()
d=json.load(open(SI+'ic/package/icons.json'));I=d['icons'];DW=d.get('width',256);DH=d.get('height',256)
def ic(key,sid):
    x=I[key];w=x.get('width',DW);h=x.get('height',DH);b=x['body']
    for m in set(re.findall(r'id="([^"]+)"',b)):
        b=b.replace(f'id="{m}"',f'id="{sid}-{m}"').replace(f'url(#{m})',f'url(#{sid}-{m})').replace(f'href="#{m}"',f'href="#{sid}-{m}"')
    return f'<symbol id="{sid}" viewBox="0 0 {w} {h}">{b}</symbol>'
def si(f,sid,c):
    path=re.search(r'<path d="([^"]+)"',open(SI+'package/icons/'+f).read()).group(1)
    return f'<symbol id="{sid}" viewBox="0 0 24 24"><path fill="{c}" d="{path}"/></symbol>'
# take existing imap defs (sf, shop, hs, ms, sap, xero, pbi, bank) out of the IMAP string
m=None  # see fixed version below
imap_defs=m.group(2)
s=s[:m.start()]+m.group(1)+s[m.end():]
extra=ic('oracle','lg-oracle')+si('myob.svg','lg-myob','#6100A5')+si('quickbooks.svg','lg-qb','#2CA01C')
sprite=f'<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false" id="logo-sprite"><defs>{imap_defs}{extra}</defs></svg>\n'
s=s.replace('<body>\n','<body>\n'+sprite,1)

# platform badges -> real logos
def badge(sid,title,w=22,h=22): return f'`<span class="pf-badge pf-logo" aria-hidden="true" title="{title}"><svg width="{w}" height="{h}"><use href="#{sid}"/></svg></span>`'
rep={'ms':badge('lg-ms','Microsoft',18,18),'sap':badge('lg-sap','SAP',26,14),'myob':badge('lg-myob','MYOB'),'xero':badge('lg-xero','Xero',24,24),
     'acu':badge('lg-myob','MYOB Acumatica'),'sf':badge('lg-sf','Salesforce',26,18),'pbi':badge('lg-pbi','Power BI',18,22),'qb':badge('lg-qb','QuickBooks')}
for k,v in rep.items():
    s,n=re.subn(r'(\n  '+k+r':)`.*?`,',lambda mm:mm.group(1)+v+',',s,count=1)
    assert n==1,k

# By-system tiles: logo row
s=s.replace("sys:[['Dynamics 365 and Business Central','Purchase invoices, vendors and journals from AP tools, bank feeds and CRM.','BC ⇄ Salesforce · AP inbox → BC · bank feed → BC'],",
 "sys:[['Dynamics 365 and Business Central','Purchase invoices, vendors and journals from AP tools, bank feeds and CRM.','BC ⇄ Salesforce · AP inbox → BC · bank feed → BC',['lg-ms','lg-sf']],",1)
for old,lg in [("'Shopify → NetSuite · NetSuite ⇄ HubSpot · payroll → GL']","['lg-oracle','lg-shop','lg-hs']"),
               ("'B1 ⇄ CRM · supplier portal → SAP · SAP → Power BI']","['lg-sap','lg-pbi']"),
               ("'T1 ⇄ procurement · T1 → reporting · HR → T1']","[]"),
               ("'Xero ⇄ CRM · MYOB → ERP migration · bills → approvals']","['lg-xero','lg-myob']"),
               ("'Oracle ⇄ procurement · Oracle → data warehouse']","['lg-oracle']")]:
    assert old in s,old
    s=s.replace(old,old[:-1]+","+lg+"]",1)
old="function homeTiles(k){return HOME_TILES[k].map(([t,d,f])=>`<div class=\"tile\"><h3>${t}</h3>"
assert old in s
s=s.replace(old,"function homeTiles(k){return HOME_TILES[k].map(([t,d,f,lg])=>`<div class=\"tile\">${lg&&lg.length?`<div class=\"tile-logos\" aria-hidden=\"true\">${lg.map(id=>`<svg class=\"${id}\"><use href=\"#${id}\"/></svg>`).join('')}</div>`:''}<h3>${t}</h3>",1)

# invoice flow: Business Central logo
s=s.replace('<span class="mono">3 · POSTED</span><h3>Business Central</h3>','<span class="mono">3 · POSTED</span><h3><svg width="16" height="16" aria-hidden="true"><use href="#lg-ms"/></svg>Business Central</h3>')

CSS='''
/* ── Real logos in badges and tiles (Nov 2026) ── */
.pf-badge.pf-logo{background:#fff;border:1px solid var(--line)}
.pf-badge.pf-logo svg{display:block}
.tile-logos{display:flex;align-items:center;gap:12px;height:28px;margin-bottom:4px}
.tile-logos svg{height:24px;width:24px}
.tile-logos svg.lg-oracle{width:76px;height:12px}
.tile-logos svg.lg-sap{width:44px;height:22px}
.tile-logos svg.lg-sf{width:34px}
'''
s=s.replace('</style>',CSS+'</style>',1)
open(p,'w',encoding='utf-8').write(s); print('ok')
# NOTE: the defs extraction above was buggy (non-greedy match stopped at SAP's inner </defs>);
# fixed in place on 2026-11-04 by rebuilding the sprite from tools/imap.html (outer defs end before <path id="pl0">).
