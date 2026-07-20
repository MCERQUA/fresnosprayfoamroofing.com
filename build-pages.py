#!/usr/bin/env python3
"""Generate interior pages for fresnosprayfoamroofing.com in the site design shell.
Each page = dict(slug, title, meta_desc, h1, subhead, schema_name, body_html, area, schema_type, faqs).
Rerun any time; overwrites site/<slug>.html. Implements ai/seo-fix-workorders-2026-07-20.md:
extensionless URLs, compiled CSS (assets/site.css — rebuild with build-css.sh after class changes),
form on every page, per-city areaServed, Article schema for guides, truth-pass wording,
city local-proof blocks + FAQs, header nav menu, sticky mobile call bar, contact FAB."""
import json
import os

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
BASE = "https://fresnosprayfoamroofing.com"

HEAD_SHARED = """<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Archivo+Narrow:wght@400;700&amp;family=Hanken+Grotesk:wght@400;500;600&amp;family=JetBrains+Mono:wght@600&amp;family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="/assets/site.css"/>
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png"/>
<link rel="icon" type="image/png" sizes="192x192" href="/assets/favicon-192.png"/>
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png"/>"""

NAV = """<nav class="hidden lg:flex items-center gap-1 font-label-caps uppercase text-[11px] text-on-primary" aria-label="Main">
<div class="relative group">
<a href="/spray-polyurethane-foam-roofing" class="px-3 py-2 hover:text-secondary-fixed flex items-center gap-1">Services <span class="material-symbols-outlined text-sm">expand_more</span></a>
<div class="absolute left-0 top-full hidden group-hover:block group-focus-within:block bg-primary border border-on-primary/10 min-w-[240px] py-2 shadow-xl">
<a href="/spray-polyurethane-foam-roofing" class="block px-5 py-3 hover:bg-secondary hover:text-on-secondary">SPF Roofing Systems</a>
<a href="/foam-roof-repair-fresno" class="block px-5 py-3 hover:bg-secondary hover:text-on-secondary">Foam Roof Repair</a>
<a href="/commercial-roofing-fresno" class="block px-5 py-3 hover:bg-secondary hover:text-on-secondary">Commercial Roofing</a>
<a href="/spray-foam-roofing-cost" class="block px-5 py-3 hover:bg-secondary hover:text-on-secondary">Cost Guide</a>
</div>
</div>
<div class="relative group">
<a href="/commercial-roofing-fresno" class="px-3 py-2 hover:text-secondary-fixed flex items-center gap-1">Service Areas <span class="material-symbols-outlined text-sm">expand_more</span></a>
<div class="absolute left-0 top-full hidden group-hover:block group-focus-within:block bg-primary border border-on-primary/10 min-w-[240px] py-2 shadow-xl">
<a href="/fresno/" class="block px-5 py-3 hover:bg-secondary hover:text-on-secondary">Fresno</a>
<a href="/clovis/" class="block px-5 py-3 hover:bg-secondary hover:text-on-secondary">Clovis</a>
<a href="/visalia/" class="block px-5 py-3 hover:bg-secondary hover:text-on-secondary">Visalia</a>
<a href="/tulare/" class="block px-5 py-3 hover:bg-secondary hover:text-on-secondary">Tulare</a>
<a href="/hanford/" class="block px-5 py-3 hover:bg-secondary hover:text-on-secondary">Hanford</a>
<a href="/madera/" class="block px-5 py-3 hover:bg-secondary hover:text-on-secondary">Madera</a>
<a href="/merced/" class="block px-5 py-3 hover:bg-secondary hover:text-on-secondary">Merced</a>
<a href="/bakersfield/" class="block px-5 py-3 hover:bg-secondary hover:text-on-secondary">Bakersfield</a>
</div>
</div>
<div class="relative group">
<a href="/how-long-does-spray-foam-roofing-last" class="px-3 py-2 hover:text-secondary-fixed flex items-center gap-1">Guides <span class="material-symbols-outlined text-sm">expand_more</span></a>
<div class="absolute left-0 top-full hidden group-hover:block group-focus-within:block bg-primary border border-on-primary/10 min-w-[260px] py-2 shadow-xl">
<a href="/how-long-does-spray-foam-roofing-last" class="block px-5 py-3 hover:bg-secondary hover:text-on-secondary">Foam Roof Lifespan</a>
<a href="/spray-foam-roofing-installation" class="block px-5 py-3 hover:bg-secondary hover:text-on-secondary">Installation Step by Step</a>
<a href="/spray-foam-vs-tpo-roofing" class="block px-5 py-3 hover:bg-secondary hover:text-on-secondary">Spray Foam vs TPO</a>
</div>
</div>
</nav>"""

MOBILE_MENU = """<button id="menu-btn" class="lg:hidden text-on-primary p-3" aria-label="Open menu" onclick="document.getElementById('mobile-menu').classList.toggle('hidden')">
<span class="material-symbols-outlined text-3xl">menu</span>
</button>
<div id="mobile-menu" class="hidden lg:hidden absolute top-full inset-x-0 bg-primary border-t border-on-primary/10 z-50 pb-4">
<p class="px-6 pt-4 pb-2 font-label-caps text-secondary-fixed text-[10px] uppercase">Services</p>
<a href="/spray-polyurethane-foam-roofing" class="block px-6 py-3 text-on-primary font-label-caps uppercase text-[12px]">SPF Roofing Systems</a>
<a href="/foam-roof-repair-fresno" class="block px-6 py-3 text-on-primary font-label-caps uppercase text-[12px]">Foam Roof Repair</a>
<a href="/commercial-roofing-fresno" class="block px-6 py-3 text-on-primary font-label-caps uppercase text-[12px]">Commercial Roofing</a>
<a href="/spray-foam-roofing-cost" class="block px-6 py-3 text-on-primary font-label-caps uppercase text-[12px]">Cost Guide</a>
<p class="px-6 pt-4 pb-2 font-label-caps text-secondary-fixed text-[10px] uppercase">Service Areas</p>
<a href="/fresno/" class="block px-6 py-3 text-on-primary font-label-caps uppercase text-[12px]">Fresno</a>
<a href="/clovis/" class="block px-6 py-3 text-on-primary font-label-caps uppercase text-[12px]">Clovis</a>
<a href="/visalia/" class="block px-6 py-3 text-on-primary font-label-caps uppercase text-[12px]">Visalia</a>
<a href="/tulare/" class="block px-6 py-3 text-on-primary font-label-caps uppercase text-[12px]">Tulare</a>
<a href="/hanford/" class="block px-6 py-3 text-on-primary font-label-caps uppercase text-[12px]">Hanford</a>
<a href="/madera/" class="block px-6 py-3 text-on-primary font-label-caps uppercase text-[12px]">Madera</a>
<a href="/merced/" class="block px-6 py-3 text-on-primary font-label-caps uppercase text-[12px]">Merced</a>
<a href="/bakersfield/" class="block px-6 py-3 text-on-primary font-label-caps uppercase text-[12px]">Bakersfield</a>
<p class="px-6 pt-4 pb-2 font-label-caps text-secondary-fixed text-[10px] uppercase">Guides</p>
<a href="/how-long-does-spray-foam-roofing-last" class="block px-6 py-3 text-on-primary font-label-caps uppercase text-[12px]">Foam Roof Lifespan</a>
<a href="/spray-foam-roofing-installation" class="block px-6 py-3 text-on-primary font-label-caps uppercase text-[12px]">Installation Step by Step</a>
<a href="/spray-foam-vs-tpo-roofing" class="block px-6 py-3 text-on-primary font-label-caps uppercase text-[12px]">Spray Foam vs TPO</a>
</div>"""

HEADER = """<header class="bg-primary sticky top-0 z-50">
<div class="relative flex justify-between items-center w-full px-margin-mobile md:px-gutter max-w-container-max mx-auto h-20">
<div class="flex items-center gap-4">
<a href="/"><img alt="Allstate Spray Foam Roofing logo" class="h-14 w-auto" src="/assets/logo-200.png" width="215" height="200"/></a>
<a href="/" class="hidden xl:block font-headline-lg text-on-primary tracking-tighter uppercase text-xl">Allstate Spray Foam Roofing</a>
</div>
""" + NAV + """
<div class="flex items-center gap-2 md:gap-4">
<a class="flex items-center gap-2 text-on-primary group p-3" href="tel:5597399519">
<span class="material-symbols-outlined text-secondary" style="font-variation-settings:'FILL' 1;">phone_in_talk</span>
<span class="hidden sm:inline font-headline-lg text-[22px] group-hover:text-secondary-fixed transition-colors">(559) 739-9519</span>
</a>
<a href="#assessment" class="hidden md:inline-block bg-secondary text-on-secondary font-label-caps px-6 py-3 uppercase tracking-widest hover:bg-on-secondary-fixed-variant transition-all duration-300">Free Roof Assessment</a>
""" + MOBILE_MENU + """
</div>
</div>
<div class="rwb-stripe"></div>
</header>"""

# Contact FAB — desktop bottom-right circle, expands on hover/focus (mobile has the call bar).
CONTACT_FAB = """<div class="hidden md:block fixed bottom-8 right-8 z-50 group">
<div class="absolute bottom-full right-0 mb-3 hidden group-hover:flex group-focus-within:flex flex-col gap-2 items-end">
<a href="tel:5597399519" class="flex items-center gap-3 bg-primary text-on-primary font-label-caps uppercase text-[11px] tracking-widest pl-5 pr-4 py-3 shadow-xl border border-on-primary/10 hover:bg-secondary hover:text-on-secondary whitespace-nowrap">Call (559) 739-9519 <span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1;">call</span></a>
<a href="#assessment" class="flex items-center gap-3 bg-primary text-on-primary font-label-caps uppercase text-[11px] tracking-widest pl-5 pr-4 py-3 shadow-xl border border-on-primary/10 hover:bg-secondary hover:text-on-secondary whitespace-nowrap">Free Assessment <span class="material-symbols-outlined">assignment</span></a>
<a href="mailto:info@allstatesprayfoam.com" class="flex items-center gap-3 bg-primary text-on-primary font-label-caps uppercase text-[11px] tracking-widest pl-5 pr-4 py-3 shadow-xl border border-on-primary/10 hover:bg-secondary hover:text-on-secondary whitespace-nowrap">Email Us <span class="material-symbols-outlined">mail</span></a>
</div>
<button aria-label="Contact options" class="w-16 h-16 rounded-full bg-secondary text-on-secondary shadow-2xl flex items-center justify-center hover:scale-110 transition-transform">
<span class="material-symbols-outlined text-3xl" style="font-variation-settings:'FILL' 1;">contact_phone</span>
</button>
</div>"""

FORM_BLOCK = """<form name="roof-assessment" method="POST" action="/thanks.html" data-netlify="true" netlify-honeypot="bot-field" class="grid md:grid-cols-2 gap-6 text-left">
<input type="hidden" name="form-name" value="roof-assessment"/>
<p class="hidden"><label>Don't fill this out: <input name="bot-field"/></label></p>
<div class="space-y-2">
<label for="f-name" class="font-label-caps text-on-primary-container text-[10px] uppercase block">Full Name</label>
<input id="f-name" name="name" required autocomplete="name" class="w-full bg-primary border-2 border-on-primary-container/30 text-on-primary px-4 py-3 focus:border-secondary outline-none transition-colors" type="text"/>
</div>
<div class="space-y-2">
<label for="f-email" class="font-label-caps text-on-primary-container text-[10px] uppercase block">Email</label>
<input id="f-email" name="email" required autocomplete="email" class="w-full bg-primary border-2 border-on-primary-container/30 text-on-primary px-4 py-3 focus:border-secondary outline-none transition-colors" type="email"/>
</div>
<div class="space-y-2">
<label for="f-phone" class="font-label-caps text-on-primary-container text-[10px] uppercase block">Phone Number</label>
<input id="f-phone" name="phone" required autocomplete="tel" class="w-full bg-primary border-2 border-on-primary-container/30 text-on-primary px-4 py-3 focus:border-secondary outline-none transition-colors" type="tel"/>
</div>
<div class="space-y-2">
<label for="f-business" class="font-label-caps text-on-primary-container text-[10px] uppercase block">Business Name</label>
<input id="f-business" name="business" autocomplete="organization" class="w-full bg-primary border-2 border-on-primary-container/30 text-on-primary px-4 py-3 focus:border-secondary outline-none transition-colors" type="text"/>
</div>
<div class="space-y-2">
<label for="f-city" class="font-label-caps text-on-primary-container text-[10px] uppercase block">Property City</label>
<input id="f-city" name="property-city" class="w-full bg-primary border-2 border-on-primary-container/30 text-on-primary px-4 py-3 focus:border-secondary outline-none transition-colors" type="text"/>
</div>
<div class="space-y-2">
<label for="f-rooftype" class="font-label-caps text-on-primary-container text-[10px] uppercase block">Current Roof Type</label>
<select id="f-rooftype" name="roof-type" class="w-full bg-primary border-2 border-on-primary-container/30 text-on-primary px-4 py-3 focus:border-secondary outline-none transition-colors">
<option>Metal</option>
<option>Built-Up / Tar &amp; Gravel</option>
<option>TPO / PVC</option>
<option>Concrete</option>
<option>Existing Foam</option>
<option>Other</option>
</select>
</div>
<div class="md:col-span-2 space-y-2">
<label for="f-message" class="font-label-caps text-on-primary-container text-[10px] uppercase block">Message / Property Details</label>
<textarea id="f-message" name="message" class="w-full bg-primary border-2 border-on-primary-container/30 text-on-primary px-4 py-3 focus:border-secondary outline-none transition-colors" rows="3"></textarea>
</div>
<div class="md:col-span-2">
<button type="submit" class="w-full bg-secondary text-on-secondary font-headline-lg text-2xl uppercase py-5 hover:scale-[1.02] active:scale-[0.98] transition-all">Get My Free Assessment</button>
<p class="text-on-primary-container text-xs text-center mt-4">Free, no-obligation. Fully Licensed · Lic #C-2-1052735 · BBB Accredited · We never share your info.</p>
</div>
</form>"""

FOOTER = """<!-- CTA band with embedded form -->
<section id="assessment" class="py-24 bg-primary relative overflow-hidden">
<div class="absolute inset-0 z-0 opacity-10 bg-cover bg-center" style="background-image:url('/assets/flag-bg.jpg')"></div>
<div class="container max-w-4xl mx-auto px-margin-mobile md:px-gutter relative z-10">
<div class="text-center space-y-6 mb-12">
<h2 class="font-headline-lg text-on-primary uppercase text-headline-lg">Get Your Free Roof Assessment</h2>
<p class="text-on-primary-container font-body-lg max-w-2xl mx-auto">Free assessment — drone survey, core sampling where needed, and a written bid within 48 hours, {cta_area}.</p>
</div>
{form_block}
<div class="mt-10 pt-8 border-t border-on-primary-container/20 text-center">
<p class="font-label-caps text-on-primary-container uppercase mb-3 text-[11px]">Or Call Directly</p>
<a class="font-headline-lg text-on-primary text-[34px] hover:text-secondary-fixed transition-colors" href="tel:5597399519">(559) 739-9519</a>
</div>
</div>
</section>
<footer class="bg-primary pt-16 pb-24 md:pb-8">
<div class="rwb-stripe mb-16"></div>
<div class="container max-w-container-max mx-auto px-margin-mobile md:px-gutter">
<div class="grid grid-cols-1 md:grid-cols-5 gap-12 mb-16">
<div class="space-y-6">
<img alt="Allstate Spray Foam Roofing logo" class="h-16 w-auto" src="/assets/logo-200.png" width="215" height="200" loading="lazy" decoding="async"/>
<p class="text-on-primary-container text-sm leading-relaxed">The Central Valley's authority on spray foam roofing and high-performance industrial coatings.</p>
<div class="font-label-caps text-secondary uppercase text-[10px]">Fully Licensed · Lic #C-2-1052735</div>
</div>
<div>
<p class="font-headline-lg text-on-primary text-xl uppercase mb-6">Our Services</p>
<ul class="space-y-3 font-body-md text-on-primary-container text-sm">
<li><a class="hover:text-secondary transition-colors" href="/spray-polyurethane-foam-roofing">SPF Roofing Systems</a></li>
<li><a class="hover:text-secondary transition-colors" href="/foam-roof-repair-fresno">Foam Roof Repair</a></li>
<li><a class="hover:text-secondary transition-colors" href="/commercial-roofing-fresno">Commercial Roofing Fresno</a></li>
<li><a class="hover:text-secondary transition-colors" href="/spray-foam-roofing-cost">Roofing Cost Guide</a></li>
</ul>
</div>
<div>
<p class="font-headline-lg text-on-primary text-xl uppercase mb-6">Guides</p>
<ul class="space-y-3 font-body-md text-on-primary-container text-sm">
<li><a class="hover:text-secondary transition-colors" href="/how-long-does-spray-foam-roofing-last">Foam Roof Lifespan</a></li>
<li><a class="hover:text-secondary transition-colors" href="/spray-foam-roofing-installation">Installation Step by Step</a></li>
<li><a class="hover:text-secondary transition-colors" href="/spray-foam-vs-tpo-roofing">Spray Foam vs TPO</a></li>
</ul>
</div>
<div>
<p class="font-headline-lg text-on-primary text-xl uppercase mb-6">Service Areas</p>
<ul class="space-y-3 font-body-md text-on-primary-container text-sm">
<li><a class="hover:text-secondary transition-colors" href="/fresno/">Fresno</a></li>
<li><a class="hover:text-secondary transition-colors" href="/clovis/">Clovis</a></li>
<li><a class="hover:text-secondary transition-colors" href="/visalia/">Visalia</a></li>
<li><a class="hover:text-secondary transition-colors" href="/tulare/">Tulare</a></li>
<li><a class="hover:text-secondary transition-colors" href="/hanford/">Hanford</a></li>
<li><a class="hover:text-secondary transition-colors" href="/madera/">Madera</a></li>
<li><a class="hover:text-secondary transition-colors" href="/merced/">Merced</a></li>
<li><a class="hover:text-secondary transition-colors" href="/bakersfield/">Bakersfield</a></li>
</ul>
</div>
<div>
<p class="font-headline-lg text-on-primary text-xl uppercase mb-6">Contact Us</p>
<div class="space-y-4 font-body-md text-on-primary-container text-sm">
<p>Serving Fresno &amp; the Central Valley</p>
<p class="text-on-primary font-bold"><a href="tel:5597399519">(559) 739-9519</a></p>
<p><a class="hover:text-secondary transition-colors" href="mailto:info@allstatesprayfoam.com">info@allstatesprayfoam.com</a></p>
</div>
</div>
</div>
<div class="flex flex-col md:flex-row justify-between items-center pt-8 border-t border-on-primary-container/10 gap-4">
<p class="text-on-primary-container text-[11px] font-label-caps uppercase max-w-3xl">© 2026 Allstate Spray Foam Roofing — Fresno. Licensed &amp; Insured. The commercial roofing division of <a class="underline hover:text-on-primary" href="https://allstatesprayfoam.com/" rel="noopener">Allstate Spray Foam Insulation</a>. Not affiliated with Allstate Insurance or Allstate Roofing Company.</p>
<div class="flex gap-6 font-label-caps text-[11px] uppercase">
<a class="text-on-primary-container hover:text-on-primary" href="/privacy.html">Privacy Policy</a>
</div>
</div>
</div>
</footer>
<!-- Sticky mobile call bar -->
<div class="fixed bottom-0 inset-x-0 z-40 grid grid-cols-2 md:hidden" style="padding-bottom:env(safe-area-inset-bottom)">
<a href="tel:5597399519" class="bg-secondary text-on-secondary font-label-caps uppercase tracking-widest text-center py-4">Call Now</a>
<a href="#assessment" class="bg-primary text-on-primary font-label-caps uppercase tracking-widest text-center py-4 border-l border-on-primary/20">Free Assessment</a>
</div>
""" + CONTACT_FAB

TEMPLATE = """<!DOCTYPE html>
<html class="scroll-smooth" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{title}</title>
<meta name="description" content="{meta_desc}"/>
<link rel="canonical" href="{base}/{slug}"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{meta_desc}"/>
<meta property="og:type" content="website"/>
<meta property="og:url" content="{base}/{slug}"/>
<meta property="og:image" content="{base}/assets/og-share.jpg"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{title}"/>
<meta name="twitter:description" content="{meta_desc}"/>
<meta name="twitter:image" content="{base}/assets/og-share.jpg"/>
<link rel="preload" as="image" href="/assets/{hero_img}" fetchpriority="high"/>
{schema_block}
{faq_schema}{head_shared}
</head>
<body class="bg-background text-on-background font-body-md overflow-x-hidden">
{header}
<!-- Page hero -->
<section class="relative py-24 bg-primary overflow-hidden">
<div class="absolute inset-0 z-0 opacity-15 bg-cover bg-center" style="background-image:url('/assets/{hero_img}')"></div>
<div class="absolute inset-0 bg-gradient-to-r from-primary via-primary/85 to-primary/50 z-10"></div>
<div class="container max-w-container-max mx-auto px-margin-mobile md:px-gutter relative z-20 space-y-6">
<h1 class="font-headline-xl text-on-primary uppercase text-[40px] md:text-[56px] leading-tight max-w-4xl">{h1}</h1>
<p class="font-body-lg text-on-primary-container max-w-2xl">{subhead}</p>
{updated_line}<div class="flex flex-col sm:flex-row gap-4 pt-2">
<a href="#assessment" class="bg-secondary text-on-secondary font-label-caps py-4 px-8 text-center uppercase tracking-widest hover:scale-105 transition-transform">Get a Free Roof Assessment</a>
<a class="border-2 border-on-primary text-on-primary font-label-caps py-4 px-8 text-center uppercase tracking-widest hover:bg-on-primary hover:text-primary transition-all" href="tel:5597399519">Call (559) 739-9519</a>
</div>
</div>
</section>
<div class="rwb-stripe"></div>
<!-- Content -->
<section class="py-20 bg-background">
<div class="container max-w-4xl mx-auto px-margin-mobile md:px-gutter prose-band">
{body}
{faq_html}
</div>
</section>
{footer}
</body></html>
"""


def breadcrumb(p):
    return ('<script type="application/ld+json">\n'
            + json.dumps({
                "@context": "https://schema.org", "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                    {"@type": "ListItem", "position": 2, "name": p["schema_name"], "item": f"{BASE}/{p['slug']}"},
                ]}) + "\n</script>")


def service_schema(p):
    return ('<script type="application/ld+json">\n'
            + json.dumps({
                "@context": "https://schema.org", "@type": "Service",
                "name": p["schema_name"],
                "provider": {"@id": BASE + "/#contractor"},
                "areaServed": p.get("area", [{"@type": "City", "name": "Fresno"}]),
                "url": f"{BASE}/{p['slug']}",
            }) + "\n</script>\n" + breadcrumb(p))


def article_schema(p):
    return ('<script type="application/ld+json">\n'
            + json.dumps({
                "@context": "https://schema.org", "@type": "Article",
                "headline": p["schema_name"],
                "author": {"@type": "Organization", "name": "Allstate Spray Foam Roofing — Fresno"},
                "publisher": {"@id": BASE + "/#contractor"},
                "datePublished": "2026-07-19", "dateModified": "2026-07-20",
                "mainEntityOfPage": f"{BASE}/{p['slug']}",
            }) + "\n</script>\n" + breadcrumb(p))


def faq_blocks(p):
    faqs = p.get("faqs") or []
    if not faqs:
        return "", ""
    schema = ('<script type="application/ld+json">\n'
              + json.dumps({
                  "@context": "https://schema.org", "@type": "FAQPage",
                  "mainEntity": [{"@type": "Question", "name": q,
                                  "acceptedAnswer": {"@type": "Answer", "text": a}}
                                 for q, a, _ in faqs]}) + "\n</script>\n")
    items = "\n".join(
        f'<details class="bg-surface-container-lowest border-b-2 border-primary p-6 group">\n'
        f'<summary class="font-headline-lg text-primary text-xl uppercase cursor-pointer list-none flex justify-between items-center">{q}<span class="material-symbols-outlined text-secondary group-open:rotate-45 transition-transform">add</span></summary>\n'
        f'<p class="pt-4 text-on-surface-variant leading-relaxed">{a_html or a}</p>\n</details>'
        for q, a, a_html in faqs)
    html = f'\n<h2>Common Questions</h2>\n<div class="space-y-4">\n{items}\n</div>'
    return schema, html


PAGES = [
dict(slug="foam-roof-repair-fresno", hero_img="service-silicone.jpg", area=[{"@type": "City", "name": "Fresno"}, {"@type": "AdministrativeArea", "name": "Fresno County"}],
 title="Foam Roof Repair Fresno, CA | Allstate Spray Foam Roofing",
 meta_desc="Foam roof repair in Fresno, CA — blisters, cracks, ponding water and UV damage fixed fast. Recoat instead of replacing. Free assessment: (559) 739-9519.",
 schema_name="Foam Roof Repair",
 h1='Foam Roof <span class="text-secondary-fixed">Repair</span> in Fresno, CA',
 subhead="Foam roof repair in Fresno usually costs a fraction of replacement — blisters, cracks, and ponding water fixed fast, and the roof comes back better than new.",
 body="""
<h2>Signs Your Foam Roof Needs Repair</h2>
<p><strong>Foam roof repair</strong> is almost always the right call before replacement. Spray polyurethane foam roofs are among the longest-lasting commercial systems available — but the protective coating on top takes the punishment of the Central Valley sun and needs attention over time. Call us for an assessment if you see any of these:</p>
<ul>
<li><strong>Exposed or yellowing foam</strong> — the coating has worn through and UV is degrading the foam surface. Caught early, this is a simple recoat.</li>
<li><strong>Blisters or bubbles</strong> — trapped moisture or an adhesion issue between coating layers. Small blisters are cut out and patched in minutes.</li>
<li><strong>Cracks and splits</strong> — usually at penetrations, parapet walls, or where the building moves. Sealed with compatible elastomeric materials.</li>
<li><strong>Ponding water</strong> — foam is the one roofing material where low spots can be re-sloped by adding more foam, eliminating the pond permanently.</li>
<li><strong>Bird or hail damage</strong> — impact dings in the coating that expose foam. Fast, inexpensive patch repairs when addressed promptly.</li>
</ul>
<h2>Repair, Recoat, or Replace?</h2>
<p>This is the decision that saves — or wastes — tens of thousands of dollars. Here's the honest breakdown we walk every building owner through:</p>
<table>
<tr><th>Condition</th><th>Right Fix</th><th>Typical Scope</th></tr>
<tr><td>Isolated damage, coating mostly intact</td><td>Spot repair</td><td>Cut out, dry, refoam, recoat the damaged areas</td></tr>
<tr><td>Coating worn but foam solid (most roofs 10–20 yrs old)</td><td>Full recoat</td><td>Clean, prime, apply new silicone coating over the entire roof</td></tr>
<tr><td>Saturated foam across large areas</td><td>Partial replacement</td><td>Remove saturated sections, refoam, coat the whole roof</td></tr>
</table>
<p>A foam roof that gets recoated on schedule is effectively <strong>renewable forever</strong> — that's the system's core advantage. We take core samples during the free assessment so the recommendation is based on what's actually inside your roof, not a guess.</p>
<h2>Why Fresno Foam Roofs Fail Faster Without Maintenance</h2>
<p>Central Valley roofs take 100°+ summer surface temperatures, intense UV exposure, and agricultural dust that holds moisture against the coating. The good news: a properly maintained silicone-coated foam roof handles all of it. The recoat cycle here is typically 10–20 years depending on coating thickness — and each recoat renews the warranty clock.</p>
<h2>Our Repair Process</h2>
<ul>
<li><strong>Free assessment</strong> — drone survey plus physical inspection and core samples where warranted.</li>
<li><strong>Moisture scan</strong> — we find saturated foam before it spreads, not after.</li>
<li><strong>Written scope &amp; bid within 48 hours</strong> — repair vs. recoat clearly priced so you can compare.</li>
<li><strong>Repair &amp; recoat</strong> — most repairs are completed in days with your business operating normally below.</li>
</ul>
<p>Not sure what system is on your roof? Read our guide to <a class="text-secondary underline" href="/spray-polyurethane-foam-roofing">spray polyurethane foam roofing</a>, our breakdown of <a class="text-secondary underline" href="/how-long-does-spray-foam-roofing-last">how long foam roofs last</a>, or see <a class="text-secondary underline" href="/spray-foam-roofing-cost">what foam roofing costs</a> compared to replacement.</p>
"""),

dict(slug="spray-foam-roofing-cost", hero_img="hero-aerial.jpg", area=[{"@type": "City", "name": "Fresno"}, {"@type": "AdministrativeArea", "name": "Central Valley"}],
 title="Spray Foam Roofing Cost 2026: Commercial Guide | Allstate",
 meta_desc="Spray foam roofing costs $4-$8/sq ft installed; recoats $2-$4. What drives commercial pricing and why SPF beats TPO on lifecycle. Bids: (559) 739-9519.",
 schema_name="Spray Foam Roofing Cost Guide",
 h1='What Does Spray Foam Roofing <span class="text-secondary-fixed">Cost</span>?',
 subhead="An honest 2026 pricing guide for commercial building owners — what drives the number, how recoating changes the math, and why SPF usually wins on lifecycle cost.",
 faqs=[("How much does spray foam roofing cost in Fresno in 2026?",
        "New commercial SPF roof systems in the Fresno area typically run $4-$8 per square foot installed; recoating an existing foam roof typically runs $2-$4 per square foot. Every roof gets a firm written bid within 48 hours of a free assessment from Allstate Spray Foam Roofing (Lic #C-2-1052735).",
        'New commercial SPF roof systems in the Fresno area typically run <strong>$4–$8 per square foot</strong> installed; recoating an existing foam roof typically runs <strong>$2–$4 per square foot</strong>. Every roof gets a firm written bid within 48 hours of a free assessment from Allstate Spray Foam Roofing (Lic #C-2-1052735).')],
 body="""
<h2>The Short Answer</h2>
<p>For commercial buildings, a new spray polyurethane foam (SPF) roof system typically runs in the <strong>$4–$8 per square foot</strong> range installed, depending on the factors below. A <strong>silicone recoat</strong> of an existing foam roof — the renewal that keeps the system alive indefinitely — typically runs <strong>$2–$4 per square foot</strong>. Every roof is different; these ranges are for orientation, and your free assessment produces a firm written bid within 48 hours.</p>
<h2>What Drives the Price</h2>
<table>
<tr><th>Factor</th><th>Why It Matters</th></tr>
<tr><td>Roof size</td><td>Larger roofs cost less per square foot — mobilization and setup are spread across more area</td></tr>
<tr><td>Foam thickness</td><td>More R-value = more material. Central Valley energy codes and your cooling costs set the target</td></tr>
<tr><td>Existing roof condition</td><td>SPF installs directly over most existing roofs — <strong>no tear-off</strong> — but wet insulation must be removed first</td></tr>
<tr><td>Coating system</td><td>Silicone thickness and granule options set the recoat interval and warranty length</td></tr>
<tr><td>Penetrations &amp; details</td><td>HVAC units, skylights, parapets, and drains all take hand detailing</td></tr>
<tr><td>Access</td><td>Equipment staging and building height affect labor</td></tr>
</table>
<h2>Why the Lifecycle Math Favors Foam</h2>
<p>Conventional commercial roofing quotes look cheaper until you count the second roof. A single-ply membrane at the end of its life becomes a <strong>tear-off + landfill + full reinstall</strong>. A foam roof at the end of its coating cycle gets a <strong>recoat</strong> — no tear-off, ever. See the full <a class="text-secondary underline" href="/spray-foam-vs-tpo-roofing">spray foam vs TPO comparison</a>.</p>
<ul>
<li><strong>No tear-off on installation</strong> — SPF applies over most existing metal, built-up, and concrete roofs, saving removal and disposal costs up front.</li>
<li><strong>Energy payback</strong> — SPF has the highest R-value per inch of any roofing material (~R-6.5/inch), and the white silicone topcoat reflects most solar energy. Central Valley owners routinely cut summer cooling loads dramatically.</li>
<li><strong>Renewable, not replaceable</strong> — recoat every 10–20 years at a fraction of replacement cost. The foam itself keeps performing for decades.</li>
</ul>
<h2>Getting a Real Number</h2>
<p>Beware of any roofing price quoted without someone on your roof. Our free assessment includes a drone survey, physical inspection, and core samples where needed — so the bid reflects your actual roof, with repair, recoat, and new-system options priced side by side.</p>
<p>Related reading: <a class="text-secondary underline" href="/spray-polyurethane-foam-roofing">how SPF roofing systems work</a> and <a class="text-secondary underline" href="/foam-roof-repair-fresno">foam roof repair in Fresno</a>.</p>
"""),

dict(slug="spray-polyurethane-foam-roofing", hero_img="service-spf-roof.jpg", area=[{"@type": "City", "name": "Fresno"}, {"@type": "AdministrativeArea", "name": "Central Valley"}],
 title="Spray Polyurethane Foam (SPF) Roofing Systems | Allstate",
 meta_desc="How spray polyurethane foam roofing works: seamless closed-cell SPF plus silicone coating. R-6.5 per inch, renewable for decades. Call (559) 739-9519.",
 schema_name="Spray Polyurethane Foam Roofing",
 h1='Spray Polyurethane Foam <span class="text-secondary-fixed">(SPF)</span> Roofing Systems',
 subhead="The engineering behind the most energy-efficient commercial roof system available — seamless, self-flashing, and renewable for the life of your building.",
 body="""
<h2>What SPF Roofing Actually Is</h2>
<p>Spray polyurethane foam roofing is a two-component liquid system applied directly to your roof deck, where it expands and cures within seconds into a rigid, closed-cell foam layer — typically 1.5 to 3 inches thick at roughly 3 lb/ft³ density. Because it's applied as a liquid, it flows around every penetration, curb, and parapet, creating a single <strong>monolithic, seamless surface with no joints, no fasteners, and no flashing failures</strong> — the places every conventional roof leaks.</p>
<p>The foam is then protected with an elastomeric topcoat — we use high-solids <strong>silicone coating</strong>, often with ceramic granules — that shields the foam from UV and takes the weathering. The coating is the sacrificial, renewable layer; the foam is the permanent structure.</p>
<figure class="my-8">
<img src="/assets/spf-roof-cross-section.webp" alt="Labeled cross-section diagram of a spray polyurethane foam roof system: structural deck, roof substrate, SPF insulation layer, base coat, and UV-protective roof coating" class="w-full border-2 border-primary" width="1200" height="900" loading="lazy" decoding="async"/>
<figcaption class="font-label-caps text-on-surface-variant text-[10px] uppercase mt-2 tracking-widest">The layered SPF roof system — deck to coating</figcaption>
</figure>
<h2>Performance Numbers That Matter</h2>
<table>
<tr><th>Property</th><th>SPF Roofing</th><th>Why It Matters in the Central Valley</th></tr>
<tr><td>R-value</td><td>~R-6.5 per inch — highest of any roofing material</td><td>Directly cuts summer cooling loads in 100°+ heat</td></tr>
<tr><td>Solar reflectance</td><td>White silicone topcoat reflects ~85% of solar energy</td><td>Roof surface runs dramatically cooler than dark membranes</td></tr>
<tr><td>Seams</td><td>Zero</td><td>Seams are where TPO, PVC, and built-up roofs fail</td></tr>
<tr><td>Wind uplift</td><td>Fully adhered — no fasteners, no edges to catch</td><td>Documented hurricane-zone performance</td></tr>
<tr><td>Weight</td><td>~1/3 lb per sq ft per inch</td><td>Adds insulation without structural loading</td></tr>
<tr><td>Service life</td><td>Decades — recoat every 10–20 years renews the system</td><td>The last roof your building needs</td></tr>
</table>
<h2>Where SPF Wins</h2>
<ul>
<li><strong>Flat and low-slope commercial roofs</strong> — warehouses, packing houses, cold storage, retail, offices, schools.</li>
<li><strong>Metal buildings</strong> — foam seals the seams and fastener heads that make metal roofs leak, and insulates in the same pass.</li>
<li><strong>Roofs with ponding problems</strong> — SPF is the only system where slope can be <em>built</em> into the application to eliminate low spots.</li>
<li><strong>Re-roofing without tear-off</strong> — SPF installs over most existing built-up, metal, and concrete roofs, avoiding removal and landfill costs.</li>
</ul>
<h2>The Renewal Cycle — Why SPF Is the Last Roof You Buy</h2>
<p>When the silicone coating reaches the end of its service window, it gets cleaned, primed, and recoated — no tear-off, no replacement, no disruption to the building below. Industry studies of SPF roofs over 30+ years consistently show the foam performing like new under a maintained coating — the full picture is in our <a class="text-secondary underline" href="/how-long-does-spray-foam-roofing-last">foam roof lifespan guide</a>. That renewal cycle is the fundamental economic difference between foam and every membrane system: read the cost breakdown in our <a class="text-secondary underline" href="/spray-foam-roofing-cost">spray foam roofing cost guide</a>.</p>
<h2>Installed by SPF Specialists</h2>
<p>SPF roofing is unforgiving of poor application — substrate prep, ambient conditions, pass thickness, and coating coverage all determine whether the system lasts 5 years or 50. Allstate Spray Foam Roofing has been spraying foam for over 20 years as SPFA-member applicators, fully licensed (Lic #C-2-1052735). See our <a class="text-secondary underline" href="/commercial-roofing-fresno">commercial roofing services in Fresno</a> or request a free assessment below.</p>
"""),

dict(slug="commercial-roofing-fresno", hero_img="truck.jpg", area=[{"@type": "City", "name": "Fresno"}, {"@type": "City", "name": "Clovis"}, {"@type": "AdministrativeArea", "name": "Fresno County"}],
 title="Commercial Roofing Fresno, CA | SPF & Coatings | Allstate",
 meta_desc="Commercial roofing contractor in Fresno, CA — spray foam roof systems and silicone restoration for warehouses, ag facilities and metal buildings. (559) 739-9519.",
 schema_name="Commercial Roofing Fresno",
 h1='Commercial Roofing in <span class="text-secondary-fixed">Fresno</span>, California',
 subhead="Fresno's flat and low-slope commercial roofs live in one of the harshest climates in the country. We build and restore roof systems engineered for exactly that.",
 faqs=[("Who installs spray foam roofing in Fresno?",
        "Allstate Spray Foam Roofing installs and restores commercial spray foam roof systems throughout Fresno and Clovis — family-owned, 20+ years in the Central Valley, fully licensed (Lic #C-2-1052735), SPFA member.", None),
       ("Do you serve Clovis and the rest of Fresno County?",
        "Yes — Fresno, Clovis, and all of Fresno County including the Highway 99, 41, and 180 industrial corridors, plus the wider Central Valley from Merced to Bakersfield.", None),
       ("How fast can you assess a commercial roof in Fresno?",
        "Assessments are free and typically scheduled within days — drone survey, physical inspection, core sampling where needed, and a written bid within 48 hours of the visit.", None)],
 body="""
<h2>Roofing for the Central Valley's Reality</h2>
<p>Fresno commercial buildings face a brutal combination: months of 100°+ heat, intense UV that destroys exposed membranes, winter tule fog holding moisture on the roof, and agricultural dust that clogs drains and abrades coatings. Roof systems that perform fine on the coast fail early here. That's why our work centers on <strong>spray polyurethane foam and silicone coating systems</strong> — the combination best suited to Central Valley conditions: seamless against dust and water, highly insulating against the heat, and renewable instead of replaceable.</p>
<h2>What We Do</h2>
<ul>
<li><strong><a class="text-secondary underline" href="/spray-polyurethane-foam-roofing">SPF roof systems</a></strong> — new seamless foam roofs installed over most existing roofs, no tear-off.</li>
<li><strong>Silicone roof restoration</strong> — recoat aging foam, metal, TPO, and built-up roofs; stop leaks and add 10–20 years of life without replacement.</li>
<li><strong><a class="text-secondary underline" href="/foam-roof-repair-fresno">Foam roof repair</a></strong> — blisters, cracks, ponding, and storm damage fixed fast.</li>
<li><strong>Commercial insulation</strong> — walls, ceilings, and metal buildings, from the same crews on the same mobilization.</li>
</ul>
<h2>Buildings We Serve Across Fresno &amp; Clovis</h2>
<p>Warehouses and distribution centers along the Highway 99 corridor. Agricultural processing and packing facilities. Cold storage — where roof insulation is money. Retail centers and office parks from downtown Fresno to Clovis. Metal buildings of every kind. Schools and churches. If it has a flat or low-slope roof in Fresno County, we've likely sprayed one like it.</p>
<h2>Why Building Owners Choose Foam Over Conventional Re-Roofing</h2>
<table>
<tr><th></th><th>Conventional Re-Roof (TPO/BUR)</th><th>SPF + Silicone System</th></tr>
<tr><td>Tear-off required</td><td>Usually — cost, disruption, landfill</td><td>Rarely — installs over existing roof</td></tr>
<tr><td>Seams</td><td>Thousands of feet of them</td><td>Zero</td></tr>
<tr><td>Added insulation</td><td>Separate line item</td><td>Built into the system (~R-6.5/inch)</td></tr>
<tr><td>End of life</td><td>Another tear-off</td><td>Recoat and renew</td></tr>
<tr><td>Business disruption</td><td>Days to weeks</td><td>Building stays open during application</td></tr>
</table>
<p>Weighing membrane options? Read the full <a class="text-secondary underline" href="/spray-foam-vs-tpo-roofing">spray foam vs TPO comparison</a>.</p>
<h2>Serving Fresno and the Entire Central Valley</h2>
<p>Based in the Valley for over 20 years, we serve Fresno, Clovis, Madera, Visalia, Tulare, Hanford, Merced, and Bakersfield. Family-owned, SPFA member, BBB accredited, fully licensed (Lic #C-2-1052735) — and every assessment starts free, with a drone survey and a written bid within 48 hours.</p>
"""),

# ---------- City money pages ----------
dict(slug="spray-foam-roofing-visalia", hero_img="hero-aerial.jpg", area=[{"@type": "City", "name": "Visalia"}, {"@type": "AdministrativeArea", "name": "Tulare County"}],
 title="Spray Foam Roofing Visalia, CA | Allstate Spray Foam",
 meta_desc="Commercial spray foam roofing & silicone coatings in Visalia, CA — Allstate's home turf. Ag processing, warehouses & metal buildings. (559) 739-9519.",
 schema_name="Spray Foam Roofing Visalia",
 h1='Spray Foam Roofing in <span class="text-secondary-fixed">Visalia</span>, CA',
 subhead="Visalia is our home turf — Allstate has been spraying foam in Tulare County for over 20 years. Commercial roofs here get our A-team, minutes from the shop.",
 faqs=[("How fast can you get to a Visalia roof?",
        "Fast — our shop is in Tulare County, so Visalia assessments are usually the quickest we schedule. Crews mobilize minutes away, and written bids follow within 48 hours.", None),
       ("Do you handle packing houses and cold storage in Visalia?",
        "Yes — ag processing, packing, and cold-storage roofs are our core Tulare County work. Seamless SPF with silicone topcoat handles washdown humidity inside and Valley heat outside.", None)],
 body="""
<h2>Visalia's Hometown Spray Foam Roofing Crew</h2>
<p>Allstate Spray Foam started in Visalia, and after 20+ years we've foamed and coated roofs across every industrial corridor in the city — from the Visalia Industrial Park to the packing houses and cold-storage facilities that keep Tulare County's ag economy moving. When your roof is minutes from our shop, you get faster mobilization, faster punch-list turnaround, and a crew that will drive past your building for years after the job is done. We stand behind every roof, because we literally can't avoid seeing them.</p>
<p><strong>Dispatch:</strong> crews roll from our Tulare County shop — Visalia jobs are typically the first stop of the day, with same-week assessments the norm.</p>
<h2>What Visalia Buildings Need From a Roof</h2>
<ul>
<li><strong>Ag processing &amp; packing facilities</strong> — washdown humidity inside, 100°+ heat outside. Closed-cell SPF handles both, sealing the roof deck and insulating in one pass.</li>
<li><strong>Cold storage</strong> — every degree matters. SPF's ~R-6.5 per inch is the highest of any roof system, cutting refrigeration loads measurably.</li>
<li><strong>Metal buildings</strong> — Tulare County's workhorse structures. Foam seals the seams and fastener heads that make metal roofs leak, permanently.</li>
<li><strong>Retail &amp; office</strong> — quiet, clean application with the building open for business below.</li>
</ul>
<h2>Repair and Restoration in Visalia</h2>
<p>Already have a foam roof? Many Visalia buildings do — some of them ours from decades back. A <a class="text-secondary underline" href="/foam-roof-repair-fresno">repair or recoat</a> renews the system for a fraction of replacement cost. If you have an aging TPO, metal, or built-up roof, a <a class="text-secondary underline" href="/spray-polyurethane-foam-roofing">silicone-coated SPF overlay</a> installs right over it — no tear-off.</p>
<h2>Serving All of Tulare County</h2>
<p>From Visalia we cover Tulare, Exeter, Farmersville, Goshen, and everything in between — and neighboring Hanford is <a class="text-secondary underline" href="/spray-foam-roofing-hanford">20 minutes west</a>. See our <a class="text-secondary underline" href="/spray-foam-roofing-cost">cost guide</a> for what to expect, then get your free assessment — drone survey, core samples where needed, written bid within 48 hours.</p>
"""),

dict(slug="spray-foam-roofing-tulare", hero_img="service-spf-roof.jpg", area=[{"@type": "City", "name": "Tulare"}, {"@type": "AdministrativeArea", "name": "Tulare County"}],
 title="Spray Foam Roofing Tulare, CA | Dairy & Ag Roofing | Allstate",
 meta_desc="Commercial spray foam roofing in Tulare, CA — dairy processing, ag facilities and Highway 99 warehouses. Seamless SPF + silicone systems. (559) 739-9519.",
 schema_name="Spray Foam Roofing Tulare",
 h1='Spray Foam Roofing in <span class="text-secondary-fixed">Tulare</span>, CA',
 subhead="Home of the World Ag Expo and some of the hardest-working roofs in California. We keep dairy, processing, and distribution buildings sealed and cool.",
 faqs=[("Can you roof dairy and food-processing plants without stopping production?",
        "Yes — SPF is applied from the roof side with no interior access needed. We coordinate spray windows around washdown schedules and air intakes, and the line keeps running.", None),
       ("Do you work around World Ag Expo scheduling?",
        "We do — February expo traffic is a real constraint in Tulare, and we plan mobilizations around it. Book assessments early in the season.", None)],
 body="""
<h2>Roofing for Dairy Country</h2>
<p>Tulare sits at the center of the most productive dairy region in America — and dairy processing is brutal on buildings. Interior humidity, washdown cycles, corrosive environments, and relentless Valley sun mean ordinary roofs fail early and often. Spray polyurethane foam was practically made for these conditions: a seamless, fully-adhered envelope with zero fastener penetrations, topped with a silicone coating that shrugs off UV and ponding water alike.</p>
<p><strong>Dispatch:</strong> our shop is up the road in Tulare County — most Tulare jobs are under 20 minutes from the yard, and assessments book same-week.</p>
<h2>Who We Serve in Tulare County</h2>
<ul>
<li><strong>Dairy &amp; food processing plants</strong> — seamless roofs with no seams to harbor leaks over production floors.</li>
<li><strong>Cheese &amp; cold storage facilities</strong> — the highest R-value per inch available cuts refrigeration costs every single day.</li>
<li><strong>Ag equipment dealers &amp; warehouses</strong> — big metal buildings sealed and insulated in one application.</li>
<li><strong>Distribution &amp; trucking terminals</strong> along Highway 99 — fast application that doesn't shut down operations.</li>
</ul>
<h2>The Economics Ag Operators Understand</h2>
<p>Farm and processing margins are tight; roof budgets compete with equipment and feed. That's exactly why SPF wins here: it installs <strong>over your existing roof with no tear-off</strong>, cuts cooling loads immediately, and never needs replacing — just a <a class="text-secondary underline" href="/foam-roof-repair-fresno">recoat every 10–20 years</a>. Run the numbers in our <a class="text-secondary underline" href="/spray-foam-roofing-cost">cost guide</a>.</p>
<h2>Local, Licensed, and Nearby</h2>
<p>We serve Tulare, Tipton, Pixley, Lindsay, and Porterville — with <a class="text-secondary underline" href="/spray-foam-roofing-visalia">Visalia</a> and <a class="text-secondary underline" href="/spray-foam-roofing-hanford">Hanford</a> minutes away. Fully licensed (Lic #C-2-1052735), SPFA member, and on dairy-country roofs every week. Free assessments include a drone survey and written bid within 48 hours.</p>
"""),

dict(slug="spray-foam-roofing-hanford", hero_img="service-silicone.jpg", area=[{"@type": "City", "name": "Hanford"}, {"@type": "AdministrativeArea", "name": "Kings County"}],
 title="Spray Foam Roofing Hanford, CA | Commercial SPF | Allstate",
 meta_desc="Commercial spray foam roofing & silicone coatings in Hanford, CA. Seamless SPF for Kings County ag processing, warehouses & metal buildings. (559) 739-9519.",
 schema_name="Spray Foam Roofing Hanford",
 h1='Spray Foam Roofing in <span class="text-secondary-fixed">Hanford</span>, CA',
 subhead="Kings County's commercial and ag buildings run hot, dusty, and hard. We build roof systems that match.",
 faqs=[("Do you serve Lemoore and the rest of Kings County?",
        "Yes — Hanford, Lemoore, Corcoran, and Avenal are all inside our regular dispatch area, about 35 minutes west of our Tulare County shop via CA-198.", None),
       ("Can spray foam fix a leaking metal building roof in Hanford?",
        "Almost always — foam seals every seam and fastener head in one application and adds ~R-6.5 per inch of insulation at the same time, with no tear-off.", None)],
 body="""
<h2>Commercial Roofing Built for Kings County</h2>
<p>Hanford's mix of ag processing, distribution, and civic buildings all share the same enemy: the Central Valley climate. Summer roof-surface temperatures well past 150°F cook conventional membranes, and wind-blown ag dust finds every seam and fastener. Spray polyurethane foam eliminates the seams entirely — one continuous, insulating, self-flashing surface over the whole roof — and the white silicone topcoat reflects the sun instead of absorbing it.</p>
<p><strong>Dispatch:</strong> Hanford is ~35 minutes west of our Tulare County shop via CA-198 — same-week assessments across Kings County, including Lemoore, Corcoran, and Avenal.</p>
<h2>Common Hanford Projects</h2>
<ul>
<li><strong>Processing &amp; packing facilities</strong> — seamless protection over production areas, applied without shutting the line down.</li>
<li><strong>Warehouses &amp; distribution</strong> — SPF over existing metal or built-up roofs, no tear-off, no landfill fees.</li>
<li><strong>Municipal &amp; institutional buildings</strong> — schools, churches, and civic structures get decades of renewable service life.</li>
<li><strong>Existing foam roofs</strong> — <a class="text-secondary underline" href="/foam-roof-repair-fresno">repair and recoat</a> to restart the clock instead of replacing.</li>
</ul>
<h2>Why Owners Pick Foam Here</h2>
<p>It's the last roof the building needs. Install once, then <a class="text-secondary underline" href="/spray-polyurethane-foam-roofing">recoat on a 10–20 year cycle</a> forever — while the ~R-6.5-per-inch insulation pays you back on every cooling bill. See <a class="text-secondary underline" href="/spray-foam-roofing-cost">what it costs</a>, then book the free assessment: drone survey, core samples where needed, written bid in 48 hours. Also serving neighboring <a class="text-secondary underline" href="/spray-foam-roofing-visalia">Visalia</a> and <a class="text-secondary underline" href="/spray-foam-roofing-tulare">Tulare</a>.</p>
"""),

dict(slug="spray-foam-roofing-merced", hero_img="hero-aerial.jpg", area=[{"@type": "City", "name": "Merced"}, {"@type": "City", "name": "Madera"}, {"@type": "AdministrativeArea", "name": "Merced County"}, {"@type": "AdministrativeArea", "name": "Madera County"}],
 title="Spray Foam Roofing Merced & Madera, CA | Allstate",
 meta_desc="Commercial spray foam roofing in Merced & Madera, CA — seamless SPF roofs and silicone coatings for warehouses, wineries and ag facilities. (559) 739-9519.",
 schema_name="Spray Foam Roofing Merced and Madera",
 h1='Spray Foam Roofing in <span class="text-secondary-fixed">Merced &amp; Madera</span>',
 subhead="The north Valley is growing fast — and every new warehouse, plant, and campus building needs a roof that can take the heat.",
 faqs=[("Do you really mobilize crews to Merced?",
        "Yes — Merced is about 75 minutes north of our Tulare County shop via CA-99. We batch north-Valley assessments so scheduling is efficient, and full installs mobilize with everything on the rig.", None),
       ("Can you roof winery and food-processing buildings in Madera County?",
        "Yes — temperature-stable, washdown-tolerant SPF systems are a natural fit for Madera County wineries and processors, and the insulation pays back on climate control immediately.", None)],
 body="""
<h2>Serving the Growing North Valley</h2>
<p>Between UC Merced's expansion, Highway 99 logistics growth, and the ag processing backbone that never left, Merced and Madera counties are adding commercial square footage fast. Whether you're building new, buying an older facility, or nursing a roof that should have been replaced years ago, spray polyurethane foam gives you the shortest path to a sealed, insulated, energy-efficient building.</p>
<p><strong>Dispatch:</strong> Merced is ~75 minutes north via CA-99, Madera closer to 45 — we batch north-Valley assessments weekly, and installs mobilize fully self-contained.</p>
<h2>What We Do in Merced &amp; Madera</h2>
<ul>
<li><strong>New construction SPF roofs</strong> — seamless and self-flashing from day one, with insulation built in.</li>
<li><strong>Re-roofing without tear-off</strong> — foam installs directly over most existing metal, built-up, and concrete roofs.</li>
<li><strong>Silicone restoration</strong> — aging foam, metal, and single-ply roofs recoated for 10–20 more years of service.</li>
<li><strong>Wine &amp; food processing facilities</strong> — Madera County's wineries and processors get temperature-stable, washdown-tolerant roof systems.</li>
</ul>
<h2>The Valley Heat Math</h2>
<p>North Valley summers hit the same 100°+ stretches as Fresno. A dark conventional roof absorbs that heat straight into your cooling bill; a white silicone-coated foam roof reflects most of it while the foam blocks the rest at ~R-6.5 per inch — the highest of any roofing material. Our <a class="text-secondary underline" href="/spray-foam-roofing-cost">cost guide</a> covers what that means in dollars, and the <a class="text-secondary underline" href="/spray-polyurethane-foam-roofing">SPF systems page</a> covers how it works.</p>
<h2>Free Assessment, Real Numbers</h2>
<p>Drone survey, physical inspection, core samples where warranted, written bid within 48 hours — free, anywhere in Merced and Madera counties including Atwater, Livingston, Chowchilla, and Oakhurst. Fully licensed (Lic #C-2-1052735), SPFA member, 20+ years in the Valley.</p>
"""),

dict(slug="spray-foam-roofing-bakersfield", hero_img="materials-warehouse.jpg", area=[{"@type": "City", "name": "Bakersfield"}, {"@type": "AdministrativeArea", "name": "Kern County"}],
 title="Spray Foam Roofing Bakersfield, CA | Commercial SPF | Allstate",
 meta_desc="Commercial spray foam roofing in Bakersfield, CA — industrial-grade SPF and silicone coatings for oil, logistics and ag buildings in Kern County. (559) 739-9519.",
 schema_name="Spray Foam Roofing Bakersfield",
 h1='Spray Foam Roofing in <span class="text-secondary-fixed">Bakersfield</span>, CA',
 subhead="Kern County's industrial buildings work as hard as any in California. We install roof systems rated for exactly that — and we stock material by the truckload.",
 faqs=[("How long does a Bakersfield mobilization take?",
        "Bakersfield is about 90 minutes south of our Tulare County shop via CA-99. Assessments are batched weekly; full installs mobilize with materials and equipment self-contained on the rig, so distance doesn't slow the job.", None),
       ("Do you roof oil-field support buildings in Kern County?",
        "Yes — shops, yards, and field offices across Kern County. SPF handles the dust, heat, and low-maintenance requirements of energy-sector facilities well.", None)],
 body="""
<h2>Industrial-Grade Roofing for Kern County</h2>
<p>Bakersfield is the southern anchor of our service area and one of the hardest environments we roof in: brutal 100°+ summer stretches, oil-field dust, and enormous low-slope industrial footprints. Spray polyurethane foam is the system of choice for exactly these conditions — seamless across huge roof areas, fully adhered against wind, and topped with a reflective silicone coating that takes the Kern County sun so your cooling system doesn't have to.</p>
<p><strong>Dispatch:</strong> ~90 minutes south via CA-99 from our Tulare County shop — assessments batch weekly, installs mobilize fully self-contained.</p>
<h2>Buildings We Roof in Bakersfield</h2>
<ul>
<li><strong>Oil &amp; energy support facilities</strong> — shops, yards, and offices that need durable, low-maintenance roofs.</li>
<li><strong>Logistics &amp; distribution centers</strong> — the 99/58 corridor's big-box roofs, foamed and coated at industrial scale.</li>
<li><strong>Ag processing &amp; packing houses</strong> — Kern's citrus, carrot, and almond operations keep product cool under SPF.</li>
<li><strong>Metal buildings everywhere</strong> — sealed seams, stopped leaks, and insulation added in a single application.</li>
</ul>
<h2>Stocked, Staffed, and Ready</h2>
<p>Big industrial roofs need a contractor with real material capacity and real crews — not a pickup truck and a rented rig. We warehouse spray foam and coating materials by the pallet, run modern high-output spray equipment, and have been doing this for 20+ years, fully licensed (Lic #C-2-1052735).</p>
<h2>Start With the Free Assessment</h2>
<p>Drone survey of the full roof area, core sampling where warranted, and a written bid within 48 hours — with <a class="text-secondary underline" href="/foam-roof-repair-fresno">repair/recoat</a> and <a class="text-secondary underline" href="/spray-polyurethane-foam-roofing">new SPF system</a> options priced side by side. Serving Bakersfield, Delano, Shafter, Wasco, and Arvin. See the <a class="text-secondary underline" href="/spray-foam-roofing-cost">cost guide</a> for typical ranges before we talk.</p>
"""),

# ---------- Supporting articles (Article schema) ----------
dict(slug="how-long-does-spray-foam-roofing-last", hero_img="foam-macro.jpg", schema_type="article",
 title="How Long Does a Spray Foam Roof Last? | Allstate",
 meta_desc="Spray foam roofs deliver 40-50+ years with scheduled recoats. Real lifespan data, the recoat cycle, and what kills foam roofs early. (559) 739-9519.",
 schema_name="How Long Does a Spray Foam Roof Last?",
 h1='How Long Does a Spray Foam Roof <span class="text-secondary-fixed">Last</span>?',
 subhead="The honest answer: longer than the building's ownership, if you maintain the coating. Here's how the lifespan actually works.",
 body="""
<h2>The Short Answer: Decades — and Renewable</h2>
<p>A properly installed spray polyurethane foam roof, protected by a maintained elastomeric coating, routinely delivers <strong>40–50+ years of service</strong>. Industry studies that tracked SPF roofs installed in the 1970s and 80s found the foam performing essentially like new decades later — because the foam itself doesn't wear out. What wears is the <em>coating</em>, and coatings are renewable.</p>
<h2>How the Lifespan Cycle Works</h2>
<table>
<tr><th>Years</th><th>What Happens</th></tr>
<tr><td>0</td><td>SPF applied, silicone coating installed over it</td></tr>
<tr><td>1–15</td><td>Coating takes all UV and weather; foam stays protected. Annual visual checks recommended</td></tr>
<tr><td>10–20</td><td>Coating reaches end of its wear window → clean and recoat. No tear-off, typically $2–$4/sq ft</td></tr>
<tr><td>Repeat</td><td>Every recoat restarts the clock. The foam underneath keeps performing indefinitely</td></tr>
</table>
<p>Compare that with single-ply membranes (TPO/PVC), which typically deliver 15–25 years and then require a full tear-off and replacement — twice the roof spend in the same 40-year window, plus landfill costs. Full comparison: <a class="text-secondary underline" href="/spray-foam-vs-tpo-roofing">spray foam vs TPO</a>.</p>
<h2>What Actually Kills Foam Roofs Early</h2>
<ul>
<li><strong>Neglected coating</strong> — the #1 cause. Once UV eats through to bare foam, degradation accelerates. Caught early it's a recoat; caught late it's foam replacement in the exposed areas.</li>
<li><strong>Bad installation</strong> — off-ratio foam, spraying in wrong conditions, or thin coating coverage. This is why applicator experience matters more with SPF than any other system.</li>
<li><strong>Unrepaired damage</strong> — hail dings and dropped-tool punctures are cheap to <a class="text-secondary underline" href="/foam-roof-repair-fresno">patch</a> — and expensive to ignore once water gets in.</li>
</ul>
<h2>Maximizing Your Roof's Life in the Central Valley</h2>
<p>Valley UV is brutal, which makes the recoat discipline even more valuable here. Our maintenance program includes periodic inspections, minor repairs, and recoat scheduling — so the 50-year outcome actually happens. Wondering about the numbers? See the <a class="text-secondary underline" href="/spray-foam-roofing-cost">cost guide</a>, or start with a free assessment of your current roof's condition.</p>
"""),

dict(slug="spray-foam-roofing-installation", hero_img="service-spf-roof.jpg", schema_type="article",
 title="Spray Foam Roofing Installation: Step by Step | Allstate",
 meta_desc="What happens during spray foam roofing installation — prep, application, coating, inspection — and how long it takes, from a 20+ year SPF contractor. (559) 739-9519.",
 schema_name="Spray Foam Roofing Installation: What to Expect",
 h1='Spray Foam Roofing <span class="text-secondary-fixed">Installation</span>, Step by Step',
 subhead="What actually happens on your roof during an SPF installation — and what it means for your building's operations while we work.",
 body="""
<h2>Before Day One: Assessment &amp; Spec</h2>
<p>Every installation starts with the free assessment: drone survey, physical inspection, moisture scan, and core samples where warranted. From that we produce a written spec — foam thickness for your target R-value, coating system and thickness, drainage corrections, and detail work at penetrations — plus a firm bid within 48 hours.</p>
<h2>The Installation Sequence</h2>
<table>
<tr><th>Step</th><th>What Happens</th><th>Typical Duration</th></tr>
<tr><td>1. Prep</td><td>Surface cleaned (usually pressure-washed or air-blown), wet insulation removed, loose materials secured. Existing roof usually stays — no tear-off</td><td>1 day</td></tr>
<tr><td>2. Masking</td><td>Walls, units, and adjacent surfaces protected from overspray; wind screens set as needed</td><td>Hours</td></tr>
<tr><td>3. Foam application</td><td>Two-component foam sprayed in controlled passes, expanding and curing in seconds. Slope built into low spots to fix ponding</td><td>1–3 days for most commercial roofs</td></tr>
<tr><td>4. Coating</td><td>Silicone base coat applied over cured foam, then top coat (with granules where specified) to full spec thickness</td><td>1–2 days</td></tr>
<tr><td>5. Inspection</td><td>Thickness verifications, adhesion checks, and final walkthrough with photos</td><td>Hours</td></tr>
</table>
<h2>What It Means for Your Operations</h2>
<ul>
<li><strong>Your building stays open.</strong> Application is from the roof side; there's no interior access needed and no roof deck removal.</li>
<li><strong>Weather windows matter.</strong> Foam needs dry conditions and moderate wind — in the Central Valley that gives us a generous work season, and we schedule around your operations.</li>
<li><strong>Odor and overspray are managed</strong> — masking, wind screens, and intake awareness are standard procedure, not extras.</li>
</ul>
<h2>Why Applicator Skill Decides Everything</h2>
<p>SPF is the most installer-sensitive roof system there is: ratio, temperature, pass thickness, and coating coverage all determine whether you get the <a class="text-secondary underline" href="/how-long-does-spray-foam-roofing-last">50-year outcome</a> or an early failure. We've been spraying for 20+ years as SPFA members, fully licensed (Lic #C-2-1052735). Read more on <a class="text-secondary underline" href="/spray-polyurethane-foam-roofing">how SPF systems work</a> or check <a class="text-secondary underline" href="/spray-foam-roofing-cost">typical costs</a>.</p>
"""),

dict(slug="spray-foam-vs-tpo-roofing", hero_img="service-silicone.jpg", schema_type="article",
 title="Spray Foam vs TPO Roofing: Which Is Better? | Allstate",
 meta_desc="Spray foam vs TPO roofing compared honestly: seams, insulation, lifespan, tear-off and lifecycle cost for commercial buildings. (559) 739-9519.",
 schema_name="Spray Foam vs TPO Roofing Comparison",
 h1='Spray Foam vs <span class="text-secondary-fixed">TPO</span> Roofing',
 subhead="The two systems commercial owners compare most — measured on the things that actually decide roof performance: seams, insulation, lifespan, and lifecycle cost.",
 faqs=[("Is spray foam roofing better than TPO in hot climates?",
        "For hot-climate flat roofs like California's Central Valley, SPF usually wins: continuous ~R-6.5-per-inch insulation plus a reflective silicone topcoat attacks cooling costs from both directions, and there are no seams to fail in thermal cycling. TPO's advantage is a lower first-cost bid on simple new-construction decks.", None)],
 body="""
<h2>The Head-to-Head</h2>
<table>
<tr><th></th><th>TPO (Single-Ply Membrane)</th><th>SPF + Silicone Coating</th></tr>
<tr><td>Seams</td><td>Thousands of linear feet, heat-welded — the primary failure point</td><td>Zero. Monolithic, self-flashing surface</td></tr>
<tr><td>Insulation</td><td>Separate board stock underneath, gaps at joints</td><td>Built-in, continuous, ~R-6.5/inch — highest available</td></tr>
<tr><td>Attachment</td><td>Mechanically fastened or glued — thousands of penetrations or adhesive fields</td><td>Fully adhered chemically, no fasteners</td></tr>
<tr><td>Tear-off at install</td><td>Often required</td><td>Rarely — applies over most existing roofs</td></tr>
<tr><td>Typical service life</td><td>15–25 years, then full replacement</td><td>Decades — recoat every 10–20 years, foam never replaced</td></tr>
<tr><td>Ponding water</td><td>Warranty exclusions common; membrane sits in it</td><td>Slope can be built in with foam to eliminate ponds</td></tr>
<tr><td>End of life</td><td>Tear-off to landfill, buy a new roof</td><td>Clean and recoat — the roof renews</td></tr>
</table>
<h2>Where TPO Makes Sense</h2>
<p>We'll be straight: TPO is a legitimate system with a lower first-cost bid on simple, new-construction decks where insulation board is being installed anyway and the roof plane drains perfectly. If you plan to sell the building within 10 years, the cheaper bid may pencil out for you (though the next owner inherits the replacement).</p>
<h2>Where Foam Wins — Especially in the Central Valley</h2>
<ul>
<li><strong>Re-roofing over an existing roof</strong> — no tear-off changes the entire cost equation.</li>
<li><strong>Hot climates</strong> — continuous insulation plus a reflective coating attacks Fresno's cooling costs from both directions.</li>
<li><strong>Complex roofs</strong> — penetrations, units, and odd geometry that would mean endless membrane detailing get seamlessly encapsulated.</li>
<li><strong>Long-hold owners</strong> — over a 40-year window, one SPF system with two recoats typically costs far less than two full TPO installations.</li>
</ul>
<h2>Already Have TPO? You Don't Have to Tear It Off</h2>
<p>An aging TPO roof is actually a good SPF candidate — foam applies directly over it (dry membrane, prepped properly), turning the roof you have into the seamless, insulated roof you wish you'd bought. Get the details in our <a class="text-secondary underline" href="/spray-polyurethane-foam-roofing">SPF systems guide</a>, check <a class="text-secondary underline" href="/spray-foam-roofing-cost">real cost ranges</a>, or book a free assessment to see if your existing roof qualifies.</p>
"""),
]


def build():
    for p in PAGES:
        is_article = p.get("schema_type") == "article"
        schema_block = article_schema(p) if is_article else service_schema(p)
        faq_schema, faq_html = faq_blocks(p)
        cta_area = {
            "spray-foam-roofing-visalia": "anywhere in Tulare County",
            "spray-foam-roofing-tulare": "anywhere in Tulare County",
            "spray-foam-roofing-hanford": "anywhere in Kings County",
            "spray-foam-roofing-merced": "anywhere in Merced and Madera counties",
            "spray-foam-roofing-bakersfield": "anywhere in Kern County",
        }.get(p["slug"], "anywhere in Fresno and the Central Valley")
        updated_line = ('<p class="font-label-caps text-on-primary-container text-[11px] uppercase">Reviewed by Allstate Spray Foam Roofing — updated July 2026</p>\n'
                        if is_article else "")
        footer = FOOTER.replace("{form_block}", FORM_BLOCK).replace("{cta_area}", cta_area)
        html = TEMPLATE.format(
            base=BASE, head_shared=HEAD_SHARED, header=HEADER, footer=footer,
            body=p["body"], schema_block=schema_block, faq_schema=faq_schema,
            faq_html=faq_html, updated_line=updated_line,
            **{k: p[k] for k in ("slug", "title", "meta_desc", "h1", "subhead", "hero_img")})
        out = os.path.join(SITE, p["slug"] + ".html")
        with open(out, "w") as f:
            f.write(html)
        print("wrote", out, len(html), "bytes")


if __name__ == "__main__":
    build()
