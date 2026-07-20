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


if __name__ == "__main__":
    build()
