#!/usr/bin/env python3
"""Patch site/index.html to match the 2026-07-20 work orders, reusing shared
blocks from build-pages.py (header+nav, footer+form+FAB+call bar). Fails loudly
if any expected anchor string is missing. Rerunnable only against the pre-patch
index — it verifies before writing."""
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("bp", os.path.join(HERE, "build-pages.py"))
bp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bp)

path = os.path.join(HERE, "site", "index.html")
src = open(path).read()
orig = src


def swap(old, new, count=1):
    global src
    if old not in src:
        print("MISSING ANCHOR:", old[:90].replace("\n", "\\n"))
        sys.exit(1)
    src = src.replace(old, new, count)


# ---- 1. HEAD: CDN tailwind + config + style block -> compiled css + fonts + favicons
head_old_start = '<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>'
i = src.index(head_old_start)
j = src.index("</style>") + len("</style>")
src = src[:i] + bp.HEAD_SHARED + src[j:]

# ---- 2. og/twitter/preload upgrades
swap('<meta property="og:image" content="https://fresnosprayfoamroofing.com/assets/hero-aerial.jpg"/>',
     '<meta property="og:image" content="https://fresnosprayfoamroofing.com/assets/og-share.jpg"/>\n'
     '<meta property="og:image:width" content="1200"/>\n<meta property="og:image:height" content="630"/>\n'
     '<meta name="twitter:card" content="summary_large_image"/>\n'
     '<meta name="twitter:title" content="Commercial Spray Foam Roofing Fresno, CA | Allstate Spray Foam Roofing"/>\n'
     '<meta name="twitter:image" content="https://fresnosprayfoamroofing.com/assets/og-share.jpg"/>\n'
     '<link rel="preload" as="image" href="/assets/hero-truck-trailer.webp" fetchpriority="high"/>')
swap('<link rel="icon" type="image/png" href="/assets/logo.png"/>', "")

# ---- 3. meta description tighten (<=160)
swap('<meta name="description" content="Commercial spray foam roofing &amp; silicone roof coatings in Fresno, CA. Seamless, leak-proof SPF roof systems for warehouses, ag facilities &amp; metal buildings. Family-owned 20+ years, licensed C-2-1052735. Free roof assessment: (559) 739-9519."/>',
     '<meta name="description" content="Commercial spray foam roofing &amp; silicone coatings in Fresno, CA. Seamless SPF roofs for warehouses &amp; ag facilities. Free assessment: (559) 739-9519."/>')

# ---- 4. schema: @id + sameAs-free hardening
swap('"@type": "RoofingContractor",\n  "name": "Allstate Spray Foam Roofing — Fresno",',
     '"@type": "RoofingContractor",\n  "@id": "https://fresnosprayfoamroofing.com/#contractor",\n  "name": "Allstate Spray Foam Roofing — Fresno",')

# ---- 5. FAQ schema wording sync (Q4 'go' vs 'applied')
swap('"name": "Can spray foam be applied over my existing roof?"',
     '"name": "Can spray foam go over my existing roof?"')

# ---- 6. header (with nav) replace
hstart = src.index("<header ")
hend = src.index("</header>") + len("</header>")
src = src[:hstart] + bp.HEADER + src[hend:]

# ---- 7. hero: contrast fix on Fresno span
swap('Roofing in <span class="text-secondary">Fresno</span>',
     'Roofing in <span class="text-secondary-fixed">Fresno</span>')
swap('<img class="absolute bottom-0 left-1/2 -translate-x-1/2 w-full max-w-[1700px] z-10 pointer-events-none drop-shadow-[0_25px_45px_rgba(0,0,0,0.55)]" alt="Allstate Spray Foam wrapped service truck and equipment trailer" src="/assets/hero-truck-trailer.webp"/>',
     '<img class="absolute bottom-0 left-1/2 -translate-x-1/2 w-full max-w-[1700px] z-10 pointer-events-none drop-shadow-[0_25px_45px_rgba(0,0,0,0.55)]" alt="Allstate Spray Foam wrapped service truck and equipment trailer" src="/assets/hero-truck-trailer.webp" width="1248" height="526" fetchpriority="high"/>')

# ---- 8. stat bar: label contrast + truthful stat
swap('<div class="font-headline-lg text-on-secondary text-2xl md:text-3xl">Up to 50%</div>\n<div class="font-label-caps text-on-secondary/80 text-[10px] uppercase">Energy Savings</div>',
     '<div class="font-headline-lg text-on-secondary text-2xl md:text-3xl">Cool-Roof</div>\n<div class="font-label-caps text-on-secondary text-[10px] uppercase">Slash Cooling Costs</div>')
src = src.replace('text-on-secondary/80 text-[10px]', 'text-on-secondary text-[10px]')

# ---- 9. service cards: link to real pages + img attrs
swap('<img alt="Spray foam roofing system installed on a commercial flat roof" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" src="/assets/service-spf-roof.jpg"/>',
     '<img alt="Spray foam roofing system installed on a commercial flat roof" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" src="/assets/service-spf-roof.jpg" width="900" height="600" loading="lazy" decoding="async"/>')
swap('<img class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" alt="Roofer spray-applying bright white silicone roof coating on a commercial flat roof" src="/assets/service-silicone.jpg"/>',
     '<img class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" alt="Roofer spray-applying bright white silicone roof coating on a commercial flat roof" src="/assets/service-silicone.jpg" width="1024" height="768" loading="lazy" decoding="async"/>')
swap('<img class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" alt="Commercial warehouse interior being insulated with spray foam along the ceiling and walls" src="/assets/service-insulation.jpg"/>',
     '<img class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" alt="Commercial warehouse interior being insulated with spray foam along the ceiling and walls" src="/assets/service-insulation.jpg" width="512" height="288" loading="lazy" decoding="async"/>')
card_link = '<a href="{href}" class="pt-4 font-label-caps text-secondary uppercase tracking-widest flex items-center gap-2 group-hover:gap-4 transition-all">\n                            View System Details <span class="material-symbols-outlined">arrow_forward</span>\n</a>'
for href in ("/spray-polyurethane-foam-roofing", "/foam-roof-repair-fresno", "/commercial-roofing-fresno"):
    swap('<a href="#assessment" class="pt-4 font-label-caps text-secondary uppercase tracking-widest flex items-center gap-2 group-hover:gap-4 transition-all">\n                            Get System Details <span class="material-symbols-outlined">arrow_forward</span>\n</a>',
         card_link.format(href=href))

# ---- 10. why-superior: diagram swap
swap('<img class="w-full aspect-square object-cover grayscale opacity-80" alt="Macro detail of dense closed-cell spray polyurethane foam showing its solid waterproof structure" src="/assets/foam-macro.jpg"/>',
     '<img class="w-full border-2 border-secondary/30" alt="Labeled cross-section diagram of a spray polyurethane foam roof system: structural deck, substrate, SPF insulation layer, base coat, and UV-protective roof coating" src="/assets/spf-roof-cross-section.webp" width="1200" height="900" loading="lazy" decoding="async"/>')

# ---- 11. truth pass
swap('From Sacramento to Bakersfield, we provide the most reliable commercial roofing service in the state.',
     'From Merced to Bakersfield — the Central Valley&#x27;s spray foam roofing specialists.')
swap('<div class="bg-primary text-on-primary px-3 py-1 font-label-caps text-[10px] mt-2">Fresno HQ</div>',
     '<div class="bg-primary text-on-primary px-3 py-1 font-label-caps text-[10px] mt-2">Serving Fresno &amp; the Central Valley</div>')
swap('Our crew is highly trained, SPFA certified,', 'Our crew is highly trained, an SPFA member,')
swap('Reflects 85%+ UV Rays', 'Reflects ~85% of Solar Energy')

# ---- 12. FAQ visible-text links -> extensionless
for a, b in ((".html", "") ,):
    pass
src = src.replace('href="/spray-polyurethane-foam-roofing.html"', 'href="/spray-polyurethane-foam-roofing"')
src = src.replace('href="/spray-foam-roofing-cost.html"', 'href="/spray-foam-roofing-cost"')
src = src.replace('href="/foam-roof-repair-fresno.html"', 'href="/foam-roof-repair-fresno"')
src = src.replace('href="/commercial-roofing-fresno.html"', 'href="/commercial-roofing-fresno"')
src = src.replace('href="/spray-foam-roofing-visalia.html"', 'href="/spray-foam-roofing-visalia"')
src = src.replace('href="/spray-foam-roofing-tulare.html"', 'href="/spray-foam-roofing-tulare"')
src = src.replace('href="/spray-foam-roofing-hanford.html"', 'href="/spray-foam-roofing-hanford"')
src = src.replace('href="/spray-foam-roofing-merced.html"', 'href="/spray-foam-roofing-merced"')
src = src.replace('href="/spray-foam-roofing-bakersfield.html"', 'href="/spray-foam-roofing-bakersfield"')

# link FAQ answer 1 to lifespan guide
swap('foam roofs over 30 years old routinely test like new underneath. Details on our <a class="text-secondary underline" href="/spray-polyurethane-foam-roofing">SPF systems page</a>.',
     'foam roofs over 30 years old routinely test like new underneath. Full data in <a class="text-secondary underline" href="/how-long-does-spray-foam-roofing-last">our lifespan guide</a>.')

# ---- 13. about imgs: attrs
swap('<img class="w-full grayscale border-2 border-primary" alt="The Allstate Spray Foam Roofing crew in branded high-visibility gear in front of a company truck" src="/assets/crew.jpg"/>',
     '<img class="w-full grayscale border-2 border-primary" alt="The Allstate Spray Foam Roofing crew in branded high-visibility gear in front of a company truck" src="/assets/crew.jpg" width="512" height="286" loading="lazy" decoding="async"/>')
swap('<img class="w-full h-full object-cover grayscale" alt="Allstate service truck at a job site in the early days" src="/assets/truck.jpg"/>',
     '<img class="w-full h-full object-cover grayscale" alt="Allstate service truck at a job site in the early days" src="/assets/truck.jpg" width="1280" height="720" loading="lazy" decoding="async"/>')
swap('<img class="w-full h-full object-cover" alt="Allstate\'s modern wrapped truck and trailer rig with American flag graphics" src="/assets/truck-trailer.jpg"/>',
     '<img class="w-full h-full object-cover" alt="Allstate\'s modern wrapped truck and trailer rig with American flag graphics" src="/assets/truck-trailer.jpg" width="1200" height="529" loading="lazy" decoding="async"/>')

# ---- 14. process h4 -> h3
src = re.sub(r'<h4 class="font-headline-lg text-primary text-xl uppercase">(Assessment|Specification|Installation|Warranty)</h4>',
             r'<h3 class="font-headline-lg text-primary text-xl uppercase">\1</h3>', src)
# link installation guide from process section intro (append under grid)
swap('</div>\n</div>\n</section>\n<!-- Service Area -->',
     '</div>\n<p class="text-center mt-10"><a class="font-label-caps text-secondary uppercase tracking-widest underline" href="/spray-foam-roofing-installation">See the full installation process step by step →</a></p>\n</div>\n</section>\n<!-- Service Area -->')

# ---- 15. form: replace with shared FORM_BLOCK (email + city fields)
fstart = src.index('<form name="roof-assessment"')
fend = src.index("</form>") + len("</form>")
src = src[:fstart] + bp.FORM_BLOCK + src[fend:]

# ---- 16. footer replace (guides column, split cities, disambiguation) + sticky bar + FAB
fstart = src.index("<footer ")
fend = src.index("</footer>") + len("</footer>")
footer_only = bp.FOOTER.split("<footer ", 1)[1]
footer_only = "<footer " + footer_only  # includes call bar + FAB after </footer>
src = src[:fstart] + footer_only + src[fend:]

# ---- 17. commercial-page FAQ vs-tpo contextual link exists via footer; done.
open(path, "w").write(src)
print("patched index.html", len(orig), "->", len(src), "bytes")
