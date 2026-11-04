"""Nov 2026 typography pass: Plus Jakarta Sans for body/UI (replaces IBM Plex Sans), Sora headings kept,
IBM Plex Mono only inside technical graphics, consistent uppercase eyebrows, form controls inherit the font."""
p='index.html'; s=open(p,encoding='utf-8').read()
s=s.replace('family=IBM+Plex+Sans:wght@400;500;600','family=Plus+Jakarta+Sans:wght@400;500;600;700')
s=s.replace("'IBM Plex Sans'","'Plus Jakarta Sans'")
CSS='''
/* ── Typography pass (Nov 2026) ── */
body{font-family:'Plus Jakarta Sans',-apple-system,'Segoe UI',system-ui,sans-serif;font-size:16px;line-height:1.7;letter-spacing:0;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
button,input,select,textarea{font-family:inherit}
.btn{font-family:'Plus Jakarta Sans',sans-serif;font-weight:600;letter-spacing:0}
h1,h2,h3,h4{font-family:'Sora',sans-serif;text-wrap:balance}
h2.st{font-weight:700;letter-spacing:-0.02em;line-height:1.15}
.sd,.hero-sub,.page-hero p{font-size:1.06rem;line-height:1.7;text-wrap:pretty}
p{text-wrap:pretty}
.eyebrow,.hc-split>div>.mono,.ls-label,.photo-band .mono{font-family:'Plus Jakarta Sans',sans-serif;font-size:.74rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--accent2)}
.photo-band .mono{color:#8FE3EE}
.ls-label{color:var(--muted)}
.hc-head b,.tile h3,.inode h3,.phase h3{font-family:'Sora',sans-serif}
.hc-opt,.hc-link,.tabs button{font-family:'Plus Jakarta Sans',sans-serif}
.nav-link,.dropdown a,.mobile-menu a{font-weight:500}

body{letter-spacing:.006em;word-spacing:.06em}
h1,h2,h3,h4,.btn,.mono,.kv,.imap,.mflow,.ptl-chip,.tile .fl{word-spacing:normal}
.sd,.hero-sub:not(.hero-photo *),.page-hero p,.card p,.tile p,.plist-item p,.phase p,.qrow-item p{color:#4F5470}
'''
s=s.replace('</style>',CSS+'</style>',1)
open(p,'w',encoding='utf-8').write(s);print('ok',s.count("IBM Plex Sans"))
