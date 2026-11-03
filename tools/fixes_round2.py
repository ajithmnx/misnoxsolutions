"""Second site review fixes (items 1-12). Run from repo root."""
import re

p = 'index.html'
s = open(p, encoding='utf-8').read()
miss = []

def rep(a, b):
    global s
    if a not in s:
        miss.append(a[:80]); return
    s = s.replace(a, b, 1)

# 2. share text
rep('<meta name="twitter:title" content="MISNOX Solutions | System Integration &amp; Finance Automation"/>',
    '<meta name="twitter:title" content="MISNOX Solutions | ERP &amp; Finance System Integration"/>')
s = re.sub(r'<meta name="twitter:description" content="[^"]*"/>',
           '<meta name="twitter:description" content="Your systems connected. Your controls enforced. ERP and finance system integration for Australian organisations."/>', s, count=1)
rep('<meta property="og:image" content="https://misnox.com.au/og-image.png"/>',
    '<meta property="og:image" content="https://misnox.com.au/og-image.png"/>\n<meta property="og:image:width" content="1200"/>\n<meta property="og:image:height" content="630"/>\n<meta property="og:image:alt" content="MISNOX Solutions — Your systems, connected. Your controls, enforced."/>')

# 4. badge letters are decoration for screen readers / search
s = s.replace('<span class="pf-badge" title=', '<span class="pf-badge" aria-hidden="true" title=')

# 5. hero point + duplicate FAQ
rep("['You own everything we build','Data stays in your systems']", "['You own everything we build','No vendor lock-in']")
rep("      ['Where does our data live?','In client systems. MISNOX does not warehouse or retain transactional data. Integrations move data directly between client platforms, inside the client environment.'],\n", "")

# 6. scope-change repetition
rep("'Each project is quoted individually against a signed-off design. Changes are agreed before we do them.'",
    "'Each project is quoted individually, based on the signed-off design.'")
rep("['target','Change Control','Scope variations are documented, priced, and approved before work commences.'],",
    "['lock','Proper Handover','Documentation and a walkthrough, so your team can run the integration without us.'],")

# 7. merge duplicate pricing FAQ
rep("      ['Do you charge for the initial conversation?','No. The intro call is free. Paid work starts with discovery, once you have agreed the scope.'],\n", "")
rep("'The intro call is free. Every project is different, so we quote each one individually, based on the agreed design. Managed support is a monthly retainer based on the integrations we look after.'",
    "'The intro call is free. Paid work starts with discovery. Every project is different, so we quote each one individually, based on the agreed design. Managed support is a monthly retainer based on the integrations we look after.'")

# 8. hero graphic
rep('<span class="fs-check">Matched to PO &amp; receipt</span>', '<span class="fs-check">Matched to purchase order</span>')

# 9. plain "we / you" voice — Security
rep("'Credentials reside in the client\\'s secret store — Azure Key Vault, AWS Secrets Manager, or equivalent. Client credentials are never held in MISNOX systems, email, or documentation. Access is via named accounts the client provisions and can revoke.'",
    "'Credentials stay in your own secret store, such as Azure Key Vault or AWS Secrets Manager. We never keep them in our systems, email or documents. We use named accounts that you create and can revoke at any time.'")
rep("'Every service account is scoped to the minimum permissions the integration requires, with each account\\'s access documented for independent review by the client\\'s security team.'",
    "'Each service account gets only the permissions the integration needs, and we document them so your security team can review them.'")
rep("'MISNOX does not store client transactional or financial data. Integrations move data directly between client systems. Where possible we test with dummy data, and anything we do handle is deleted when the project ends.'",
    "'We do not store your transactional or financial data. Integrations move data directly between your systems. Where possible we test with dummy data, and anything we do handle is deleted when the project ends.'")
rep("'All data in transit uses TLS 1.2 or above. Integration endpoints are authenticated — no anonymous endpoints, no unencrypted transfers. Where a legacy platform cannot meet this standard, it is flagged before build, not after.'",
    "'All data in transit uses TLS 1.2 or higher, and every endpoint requires authentication. If an older system cannot meet this, we tell you before we build, not after.'")
rep("'At engagement close, a documented register of every account, key, and permission granted during the work is provided, enabling verified revocation. Offboarding is a deliverable.'",
    "'When the project ends, you get a list of every account, key and permission we used, so you can confirm each one has been removed.'")
rep("Integrations fail. Networks drop, APIs deprecate, upstream systems change. What matters is whether the failure is detected, contained, and recoverable.",
    "Every integration fails sometimes: networks drop, APIs change, upstream systems change. What matters is that failures are caught, contained and easy to recover from.")
rep("'Every integration is built with logging and alerting from day one. Failures raise an alert to the client\\'s nominated channel — not a silent error in an unread log.'",
    "'Every integration has logging and alerts from day one. Failures alert your chosen channel, instead of sitting silently in a log.'")
rep("'Failed records are quarantined rather than dropped or partially written. A failed batch never leaves the ERP half-updated.'",
    "'Failed records are set aside, not dropped or half-written, so your ERP is never left half-updated.'")
rep("'Integrations are built to be replayable. Once the cause is resolved, quarantined records reprocess without manual re-entry or duplicate posting.'",
    "'Once the cause is fixed, the set-aside records run through again, with no re-keying and no duplicates.'")
# 12. jargon heading (Security)
rep('<h2 class="st">Delivery Inside the Client Tenancy</h2>', '<h2 class="st">We Work Inside Your Environment</h2>')

# 9. Delivery exit criteria
rep("'The client confirms the assessment reflects reality and priorities stand.'", "'You confirm the findings are accurate and agree the priorities.'")
rep("'UAT signed off, cutover executed, and the client team can operate the solution.'", "'You have signed off testing, the integration is live, and your team can run it.'")
rep("'Ongoing — reviewed at agreed intervals.'", "'Reviewed with you at agreed intervals.'")

# 9. FAQ voice
rep("Straight answers to the questions asked before engaging.", "Straight answers to what people ask before working with us.")
rep("'Custom, built on platform-native APIs and mainstream middleware. MISNOX does not sell a proprietary connector product. We reuse our own patterns to move faster, without locking you into anything MISNOX-specific.'",
    "'Custom, built on each platform\\'s own APIs and standard tools. We do not sell a connector product. We reuse our own patterns to move faster, without locking you into anything of ours.'")
rep("'The client. Code, configuration, documentation, and design artefacts transfer in full. Should the engagement end, everything continues to run and a successor partner can operate from the documentation.'",
    "'You do. All code, configuration and documentation is handed over in full. If we stop working together, everything keeps running and another team can pick it up from the documentation.'")
rep("'Yes — preferably. Internal IT holds the environment knowledge that makes integrations succeed. MISNOX operates either as an extension of the internal team or delivers end-to-end with defined touchpoints.'",
    "'Yes, and we prefer it. Your IT team knows your environment best. We can work as an extension of your team, or deliver end to end with clear check-in points.'")
rep("'Variations are documented, priced, and approved before any work begins. No invoice is issued for scope not explicitly approved.'",
    "'We write up the change and its cost, and only do it once you approve. You are never invoiced for work you did not approve.'")
rep("'Failures raise an immediate alert to the nominated channel. Failed records are quarantined rather than partially written, so the ERP is never left inconsistent. Once resolved, quarantined records replay without manual re-entry. Managed support clients have agreed response times.'",
    "'An alert goes straight to your chosen channel. Failed records are set aside rather than half-written, so your ERP stays consistent, and once the issue is fixed they run again with no re-keying. Managed support clients have agreed response times.'")
rep("'If it exposes an API, it can almost certainly be integrated. Our platform list shows where we work most often, not the limit of what we can connect.'",
    "'If it has an API, we can almost certainly connect it. Our platform list shows where we work most often, not the limit.'")
rep("'Often, yes. Existing work is reviewed and a candid assessment provided — maintain or rebuild — with the reasoning either way.'",
    "'Often, yes. We review what exists and tell you honestly whether to keep it or rebuild it, and why.'")

# 10 + 11. Who We Help
rep("['Multi-Entity Enterprises',", "['Multi-Entity Organisations',")
rep("['Multi-Entity ERP','AP/AR Automation','Audit-Ready Flows','Platform Migration','Data Synchronisation']", "['AP and AR automation','Month-end reconciliation','Approval controls']")
rep("['P2P Automation','PO and Receipt Matching','Procurement Controls','Master Data Sync']", "['Purchase-to-pay automation','PO matching','Supplier data sync']")
rep("['Secure Architecture','Segregation of Duties','API & Middleware','Data Governance','Operational Sync']", "['Intercompany transactions','Group reporting','Segregation of duties']")
rep("['Project Accounting','CRM Integration','Billing Automation','Resource Planning','Practice Management Sync']", "['Project accounting','CRM to finance','Billing automation']")

open(p, 'w', encoding='utf-8').write(s)
print('MISSING:' if miss else 'all applied', *miss, sep='\n  ')
