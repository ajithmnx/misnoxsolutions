"""One-off content fixes from the Nov 2026 site audit. Run from repo root."""
import re, sys

p = 'index.html'
s = open(p, encoding='utf-8').read()
miss = []

def rep(old, new, count=1):
    global s
    if old not in s:
        miss.append(old[:90]); return
    s = s.replace(old, new, count)

def rep_block(start, end, new):
    """Replace from `start` up to (not incl.) `end`."""
    global s
    i = s.find(start); j = s.find(end, i + 1)
    if i < 0 or j < 0:
        miss.append('BLOCK ' + start[:60]); return
    s = s[:i] + new + s[j:]

# ── shared: CTA wording (one free first step) ─────────────────────────
s = s.replace('Book a Discovery Call', 'Book an Intro Call')
rep("const ctaBand=(title,desc,b1='Book an Intro Call',b2='Explore Services',p2='services')",
    "const ctaBand=(title,desc,b1='Book an Intro Call',b2='View Services',p2='services')")

# ── shared platform grid (Home, ERP page) — match the Services list ───
rep_block("const platformsGrid=(cls='section')=>`", "const platformTags=",
"""const platformsGrid=(cls='section')=>`
<section class="${cls}">
  <div class="container">
    <div class="sh c reveal">
      <p class="eyebrow">Platforms</p>
      <h2 class="st">Platforms We Integrate</h2>
      <p class="sd">ERP and finance platforms we connect through their documented APIs.</p>
    </div>
    <div class="grid-3">${[
      [PF.ms,'Microsoft Dynamics 365','Business Central and Finance &amp; Operations.'],
      [PF.oracle,'Oracle NetSuite &amp; Fusion','AP, supplier and GL integration.'],
      [PF.sap,'SAP','Vendor and payables integration for multi-entity environments.'],
      [PF.t1,'TechnologyOne','Government, education and council finance.'],
      [PF.xero,'Xero','Often the counterpart to a larger ERP.'],
      [PF.myob,'MYOB','Australian SME accounting and payroll.'],
    ].map(([b,t,d])=>`<div class="card reveal"><div class="pf-head">${b}<h3>${t}</h3></div><p>${d}</p></div>`).join('')}</div>
    <p style="text-align:center;margin-top:24px" class="reveal"><a class="card-link" href="#services">Full platform list <span class="arrow">→</span></a></p>
  </div>
</section>`;

""")

# ── HOME ──────────────────────────────────────────────────────────────
rep('<span class="sr-only"> — ERP integration services for Australian mid-market and enterprise organisations</span>',
    '<span class="sr-only"> — ERP and finance system integration for Australian organisations</span>')
rep('Integration architecture, implementation, and managed operations for ERP, finance, and procurement platforms — engineered so data moves automatically and controls hold.',
    'We connect your ERP, finance and procurement systems so data moves on its own and your approval rules are enforced, not just written down.')
rep("onclick=\"navigate('services')\">Explore Capabilities</button>", "onclick=\"navigate('services')\">See Our Services</button>")
rep("['Fixed-scope engagements','Client-owned IP','Data stays in Australia']",
    "['Fixed-scope pricing','You own everything we build','Data stays in your systems']")
rep('<span class="fs-check">Duplicate &amp; bank details checked</span>', '<span class="fs-check">GL coding validated</span>')

# home: replace everything after the hero up to the end of the home route
home_start = s.find("${platformsGrid('section section-alt')}", s.find("register('home'"))
home_end = s.find("// ══ ABOUT ══")
if home_start < 0 or home_end < 0:
    miss.append('HOME body')
else:
    s = s[:home_start] + r"""${platformsGrid('section section-alt')}

<!-- PROBLEMS -->
<section class="section">
  <div class="container">
    <div class="sh c reveal">
      <p class="eyebrow">Common starting points</p>
      <h2 class="st">Sound Familiar?</h2>
    </div>
    <div class="grid-2 reveal reveal-delay-1">
      ${[
        ['Month-end takes days','Manual journals and spreadsheet reconciliations, because the systems that should be connected aren\'t.'],
        ['The same data is typed in twice','Invoices keyed into one system, then again into the ERP. Slow, and a common source of errors.'],
        ['Approval limits live on paper','Policy says $50k needs two sign-offs, but nothing in the system stops it.'],
        ['Failures are found by accident','A sync stops quietly and nobody notices until the numbers look wrong.'],
      ].map(([t,d])=>`
      <div class="card" style="border-left:3px solid rgba(239,68,68,0.4)">
        <h3 style="margin-bottom:10px">${t}</h3>
        <p>${d}</p>
      </div>`).join('')}
    </div>
  </div>
</section>

<!-- SERVICES -->
<section class="section section-alt">
  <div class="container">
    <div class="sh c reveal">
      <p class="eyebrow">Services</p>
      <h2 class="st">What We Do</h2>
    </div>
    <div class="bento reveal reveal-delay-1">
      <div class="bcard bcard-wide" style="background:rgba(122,76,240,0.05);border-color:rgba(122,76,240,0.18)">
        <div style="display:flex;align-items:center;gap:14px;margin-bottom:14px">
          <div class="bcard-icon" style="margin-bottom:0">${ic('gitmerge',22)}</div>
          <h3 style="font-size:1.25rem;margin-bottom:0">System Integration</h3>
        </div>
        <p style="font-size:0.9375rem;line-height:1.7;max-width:560px;margin-bottom:20px">We connect your systems using their own APIs and standard tools, so there's no proprietary connector to get locked into.</p>
        <p style="font-size:0.72rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:rgba(255,255,255,0.35);margin-bottom:10px">Typical flows</p>
        <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:4px">
          ${['Supplier invoices → ERP with 3-way match','PO and receipt sync','GL consolidation across entities','CRM orders → finance'].map(t=>`<span style="padding:7px 15px;background:rgba(122,76,240,0.1);border:1px solid rgba(122,76,240,0.22);border-radius:100px;font-size:0.76rem;font-weight:600;color:var(--accent2)">${t}</span>`).join('')}
        </div>
        <a class="bcard-cta" href="#services">All services <span class="arrow">→</span></a>
      </div>
      ${SERVICES.filter(x=>x[0]!=='System Integration').map(([title,icon,desc,page])=>`
      <div class="bcard">
        <div class="bcard-icon">${ic(icon,20)}</div>
        <h3>${title}</h3>
        <p>${desc}</p>
        ${page?`<a class="bcard-cta" href="#${page}">Learn more <span class="arrow">→</span></a>`:''}
      </div>`).join('')}
    </div>
  </div>
</section>

<!-- HOW WE WORK -->
<section class="section">
  <div class="container">
    <div class="sh c reveal">
      <p class="eyebrow">How we work</p>
      <h2 class="st">Four Steps, Fixed Price</h2>
      <p class="sd">Every project follows the same path, and you know the cost before we build.</p>
    </div>
    <div class="grid-2">
      ${PHASES.map(([n,t,time,d])=>`
      <div class="why-card reveal">
        <div class="ps-num" style="font-size:1.4rem;margin-bottom:10px">${n}</div>
        <h3 style="margin-top:0">${t} <span style="font-size:0.8rem;font-weight:500;color:var(--muted)">· ${time}</span></h3>
        <p>${d}</p>
      </div>`).join('')}
    </div>
    <p style="text-align:center;margin-top:28px" class="reveal"><a class="card-link" href="#delivery">How we work in detail <span class="arrow">→</span></a></p>
  </div>
</section>

<!-- PROMISES -->
<section class="section section-alt">
  <div class="container">
    <div class="sh c reveal">
      <p class="eyebrow">What you can count on</p>
      <h2 class="st">Our Commitments</h2>
    </div>
    <div class="grid-2">
      ${[
        ['lock','You own it','All code, configuration and documentation is yours. Another team could run it from our handover notes.'],
        ['shield','Controls built in','Approval limits, segregation of duties and audit trails are part of the design, not added later.'],
        ['database','Your data stays put','Integrations run inside your environment. We don\'t host, copy or keep your financial data.'],
        ['target','Fixed price','We quote against a signed-off design. Any change is priced and approved before we do it.'],
      ].map(([icon,t,d])=>`
      <div class="why-card reveal">
        <div class="card-icon">${ic(icon,22)}</div>
        <h3 style="margin-top:0">${t}</h3>
        <p>${d}</p>
      </div>`).join('')}
    </div>
  </div>
</section>

${ctaBand('Let\'s Talk','A free 30-minute call to understand your systems and whether we can help.')}`);

""" + s[home_end:]

# shared data used by Home, Services, footer
rep("const routes={};", r"""// Single source of truth for services and process
const SERVICES=[
  ['System Integration','gitmerge','Connect finance, procurement, CRM and operational systems through their own APIs.',null],
  ['Workflow Automation','zap','Invoice processing, approval routing and month-end tasks, automated with controls built in.',null],
  ['Data Migration & Sync','database','Move data cleanly between platforms, and keep systems in sync afterwards.',null],
  ['ERP Integration Projects','cpu','Connect a new or existing ERP to the rest of your business.','erp'],
  ['Managed Support','wrench','Monitoring, fixes and improvements for integrations once they are live.',null],
];
const PHASES=[
  ['01','Discover','2–3 weeks','A short, fixed-price review of your systems and data flows. You keep the findings whether or not you go ahead.'],
  ['02','Design','1–2 weeks','We document exactly what will be built, field by field, and you sign it off before any code is written.'],
  ['03','Build & go live','4–8 weeks','Built and tested against the design, then switched on in a planned window with a rollback ready.'],
  ['04','Support','Ongoing','Optional monthly support: monitoring, fixes and improvements.'],
];

const routes={};""")

# ── ABOUT (absorbs Why MISNOX) ────────────────────────────────────────
rep_block("register('about',()=>`", "// ══ SERVICES ══", r"""register('about',()=>`
<section class="page-hero"><div class="container"><div class="page-hero-content"><p class="eyebrow">About MISNOX Solutions</p><h1>Integration Specialists, Based in Canberra</h1><p>We do one thing: connect the systems that run your finance and procurement, and keep them running.</p></div></div></section>
<section class="section"><div class="container"><div style="max-width:720px" class="reveal">
  <p class="eyebrow">What we do</p><h2 class="st">One Focus</h2>
  <p style="color:var(--muted);line-height:1.75;font-size:1.0625rem">MISNOX Solutions is a small, specialist practice. We connect ERP, finance and procurement systems, automate the work between them, and support those connections once they're live. Because that's all we do, the person who designs your integration is the person who builds it.</p>
  <p style="color:var(--muted);line-height:1.75;font-size:1.0625rem;margin-top:16px">Our team's certifications include Workato Automation Pro.</p>
</div></div></section>
<section class="section section-alt"><div class="container">
  <div class="sh c reveal"><p class="eyebrow">How we work</p><h2 class="st">What Working With Us Is Like</h2></div>
  <div class="grid-2">${[
    ['target','Honest advice','We recommend what suits your environment, not what earns us the most. If you don\'t need us, we\'ll say so.'],
    ['check','Built to last','We measure success by what runs reliably in production, not by documents.'],
    ['layers','The designer builds it','The person who designs your integration stays through build and go-live.'],
    ['users','Clear updates','You always know what\'s done, what\'s next and what has changed.'],
  ].map(([icon,t,d])=>`<div class="card reveal" style="display:flex;gap:16px;align-items:flex-start"><div style="flex-shrink:0;margin-top:2px;color:var(--accent)">${ic(icon,22)}</div><div><h3>${t}</h3><p>${d}</p></div></div>`).join('')}</div>
</div></section>
${ctaBand('Get in Touch','Tell us what you are trying to connect.')}`);

""")

# ── SERVICES ──────────────────────────────────────────────────────────
rep('<p class="eyebrow">Our Services</p><h1>Integration &amp; Implementation Services</h1><p>ERP implementation, system integration, and managed operations — delivered end-to-end.</p>',
    '<p class="eyebrow">Our Services</p><h1>Integration Services</h1><p>Five services, one goal: systems that share data reliably and enforce your controls.</p>')
i = s.find("<section class=\"section\"><div class=\"container\"><div class=\"grid-3\">${[\n  ['cpu','System Implementations'")
j = s.find("<!-- PLATFORM DEPTH", i)
if i < 0 or j < 0: miss.append('SERVICES grid')
else:
    s = s[:i] + """<section class="section"><div class="container"><div class="grid-3">${SERVICES.map(([title,icon,desc,page])=>`<div class="card reveal"><div class="card-icon">${ic(icon,22)}</div><h3>${title}</h3><p>${desc}</p>${page?`<a class="card-link" href="#${page}">Learn more <span class="arrow">→</span></a>`:''}</div>`).join('')}</div></div></section>
""" + s[j:]
rep('<p class="eyebrow">Platform Capability</p>\n      <h2 class="st">Depth Where It Counts</h2>\n      <p class="sd">Depth is concentrated deliberately on fewer platforms. Where first-hand depth does not exist, integration proceeds through documented APIs — stated plainly, never implied.</p>',
    '<p class="eyebrow">Platforms</p>\n      <h2 class="st">Platforms We Integrate</h2>')
rep('<h3 style="font-size:1.05rem;font-weight:700;color:#fff;margin:0">Platforms We Integrate</h3>',
    '<h3 style="font-size:1.05rem;font-weight:700;color:#fff;margin:0">ERP, finance, CRM and reporting</h3>')
rep('<p style="font-size:0.875rem;color:rgba(255,255,255,0.6);line-height:1.65;margin-bottom:20px">ERP, finance, CRM and reporting platforms — connected through their documented APIs, data models and configuration frameworks.</p>',
    '<p style="font-size:0.875rem;color:rgba(255,255,255,0.6);line-height:1.65;margin-bottom:20px">Connected through each platform\'s documented APIs.</p>')
rep("If a platform exposes an API, it can usually be integrated — the list above reflects depth, not limits.",
    "Not on the list? If it has an API, we can usually connect it.")
# engagement section on Services (normalise wording)
rep("A short, paid engagement to map your systems, data flows, and integration gaps. Fixed price, fixed duration. Documentation remains with the client regardless of continuation.",
    "A short, fixed-price review of your systems, data flows and gaps. You keep the findings whether or not you go ahead.")
rep("Implementations and integrations quoted as fixed-scope, fixed-price work against an agreed design document. Change requests are priced transparently, not absorbed into a running meter.",
    "Each integration is quoted at a fixed price against a signed-off design. Changes are priced and approved before we do them.")
rep("Monthly retainer covering monitoring, exception handling, and continuous optimisation of live integrations. Scaled to the number of integrations under management.",
    "A monthly retainer for monitoring, fixes and improvements, priced by the number of integrations.")
rep("Engagements typically run discovery → fixed-scope delivery → managed support, and may conclude at any stage — all work produced transfers with the client.",
    "Most clients go discovery → build → support, but you can stop after any stage and keep everything produced so far.")
rep("${ctaBand('Discuss a Programme','Outline the systems involved and the connections required — practical guidance follows.','Book an Intro Call','Contact Us')}",
    "${ctaBand('Discuss Your Project','Tell us which systems are involved and what needs to connect.','Book an Intro Call','How We Work','delivery')}")

# ── ERP page (integration, not implementation) ────────────────────────
rep_block("register('erp',()=>`", "// ══ INDUSTRIES ══", r"""register('erp',()=>`
<section class="page-hero"><div class="container"><div class="page-hero-content"><p class="eyebrow">ERP Integration</p><h1>ERP Integration Projects</h1><p>Whether you're moving to a new ERP or getting more out of the one you have, we connect it to the rest of your business.</p></div></div></section>
<section class="section"><div class="container"><div class="split">
  <div class="reveal"><p class="eyebrow">Where we fit</p><h2 class="st">The Connections Around Your ERP</h2><p style="color:var(--muted);line-height:1.75;font-size:1.0625rem">Your ERP partner configures the ERP. We handle what connects to it: invoice capture, procurement, CRM, banking, reporting and data migration. We work alongside your ERP partner or internal team.</p></div>
  <div class="reveal reveal-delay-1"><div class="steps">${PHASES.map(([n,t,time,d],i)=>`<div class="step"><div class="step-num">${i+1}</div><div><h4>${t} · ${time}</h4><p>${d}</p></div></div>`).join('')}</div></div>
</div></div></section>
${platformsGrid('section section-alt')}
${ctaBand('Planning an ERP Change?','A free call to talk through what needs to connect, before you commit to anything.','Book an Intro Call','View Services')}`);

""")

# ── WHO WE HELP ───────────────────────────────────────────────────────
rep('<p class="eyebrow">Who We Help</p><h1>Teams and Organisations We Serve</h1><p>Finance and procurement functions, multi-entity enterprises, and professional services firms.</p>',
    '<p class="eyebrow">Who We Help</p><h1>Who We Work With</h1><p>Mid-sized Australian organisations, typically 50 to 500 staff, whose finance and procurement run across several systems.</p>')
rep("['P2P Automation','Supplier Onboarding','Procurement Controls','Master Data Sync','Compliance Workflows']",
    "['P2P Automation','PO and Receipt Matching','Procurement Controls','Master Data Sync']")
rep("'Accurate reporting, payment controls, and finance workflow automation — end to end.'",
    "'Faster month-end, enforced approvals and fewer manual journals.'")
rep("'Supplier management, P2P automation, and connected procurement operations.'",
    "'Purchase-to-pay that flows from request to ERP without re-keying.'")
rep("'Multi-system environments demanding governance, data control, and integration rigour.'",
    "'Several entities and systems that need to report as one.'")
rep("'Connected finance, resource, and billing systems for project-driven organisations.'",
    "'Projects, time and billing connected to finance.'")
rep("${ctaBand('Discuss a Programme','Sector and system context reviewed; fit advised candidly.','Book an Intro Call','View Services')}",
    "${ctaBand('Is This You?','Tell us about your setup and we will tell you honestly whether we can help.')}")

# ── WHY MISNOX → merged into About ────────────────────────────────────
rep_block("register('why-misnox',()=>`", "// ══ SECURITY & DATA HANDLING ══",
"register('why-misnox',()=>routes['about']());\n\n")

# ── SECURITY ──────────────────────────────────────────────────────────
rep("<h1>Client Data Remains in Client Environments</h1><p>MISNOX integrations run inside client infrastructure. No hosting, warehousing, or retention of financial data. This page sets out how access, credentials, and data are handled during and after an engagement.</p>",
    "<h1>Your Data Stays in Your Systems</h1><p>Our integrations run inside your environment. We don't host or keep your financial data. Here is how we handle access, credentials and data.</p>")
rep('<p class="sd">The defining feature of the MISNOX security posture: integrations run in the client environment, under client controls, with client logging.</p>',
    '<p class="sd">Integrations run in your environment, under your controls, with your logging.</p>')
rep("['landmark','Data Residency','Engagements are led and accountable from Australia. Client data does not leave Australian jurisdiction, and no client data is copied to delivery-team systems. Integrations deploy into the client\\'s nominated region.'],",
    "['landmark','Data Location','Integrations are deployed in your environment and the region you choose. We don\\'t copy your data to our own systems.'],")
rep("Testing uses de-identified or synthetic records wherever practical; any client data is deleted at engagement close.",
    "Where possible we test with dummy data, and anything we do handle is deleted when the project ends.")
i = s.find('<div style="max-width:760px;margin:44px auto 0;padding:28px 32px;background:rgba(255,255,255,0.03)', s.find("register('security'"))
j = s.find('</div>\n</div></section>\n${ctaBand(\'Security Questions\'', i)
if i < 0 or j < 0: miss.append('SECURITY response table')
else:
    s = s[:i] + '<p style="text-align:center;margin-top:36px;font-size:0.9rem;color:var(--muted)" class="reveal">Support response times are agreed for each client as part of a managed support arrangement.</p>\n  ' + s[j:]
rep("${ctaBand('Security Questions','The full posture can be walked through with your security or IT team, including access handling for your specific environment.','Talk to Us','Read the FAQ','faq')}",
    "${ctaBand('Security Questions?','We are happy to walk your IT or security team through how we would handle access in your environment.','Talk to Us','Read the FAQ','faq')}")

# ── DELIVERY ──────────────────────────────────────────────────────────
rep("<h1>Delivery Methodology</h1><p>Four phases, each with defined inputs, deliverables, and exit criteria — what is produced, when it arrives, and what must be true before the next phase begins.</p>",
    "<h1>How We Work</h1><p>Four phases. For each one: what we do, what you get, and what has to be true before we move on.</p>")
rep("['02','Design · 2–4 weeks'", "['02','Design · 1–2 weeks'")
rep("['03','Deliver · 4–12 weeks'", "['03','Build &amp; go live · 4–8 weeks'")
rep("'Design document signed off by finance, technology, and operations stakeholders.'",
    "'You sign off the design document.'")
rep("['users','Weekly Status','A concise written status each week: what moved, what is blocked, what changed.'],",
    "['users','Regular Updates','A short written update at an agreed rhythm: what moved, what is blocked, what changed.'],")
rep("['check','Single Point of Accountability','One named consultant accountable for the engagement end-to-end — the same consultant who designed it.'],",
    "['check','One Person Accountable','The person who designs your integration stays with it through build and go-live.'],")
rep('<h2 class="st">Governance During Delivery</h2>', '<h2 class="st">During the Project</h2>')
rep("${ctaBand('Start With Discovery','A discovery engagement maps your systems and shows what integration would involve.','Book an Intro Call','View Services')}",
    "${ctaBand('Start With a Conversation','A free intro call, then a fixed-price discovery if it makes sense.')}")

# ── FAQ ───────────────────────────────────────────────────────────────
rep("Proven patterns are reused across engagements — the speed benefit of prior work without lock-in to MISNOX-specific technology.",
    "We reuse our own patterns to move faster, without locking you into anything MISNOX-specific.")
rep("A single point-to-point integration typically takes four to eight weeks to build once design is signed off — around eight to fourteen weeks end to end including discovery and design.",
    "A single integration typically takes four to eight weeks to build once the design is signed off — around seven to thirteen weeks end to end, including discovery and design.")
rep("Discovery engagements are fixed price and fixed duration.", "The intro call is free. Discovery is fixed price and fixed duration.")
rep("'The initial conversation and fit assessment carry no charge. Paid work begins at discovery, once scope is agreed.'",
    "'The intro call is free. Paid work starts with discovery, once you have agreed the scope.'")
rep("Managed-support clients hold defined response targets by severity.", "Managed support clients have agreed response times.")
rep("The published platform list reflects deepest first-hand configuration knowledge — not the limit of what can be connected.",
    "Our platform list shows where we work most often, not the limit of what we can connect.")
rep("${ctaBand('Another Question?','Direct enquiries receive an answer within one business day.','Get in Touch','Security & Data','security')}",
    "${ctaBand('Another Question?','Ask us directly.','Get in Touch','Security & Data','security')}")

# ── CONTACT ───────────────────────────────────────────────────────────
rep('<p class="eyebrow">Get in Touch</p><h1>Contact</h1><p>Enquiries receive a response within one business day.</p>',
    '<p class="eyebrow">Get in Touch</p><h1>Contact</h1><p>We reply to every enquiry within one business day.</p>')
rep('<h2 style="font-size:1.5rem;font-weight:800;color:#f0f6ff;margin-bottom:8px;letter-spacing:-0.02em">Book an Intro Call</h2>\n    <p style="color:var(--muted);margin-bottom:18px">Outline the project; a response follows within one business day.</p>',
    '<h2 style="font-size:1.5rem;font-weight:800;color:#f0f6ff;margin-bottom:8px;letter-spacing:-0.02em">Book an Intro Call</h2>\n    <p style="color:var(--muted);margin-bottom:18px">A free 30-minute call. Tell us a little about your systems and we will suggest a time.</p>')
rep("['No obligation','Response within 1 business day','Australian-led delivery']", "['Free, no obligation','Canberra-based']")
s = re.sub(r'<select id="f-service" name="service"><option value="">Select a service...</option>.*?</select>',
    '<select id="f-service" name="service"><option value="">Select a service...</option><option>System Integration</option><option>Workflow Automation</option><option>Data Migration &amp; Sync</option><option>ERP Integration Project</option><option>Managed Support</option><option>Not sure yet</option></select>', s, count=1, flags=re.S)
rep('value="New discovery call request — misnox.com.au"', 'value="New intro call request — misnox.com.au"')
rep('<div class="expect-item">Initial call to understand your requirements</div>\n        <div class="expect-item">No-obligation project discussion</div>\n        <div class="expect-item">Practical guidance on approach and timeline</div>',
    '<div class="expect-item">A free 30-minute call about your systems</div>\n        <div class="expect-item">An honest view on whether we can help</div>\n        <div class="expect-item">If so, a fixed-price discovery proposal</div>')
rep('subject=Discovery%20call', 'subject=Intro%20call')

# ── NAV, MOBILE MENU, FOOTER ──────────────────────────────────────────
rep('<a href="#erp">ERP Implementations</a>\n          <a href="#delivery">Delivery Methodology</a>',
    '<a href="#erp">ERP Integration</a>\n          <a href="#delivery">How We Work</a>')
rep('<a href="#faq">FAQ</a>\n          <a href="#why-misnox">Why MISNOX</a>\n        </div>', '<a href="#faq">FAQ</a>\n        </div>')
rep('<a href="#erp" onclick="toggleMobile()">ERP Implementations</a>\n    <a href="#delivery" onclick="toggleMobile()">Delivery Methodology</a>',
    '<a href="#erp" onclick="toggleMobile()">ERP Integration</a>\n    <a href="#delivery" onclick="toggleMobile()">How We Work</a>')
rep('    <a href="#why-misnox" onclick="toggleMobile()">Why MISNOX</a>\n', '')
rep('<p>System integration and finance automation for organisations that need reliability, control, and connected operations.</p>',
    '<p>ERP and finance system integration for Australian organisations.</p>')
rep('<a href="#erp">ERP Implementations</a>\n        <a href="#services">System Integrations</a>\n        <a href="#delivery">Delivery Methodology</a>\n        <a href="#services">API &amp; Middleware</a>\n        <a href="#services">Data Migration</a>\n        <a href="#services">Managed Support</a>',
    '<a href="#services">System Integration</a>\n        <a href="#services">Workflow Automation</a>\n        <a href="#services">Data Migration &amp; Sync</a>\n        <a href="#erp">ERP Integration Projects</a>\n        <a href="#services">Managed Support</a>')
rep('        <a href="#why-misnox">Why MISNOX</a>\n', '        <a href="#delivery">How We Work</a>\n')

# ── META ──────────────────────────────────────────────────────────────
rep('content="MISNOX Solutions connects finance, procurement, and operational systems — delivering the integration architecture, automation, and controls that high-performing organisations depend on. Based in Canberra, ACT."',
    'content="MISNOX Solutions connects ERP, finance and procurement systems for Australian organisations: integration, workflow automation, data migration and support. Based in Canberra, ACT."')
rep('content="Your systems connected. Your controls enforced. ERP integration, finance automation, and implementation delivery for Australian organisations."',
    'content="Your systems connected. Your controls enforced. ERP and finance system integration for Australian organisations."')

open(p, 'w', encoding='utf-8').write(s)
print('MISSING:' if miss else 'all applied', *miss, sep='\n  ')
