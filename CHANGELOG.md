# Changelog

Every change to the live site is committed straight to `main` and logged here (newest first), so any version can be restored.

**To roll back:** tell Claude "revert the site to <commit>" — or run `git checkout <commit> -- index.html`, then `python3 tools/build_pages.py`, and commit.

**Editing:** `index.html` is the only page source. After editing it, run `python3 tools/build_pages.py` to regenerate the per-page copies and `sitemap.xml`.

| Date | Change | Commit |
|---|---|---|
| 2026-11-03 | Review round 2: link-preview image (og-image.png) + per-page share text; branded 404 page (wrangler.jsonc not_found_handling); badge letters hidden from screen readers; hero point → "No vendor lock-in"; removed duplicate FAQs (data location, initial-call charge); scope-change message no longer repeated; hero "Matched to purchase order"; Security/How We Work/FAQ rewritten in we/you voice; "Multi-Entity Organisations"; Who We Help tags trimmed to 3 concrete each; "We Work Inside Your Environment" | 06889a1 |
| 2026-11-03 | "How we work" band changed from light grey-blue to a lifted navy band with a soft cyan glow and violet edge lines | 0e9f0d1 |
| 2026-11-03 | "How we work" light band toned down from near-white to a soft grey-blue (#C9D0DE); cards dimmed; text contrast kept above 5:1 | a8f598f |
| 2026-11-03 | Look & feel: Sora font for headings; platform card grid replaced by an animated "one layer between your systems" hub diagram (Home + ERP); "Sound familiar?" as a clean numbered list (red borders removed); "How we work" on a light background; commitments as a quiet row instead of cards | 23369ac |
| 2026-11-03 | Location Canberra → Sydney; removed all "fixed price/fixed-scope" wording and every timeline (process, services, delivery, FAQ); hero chip "Fixed-scope pricing" removed; flow "Supplier invoices → 3-way match" → "Bank feeds → automated reconciliation"; "Four Steps, Fixed Price" → "Four Clear Steps"; commitment "Fixed price" → "Clear quotes" | bf44933 |
| 2026-11-03 | Site audit fixes: removed risky claims (Australian data residency, "implementation", supplier/bank-detail checks, SLAs/same-day response, implied track record); one free "Intro Call" + paid discovery; one timeline (7–13 weeks), one 5-service list, one platform list, one 4-phase process; Home cut ~35%; plain-English rewrite; Why MISNOX merged into About; Workato certification added; real page URLs (/services/ etc.) with own titles + sitemap.xml; old #links redirect; CHANGELOG and tools hidden from the live site | 5ce5312 |
| 2026-11-03 | Services page: removed "Also Integrate With"; one "Platforms We Integrate" list in 2 columns; Xero and MYOB split; added MYOB Acumatica, QuickBooks, Salesforce, Power BI with badges; removed Boomi, MuleSoft, Azure Integration Services | 0a2d870 |
| 2026-11-03 | Site colours switched from indigo to the logo palette: cyan→violet gradient on headline highlights and main buttons; violet links/icons, cyan accents (all pass contrast) | e4ac3fa |
| 2026-11-03 | Logo 46→50px, wordmark 1.5rem, brighter SOLUTIONS line, header 68→74px; phones: compact logo + hide header button so the menu button is visible again (was pushed off-screen) | 8c3ec7f |
| 2026-11-03 | Logo enlarged in nav and footer (mark 34→46px, wordmark 1.05→1.4rem; smaller on phones) | af28433 |
| 2026-11-03 | Added brand/ logo images for email signatures and Microsoft sign-in page (site pages unchanged) | 8ee7012 |
| 2026-11-03 | New Crossflow logo (from Claude Design) in nav, footer and integration graphic; Unbounded wordmark; new browser-tab icon | eb0e8a1 |
| 2026-11-03 | Added this changelog (site itself unchanged) | 2a77393 |
| 2026-11-03 | **Baseline** — site as uploaded manually ("Add files via upload") | 1fa2acf |
