# SEO Fix Work Orders — fresnosprayfoamroofing.com — 2026-07-20

RULES FOR ALL AGENTS: never delete (rename `.old`) · interior pages are GENERATED — fix `build-pages.py` templates and rerun, never hand-patch generated files · index.html is hand-maintained · one wave = one commit · after every wave: zip-deploy + live curl verify + form registration check · final wave ends with Playwright visual strips 390px+1280px that the agent LOOKS at.

DECISIONS (owner) — see plan doc: D1 dedicated 559 number · D2 domain mailbox · D3 Fresno address · D4 analytics choice · D5 confirm drone/48h promises · D6 GBP · D7 home-base wording (safe interim implemented).

## WAVE 1 — perf + URL foundation (files: build-pages.py, index.html, netlify.toml, sitemap.xml, assets/)
- **WO-1 Compiled CSS:** build static Tailwind (v3 CLI, forms plugin, theme from inline config) → `assets/site.css`; remove CDN `<script>` + inline config from all 15 pages. ACCEPT: no `cdn.tailwindcss.com` reference live; pages render identically (visual strip).
- **WO-2 Extensionless URLs:** canonicals, og:url, schema url/breadcrumb, ALL internal links, sitemap → extensionless; netlify.toml `[[redirects]]` 301 `.html`→extensionless (per page). ACCEPT: `curl -I /spray-foam-roofing-cost.html` → 301; canonical == final URL everywhere.
- **WO-3 Images:** width/height + `loading="lazy" decoding="async"` on every below-fold img; hero eager + `fetchpriority=high` + preload; favicon-32/-192/apple-touch generated (square-padded); `logo-200.png` for header/footer; recompress service-spf-roof.jpg + truck-trailer.jpg (≤120KB); asset cache 30d. ACCEPT: 0 imgs missing dims; favicon <10KB.
- **WO-4 Fonts:** preconnect googleapis+gstatic(crossorigin); merge font CSS requests. ACCEPT: single fonts.googleapis.com stylesheet + 2 preconnects per page.

## WAVE 2 — lead capture (build-pages.py TEMPLATE/FOOTER, index.html)
- **WO-5 Form everywhere:** embed Netlify form (same `name="roof-assessment"`, hidden form-name, honeypot) in every interior page CTA band; ADD fields sitewide: Email (required, type=email) + Property City (text) + autocomplete attrs. Button → "Get My Free Assessment"; reassurance line + badge chips at form. ACCEPT: form present on 13 pages; Netlify still shows ONE form `roof-assessment` with new fields after deploy; test POST lands.
- **WO-6 Sticky mobile call bar:** fixed bottom bar `[Call] [Free Assessment]` <768px, all pages, ≥44px targets. ACCEPT: visible in 390px strip, doesn't cover footer content (safe-area padding).

## WAVE 3 — targeting/truth/schema (build-pages.py page dicts + templates, index.html)
- **WO-7 Tulare/Hanford de-conflict:** Tulare page → Tulare-only title/H1/meta/schema (Hanford mention → single cross-link); footer splits into separate Tulare and Hanford links (all pages). ACCEPT: grep "Tulare & Hanford" → 0 hits.
- **WO-8 areaServed per city** + `@id:#contractor` on RoofingContractor; Service pages' provider → `@id` ref; 3 guides → `Article` schema (author=Org, datePublished 2026-07-19, dateModified today, visible "Updated July 2026" line); FAQPage schema strings = visible text verbatim; `sameAs` only if real profile URLs supplied (else omit). ACCEPT: city page schema names its own city; guides validate as Article.
- **WO-9 Truth pass:** "SPFA certified/trained"→"SPFA member" (3 sites) · map pin "Fresno HQ"→"Serving Fresno & the Central Valley" + schema stays locality-only · "From Sacramento to Bakersfield…most reliable in the state"→"From Merced to Bakersfield — the Central Valley's spray foam roofing specialists" · "85%+ UV"→"~85% of solar energy" · stat "Up to 50% Energy Savings"→"Slash Cooling Costs" · CTA band → "core sampling where needed". ACCEPT: greps return 0 for banned strings.
- **WO-10 De-orphan:** footer "Guides" column (3 articles) all pages; contextual links: FAQ#1→lifespan, commercial page→vs-TPO, Process→installation; repair page opening sentence leads with "Foam roof repair in Fresno". ACCEPT: crawler orphan count 0.

## WAVE 4 — meta/AEO/content polish
- **WO-11 Social meta:** 1200×630 og-share.jpg (truck-trailer composite) + og:image(+dims) + twitter:card on all pages; trim titles >60 ("| Allstate" suffix) + descriptions ≤160 keeping phone. ACCEPT: lengths pass, image live.
- **WO-12 llms.txt + llms-full.txt** (drafts in run dir; extensionless URLs) + **404.html** in site shell. ACCEPT: /llms.txt 200; bogus URL serves branded 404.
- **WO-13 City local proof:** per-city dispatch/driving-time block (honest: Tulare County shop; Bakersfield ~90min via CA-99) + county+satellite-town sentence + 2-3 city-specific FAQs w/ FAQPage schema + CTA band names the county. ACCEPT: no two city pages share FAQ questions; each names its county.
- **WO-14 A11y/contrast:** hero "Fresno" span → secondary-fixed on dark; stat labels full-white; process h4→h3; footer h5→p. ACCEPT: contrast ≥3:1 large/4.5:1 small on flagged nodes.

## FINAL VERIFICATION
1. All 13 pages live 200 extensionless, .html 301s, canonical==URL.
2. Netlify form registered w/ email+city fields; email hook intact.
3. Playwright strips 390+1280 of home + 1 city + 1 guide — LOOKED at.
4. Crawler re-run vs baseline: 0 new CRITICAL/HIGH; orphans resolved.
5. Commit per wave; ledger entry; register site in scripts/seo-review/sites.txt; pledge 4-week DataForSEO re-pull.

## DEFERRED (blocked on DECISIONS)
Phone/email swap (D1/D2) · address schema sequence (D3) · analytics + tel tracking (D4) · GBP (D6) · citations (after D1/D2) · 8 article-writer articles (owner scope call).
