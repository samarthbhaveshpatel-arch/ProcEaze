"""Procurement Services: the services hub (formerly Engagement Models) and three service pages.

Every claim here follows what the rest of the site already says. Managed Procurement:
choose ProcEaze as the vendor on a requisition, it goes straight to purchase approval in
your hierarchy, and ProcEaze handles sourcing, pricing and fulfilment from its own
catalogue. Links are built with L() inside the body functions only (render time).
"""
from lib import (icon, icon_tile, badge, esc, L, section_head, page_hero, btn_demo, btn_link,
                 feature_cards, workflow, benefits, challenge_list, check_list, related, BASE_URL)
from pages_company import COMPARE
import mockups as M
import blocks as B
import signature as S


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------
def service_schema(path, name, service_type, description):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "serviceType": service_type,
        "description": description,
        "url": BASE_URL + "/" + path,
        "provider": {"@type": "Organization", "name": "ProcEaze", "url": BASE_URL + "/"},
        "areaServed": {"@type": "Country", "name": "India"},
    }


def faq_schema(items):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items],
    }


def faq_section(uid, title, items, lead=None, cls="section"):
    """Accordion FAQ (same markup as the FAQ page, ids prefixed per page)."""
    qs = "".join(
        f'<div class="faq-item"><h3 style="margin:0;font-size:inherit"><button class="faq-q" type="button" aria-expanded="false" '
        f'aria-controls="{uid}-a-{i}" id="{uid}-q-{i}">{esc(q)}<span class="faq-icon">{icon("plus")}</span></button></h3>'
        f'<div class="faq-a" id="{uid}-a-{i}" role="region" aria-labelledby="{uid}-q-{i}"><div><p>{esc(a)}</p></div></div></div>'
        for i, (q, a) in enumerate(items, 1))
    return (f'<section class="{cls}" id="faq"><div class="container">'
            + section_head("FAQ", title, lead, center=True)
            + f'<div class="faq reveal" style="max-width:860px;margin-inline:auto">{qs}</div>'
            + f'<p class="center small muted mt-32">More questions? See all <a href="{L("faq.html")}">FAQs</a> or '
            f'<a href="{L("contact.html")}">ask our team</a>.</p></div></section>')


def compare_table(caption, heads, rows):
    """A three-column comparison table using the site's .compare styles."""
    th = "".join(f'<th scope="col" class="col-head">{h}</th>' for h in heads[1:])
    body = "".join(f'<tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td></tr>' for a, b, c in rows)
    return (f'<div class="compare-wrap reveal"><table class="compare"><caption class="sr-only">{esc(caption)}</caption>'
            f'<thead><tr><th scope="col">{heads[0]}</th>{th}</tr></thead><tbody>{body}</tbody></table></div>')


def cta_band(title, text, interest="Managed Procurement"):
    return (f'<section class="section section-light section-tight"><div class="container"><div class="split">'
            f'<div>{section_head("Next step", title, text)}</div>'
            f'<div class="btn-row reveal" style="justify-content:flex-end">{btn_demo("Talk through your scope", "btn-primary btn-lg", interest)}'
            f'{btn_link("request-a-demo/", "Request a demo", "btn-secondary btn-lg")}</div></div></div></section>')


# ---------------------------------------------------------------------------
# Hub: Procurement Services (replaces Engagement Models)
# ---------------------------------------------------------------------------
HUB_FAQ = [
    ("What are procurement services?",
     "Procurement services cover the work of buying for an organisation: finding and pricing items, raising and approving requisitions, issuing orders and getting goods delivered. "
     "ProcEaze offers this two ways: as a platform your own team runs, or as Managed Procurement, where ProcEaze supplies for you."),
    ("What is the difference between the ProcEaze Platform and Managed Procurement?",
     "With the Platform (SaaS), your teams run procurement on ProcEaze with your own vendors and their ARC prices. With Managed Procurement, you choose ProcEaze as the vendor on a requisition "
     "and ProcEaze handles sourcing, pricing and fulfilment. Both run on the same platform, with the same approvals, dashboards and audit trail."),
    ("Who is Managed Procurement best suited to?",
     "Companies wanting to outsource indirect / MRO buying. Enterprises with an in-house procurement team usually start with the Platform."),
    ("Do requisitions placed with ProcEaze still go through our approvals?",
     "Yes. A requisition placed with ProcEaze as the vendor goes straight to purchase approval in your own hierarchy, configured from one level to five."),
    ("How much do ProcEaze procurement services cost?",
     "We don't publish numerical pricing. Commercials depend on your engagement model and scope, and are shared on request."),
    ("Who supports us after onboarding?",
     "Every client gets a dedicated Key Account Manager who configures your catalogue, loads ARC prices, MOQs and contract validity, and handles renewals and price updates."),
]

HUB_DESC = ('ProcEaze procurement services: run buying on our platform with your own vendors, or outsource indirect and MRO buying to Managed Procurement, with a KAM.')


def hub_body():
    hero = page_hero(
        [("Procurement Services", None)], "Procurement services",
        "Procurement services, run your way.",
        "Run procurement yourself on the ProcEaze platform, or let ProcEaze supply for you through Managed Procurement. "
        "Both run on the same platform, with the same approvals, dashboards and audit trail, and every client gets a dedicated Key Account Manager.",
        actions=btn_demo("Contact Us", "btn-primary btn-lg magnetic", "Managed Procurement")
                + '<a class="btn btn-secondary btn-lg" href="#compare">Compare side by side</a>',
        visual=M.browser("app.proceaze.in/cart", M.cart_requisition(), aria="Illustrative requisition screen"))
    out = hero

    # The three service pages, up front
    services = [
        dict(icon="repeat", title="End-to-End Procurement Services",
             text="From requisition to delivery. Your team approves; ProcEaze handles sourcing, pricing and fulfilment, with every step on one record.",
             href="services/end-to-end-procurement-services/", cta="End-to-end services"),
        dict(icon="building", title="B2B & Corporate Procurement Services",
             text="Indirect and MRO buying for plants, sites and corporate offices, with approvals that follow your Delegation of Authority.",
             href="services/b2b-procurement-services/", cta="B2B & corporate services"),
        dict(icon="lock", title="ARC-Based Procurement Services",
             text="Annual rate contracts loaded into your catalogue, prices locked at order, and renewals tracked by your Key Account Manager.",
             href="services/arc-procurement-services/", cta="ARC-based services"),
    ]
    out += (f'<section class="section"><div class="container">'
            + section_head("Our services", "Managed procurement services for indirect and MRO buying.",
                           "Three ways ProcEaze takes work off your procurement team, each built on the same platform and the same controls.")
            + feature_cards(services) + '</div></section>')

    # Two ways to work with ProcEaze (the visual switch). On this page its
    # "Compare engagement models" link would point at itself, so aim it at the table.
    out += S.engagement_section("section section-light").replace(
        f'href="{L("engagement-models.html")}"', 'href="#compare"')

    # Side-by-side comparison
    rows = "".join(f'<tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td></tr>' for a, b, c in COMPARE)
    table = (f'<div class="compare-wrap reveal"><table class="compare"><caption class="sr-only">ProcEaze Platform compared with ProcEaze Managed Procurement</caption>'
             f'<thead><tr><th scope="col">Compare</th><th scope="col" class="col-head">ProcEaze Platform <span class="badge badge-ready" style="margin-left:6px">SaaS</span></th>'
             f'<th scope="col" class="col-head">ProcEaze Managed Procurement</th></tr></thead><tbody>{rows}</tbody></table></div>')
    out += (f'<section class="section" id="compare"><div class="container">'
            + section_head("Side by side", "Platform SaaS vs managed procurement services.",
                           "We don't publish numerical pricing. Commercials depend on your scope and are shared on request.")
            + table + '</div></section>')

    # Procurement outsourcing without losing control
    out += (f'<section class="section section-light"><div class="container"><div class="split" style="align-items:start">'
            f'<div>{section_head("Procurement outsourcing", "Outsource the buying. Keep the control.", "Managed Procurement works inside the platform. On a requisition, ProcEaze can be chosen as the vendor. It goes straight to purchase approval in your hierarchy, and ProcEaze handles sourcing, pricing and fulfilment.")}'
            f'<div class="btn-row">{btn_link("how-it-works.html", "See how it works", "btn-secondary btn-lg")}</div></div>'
            f'<div class="grid grid-2">'
            f'<article class="card card-flat reveal"><div class="card-head">{icon_tile("store")}</div><h3>ProcEaze handles</h3>'
            + check_list(["Sourcing for requisitions placed with ProcEaze", "Pricing, from ProcEaze's own catalogue", "Fulfilment through to delivery",
                          "Catalogue set-up and updates, by your KAM"])
            + f'</article><article class="card card-flat reveal" style="--d:1"><div class="card-head">{icon_tile("shield-check")}</div><h3>You keep</h3>'
            + check_list(["Purchase approval in your own 1–5 level hierarchy", "Role-based dashboards and spend analytics",
                          "A permanent, downloadable audit trail", "Complete data isolation for your company"])
            + '</article></div></div></div></section>')

    # How a managed requisition moves
    out += (f'<section class="section"><div class="container">'
            + section_head("How it works", "How a requisition placed with ProcEaze moves.", "The same flow your teams already use, with ProcEaze as the vendor.", center=True)
            + workflow([("cart", "Requisition", "Raised from the catalogue"),
                        ("store", "ProcEaze as vendor", "Chosen on the requisition"),
                        ("check-circle", "Purchase approval", "Through your hierarchy"),
                        ("package", "Sourcing & pricing", "Handled by ProcEaze"),
                        ("truck", "Fulfilment", "Tracked to delivery"),
                        ("history", "On record", "Every step in the audit trail")])
            + '</div></section>')

    out += S.kam_section("section section-light")
    out += faq_section("svc", "Procurement services: common questions", HUB_FAQ)
    out += related(["platform.html", "procure-to-pay-software/", "arc-pricing.html", "how-it-works.html", "request-a-demo/", "faq.html"], "Related")
    return out


# ---------------------------------------------------------------------------
# End-to-End Procurement Services
# ---------------------------------------------------------------------------
E2E_FAQ = [
    ("What are end-to-end procurement services?",
     "End-to-end procurement services cover the full cycle of a purchase: the requisition, its approval, sourcing and pricing, fulfilment, delivery and the record that proves it all happened. "
     "With ProcEaze Managed Procurement, your team raises and approves the requisition, and ProcEaze handles sourcing, pricing and fulfilment."),
    ("What does ProcEaze handle, and what stays with us?",
     "ProcEaze handles sourcing, pricing and fulfilment for requisitions placed with ProcEaze, from ProcEaze's own catalogue. Your team keeps the requisition, the purchase approval in your own hierarchy, "
     "and full visibility through dashboards and the audit trail."),
    ("Do our approval rules still apply?",
     "Yes. A requisition placed with ProcEaze goes straight to purchase approval in your hierarchy, configured from one to five levels to match your Delegation of Authority."),
    ("Which items can ProcEaze supply?",
     "Managed Procurement supplies from ProcEaze's own catalogue and suits indirect / MRO buying. Your Key Account Manager will confirm which categories and items are set up for your sites."),
    ("Does the service include payment and invoice matching?",
     "Not yet. Payment & Reconciliation, including payment gateway and invoice matching, is on the roadmap."),
    ("Can it connect to our ERP?",
     "ProcEaze is ERP plug-in ready. Integration with SAP and other ERPs is scoped during onboarding, including what data moves and in which direction."),
]

E2E_DESC = ('End-to-end procurement services: you raise and approve the requisition; ProcEaze handles sourcing, pricing and fulfilment through to delivery, on one record.')


def e2e_body():
    hero = page_hero(
        [("Procurement Services", "services/"), ("End-to-End Procurement Services", None)], "End-to-end procurement services",
        "End-to-end procurement services, from requisition to delivery.",
        "With ProcEaze Managed Procurement, your teams raise the requisition and approve it in your own hierarchy. "
        "ProcEaze handles sourcing, pricing and fulfilment, and every step stays on one record.",
        actions=btn_demo("Contact Us", "btn-primary btn-lg magnetic", "Managed Procurement")
                + '<a class="btn btn-secondary btn-lg" href="#process">See the process</a>',
        visual=M.browser("app.proceaze.in/cart", M.cart_requisition(), aria="Illustrative requisition screen with ProcEaze as the vendor"))
    out = hero

    # The problem
    out += (f'<section class="section"><div class="container"><div class="split">'
            f'<div>{section_head("The problem", "Indirect buying has too many hand-offs.", "A single requisition for safety shoes or bearings can pass through emails, phone calls, quotes and follow-ups before anything arrives. Nobody owns it end to end, and nothing is on one record.")}</div>'
            f'<div>{challenge_list([("Too many vendors for small orders", "Separate suppliers for PPE, electricals, stationery and spares, each with its own process."), ("Prices chased on every order", "Buyers ask, wait and compare before they can place a routine order."), ("No trail from request to delivery", "Requests by email or WhatsApp leave no record of who asked, who approved and what arrived.")])}</div>'
            f'</div></div></section>')

    # The process
    out += (f'<section class="section section-light" id="process"><div class="container">'
            + section_head("The process", "The end-to-end procurement process, step by step.",
                           "Managed Procurement runs inside the ProcEaze platform, so every stage uses the same approvals, dashboards and audit trail as the rest of your buying.", center=True)
            + workflow([("cart", "Requisition", "Raised from the catalogue, with ProcEaze as the vendor"),
                        ("check-circle", "Approval", "Purchase approval in your 1–5 level hierarchy"),
                        ("package", "Sourcing & pricing", "Handled by ProcEaze"),
                        ("store", "Fulfilment", "Supplied by ProcEaze"),
                        ("truck", "Delivery", "Order tracked through to delivery"),
                        ("history", "Audit trail", "Every step time-stamped and attributed")])
            + '</div></section>')

    # Who does what
    rows = [
        ("Requisition", "Raised by your buyer from the catalogue. ProcEaze is chosen as the vendor.", "Supplies from ProcEaze's own catalogue."),
        ("Approval", "Your approvers decide, in your own hierarchy of one to five levels.", "Nothing moves until your approval is complete."),
        ("Sourcing & pricing", "No RFQs or quote chasing for your team.", "Handles sourcing and pricing for the requisition."),
        ("Fulfilment & delivery", "Follows the order status in the platform.", "Handles fulfilment through to delivery."),
        ("Record & reporting", "Role-based dashboards, spend analytics and a downloadable audit trail.", "Your Key Account Manager stays your single point of contact."),
    ]
    out += (f'<section class="section"><div class="container">'
            + section_head("Who does what", "Managed procurement services, with clear ownership.",
                           "End to end does not mean out of sight. Here is what your team does at each stage, and what ProcEaze does.")
            + compare_table("Who does what at each stage of end-to-end procurement", ["Stage", "Your team", "ProcEaze"], rows)
            + '</div></section>')

    # What's included
    out += (f'<section class="section section-light"><div class="container">'
            + section_head("What's included", "What end-to-end procurement outsourcing includes.", None, center=True)
            + feature_cards([
                dict(icon="store", title="ProcEaze as the vendor", text="Choose ProcEaze on a requisition. It goes straight to purchase approval in your hierarchy."),
                dict(icon="package", title="Sourcing & pricing", text="ProcEaze handles sourcing and pricing for requisitions placed with ProcEaze, from its own catalogue."),
                dict(icon="truck", title="Fulfilment & tracking", text="ProcEaze fulfils the order, and your team follows it through to delivery."),
                dict(icon="network", title="Your approvals", text="One to five levels, set to your Delegation of Authority. Approve, reject or send back in one click."),
                dict(icon="bar-chart", title="Dashboards", text="The same role-based dashboards, including spend placed with ProcEaze."),
                dict(icon="headset", title="Dedicated KAM", text="A named Key Account Manager for configuration, updates and escalations."),
            ]) + '</div></section>')

    # Inside the product
    out += (f'<section class="section"><div class="container">'
            + B.spotlight("Inside the product", "One requisition, one record, start to finish.",
                          "The cart checks every line before it is submitted and shows the approval route. Once approved, the order is tracked to delivery, and the whole history stays in the audit trail.",
                          ["Cart validation before submission", "Approval route shown up front", "Requisition, approval and order on one record"],
                          M.browser("app.proceaze.in/approvals", M.approvals(), aria="Illustrative approval chain screen"),
                          btn_demo("See it in a demo", "btn-primary btn-lg", "Managed Procurement"), reverse=True)
            + '</div></section>')

    # Honest scope
    out += (f'<section class="section section-light"><div class="container"><div class="split">'
            f'<div>{section_head("Where it ends today", "What end to end covers now, and what is next.", "We label what is live and what is planned, so you can plan around it.")}</div>'
            f'<div class="stack">'
            f'<div class="notice info reveal">{icon("check-circle")}<p><strong>Live today:</strong> requisition, purchase approval, sourcing, pricing and fulfilment by ProcEaze, order tracking, dashboards and a permanent audit trail.</p></div>'
            f'<div class="notice info reveal">{icon("info")}<p><strong>Payment & Reconciliation</strong>, including payment gateway and invoice matching, is planned. {badge("roadmap")}</p></div>'
            f'<div class="notice info reveal">{icon("info")}<p><strong>ERP integration</strong> is scoped during onboarding, including what data moves and in which direction. {badge("ready", text="Plug-in ready")}</p></div>'
            f'</div></div></div></section>')

    out += (f'<section class="section section-tight"><div class="container">'
            + section_head("Benefits", "What changes for your teams.", None)
            + benefits([("clock", "Less chasing", "No quote rounds for requisitions placed with ProcEaze."),
                        ("network", "Control kept", "Your approvals decide every order."),
                        ("eye", "One view", "Spend with ProcEaze on the same dashboards."),
                        ("history", "Audit-ready", "Every step on the record.")])
            + '</div></section>')

    out += faq_section("e2e", "End-to-end procurement services: FAQs", E2E_FAQ, cls="section section-light")
    out += related(["services/", "services/b2b-procurement-services/", "services/arc-procurement-services/",
                    "procure-to-pay-software/", "procurement-automation/", "how-it-works.html"], "Related services and software")
    return out


# ---------------------------------------------------------------------------
# B2B & Corporate Procurement Services
# ---------------------------------------------------------------------------
B2B_CATEGORIES = [("hard-hat", "Safety & PPE"), ("wrench", "MRO"), ("zap", "Electricals"), ("nut", "Fasteners"),
                  ("bearing", "Bearings & Power Transmission"), ("notebook", "Paper & Stationery"), ("pen", "Office Supplies"),
                  ("laptop", "IT & Electronics"), ("hammer", "Hand Tools"), ("cog", "Industrial Plants & Machinery")]

B2B_FAQ = [
    ("What are B2B procurement services?",
     "B2B procurement services help one business buy what it needs from others: finding items, getting the right price, routing approvals, placing orders and getting goods delivered. "
     "ProcEaze provides this through its platform, or through Managed Procurement, where ProcEaze supplies for you."),
    ("What are corporate procurement services?",
     "Corporate procurement services cover company-wide buying of indirect goods for offices, plants and sites. With ProcEaze, every department orders from one catalogue, "
     "approvals follow your Delegation of Authority, and leadership sees spend on live dashboards."),
    ("Which categories can we buy?",
     "The ProcEaze platform covers 5,00,000+ products across 56+ categories, including safety & PPE, MRO, electricals, fasteners, bearings, stationery, office supplies, IT, hand tools and industrial machinery. "
     "Your catalogue is configured for your company by your Key Account Manager."),
    ("Can different departments and sites have different approvers?",
     "Yes. Departments, users, roles and approval chains of one to five levels are set up for your organisation during onboarding."),
    ("Do we need our own vendors?",
     "Not for Managed Procurement: you choose ProcEaze as the vendor and ProcEaze handles sourcing, pricing and fulfilment. On the Platform, your teams buy from your own vendors at their ARC prices."),
    ("How is ProcEaze priced for corporate buyers?",
     "Pricing is on request. It depends on your engagement model and scope, and our team will talk it through with you."),
]

B2B_DESC = ('B2B and corporate procurement services for Indian companies: indirect and MRO buying for plants and offices, 1–5 level approvals and a dedicated KAM.')


def b2b_body():
    hero = page_hero(
        [("Procurement Services", "services/"), ("B2B Procurement Services", None)], "B2B & corporate procurement services",
        "B2B procurement services for plants, sites and corporate offices.",
        "ProcEaze takes the effort out of indirect and MRO buying for Indian businesses. Run it on the platform with your own vendors, "
        "or let ProcEaze supply for you, with your approvals and your visibility intact.",
        actions=btn_demo("Contact Us", "btn-primary btn-lg magnetic", "Managed Procurement")
                + '<a class="btn btn-secondary btn-lg" href="#corporate">Corporate procurement</a>',
        visual=M.browser("app.proceaze.in/catalogue", M.catalogue_arc(), aria="Illustrative B2B catalogue with contracted prices"))
    out = hero

    # What B2B procurement services cover
    cats = "".join(f'<li class="reveal" style="--d:{i % 4}">{icon_tile(ic)}{esc(n)}</li>' for i, (ic, n) in enumerate(B2B_CATEGORIES))
    out += (f'<section class="section"><div class="container"><div class="split" style="align-items:start">'
            f'<div>{section_head("What we cover", "B2B procurement services for indirect and MRO spend.", "Indirect and MRO buying is high in volume and low in visibility. Most of the effort goes into finding items, prices and approvers, not into the purchase itself.")}'
            f'<div class="stack reveal"><p>ProcEaze brings that buying into one place: 5,00,000+ products across 56+ categories, contracted prices on the product, cart validation, '
            f'one-click requisitions and approvals that route themselves. The categories below form the core of a typical catalogue.</p>'
            f'<a class="link-arrow" href="{L("categories.html")}">Browse categories {icon("arrow-right")}</a></div></div>'
            f'<ul class="get-list">{cats}</ul></div></div></section>')

    # Corporate procurement services (secondary keyword, prominent)
    out += (f'<section class="section section-light" id="corporate"><div class="container">'
            + section_head("Corporate procurement", "Corporate procurement services for every department.",
                           "Corporate purchasing spans offices, plants, sites and departments, each with its own requesters and approvers. "
                           "ProcEaze gives them one catalogue and one set of rules, and gives leadership one view of the spend.", center=True)
            + feature_cards([
                dict(icon="grid", title="One catalogue for every site", text="Plants, offices and project sites order from the same catalogue, configured for your company."),
                dict(icon="network", title="Approvals to your DoA", text="Chains of one to five levels, built around your Delegation of Authority."),
                dict(icon="users", title="Departments and roles", text="Users, departments and roles are set up during onboarding, so each team sees its own queue."),
                dict(icon="stamp", title="NFAs and POs", text="Notes for Approval and purchase orders run through the same hierarchy."),
                dict(icon="bar-chart", title="Spend by department", text="Role-based dashboards show spend by plant, department, category and vendor."),
                dict(icon="landmark", title="Clean records for finance", text="Every order, approval and rejection is time-stamped and downloadable."),
            ])
            + f'<p class="center small muted mt-32">Running corporate offices or facilities? See <a href="{L("industries/facility-management.html")}">procurement for facility management &amp; corporate offices</a>.</p>'
            + '</div></section>')

    # Two ways to buy
    out += (f'<section class="section"><div class="container">'
            + section_head("Two ways to work with us", "Indirect procurement services, or your own platform.",
                           "Bring your own vendors and ARC prices to the platform, or let ProcEaze supply for you. Both run on the same platform, with the same approvals and visibility.")
            + B.engagement_cards()
            + f'<p class="center small muted mt-32"><a href="{L("services/")}#compare">Compare both models side by side</a></p>'
            + '</div></section>')

    # Control
    out += (f'<section class="section section-light"><div class="container"><div class="split">'
            f'<div>{section_head("Control by design", "Corporate purchasing that stands up to audit.", "B2B buying involves commercially sensitive data: prices, vendors and approvals. ProcEaze keeps each client separate and records every action.")}'
            + check_list(["Complete data isolation for every client", "Passwordless OTP sign-in for every user", "Role-based access to orders, approvals and spend",
                          "A permanent, downloadable audit trail", "Email notifications as requests move"])
            + f'<a class="link-arrow mt-24" href="{L("security.html")}">Read about security {icon("arrow-right")}</a></div>'
            f'<div class="reveal-frame">{M.browser("app.proceaze.in/approvals", M.approvals(), aria="Illustrative approval chain screen")}</div></div></div></section>')

    # Who it suits
    out += (f'<section class="section section-tight"><div class="container">'
            + section_head("Who it suits", "Built for how Indian businesses buy.", None)
            + benefits([("factory", "Manufacturing & process plants", "MRO, spares and consumables across plants."),
                        ("construction", "Infrastructure & construction", "Supplies for project sites."),
                        ("anchor", "Logistics, ports & ICDs", "Indirect buying for operations."),
                        ("office", "Corporate offices", "Stationery, IT and office supplies.")])
            + '</div></section>')

    out += B.kam_section("section section-light")
    out += faq_section("b2b", "B2B and corporate procurement services: FAQs", B2B_FAQ)
    out += related(["services/", "services/end-to-end-procurement-services/", "services/arc-procurement-services/",
                    "platform.html", "e-procurement-software/", "categories.html"], "Related services and software")
    return out


# ---------------------------------------------------------------------------
# ARC-Based Procurement Services
# ---------------------------------------------------------------------------
ARC_FAQ = [
    ("What is an annual rate contract (ARC)?",
     "An annual rate contract is an agreement with a vendor that fixes prices for a set of items for a period, usually a year. Buyers then order against those rates as needs arise, "
     "instead of asking for a fresh quote each time."),
    ("What are ARC procurement services?",
     "ARC procurement services cover the work of running rate contracts day to day: loading contract prices, MOQs and validity into the catalogue, making sure orders use those prices, "
     "and tracking renewals. At ProcEaze, your Key Account Manager does this, and the platform locks the ARC price at the point of order."),
    ("Can a buyer change an ARC price at order?",
     "No. The ARC price is applied automatically and cannot be edited in the cart. 100% of catalogue requisitions are priced at ARC rates."),
    ("What happens when a rate contract is due for renewal?",
     "Your Key Account Manager handles renewals and price updates before contracts lapse, so orders don't continue at old or unagreed prices."),
    ("How are items outside the rate contract bought?",
     "Off-contract items are routed to RFQ instead of ad-hoc buying. Reverse auctions and the AI Price Negotiator (early access) add further routes, and ProcEaze can also be chosen as the vendor through Managed Procurement."),
    ("Does ProcEaze negotiate our rate contracts with vendors?",
     "ARC terms are agreed between you and your vendors; ProcEaze loads them and enforces them at order. If you want support with sourcing or renewing a contract, talk it through with our team."),
]

ARC_DESC = ('ARC procurement services: your KAM loads annual rate contract prices, MOQs and validity, prices lock at order, and renewals are tracked before they lapse.')


def arc_body():
    hero = page_hero(
        [("Procurement Services", "services/"), ("ARC-Based Procurement Services", None)], "ARC-based procurement services",
        "ARC procurement services that keep your rate contracts working.",
        "An annual rate contract is only worth what reaches the purchase order. Your Key Account Manager loads ARC prices, MOQs and validity into your catalogue, "
        "the platform locks the price at order, and renewals are handled before contracts lapse.",
        actions=btn_demo("Contact Us", "btn-primary btn-lg magnetic", "Platform SaaS")
                + '<a class="btn btn-secondary btn-lg" href="#lifecycle">See the ARC lifecycle</a>',
        visual=M.browser("app.proceaze.in/contracts", M.arc_contracts(), aria="Illustrative ARC contract register"))
    out = hero

    # The problem
    out += (f'<section class="section"><div class="container"><div class="split">'
            f'<div>{section_head("The problem", "Why annual rate contract procurement breaks down.", "Procurement negotiates the rate. Then it has to survive every buyer, every site and every order for a year.")}</div>'
            f'<div>{challenge_list([("Rates live in spreadsheets", "Buyers cannot see the ARC, so orders go out at whatever price is quoted."), ("Expiry goes unnoticed", "Contracts lapse quietly and orders continue at old or unagreed prices."), ("Compliance is hard to prove", "Finance cannot show that orders matched the contract without manual checks.")])}</div>'
            f'</div></div></section>')

    # Lifecycle
    out += (f'<section class="section section-light" id="lifecycle"><div class="container">'
            + section_head("The ARC lifecycle", "Annual rate contract procurement services, from contract to renewal.",
                           "You agree ARC terms with your vendors. From there, ProcEaze and your Key Account Manager carry the contract through every order until it is renewed.", center=True)
            + workflow([("file-text", "Contract agreed", "ARC terms finalised with your vendors"),
                        ("headset", "KAM loads it", "Prices, MOQs and validity configured"),
                        ("cart", "Buyer orders", "ARC price applied automatically"),
                        ("check-circle", "Approval", "Routes through your hierarchy"),
                        ("file-check", "PO at ARC", "Issued at the contracted rate"),
                        ("refresh", "Renewal", "Tracked and handled by your KAM")])
            + '</div></section>')

    # Locked price (signature section, id="arc")
    out += S.arc_section("section")

    # Rate contract management by your KAM
    out += (f'<section class="section section-light"><div class="container">'
            + B.spotlight("Rate contract management", "Rate contract management, handled by your KAM.",
                          "Your Key Account Manager keeps the contract register current: what is loaded, how long each contract runs and which renewals are due. You see the same register in the platform.",
                          ["ARC prices, MOQs and contract validity loaded", "Renewals and price updates before contracts lapse",
                           "New items and catalogue changes on request"],
                          M.kam_card(), btn_link("arc-pricing.html", "Explore rate contract management", "btn-primary btn-lg"), reverse=True)
            + '</div></section>')

    # What's included
    out += (f'<section class="section"><div class="container">'
            + section_head("What's included", "What ARC-based procurement services include.", None, center=True)
            + feature_cards([
                dict(icon="lock", title="Locked ARC price", text="The contracted price is applied automatically and cannot be edited at order."),
                dict(icon="package", title="MOQ on every item", text="Minimum order quantities are shown on the product and validated in the cart."),
                dict(icon="calendar", title="Contract validity", text="Each ARC item shows how long its contract runs."),
                dict(icon="refresh", title="Renewals handled", text="Your KAM manages renewals and price updates before contracts lapse."),
                dict(icon="pie-chart", title="ARC utilisation", text="Dashboards show how much catalogue spend runs on contracted prices."),
                dict(icon="history", title="Compliance on record", text="Every requisition, approval and PO is time-stamped and downloadable for audit."),
            ]) + '</div></section>')

    # Off-contract routes
    routes = [
        ("clipboard-list", "RFQ", None, "Items outside the contract go to RFQ instead of ad-hoc buying, then through NFA approval to a PO."),
        ("gavel", "Reverse auction", None, "Live competitive bidding for requirements where competition helps the price."),
        ("bot", "AI negotiation", "early", "An AI agent negotiates with vendors against your target price. The buyer stays in control."),
        ("store", "ProcEaze as vendor", None, "Choose ProcEaze on the requisition through Managed Procurement. It goes straight to purchase approval."),
    ]
    cards = "".join(f'<article class="card card-hover feature-card reveal" style="--d:{i % 4}"><div class="card-head">{icon_tile(ic)}{badge(st)}</div>'
                    f'<h3>{t}</h3><p>{d}</p></article>' for i, (ic, t, st, d) in enumerate(routes))
    out += (f'<section class="section section-light"><div class="container">'
            + section_head("Off-contract buying", "When an item is not on the rate contract.",
                           "Not everything is on an ARC. Off-contract needs are routed, not improvised, so they stay inside your approvals.", center=True)
            + f'<div class="grid grid-4">{cards}</div></div></section>')

    # Resources (guide + template are not in related()'s lookup for the guide, so link directly)
    out += (f'<section class="section"><div class="container">'
            + section_head("Planning a rate contract?", "Annual rate contract resources.", "A practical guide and a ready template, free to use.")
            + f'<div class="grid grid-2">'
            f'<a class="card card-hover card-link reveal" href="{L("knowledge-hub/procurement-guides/annual-rate-contract-procurement/")}">'
            f'<div class="card-head">{icon_tile("book-open")}</div><h3>Annual rate contract procurement: a guide</h3>'
            f'<p>How ARCs work, what to include and how to keep them running through the year.</p><span class="link-arrow">Read the guide {icon("arrow-right")}</span></a>'
            f'<a class="card card-hover card-link reveal" style="--d:1" href="{L("tools/annual-rate-contract-template/")}">'
            f'<div class="card-head">{icon_tile("file-text")}</div><h3>Annual Rate Contract Template</h3>'
            f'<p>A ready ARC structure to download and adapt for your vendors.</p><span class="link-arrow">Get the template {icon("arrow-right")}</span></a>'
            f'</div></div></section>')

    out += faq_section("arc", "ARC procurement services: FAQs", ARC_FAQ, cls="section section-light")
    out += related(["services/", "services/end-to-end-procurement-services/", "services/b2b-procurement-services/",
                    "arc-pricing.html", "dashboards.html", "tools/annual-rate-contract-template/"], "Related services and software")
    return out


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
PAGES = [
    dict(path="services/", title="Procurement Services: Platform or Managed | ProcEaze",
         desc=HUB_DESC, section="services", crumbs=[("Procurement Services", None)], body=hub_body,
         schemas=[service_schema("services/", "ProcEaze Procurement Services", "Procurement services", HUB_DESC), faq_schema(HUB_FAQ)]),
    dict(path="services/end-to-end-procurement-services/", title="End-to-End Procurement Services in India | ProcEaze",
         desc=E2E_DESC, section="services",
         crumbs=[("Procurement Services", "services/"), ("End-to-End Procurement Services", None)], body=e2e_body,
         schemas=[service_schema("services/end-to-end-procurement-services/", "End-to-End Procurement Services",
                                 "End-to-end procurement services", E2E_DESC), faq_schema(E2E_FAQ)]),
    dict(path="services/b2b-procurement-services/", title="B2B Procurement Services & Corporate Procurement | ProcEaze",
         desc=B2B_DESC, section="services",
         crumbs=[("Procurement Services", "services/"), ("B2B Procurement Services", None)], body=b2b_body,
         schemas=[service_schema("services/b2b-procurement-services/", "B2B & Corporate Procurement Services",
                                 "B2B procurement services", B2B_DESC), faq_schema(B2B_FAQ)]),
    dict(path="services/arc-procurement-services/", title="ARC Procurement Services: Annual Rate Contracts | ProcEaze",
         desc=ARC_DESC, section="services",
         crumbs=[("Procurement Services", "services/"), ("ARC-Based Procurement Services", None)], body=arc_body,
         schemas=[service_schema("services/arc-procurement-services/", "ARC-Based Procurement Services",
                                 "Annual rate contract procurement services", ARC_DESC), faq_schema(ARC_FAQ)]),
]
