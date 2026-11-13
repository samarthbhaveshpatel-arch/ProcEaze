"""Partners & Integrations (/partners/): the ProcEaze ecosystem, integration
categories and a partnership enquiry form.

The technical integration detail lives on /platform/integrations/; statuses
here mirror INTEGRATION_ITEMS on that page. No partner is named: none is
confirmed, so the page describes partner types, not partners.
"""
from lib import (icon, icon_tile, badge, L, logo_mark, section_head, page_hero, btn_link, feature_cards, workflow, check_list,
                 related, f_input, f_phone, f_select, f_textarea, f_consent, success_panel)


def hub(nodes, label):
    """Ecosystem diagram: ProcEaze at the centre, linked to each node (reuses the integrations hub styles)."""
    paths = "".join(f'<path d="M50 50 L{x} {y}" vector-effect="non-scaling-stroke"/>' for x, y, _, _ in nodes)
    items = "".join(f'<div class="hub-node" style="left:{x}%;top:{y}%">{icon(ic)}<strong>{t}</strong></div>' for x, y, ic, t in nodes)
    return (f'<div class="dark-panel panel-royal" role="img" aria-label="{label}"><div class="hub">'
            f'<svg class="hub-lines" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">{paths}</svg>'
            f'<div class="hub-center">{logo_mark("")}<div><strong>ProcEaze</strong></div></div>{items}</div></div>')


HERO_NODES = [
    (50, 9, "database", "Enterprise systems"),
    (88, 34, "plug", "Technology partners"),
    (80, 86, "store", "Suppliers"),
    (20, 86, "users", "Procurement teams"),
    (12, 34, "layers", "Business applications"),
]

TECH_NODES = [
    (50, 9, "database", "ERP systems"),
    (88, 32, "layers", "Enterprise applications"),
    (88, 72, "landmark", "Finance &amp; accounting"),
    (50, 93, "store", "Supplier systems"),
    (12, 72, "code", "APIs &amp; data exchange"),
    (12, 32, "cloud", "Cloud infrastructure"),
]

ECOSYSTEM = [
    dict(icon="plug", title="Technology Partners",
         text="Technology providers and software platforms that help businesses connect procurement with their existing digital infrastructure."),
    dict(icon="database", title="ERP &amp; Enterprise Integrations",
         text="Integration capabilities designed to connect procurement workflows with enterprise resource planning and business management systems."),
    dict(icon="store", title="Supplier Ecosystem",
         text="A connected supplier ecosystem that helps buyers discover, evaluate, engage and collaborate with vendors."),
    dict(icon="briefcase", title="Strategic &amp; Business Partners",
         text="Organisations and industry collaborators working together to improve procurement efficiency and business operations."),
]

# (icon, title, purpose, status, label) — statuses follow /platform/integrations/
CATEGORIES = [
    ("database", "ERP Systems", "Connect ProcEaze with SAP and other ERPs, so procurement runs in ProcEaze and finance stays in your ERP. ProcEaze is plug-in ready; the connection is scoped and delivered per client.",
     "ready", "Scoped during onboarding"),
    ("landmark", "Finance &amp; Accounting Systems", "Approved purchase orders and the audit trail give finance a clean record today. Payment gateway and invoice matching are planned for the Payment &amp; Reconciliation stage.",
     "roadmap", None),
    ("layers", "Enterprise Resource Planning Data Flows", "Agree which masters and transactions move between ProcEaze and your ERP, in which direction and when, as part of onboarding.",
     "ready", "Scoped during onboarding"),
    ("store", "Supplier Management Systems", "Vendors register, are verified and work with buyers in the Vendor Portal. Connections to an existing supplier system can be discussed as an integration project.",
     "on-request", "On request"),
    ("code", "API &amp; Custom Integrations", "APIs are available for integration projects, for data exchange that a standard connection does not cover.",
     "on-request", "On request"),
    ("cloud", "Cloud Document Management", "Quotes, NFAs and purchase orders are stored securely in the cloud, linked to the transaction they belong to.",
     "live", None),
]

PARTNER_TYPES = ["Technology Partner", "ERP / Integration Partner", "Supplier Ecosystem Partner", "Strategic Business Partner", "Other"]


def partner_form():
    p = "pt"
    return (
        f'<div class="form-card form-wrap" id="partner-form" tabindex="-1">'
        f'<h2 style="font-size:1.6rem">Partnership enquiry</h2>'
        f'<p class="muted" style="margin-bottom:16px">Tell us about your organisation and how you would like to work together. Fields marked * are required.</p>'
        f'<div class="notice info" style="margin-bottom:24px">{icon("info")}<p><strong>Prototype form.</strong> Your entries are checked in the browser, '
        f'but this form is not yet connected to our team, so nothing is sent.</p></div>'
        f'<form data-form="partner" novalidate data-toast="Enquiry checked. This prototype form did not send it.">'
        f'<div class="form-grid">'
        + f_input(p, "name", "Full name", auto="name", placeholder="Your full name")
        + f_input(p, "company", "Company name", auto="organization", placeholder="Company name")
        + f_input(p, "email", "Business email", "email", auto="email", placeholder="name@company.com", rule="work-email")
        + f_phone(p)
        + f_select(p, "type", "Partnership type", PARTNER_TYPES)
        + f_input(p, "website", "Company website", "url", required=False, auto="url", placeholder="https://")
        + f_textarea(p, "message", "Message", required=True, placeholder="What you offer, who you work with and the partnership you have in mind")
        + f_consent(p)
        + f'</div><div class="form-actions mt-16"><span class="form-note">{icon("lock")} Prototype: nothing is sent.</span>'
        f'<button class="btn btn-primary btn-lg" type="submit">Send enquiry {icon("arrow-right", "icon icon-arrow")}</button></div></form>'
        + success_panel("Your enquiry passed every check.",
                        "This is a prototype form, so it was not delivered. To reach our team today, use the Contact page.",
                        f'<div class="btn-row mt-24" style="justify-content:center"><a class="btn btn-primary" href="{L("contact.html")}">Contact Us</a>'
                        f'<button class="btn btn-secondary" type="button" data-form-again>Edit enquiry</button></div>')
        + '</div>')


def partners_body():
    hero = page_hero([("Partners & Integrations", None)], "Partners & integrations", "Building a connected procurement ecosystem.",
                     "ProcEaze brings procurement teams, technology platforms, suppliers and business systems together to create a more connected, "
                     "transparent and efficient procurement ecosystem.",
                     actions=(f'<a class="btn btn-primary btn-lg magnetic" href="#partner-form">Become a Partner {icon("arrow-right", "icon icon-arrow")}</a>'
                              + btn_link("integrations.html", "Explore Integrations", "btn-secondary btn-lg")),
                     visual=hub(HERO_NODES, "ProcEaze connected to enterprise systems, technology partners, suppliers, procurement teams and business applications"))
    out = hero

    # Partner ecosystem
    out += (f'<section class="section"><div class="container">'
            + section_head("Our partner ecosystem", "An ecosystem built for connected procurement.",
                           "We believe procurement works better when businesses, technology providers and suppliers work together.", center=True)
            + feature_cards(ECOSYSTEM, cols=4) + '</div></section>')

    # Technology & integration ecosystem
    notes = ["ProcEaze works alongside your ERP, without a rip-and-replace",
             "What connects, in which direction and when is agreed during onboarding",
             "Email notifications and cloud document storage are live today"]
    out += (f'<section class="section section-light" id="technology"><div class="container"><div class="split">'
            f'<div>{section_head("Technology & integration ecosystem", "Connect ProcEaze with your business systems.", "ProcEaze is designed to work alongside existing enterprise systems, supporting connected procurement workflows and integration projects.")}'
            f'{check_list(notes)}'
            f'<p class="small muted mt-24">SAP is named as an example of an ERP whose integration requirements can be scoped during onboarding. It is a trademark of its owner; '
            f'ProcEaze does not claim a certified integration or partnership with SAP or any other ERP vendor.</p></div>'
            f'<div class="reveal-frame">{hub(TECH_NODES, "ProcEaze connected to ERP systems, enterprise applications, finance and accounting, supplier systems, APIs and data exchange, and cloud infrastructure")}</div>'
            f'</div></div></section>')

    # Integration categories, with the same statuses as /platform/integrations/
    cards = "".join(
        f'<article class="card card-hover feature-card reveal" style="--d:{i % 3}"><div class="card-head">{icon_tile(ic)}{badge(st, text=lab)}</div>'
        f'<h3>{t}</h3><p>{d}</p></article>'
        for i, (ic, t, d, st, lab) in enumerate(CATEGORIES))
    out += (f'<section class="section" id="integrations"><div class="container">'
            + '<div class="section-head-row">'
            + section_head("Featured technology ecosystem", "Designed to work with your enterprise technology.",
                           "Each category is labelled with its status today, so you can plan around what is real.")
            + f'<a class="link-arrow reveal" href="{L("integrations.html")}">Integration details {icon("arrow-right")}</a></div>'
            + f'<div class="grid grid-3">{cards}</div></div></section>')

    # Supplier ecosystem
    out += (f'<section class="section section-light" id="suppliers"><div class="container">'
            + section_head("Supplier ecosystem", "Connecting buyers with the right suppliers.",
                           "ProcEaze helps enterprises streamline supplier discovery, supplier engagement, procurement sourcing and vendor collaboration "
                           "through one connected procurement platform.", center=True)
            + workflow([("search", "Supplier discovery", "Find vendors for the requirement"),
                        ("badge-check", "Vendor evaluation", "GSTIN, documents and fit"),
                        ("clipboard-list", "RFQ & sourcing", "Quotes compared side by side"),
                        ("message-circle", "Negotiation", "Auction or AI-assisted"),
                        ("file-check", "Purchase order", "Issued once approved")])
            + f'<div class="center mt-48 reveal">{btn_link("vendor-portal.html", "Explore Supplier Portal", "btn-primary btn-lg", "store")}</div>'
            + '</div></section>')

    # Become a partner
    out += (f'<section class="section cta-band"><div class="bg-circle c1" aria-hidden="true"></div><div class="bg-circle c2" aria-hidden="true"></div>'
            f'<div class="container reveal"><h2>Let\'s build a smarter procurement ecosystem together.</h2>'
            f'<p class="lead">Are you a technology provider, ERP consultant, supplier network or business organisation interested in collaborating with ProcEaze? '
            f'Let\'s explore opportunities to work together.</p>'
            f'<div class="btn-row"><a class="btn btn-white btn-lg" href="#partner-form">Become a Partner {icon("arrow-right", "icon icon-arrow")}</a>'
            f'{btn_link("contact.html", "Contact Our Team", "btn-ghost-light btn-lg")}</div></div></section>')

    # Enquiry form
    who = ["Technology providers and software platforms",
           "ERP consultants and system integrators",
           "Supplier networks, distributors and OEMs",
           "Industry bodies and business organisations"]
    out += (f'<section class="section"><div class="container"><div class="split split-form">'
            f'{partner_form()}'
            f'<aside class="stack"><div class="card card-flat"><h2 style="font-size:1.35rem">Who we partner with</h2>{check_list(who)}</div>'
            f'<div class="card card-flat"><div class="card-head">{icon_tile("store")}</div><h3>Want to supply through ProcEaze?</h3>'
            f'<p>Vendors register separately.</p><a class="link-arrow" href="{L("vendors.html")}">Become a Vendor {icon("arrow-right")}</a></div>'
            f'</aside></div></div></section>')

    out += related(["integrations.html", "security.html", "vendors.html"], "Related")
    return out


PAGES = [
    dict(path="partners/", title="Partners & Integrations: Procurement Ecosystem | ProcEaze",
         desc="ProcEaze partners and integrations: technology, ERP, supplier and business partners building a connected procurement ecosystem. Become a partner.",
         section="partners", crumbs=[("Partners & Integrations", None)], body=partners_body),
]
