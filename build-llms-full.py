#!/usr/bin/env python3
"""Generate site/llms-full.txt — concatenated prose content of all indexable pages.
Strips nav/footer chrome; keeps heading structure; one ----separated section per page."""
import os
import re
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "site")
BASE = "https://fresnosprayfoamroofing.com"

import glob as _glob
PAGES = ["index.html", "spray-polyurethane-foam-roofing.html", "foam-roof-repair-fresno.html",
         "commercial-roofing-fresno.html", "spray-foam-roofing-cost.html",
         "how-long-does-spray-foam-roofing-last.html",
         "spray-foam-roofing-installation.html", "spray-foam-vs-tpo-roofing.html"]
PAGES += sorted(os.path.relpath(p, SITE) for p in _glob.glob(os.path.join(SITE, "*", "*.html")))


class Extract(HTMLParser):
    SKIP = {"script", "style", "nav", "footer", "header", "form", "select", "option", "button", "label", "figcaption"}

    def __init__(self):
        super().__init__()
        self.out, self.skip_depth, self.cur_tag = [], 0, None

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip_depth += 1
        self.cur_tag = tag

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip_depth:
            self.skip_depth -= 1
        if tag in ("h1", "h2", "h3", "p", "li", "tr", "summary"):
            self.out.append("\n")

    def handle_data(self, data):
        if self.skip_depth:
            return
        t = data.strip()
        if not t:
            return
        if self.cur_tag == "h1":
            self.out.append("\n# " + t + " ")
        elif self.cur_tag in ("h2", "h3"):
            self.out.append("\n## " + t + " ")
        elif self.cur_tag == "summary":
            self.out.append("\nQ: " + t + " ")
        else:
            self.out.append(t + " ")


sections = []
for f in PAGES:
    html = open(os.path.join(SITE, f)).read()
    title = re.search(r"<title>([^<]*)</title>", html).group(1)
    body = html[html.index("<body"):]
    ex = Extract()
    ex.feed(body)
    text = re.sub(r"\n{3,}", "\n\n", "".join(ex.out)).strip()
    url = BASE + "/" + (f[:-11] if f.endswith("/index.html") else (f[:-5] if f != "index.html" else ""))
    sections.append(f"URL: {url}\nTITLE: {title}\n\n{text}")

open(os.path.join(SITE, "llms-full.txt"), "w").write(
    "# Allstate Spray Foam Roofing — Fresno — full site content\n\n" + "\n\n---\n\n".join(sections) + "\n")
print("wrote llms-full.txt", os.path.getsize(os.path.join(SITE, "llms-full.txt")), "bytes")
