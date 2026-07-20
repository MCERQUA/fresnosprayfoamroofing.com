# SEO Improvement Plan — fresnosprayfoamroofing.com — 2026-07-20

_Full seo-review run: crawler + DataForSEO ($0.23) + 3 parallel deep-review agents (technical, content/conversion, local/franchise). Raw data: `/home/mike/MIKE-AI/scripts/seo-review/runs/fresnosprayfoamroofing.com/2026-07-20/`._

## Baseline
- **Domain:** live <48h, **0 ranked keywords**, 9 referring domains (vs incumbent foamroofingfresno.com: 30 RDs, 4 years old). Very winnable link neighborhood.
- **SERP "spray foam roofing fresno":** local pack (3 GBP contractors) then #4 allstatesprayfoamroofing.com (sister, city-page pattern), #5 jakesroofingandcoating.com, #6 foamroofingfresno.com. We are absent (expected).
- **Business context:** franchise-location model. Main brand site + GBP managed by a third party — this site must stand fully alone: own NAP, own future Fresno address + GBP (owner actions), zero entanglement with sister properties.

## Strategy (from real data)
1. **Own the commercial-intent cluster** ("commercial roofing fresno", foam repair, cost, building-type queries) while sister site keeps generic "spray foam roofing fresno" — two family domains, two SERP slots, no cannibalization. **Never interlink with allstatesprayfoamroofing.com.**
2. **Repair is the wedge:** foam roofing repair $29 CPC / roof repair fresno 320/mo / national "roof repair" KD 0.
3. **Local pack is positions 1–3** → future GBP (owner). Until then, on-page local proof carries everything.
4. Close the 21-referring-domain gap via niche directories ONLY (policy: GBP/Yelp/BBB/Apple/Bing = owner-only) — **after** dedicated NAP exists (D1/D2), never with the shared number.

## Reconciliation vs prior plan (docs/IMPROVEMENT-PLAN.md 2026-07-19)
| Item | Status |
|---|---|
| Phase 1: 4 money pages, FAQ+schema, interlinks | SHIPPED |
| Phase 2: 5 city pages, 3 articles, warehouse img | SHIPPED (articles = direct-written guides, not article-writer pipeline) |
| 8 remaining articles via article-writer | NOT DONE (queued) |
| Cross-domain linking decision | RESOLVED by this review: do not link sister site |
| GSC/GA setup | NOT DONE → DECISIONS |
| AI-crawler unblock on CF zone | BLOCKED on token scope (Mike: add Zone>Bot Management>Edit) |

## Priorities (detail in seo-fix-workorders-2026-07-20.md)
- **P0:** compiled Tailwind CSS (kill 124KB render-blocking CDN JS) · extensionless URL canonicalization + 301s · lead form on EVERY page + email/property fields · image width/height/lazy · Tulare↔Hanford cannibalization fix
- **P1:** areaServed-per-city schema bug · truth pass (SPFA member not certified; drop "Fresno HQ"; Sacramento overreach; 85% UV→solar) · de-orphan 3 articles · favicon/logo weight · preload/preconnect · og:image 1200×630 + twitter cards · llms.txt + llms-full.txt + 404 page · sticky mobile call bar · Article schema on guides
- **P2:** title/desc trims · contrast fixes (red-on-navy hero span, stat-band labels) · heading hierarchy · city local-proof blocks (dispatch/driving-time, county+satellite towns, per-city FAQs) · trust badges at form
- **P3 (growth):** 8 article-writer articles · per-city project proof + testimonials as real jobs land · niche-directory citations after D1/D2 · 4-week DataForSEO re-pull

## DECISIONS (Mike/owner only — plan proceeds around them)
- **D1 — Dedicated 559 phone number** (Telnyx/InkBox, permanent DID, forwards to main line). STRONGLY recommended before any citation work; prevents NAP fusion with third-party-managed GBP. Say go and I provision.
- **D2 — info@fresnosprayfoamroofing.com** mailbox (InkBox custom domain). Recommended with D1.
- **D3 — Fresno street address** — when acquired: full PostalAddress + geo + openingHoursSpecification + real map embed (sequence documented in run dir).
- **D4 — Analytics:** GA4 (needs your Google account) or lightweight self-hosted? Conversion tracking is blind until this lands.
- **D5 — Confirm standing promises:** free drone survey + written bid within 48h (sitewide claims).
- **D6 — GBP creation** for this location — owner-only, after D3.
- **D7 — Home-base wording:** true base is Visalia/Tulare County today. Implementing safe version now ("Serving Fresno & the Central Valley"); flip when D3 lands.

## Verification
Every WO carries ACCEPT checks; final pass = live curl per page + Playwright visual strips (390px + 1280px) + form registration + Lighthouse-class perf sanity.
