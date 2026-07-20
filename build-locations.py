#!/usr/bin/env python3
"""Generate the service×area geo-page matrix: site/<area>/<service>.html + site/<area>/index.html hubs.
Content bodies come from content/<area>.json (written by writer agents); this script provides the
shell (from build-pages.py), schema, silo interlinks, sitemap entries, and netlify 301s.

Matrix: 8 areas × 4 services, EXCEPT fresno/foam-roof-repair (existing /foam-roof-repair-fresno
page keeps that term — hub links it instead; no internal cannibalization).
Old flat city pages 301 → /<area>/spray-foam-roofing."""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("bp", os.path.join(HERE, "build-pages.py"))
bp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bp)

SITE, BASE = bp.SITE, bp.BASE
CONTENT = os.path.join(HERE, "content")

AREAS = {
    "fresno":      dict(name="Fresno", county="Fresno County", drive="45 min north via CA-99",
                        satellites=["Clovis", "Sanger", "Selma", "Fowler", "Kerman", "Kingsburg"]),
    "clovis":      dict(name="Clovis", county="Fresno County", drive="55 min north via CA-99 and CA-168",
                        satellites=["Fresno", "Sanger", "Friant"]),
    "visalia":     dict(name="Visalia", county="Tulare County", drive="minutes from our shop",
                        satellites=["Exeter", "Farmersville", "Goshen", "Woodlake"]),
    "tulare":      dict(name="Tulare", county="Tulare County", drive="under 20 min from the yard",
                        satellites=["Tipton", "Pixley", "Lindsay", "Porterville"]),
    "hanford":     dict(name="Hanford", county="Kings County", drive="35 min west via CA-198",
                        satellites=["Lemoore", "Corcoran", "Avenal"]),
    "madera":      dict(name="Madera", county="Madera County", drive="60 min north via CA-99",
                        satellites=["Chowchilla", "Oakhurst", "Coarsegold"]),
    "merced":      dict(name="Merced", county="Merced County", drive="75 min north via CA-99",
                        satellites=["Atwater", "Livingston", "Los Banos"]),
    "bakersfield": dict(name="Bakersfield", county="Kern County", drive="90 min south via CA-99",
                        satellites=["Delano", "Shafter", "Wasco", "Arvin"]),
}

SERVICES = {
    "spray-foam-roofing":    dict(name="Spray Foam Roofing", hero_img="service-spf-roof.jpg",
                                  parent="/spray-polyurethane-foam-roofing"),
    "silicone-roof-coating": dict(name="Silicone Roof Coating", hero_img="service-silicone.jpg",
                                  parent="/spray-polyurethane-foam-roofing"),
    "foam-roof-repair":      dict(name="Foam Roof Repair", hero_img="service-silicone.jpg",
                                  parent="/foam-roof-repair-fresno"),
    "commercial-insulation": dict(name="Commercial Insulation", hero_img="service-insulation.jpg",
                                  parent="/spray-polyurethane-foam-roofing"),
}

SKIP = {("fresno", "foam-roof-repair")}  # existing /foam-roof-repair-fresno owns this

# Old flat city pages → new matrix URLs (301s appended to netlify.toml by rebuild_netlify()).
LEGACY_301 = {
    "/spray-foam-roofing-visalia": "/visalia/spray-foam-roofing",
    "/spray-foam-roofing-tulare": "/tulare/spray-foam-roofing",
    "/spray-foam-roofing-hanford": "/hanford/spray-foam-roofing",
    "/spray-foam-roofing-merced": "/merced/spray-foam-roofing",
    "/spray-foam-roofing-bakersfield": "/bakersfield/spray-foam-roofing",
}


def cells():
    for a in AREAS:
        for s in SERVICES:
            if (a, s) not in SKIP:
                yield a, s


def area_schema(a, extra_city=None):
    ar = AREAS[a]
    out = [{"@type": "City", "name": ar["name"]}, {"@type": "AdministrativeArea", "name": ar["county"]}]
    return out


def svc_page(a, s, c):
    ar, sv = AREAS[a], SERVICES[s]
    slug = f"{a}/{s}"
    title = c.get("title") or f"{sv['name']} {ar['name']}, CA | Allstate Spray Foam"
    schema = ('<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org", "@type": "Service",
        "name": f"{sv['name']} — {ar['name']}, CA",
        "provider": {"@id": BASE + "/#contractor"},
        "areaServed": area_schema(a), "url": f"{BASE}/{slug}",
    }) + "\n</script>\n"
        + '<script type="application/ld+json">\n' + json.dumps({
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": ar["name"], "item": f"{BASE}/{a}/"},
                {"@type": "ListItem", "position": 3, "name": sv["name"], "item": f"{BASE}/{slug}"},
            ]}) + "\n</script>")
    faqs = [(q, ans, None) for q, ans in c.get("faqs", [])]
    faq_schema, faq_html = bp.faq_blocks({"faqs": faqs})
    # silo links: hub + sibling services + same service in 2 neighbor areas
    sibs = [f'<a class="text-secondary underline" href="/{a}/{s2}">{SERVICES[s2]["name"]} in {ar["name"]}</a>'
            for s2 in SERVICES if s2 != s and (a, s2) not in SKIP]
    order = list(AREAS)
    i = order.index(a)
    neighbors = [order[(i + 1) % len(order)], order[(i - 1) % len(order)]]
    nb = [f'<a class="text-secondary underline" href="/{n}/{s}">{SERVICES[s]["name"]} in {AREAS[n]["name"]}</a>'
          for n in neighbors if (n, s) not in SKIP]
    silo = ('\n<h2>More From Allstate in ' + ar["name"] + '</h2>\n<p>Also serving ' + ar["name"]
            + ': ' + ' · '.join(sibs) + '. See all ' + ar["name"] + ' services on the '
            + f'<a class="text-secondary underline" href="/{a}/">{ar["name"]} service hub</a>, '
            + f'or read our full <a class="text-secondary underline" href="{sv["parent"]}">'
            + sv["name"].lower() + ' guide</a>.'
            + (' Nearby: ' + ' · '.join(nb) + '.' if nb else '') + '</p>')
    breadcrumb_html = (f'<p class="font-label-caps text-on-primary-container text-[11px] uppercase">'
                       f'<a class="hover:text-secondary-fixed" href="/">Home</a> / '
                       f'<a class="hover:text-secondary-fixed" href="/{a}/">{ar["name"]}</a> / {sv["name"]}</p>\n')
    html = bp.TEMPLATE.format(
        base=BASE, head_shared=bp.HEAD_SHARED, header=bp.HEADER,
        footer=bp.FOOTER.replace("{form_block}", bp.FORM_BLOCK).replace("{cta_area}", f'anywhere in {ar["county"]}'),
        slug=slug, title=title, meta_desc=c["meta_desc"], h1=c["h1"], subhead=c["subhead"],
        hero_img=sv["hero_img"], schema_block=schema, faq_schema=faq_schema,
        faq_html=faq_html, body=c["body_html"] + silo, updated_line=breadcrumb_html)
    out = os.path.join(SITE, a, s + ".html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(html)
    words = len(__import__("re").sub(r"<[^>]+>", " ", c["body_html"]).split())
    print(f"wrote {out} ({words} body words)")
    return words


def hub_page(a, c):
    ar = AREAS[a]
    slug = f"{a}/"
    cards = "\n".join(
        f'<div class="bg-surface-container-lowest industrial-card-border p-8 space-y-3">'
        f'<h3 class="font-headline-lg text-primary text-2xl uppercase">{SERVICES[s]["name"]}</h3>'
        f'<p class="text-on-surface-variant">{c["service_teasers"].get(s, "")}</p>'
        f'<a href="{("/foam-roof-repair-fresno" if (a, s) in SKIP else f"/{a}/{s}")}" class="font-label-caps text-secondary uppercase tracking-widest">'
        f'{SERVICES[s]["name"]} in {ar["name"]} →</a></div>'
        for s in SERVICES)
    schema = ('<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org", "@type": "Service",
        "name": f"Commercial Roofing & Insulation Services — {ar['name']}, CA",
        "provider": {"@id": BASE + "/#contractor"}, "areaServed": area_schema(a),
        "url": f"{BASE}/{slug}"}) + "\n</script>\n"
        + '<script type="application/ld+json">\n' + json.dumps({
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": ar["name"], "item": f"{BASE}/{a}/"},
            ]}) + "\n</script>")
    body = (c["hub_intro_html"]
            + '\n<h2>Our Services in ' + ar["name"] + '</h2>\n'
            + '<div class="grid md:grid-cols-2 gap-6">' + cards + '</div>'
            + '\n<h2>Service Area</h2>\n<p>From ' + ar["name"] + ' we cover all of ' + ar["county"]
            + ' including ' + ', '.join(ar["satellites"]) + '. Crews dispatch from our Tulare County shop — '
            + ar["name"] + ' is ' + ar["drive"] + '.</p>')
    html = bp.TEMPLATE.format(
        base=BASE, head_shared=bp.HEAD_SHARED, header=bp.HEADER,
        footer=bp.FOOTER.replace("{form_block}", bp.FORM_BLOCK).replace("{cta_area}", f'anywhere in {ar["county"]}'),
        slug=slug, title=c.get("hub_title") or f"Commercial Roofing & Insulation {ar['name']}, CA | Allstate",
        meta_desc=c["hub_meta_desc"], h1=c["hub_h1"], subhead=c["hub_subhead"],
        hero_img="hero-aerial.jpg", schema_block=schema, faq_schema="", faq_html="",
        body=body, updated_line="")
    out = os.path.join(SITE, a, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(html)
    print("wrote", out)


def rebuild_netlify():
    """Regenerate the redirects portion: original 12 .html 301s + matrix .html 301s + legacy city 301s."""
    path = os.path.join(SITE, "netlify.toml")
    head = open(path).read().split("# Canonical URL scheme")[0].rstrip()
    lines = [head, "", "# Canonical URL scheme: extensionless (generated by build-locations.py)"]
    flat = ["spray-polyurethane-foam-roofing", "foam-roof-repair-fresno", "commercial-roofing-fresno",
            "spray-foam-roofing-cost", "how-long-does-spray-foam-roofing-last",
            "spray-foam-roofing-installation", "spray-foam-vs-tpo-roofing"]
    for p in flat:
        lines += [f'[[redirects]]\n  from = "/{p}.html"\n  to = "/{p}"\n  status = 301\n  force = true']
    for a, s in cells():
        lines += [f'[[redirects]]\n  from = "/{a}/{s}.html"\n  to = "/{a}/{s}"\n  status = 301\n  force = true']
    for old, new in LEGACY_301.items():
        lines += [f'[[redirects]]\n  from = "{old}"\n  to = "{new}"\n  status = 301\n  force = true',
                  f'[[redirects]]\n  from = "{old}.html"\n  to = "{new}"\n  status = 301\n  force = true']
    open(path, "w").write("\n".join(lines) + "\n")
    print("rebuilt netlify.toml with", sum(1 for _ in cells()) + len(flat) + 2 * len(LEGACY_301), "redirects")


def rebuild_sitemap():
    path = os.path.join(SITE, "sitemap.xml")
    urls = [("", "1.0"), ("spray-polyurethane-foam-roofing", "0.9"), ("foam-roof-repair-fresno", "0.9"),
            ("commercial-roofing-fresno", "0.9"), ("spray-foam-roofing-cost", "0.8"),
            ("how-long-does-spray-foam-roofing-last", "0.7"), ("spray-foam-roofing-installation", "0.7"),
            ("spray-foam-vs-tpo-roofing", "0.7")]
    urls += [(f"{a}/", "0.8") for a in AREAS]
    urls += [(f"{a}/{s}", "0.8") for a, s in cells()]
    body = "\n".join(
        f"  <url>\n    <loc>{BASE}/{u}</loc>\n    <lastmod>2026-07-20</lastmod>\n"
        f"    <changefreq>monthly</changefreq>\n    <priority>{p}</priority>\n  </url>" for u, p in urls)
    open(path, "w").write('<?xml version="1.0" encoding="UTF-8"?>\n'
                          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "\n</urlset>\n")
    print("rebuilt sitemap.xml:", len(urls), "urls")


def build():
    total = short = 0
    for a in AREAS:
        cf = os.path.join(CONTENT, a + ".json")
        if not os.path.exists(cf):
            print("SKIP (no content):", a)
            continue
        c = json.load(open(cf))
        hub_page(a, c)
        for s in SERVICES:
            if (a, s) in SKIP or s not in c["services"]:
                continue
            w = svc_page(a, s, c["services"][s])
            total += 1
            if w < 2800:
                short += 1
                print("  !! UNDER 2800 WORDS:", a, s, w)
    rebuild_netlify()
    rebuild_sitemap()
    print(f"done: {total} service pages, {short} under length")


# ====================================================================
# VISUAL-RHYTHM OVERRIDES (2026-07-20, per Mike: pages too light/monotone)
# Band-based assembly + validated brand charts (#3b5a9a/#bb001b, dataviz six-checks PASS).
# These redefine svc_page/hub_page; the originals above are kept for reference.
# ====================================================================
import re as _re

CHART_BLUE, CHART_RED = "#3b5a9a", "#bb001b"


def _bar_path(x, y, w, h, r=4):
    return (f"M{x},{y + h} L{x},{y + r} Q{x},{y} {x + r},{y} L{x + w - r},{y} "
            f"Q{x + w},{y} {x + w},{y + r} L{x + w},{y + h} Z")


def _hbar_path(x, y, w, h, r=4):
    return (f"M{x},{y} L{x + w - r},{y} Q{x + w},{y} {x + w},{y + r} L{x + w},{y + h - r} "
            f"Q{x + w},{y + h} {x + w - r},{y + h} L{x},{y + h} Z")


def chart_lifecycle():
    groups = [("Year 0", 6, 7), ("Year 20", 9, 16), ("Year 40", 12, 25)]
    W, H, TOP, BOT, LEFT = 640, 300, 24, 40, 40
    plot_h = H - TOP - BOT
    vmax = 28.0
    bars, labels, gx = [], [], []
    gw = (W - LEFT - 20) / len(groups)
    for i, (name, spf, tpo) in enumerate(groups):
        cx = LEFT + gw * i + gw / 2
        for j, (val, col, series) in enumerate(((spf, CHART_BLUE, "SPF + recoats"), (tpo, CHART_RED, "TPO replacements"))):
            bw = 44
            x = cx - bw - 1 if j == 0 else cx + 1
            h = plot_h * val / vmax
            y = TOP + plot_h - h
            bars.append(f'<path d="{_bar_path(x, y, bw, h)}" fill="{col}"><title>{series}, {name}: ${val}/sq ft cumulative</title></path>')
            labels.append(f'<text x="{x + bw / 2}" y="{y - 6}" text-anchor="middle" font-size="13" font-weight="600" fill="#101c2c">${val}</text>')
        gx.append(f'<text x="{cx}" y="{H - 14}" text-anchor="middle" font-size="12" fill="#44464e">{name}</text>')
    grid = "".join(f'<line x1="{LEFT}" x2="{W - 20}" y1="{TOP + plot_h - plot_h * v / vmax}" y2="{TOP + plot_h - plot_h * v / vmax}" stroke="#c5c6cf" stroke-width="1"/>'
                   f'<text x="{LEFT - 6}" y="{TOP + plot_h - plot_h * v / vmax + 4}" text-anchor="end" font-size="11" fill="#75777f">${v}</text>'
                   for v in (10, 20))
    base = f'<line x1="{LEFT}" x2="{W - 20}" y1="{TOP + plot_h}" y2="{TOP + plot_h}" stroke="#75777f" stroke-width="1"/>'
    legend = (f'<div class="flex gap-6 mb-2 font-label-caps text-[11px] uppercase text-on-surface-variant">'
              f'<span class="flex items-center gap-2"><span style="background:{CHART_BLUE};width:14px;height:14px;display:inline-block;border-radius:3px"></span>SPF + recoats</span>'
              f'<span class="flex items-center gap-2"><span style="background:{CHART_RED};width:14px;height:14px;display:inline-block;border-radius:3px"></span>TPO replacements</span></div>')
    return (f'<figure class="chart-fig my-10"><h3>Cumulative Cost of Ownership: Typical $/Sq Ft</h3>{legend}'
            f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Cumulative cost per square foot over 40 years: SPF reaches about 12 dollars with recoats while TPO reaches about 25 dollars with replacements">'
            f"{grid}{''.join(bars)}{''.join(labels)}{''.join(gx)}{base}</svg>"
            f'<figcaption class="chart-note">Typical mid-range figures for illustration: SPF ~$6/sq ft installed plus ~$3 recoats on a 15-20 year cycle; '
            f'TPO ~$7/sq ft installed plus tear-off and full replacement each ~20-year life. Your written bid prices your actual roof.</figcaption></figure>')


def chart_rvalue():
    rows = [("SPF closed-cell foam", 6.5, CHART_RED), ("Polyiso board", 5.7, CHART_BLUE),
            ("XPS board", 5.0, CHART_BLUE), ("EPS board", 3.8, CHART_BLUE), ("Fiberglass batt", 3.2, CHART_BLUE)]
    W, LEFT, RH, GAP, TOP = 640, 170, 34, 14, 16
    H = TOP + len(rows) * (RH + GAP) + 24
    vmax = 7.0
    parts = []
    for i, (name, val, col) in enumerate(rows):
        y = TOP + i * (RH + GAP)
        w = (W - LEFT - 60) * val / vmax
        parts.append(f'<text x="{LEFT - 8}" y="{y + RH / 2 + 4}" text-anchor="end" font-size="12" fill="#44464e">{name}</text>')
        parts.append(f'<path d="{_hbar_path(LEFT, y, w, RH)}" fill="{col}"><title>{name}: R-{val} per inch</title></path>')
        parts.append(f'<text x="{LEFT + w + 8}" y="{y + RH / 2 + 4}" font-size="13" font-weight="600" fill="#101c2c">R-{val}</text>')
    base = f'<line x1="{LEFT}" x2="{LEFT}" y1="{TOP - 4}" y2="{H - 20}" stroke="#75777f" stroke-width="1"/>'
    return (f'<figure class="chart-fig my-10"><h3>Insulation R-Value Per Inch</h3>'
            f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="R-value per inch by material: SPF closed-cell foam leads at R-6.5">'
            f"{''.join(parts)}{base}</svg>"
            f'<figcaption class="chart-note">Nominal R-value per inch of thickness, typical published values. Closed-cell SPF leads every common commercial insulation.</figcaption></figure>')


STAT_TILES = (
    '<div class="grid grid-cols-2 lg:grid-cols-4 gap-6 py-4 text-center">'
    '<div><div class="font-headline-lg text-on-primary text-3xl">R-6.5</div><div class="font-label-caps text-secondary-fixed text-[10px] uppercase">Per Inch, Highest Available</div></div>'
    '<div><div class="font-headline-lg text-on-primary text-3xl">~85%</div><div class="font-label-caps text-secondary-fixed text-[10px] uppercase">Solar Energy Reflected</div></div>'
    '<div><div class="font-headline-lg text-on-primary text-3xl">10-20 yr</div><div class="font-label-caps text-secondary-fixed text-[10px] uppercase">Renewable Recoat Cycle</div></div>'
    '<div><div class="font-headline-lg text-on-primary text-3xl">48 hr</div><div class="font-label-caps text-secondary-fixed text-[10px] uppercase">Written Bid After Assessment</div></div>'
    '</div>')

SERVICE_PHOTO = {
    "spray-foam-roofing": ("service-spf-roof.jpg", "Fresh spray polyurethane foam on a commercial low-slope roof"),
    "silicone-roof-coating": ("service-silicone.jpg", "Spray-applying bright white silicone coating over a commercial roof"),
    "foam-roof-repair": ("foam-macro.jpg", "Closed-cell spray foam up close: dense, waterproof, repairable"),
    "commercial-insulation": ("service-insulation.jpg", "Spray foam insulation going into a commercial warehouse ceiling"),
}

_CONTENT_ANCHOR = ('<!-- Content -->\n<section class="py-20 bg-background">\n'
                   '<div class="container max-w-4xl mx-auto px-margin-mobile md:px-gutter prose-band">\n'
                   '{body}\n{faq_html}\n</div>\n</section>')


def _split_sections(body):
    parts = _re.split(r"(?=<h2>)", body)
    if parts and not parts[0].strip():
        parts = parts[1:]
    if len(parts) >= 2 and not parts[0].startswith("<h2>"):
        parts[1] = parts[0] + parts[1]
        parts = parts[1:]
    return parts


def _band(inner, style, dark=False):
    prose = "prose-dark" if dark else "prose-band"
    return (f'<section class="py-16 {style}">'
            f'<div class="container max-w-4xl mx-auto px-margin-mobile md:px-gutter {prose}">{inner}</div></section>')


def svc_page(a, s, c):
    ar, sv = AREAS[a], SERVICES[s]
    slug = f"{a}/{s}"
    title = c.get("title") or f"{sv['name']} {ar['name']}, CA | Allstate Spray Foam"
    schema = ('<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org", "@type": "Service",
        "name": f"{sv['name']} — {ar['name']}, CA",
        "provider": {"@id": BASE + "/#contractor"},
        "areaServed": area_schema(a), "url": f"{BASE}/{slug}",
    }) + "\n</script>\n"
        + '<script type="application/ld+json">\n' + json.dumps({
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": ar["name"], "item": f"{BASE}/{a}/"},
                {"@type": "ListItem", "position": 3, "name": sv["name"], "item": f"{BASE}/{slug}"},
            ]}) + "\n</script>")
    faqs = [(q, ans, None) for q, ans in c.get("faqs", [])]
    faq_schema, faq_html = bp.faq_blocks({"faqs": faqs})
    sibs = [f'<a class="text-secondary underline" href="/{a}/{s2}">{SERVICES[s2]["name"]} in {ar["name"]}</a>'
            for s2 in SERVICES if s2 != s and (a, s2) not in SKIP]
    order = list(AREAS)
    i = order.index(a)
    neighbors = [order[(i + 1) % len(order)], order[(i - 1) % len(order)]]
    nb = [f'<a class="text-secondary underline" href="/{n}/{s}">{SERVICES[s]["name"]} in {AREAS[n]["name"]}</a>'
          for n in neighbors if (n, s) not in SKIP]
    silo = ('<h2>More From Allstate in ' + ar["name"] + '</h2><p>Also serving ' + ar["name"]
            + ': ' + ' · '.join(sibs) + '. See all ' + ar["name"] + ' services on the '
            + f'<a class="text-secondary underline" href="/{a}/">{ar["name"]} service hub</a>, '
            + f'or read our full <a class="text-secondary underline" href="{sv["parent"]}">'
            + sv["name"].lower() + ' guide</a>.'
            + (' Nearby: ' + ' · '.join(nb) + '.' if nb else '') + '</p>')

    secs = _split_sections(c["body_html"])
    n = len(secs)
    q = max(1, n // 4)
    g1, g2, g3, g4 = secs[:q + 1], secs[q + 1:2 * q + 1], secs[2 * q + 1:3 * q + 1], secs[3 * q + 1:]
    chart = chart_rvalue() if s == "commercial-insulation" else chart_lifecycle()
    photo_f, photo_alt = SERVICE_PHOTO[s]
    photo = (f'<figure class="my-4"><img src="/assets/{photo_f}" alt="{photo_alt}" '
             f'class="w-full border-2 border-primary" loading="lazy" decoding="async" width="900" height="600"/>'
             f'<figcaption class="font-label-caps text-on-surface-variant text-[10px] uppercase mt-2 tracking-widest">{photo_alt}</figcaption></figure>')
    diagram = ('<figure class="my-4"><img src="/assets/spf-roof-cross-section.webp" '
               'alt="Labeled cross-section diagram of a spray polyurethane foam roof system" '
               'class="w-full border-2 border-primary" loading="lazy" decoding="async" width="1200" height="900"/>'
               '<figcaption class="font-label-caps text-on-surface-variant text-[10px] uppercase mt-2 tracking-widest">The layered SPF roof system, deck to coating</figcaption></figure>') \
        if s == "spray-foam-roofing" else ""
    body = (
        _band("".join(g1), "bg-background")
        + '<div class="rwb-stripe"></div>'
        + _band(STAT_TILES + "".join(g2), "bg-primary-container", dark=True)
        + _band(chart + "".join(g3), "bg-background")
        + _band(photo + "".join(g4[:max(0, len(g4) - 1)]), "bg-surface-variant")
        + _band(diagram + "".join(g4[max(0, len(g4) - 1):]) + silo, "bg-background")
        + (_band(faq_html, "bg-surface-container-low") if faq_html else "")
    )
    breadcrumb_html = (f'<p class="font-label-caps text-on-primary-container text-[11px] uppercase">'
                       f'<a class="hover:text-secondary-fixed" href="/">Home</a> / '
                       f'<a class="hover:text-secondary-fixed" href="/{a}/">{ar["name"]}</a> / {sv["name"]}</p>\n')
    tpl = bp.TEMPLATE.replace(_CONTENT_ANCHOR, '<!-- Content bands -->\n{body}')
    assert '<!-- Content bands -->' in tpl, "content anchor not matched in bp.TEMPLATE"
    html = tpl.format(
        base=BASE, head_shared=bp.HEAD_SHARED, header=bp.HEADER,
        footer=bp.FOOTER.replace("{form_block}", bp.FORM_BLOCK).replace("{cta_area}", f'anywhere in {ar["county"]}'),
        slug=slug, title=title, meta_desc=c["meta_desc"], h1=c["h1"], subhead=c["subhead"],
        hero_img=sv["hero_img"], schema_block=schema, faq_schema=faq_schema,
        body=body, updated_line=breadcrumb_html)
    out = os.path.join(SITE, a, s + ".html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(html)
    words = len(_re.sub(r"<[^>]+>", " ", c["body_html"]).split())
    print(f"wrote {out} ({words} body words, banded)")
    return words


def hub_page(a, c):
    ar = AREAS[a]
    slug = f"{a}/"
    cards = "\n".join(
        f'<div class="bg-surface-container-lowest industrial-card-border p-8 space-y-3">'
        f'<h3 class="font-headline-lg text-primary text-2xl uppercase">{SERVICES[s]["name"]}</h3>'
        f'<p class="text-on-surface-variant">{c["service_teasers"].get(s, "")}</p>'
        f'<a href="{("/foam-roof-repair-fresno" if (a, s) in SKIP else f"/{a}/{s}")}" class="font-label-caps text-secondary uppercase tracking-widest">'
        f'{SERVICES[s]["name"]} in {ar["name"]} →</a></div>'
        for s in SERVICES)
    schema = ('<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org", "@type": "Service",
        "name": f"Commercial Roofing & Insulation Services — {ar['name']}, CA",
        "provider": {"@id": BASE + "/#contractor"}, "areaServed": area_schema(a),
        "url": f"{BASE}/{slug}"}) + "\n</script>\n"
        + '<script type="application/ld+json">\n' + json.dumps({
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": ar["name"], "item": f"{BASE}/{a}/"},
            ]}) + "\n</script>")
    photo = ('<figure class="my-4"><img src="/assets/truck-trailer.jpg" alt="Allstate wrapped service truck and equipment trailer" '
             'class="w-full border-2 border-primary" loading="lazy" decoding="async" width="1200" height="529"/></figure>')
    coverage = ('<h2>Service Area</h2><p>From ' + ar["name"] + ' we cover all of ' + ar["county"]
                + ' including ' + ', '.join(ar["satellites"]) + '. Crews dispatch from our Tulare County shop — '
                + ar["name"] + ' is ' + ar["drive"] + '.</p>')
    body = (
        _band(c["hub_intro_html"], "bg-background")
        + '<div class="rwb-stripe"></div>'
        + _band(STAT_TILES, "bg-primary-container", dark=True)
        + _band('<h2>Our Services in ' + ar["name"] + '</h2><div class="grid md:grid-cols-2 gap-6">' + cards + '</div>', "bg-background")
        + _band(photo + coverage, "bg-surface-variant")
    )
    tpl = bp.TEMPLATE.replace(_CONTENT_ANCHOR, '<!-- Content bands -->\n{body}')
    html = tpl.format(
        base=BASE, head_shared=bp.HEAD_SHARED, header=bp.HEADER,
        footer=bp.FOOTER.replace("{form_block}", bp.FORM_BLOCK).replace("{cta_area}", f'anywhere in {ar["county"]}'),
        slug=slug, title=c.get("hub_title") or f"Commercial Roofing & Insulation {ar['name']}, CA | Allstate",
        meta_desc=c["hub_meta_desc"], h1=c["hub_h1"], subhead=c["hub_subhead"],
        hero_img="hero-aerial.jpg", schema_block=schema, faq_schema="",
        body=body, updated_line="")
    out = os.path.join(SITE, a, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(html)
    print("wrote", out, "(banded hub)")


if __name__ == "__main__":
    build()
