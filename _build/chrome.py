"""
Site chrome: header, mobile menu, footer, intro loader and the HTML page shell.
"""
import hashlib
import json
import os
from lib import (CTX, BASE_URL, APP_URL, L, esc, icon, icon_tile, badge, brand, logo_mark, route,
                 SOFTWARE, SERVICES, INDUSTRIES, KNOWLEDGE, TOOLS, COMPANY, ORG_SCHEMA)
import mockups as M


# Content hash appended to CSS/JS URLs so browsers fetch a fresh copy whenever
# the file changes, instead of pairing new markup with a cached stylesheet
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")


def asset(rel):
    with open(os.path.join(ASSETS, *rel.split("/")), "rb") as f:
        v = hashlib.md5(f.read()).hexdigest()[:8]
    return f'{CTX["root"]}assets/{rel}?v={v}'


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
def _link_item(i, href, label, section):
    cur = ' aria-current="page"' if CTX["section"] == section else ""
    return f'<li class="nav-item" style="--i:{i}"><a class="nav-link" href="{L(href)}"{cur}><span>{label}</span></a></li>'


# Top-level navigation: plain links, no dropdowns (sub-pages are reached from
# each hub page and the footer)
NAV_LINKS = [
    ("index.html", "Home", "home"), ("platform.html", "Software", "platform"),
    ("services/", "Services", "services"), ("industries.html", "Industries", "industries"),
    ("categories.html", "Categories", "categories"), ("partners/", "Partners", "partners"),
    ("about.html", "Company", "company"),
]


def header():
    links = "".join(_link_item(i, h, t, s) for i, (h, t, s) in enumerate(NAV_LINKS))
    # The indicator pill glides to the hovered link and rests on the current page
    nav = f'<div class="nav-track" data-nav-track><ul class="nav-list">{links}</ul><span class="nav-pill" aria-hidden="true"></span></div>'
    return (f'<header class="site-header" data-header><div class="container header-inner">{brand()}'
            f'<nav class="main-nav" aria-label="Primary">{nav}</nav>'
            f'<div class="header-actions"><a class="header-signin" href="{APP_URL}" rel="nofollow">Sign In</a>'
            f'<a class="btn btn-primary btn-sm btn-shine" href="{L("request-a-demo/")}">Request a Demo</a>'
            f'<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="mobile-nav" aria-label="Open menu" data-nav-toggle>'
            f'<span class="burger" aria-hidden="true"><i></i><i></i><i></i></span></button></div></div>'
            f'<span class="header-progress" aria-hidden="true"><i data-scroll-progress></i></span></header>'
            + mobile_nav())


def mobile_nav():
    links = "".join(f'<a class="m-link" style="--i:{i}" href="{L(h)}"{" aria-current=\"page\"" if CTX["section"] == s else ""}>'
                    f'<span class="m-num">{i + 1:02d}</span>{t} {icon("arrow-right")}</a>'
                    for i, (h, t, s) in enumerate(NAV_LINKS))
    n = len(NAV_LINKS)
    return (f'<div class="mobile-nav" id="mobile-nav" data-mobile-nav>'
            f'<div class="mobile-nav-inner">{links}'
            + f'<div class="m-actions" style="--i:{n}"><a class="btn btn-primary btn-lg btn-block" href="{L("request-a-demo/")}">Request a Demo {icon("arrow-right", "icon icon-arrow")}</a>'
            + f'<a class="btn btn-secondary btn-lg btn-block" href="{APP_URL}" rel="nofollow">{icon("log-in")} Sign In</a></div>'
            + f'<p class="m-tagline" style="--i:{n + 1}">Procurement, under one view.</p></div></div>')


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
def footer():
    def col(title, items, d):
        lis = "".join(f'<li style="--i:{i}"><a href="{L(h)}">{t}</a></li>' for i, (h, t) in enumerate(items))
        return f'<div class="footer-col reveal" style="--d:{d}"><h3>{title}</h3><ul>{lis}</ul></div>'
    # Kept short on purpose: only the main pages. Every other page is linked
    # from its hub (Software, Services, Industries, Knowledge Hub, Tools, Company)
    software = [("platform.html", "B2B Procurement Platform"),
                ("procurement-management-software/", "Procurement Management Software"),
                ("e-procurement-software/", "E-Procurement Software"),
                ("procure-to-pay-software/", "Procure-to-Pay Software")]
    services = [("services/", "Procurement Services"),
                ("services/end-to-end-procurement-services/", "End-to-End Procurement"),
                ("services/arc-procurement-services/", "ARC-Based Procurement"),
                ("industries.html", "Industries We Serve")]
    # Knowledge Hub and Tools live here rather than in the top navigation
    resources = [("knowledge-hub/", "Knowledge Hub"), ("knowledge-hub/blog/", "Blog"),
                 ("knowledge-hub/procurement-guides/", "Procurement Guides"), ("faq.html", "FAQs"),
                 ("tools/", "Procurement Tools"), ("tools/procurement-savings-calculator/", "Savings Calculator"),
                 ("tools/rfq-template-generator/", "RFQ Template Generator")]
    company = [("about.html", "About Us"), ("why-proceaze/", "Why ProcEaze"),
               ("partners/", "Partners & Integrations"), ("contact.html", "Contact Us"), ("request-a-demo/", "Request a Demo")]
    legal = [("privacy.html", "Privacy"), ("terms.html", "Terms"), ("cookies.html", "Cookie Policy"), ("vendor-terms.html", "Vendor Terms")]
    legal_links = "".join(f'<a href="{L(h)}">{t}</a>' for h, t in legal)
    return (
        f'<footer class="site-footer reveal"><div class="footer-net" aria-hidden="true"></div><div class="container">'
        f'<div class="footer-main"><div class="footer-brand reveal">{brand()}'
        f'<p>Procurement software for Indian enterprises: contracted catalogue buying, ARC pricing and approvals in one place.</p></div>'
        + col("Software", software, 1) + col("Services", services, 2)
        + col("Resources", resources, 3) + col("Company", company, 4) +
        f'</div><div class="footer-bottom reveal" style="--d:4"><span>&copy; 2026 ProcEaze. All rights reserved.</span>'
        f'<nav class="footer-legal" aria-label="Legal">{legal_links}</nav>'
        f'<a class="footer-signin" href="{APP_URL}" rel="nofollow">{icon("log-in")} Sign In</a></div>'
        f'</div></footer>'
    )


# ---------------------------------------------------------------------------
# Intro loader (first visit per session, ~1s, skippable, off for reduced motion)
# ---------------------------------------------------------------------------
def loader():
    return (f'<div class="loader" data-loader aria-hidden="true"><div class="loader-inner">'
            f'<img class="loader-logo" src="{L("assets/logo/proceaze-logo.png")}" width="560" height="147" alt="">'
            f'<div class="loader-line"><i></i></div>'
            f'<p class="loader-status">CONNECTING PROCUREMENT<span class="loader-dots"><i></i><i></i><i></i></span></p>'
            f'</div></div>')


# ---------------------------------------------------------------------------
# Page shell
# ---------------------------------------------------------------------------
def page(path, title, description, body, crumbs=None, section="", schemas=None, og_type="website", noindex=False, js=()):
    canonical = BASE_URL + "/" + route(path)
    og_img = BASE_URL + "/assets/images/og-image.png"
    ld = [ORG_SCHEMA] + (schemas or [])
    if crumbs:
        items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL + "/"}]
        for label, href in crumbs:
            if href == "":
                continue
            items.append({"@type": "ListItem", "position": len(items) + 1, "name": label, "item": BASE_URL + "/" + route(href or path)})
        ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items})
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in ld)
    R = CTX["root"]
    robots = "noindex, follow" if noindex else "index, follow"
    scripts = "".join(f'<script src="{asset(f"js/{n}.js")}" defer></script>' for n in ("main", "forms", "interactions", "animations", *js))
    return f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#184AC3">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="ProcEaze">
<meta property="og:locale" content="en_IN">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{og_img}">
<link rel="icon" href="{R}assets/icons/favicon.svg" type="image/svg+xml">
<link rel="icon" href="{R}assets/icons/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{R}assets/icons/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Serif:ital,wght@0,500;0,600;1,500&amp;family=Inter:wght@400;500;600;700;800&amp;display=swap">
<link rel="stylesheet" href="{asset("css/style.css")}">
<link rel="stylesheet" href="{asset("css/responsive.css")}">
<script>(function(d){{var h=d.documentElement;h.classList.add('js');try{{if(sessionStorage.getItem('pe-intro')||matchMedia('(prefers-reduced-motion: reduce)').matches)h.classList.add('no-loader');}}catch(e){{h.classList.add('no-loader');}}}})(document);</script>
<script type="speculationrules">{{"prefetch":[{{"where":{{"and":[{{"href_matches":"/*"}},{{"not":{{"selector_matches":"[rel~=nofollow]"}}}}]}},"eagerness":"moderate"}}]}}</script>
{scripts}
{ld_html}
</head>
<body data-page="{esc(route(path) or "index")}">
<a class="skip-link" href="#main">Skip to content</a>
{loader()}
{header()}
<main id="main" tabindex="-1">
{body}
</main>
{footer()}
<div class="toast-region" aria-live="polite" aria-atomic="false" data-toasts></div>
<button class="to-top" type="button" aria-label="Back to top" data-to-top>{icon("arrow-up")}</button>
</body>
</html>
"""
