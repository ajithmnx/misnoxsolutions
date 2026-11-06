"""Generate one static copy of index.html per page so every page has its own URL,
title and description (better for Google), plus sitemap.xml.

index.html is the only file to edit. After editing it, run:  python3 tools/build_pages.py
"""
import re, os, datetime

SITE = 'https://misnox.com.au'
PAGES = {  # route: (title, description)
    'home': ('Misnox Solutions | Your systems, connected',
             'ERP and finance integration solutions.'),
    'about': ('About | Misnox Solutions',
              'Integration specialists for organisations whose finance and procurement run across several systems.'),
    'services': ('Integration Services | Misnox Solutions',
                 'System integration, workflow automation, data migration, ERP integration and managed support, and how we deliver them.'),
    'erp': ('ERP Migrations | Misnox Solutions',
            'Change your ERP without breaking the business: every connection mapped, data reconciled, and a cutover with a way back.'),
    'security': ('Security & Data Handling | Misnox Solutions',
                 'Integrations run inside your environment. How we handle access, credentials and data.'),
    'faq': ('FAQ | Misnox Solutions',
            'Answers on ownership, pricing, process, support and data handling.'),
    'privacy': ('Privacy Policy | Misnox Solutions',
                'How Misnox Solutions handles personal information under the Australian Privacy Principles.'),
    'contact': ('Contact | Misnox Solutions',
                'Book a free intro call with Misnox Solutions, Sydney.'),
}
# Retired pages: kept as small redirect files so old links keep working.
REDIRECTS = {'industries': '/about/#who', 'delivery': '/services/#how'}

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
h404 = re.sub(r'<title>.*?</title>', '<title>Page Not Found | Misnox Solutions</title>', h404, count=1, flags=re.S)
open('404.html', 'w', encoding='utf-8').write(h404)

today = datetime.date.today().isoformat()
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
sm += [f'  <url><loc>{url(r)}</loc><lastmod>{today}</lastmod></url>' for r in PAGES]
sm.append('</urlset>')
open('sitemap.xml', 'w').write('\n'.join(sm) + '\n')
for r, to in REDIRECTS.items():
    os.makedirs(r, exist_ok=True)
    open(f'{r}/index.html', 'w', encoding='utf-8').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex"><link rel="canonical" href="{SITE}{to.split('#')[0]}"><meta http-equiv="refresh" content="0; url={to}"><title>Moved | Misnox Solutions</title><script>location.replace({to!r})</script></head><body><p>This page has moved: <a href="{to}">{to}</a></p></body></html>')
print('built', len(PAGES), 'pages + sitemap.xml +', len(REDIRECTS), 'redirects')

# ── Pre-render: put each page's content into its HTML so search engines and
#    link-preview bots see it without running JavaScript. Needs Playwright + Chrome;
#    skipped (pages still work) if unavailable.
def prerender():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print('prerender skipped (no playwright)'); return
    import threading, http.server, socketserver, functools
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    handler = functools.partial(Quiet, directory='.')
    srv = socketserver.TCPServer(('127.0.0.1', 0), handler); port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    files = {r: ('index.html' if r == 'home' else f'{r}/index.html') for r in PAGES}
    with sync_playwright() as p:
        exe = '/usr/bin/google-chrome' if os.path.exists('/usr/bin/google-chrome') else None
        b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        pg = b.new_page()
        pg.route('**/fonts.googleapis.com/**', lambda r: r.abort())
        for r, f in files.items():
            pg.goto(f'http://127.0.0.1:{port}/' + ('' if r == 'home' else r + '/'))
            pg.wait_for_selector('#app > *')
            inner = pg.evaluate("document.getElementById('app').innerHTML")
            h = open(f, encoding='utf-8').read()
            h = re.sub(r'<main id="app">.*?</main>', lambda m: '<main id="app">' + inner + '</main>', h, count=1, flags=re.S)
            open(f, 'w', encoding='utf-8').write(h)
        b.close()
    srv.shutdown()
    print('prerendered', len(files), 'pages')

prerender()
