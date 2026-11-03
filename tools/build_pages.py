"""Generate one static copy of index.html per page so every page has its own URL,
title and description (better for Google), plus sitemap.xml.

index.html is the only file to edit. After editing it, run:  python3 tools/build_pages.py
"""
import re, os, datetime

SITE = 'https://misnox.com.au'
PAGES = {  # route: (title, description)
    'home': ('MISNOX Solutions | ERP & Finance System Integration, Sydney',
             'MISNOX Solutions connects ERP, finance and procurement systems for organisations: integration, workflow automation, data migration and support.'),
    'about': ('About | MISNOX Solutions',
              'A small, specialist integration practice based in Sydney, connecting the systems that run finance and procurement.'),
    'services': ('Integration Services | MISNOX Solutions',
                 'System integration, workflow automation, data migration and sync, ERP integration projects and managed support.'),
    'erp': ('ERP Integration Projects | MISNOX Solutions',
            'Connect a new or existing ERP (Dynamics 365, NetSuite, SAP, TechnologyOne, Xero, MYOB) to the rest of your business.'),
    'industries': ('Who We Help | MISNOX Solutions',
                   'Finance and procurement teams in organisations running across several systems.'),
    'security': ('Security & Data Handling | MISNOX Solutions',
                 'Integrations run inside your environment. How we handle access, credentials and data.'),
    'delivery': ('How We Work | MISNOX Solutions',
                 'Four clear phases: discover, design, build and go live, support.'),
    'faq': ('FAQ | MISNOX Solutions',
            'Answers on ownership, pricing, process, support and data handling.'),
    'privacy': ('Privacy Policy | MISNOX Solutions',
                'How MISNOX Solutions handles personal information under the Australian Privacy Principles.'),
    'contact': ('Contact | MISNOX Solutions',
                'Book a free intro call with MISNOX Solutions, Sydney.'),
}

def url(r): return SITE + ('/' if r == 'home' else f'/{r}/')

def esc(t): return t.replace('&', '&amp;').replace('"', '&quot;')

src = open('index.html', encoding='utf-8').read()

def page_html(r):
    title, desc = PAGES[r]
    h = src
    h = re.sub(r'<title>.*?</title>', f'<title>{esc(title)}</title>', h, count=1, flags=re.S)
    h = re.sub(r'<meta name="description" content="[^"]*"\s*/?>', f'<meta name="description" content="{esc(desc)}"/>', h, count=1)
    h = re.sub(r'<meta property="og:title" content="[^"]*"\s*/?>', f'<meta property="og:title" content="{esc(title)}"/>', h, count=1)
    h = re.sub(r'<meta property="og:url" content="[^"]*"\s*/?>', f'<meta property="og:url" content="{url(r)}"/>', h, count=1)
    h = re.sub(r'<meta name="twitter:title" content="[^"]*"\s*/?>', f'<meta name="twitter:title" content="{esc(title)}"/>', h, count=1)
    h = re.sub(r'<meta property="og:description" content="[^"]*"\s*/?>', f'<meta property="og:description" content="{esc(desc)}"/>', h, count=1)
    h = re.sub(r'<meta name="twitter:description" content="[^"]*"\s*/?>', f'<meta name="twitter:description" content="{esc(desc)}"/>', h, count=1)
    if '<link rel="canonical"' in h:
        h = re.sub(r'<link rel="canonical" href="[^"]*"\s*/?>', f'<link rel="canonical" href="{url(r)}"/>', h, count=1)
    else:
        h = h.replace('</title>', f'</title>\n<link rel="canonical" href="{url(r)}"/>', 1)
    return h

open('index.html', 'w', encoding='utf-8').write(page_html('home'))
src = open('index.html', encoding='utf-8').read()
for r in PAGES:
    if r == 'home': continue
    os.makedirs(r, exist_ok=True)
    open(f'{r}/index.html', 'w', encoding='utf-8').write(page_html(r))

# 404 page: served by Cloudflare for any unknown address (wrangler.jsonc not_found_handling)
h404 = page_html('home').replace('<title>', '<meta name="robots" content="noindex"/>\n<title>', 1)
h404 = re.sub(r'<title>.*?</title>', '<title>Page Not Found | MISNOX Solutions</title>', h404, count=1, flags=re.S)
open('404.html', 'w', encoding='utf-8').write(h404)

today = datetime.date.today().isoformat()
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
sm += [f'  <url><loc>{url(r)}</loc><lastmod>{today}</lastmod></url>' for r in PAGES]
sm.append('</urlset>')
open('sitemap.xml', 'w').write('\n'.join(sm) + '\n')
print('built', len(PAGES), 'pages + sitemap.xml')
