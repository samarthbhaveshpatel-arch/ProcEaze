"""Software Solutions pages (SEO structure, section 2).

Four keyword landing pages, each with a distinct angle so they don't compete:
  procurement-management-software/  the system of record for the procurement function
  e-procurement-software/           moving buying online, instead of email, WhatsApp and Excel
  procurement-automation/           what the system automates, and what people still decide
  procure-to-pay-software/          requisition -> approval -> PO -> delivery on one record

Platform features live here as sections (per the SEO plan) and link to the deeper
capability pages. Every claim mirrors what the rest of the site already states.
Links are only built inside the body functions, at render time.
"""
from lib import (icon, icon_tile, esc, badge, section_head, page_hero, hero_actions, btn_link,
                 feature_cards, workflow, benefits, challenge_list, check_list, related)
import mockups as M
import blocks as B


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------
def _prose(*paras):
    return '<div class="prose reveal">' + "".join(f"<p>{p}</p>" for p in paras) + '</div>'


def _intro(eyebrow, title, paras, problems, problems_title):
    """'What is ...' section: definition copy on the left, the pain it solves on the right."""
    return (f'<section class="section"><div class="container"><div class="split">'
            f'<div>{section_head(eyebrow, title)}{_prose(*paras)}</div>'
            f'<div><h3 class="mt-16">{problems_title}</h3>{challenge_list(problems)}</div>'
            f'</div></div></section>')


def _feature(fid, eyebrow, title, lead, points, visual, cta, cls="section", reverse=False, status=None, after=""):
    """A platform-feature section (H2) with a stable id for deep links."""
    return (f'<section class="{cls}" id="{fid}"><div class="container">'
            + B.spotlight(eyebrow, title, lead, points, visual, cta, reverse=reverse, status=status)
            + after + '</div></section>')


def _notice(html):
    return f'<div class="notice info reveal mt-32">{icon("info")}<p>{html}</p></div>'


def _table(caption, head, rows):
    col = ' class="col-head"'
    ths = "".join(f'<th scope="col"{col if i else ""}>{h}</th>' for i, h in enumerate(head))
    trs = "".join('<tr><th scope="row">' + r[0] + '</th>' + "".join(f"<td>{c}</td>" for c in r[1:]) + '</tr>' for r in rows)
    return (f'<div class="compare-wrap reveal"><table class="compare"><caption class="sr-only">{esc(caption)}</caption>'
            f'<thead><tr>{ths}</tr></thead><tbody>{trs}</tbody></table></div>')


def _faq(prefix, items, title):
    qs = []
    for n, (q, a) in enumerate(items, 1):
        qs.append(f'<div class="faq-item"><h3 style="margin:0;font-size:inherit"><button class="faq-q" type="button" aria-expanded="false" '
                  f'aria-controls="{prefix}-a-{n}" id="{prefix}-q-{n}">{esc(q)}<span class="faq-icon">{icon("plus")}</span></button></h3>'
                  f'<div class="faq-a" id="{prefix}-a-{n}" role="region" aria-labelledby="{prefix}-q-{n}"><div><p>{esc(a)}</p></div></div></div>')
    return (f'<section class="section" id="faqs"><div class="container">'
            + section_head("FAQs", title, None, center=True)
            + f'<div class="faq" style="max-width:860px;margin-inline:auto">{"".join(qs)}</div></div></section>')


def _faq_schema(items):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items],
    }


def _split_lists(eyebrow, title, lead, left_title, left, right_title, right, cls="section section-light"):
    return (f'<section class="{cls}"><div class="container">'
            + section_head(eyebrow, title, lead, center=True)
            + f'<div class="grid grid-2">'
            f'<article class="card reveal"><h3>{left_title}</h3>{check_list(left)}</article>'
            f'<article class="card reveal" style="--d:1"><h3>{right_title}</h3>{check_list(right)}</article>'
            f'</div></div></section>')


SIBLINGS = ["procurement-management-software/", "e-procurement-software/", "procurement-automation/", "procure-to-pay-software/"]


def _related(key, extra):
    return related([k for k in SIBLINGS if k != key] + extra, "Related software and capabilities")


# ---------------------------------------------------------------------------
# 1. Procurement Management Software
# ---------------------------------------------------------------------------
PMS_KEY = "procurement-management-software/"

PMS_FAQ = [
    ("What is procurement management software?",
     "Procurement management software is the system a company uses to run its procurement function: who its vendors are, what prices are agreed, what people can buy, who approves what, and what has been spent. ProcEaze does this for indirect and MRO procurement, with vendors, ARC prices, a contracted catalogue, requisitions, approvals, purchase orders and spend analytics in one workspace."),
    ("How is procurement management software different from e-procurement software?",
     "E-procurement software is about moving the act of buying online. Procurement management software is broader: it is the record of how the whole function runs, including vendors, contracts, roles, approval rules and spend. ProcEaze covers both, from the same workspace."),
    ("Can we keep working with our own vendors?",
     "Yes. On the ProcEaze Platform your teams buy from your own vendors. Your Key Account Manager loads their annual rate contract prices, MOQs and validity into your catalogue. You can also choose ProcEaze as the vendor on a requisition through Managed Procurement."),
    ("Does ProcEaze include supplier management?",
     "ProcEaze keeps your vendors and their contracted prices in your workspace, and every order and approval involving a vendor is recorded in the audit trail. Vendors who supply through ProcEaze are verified with documents such as GSTIN and PAN. The Vendor Portal, where vendors receive matched RFQs, join auctions and track POs, is part of the platform."),
    ("Does ProcEaze integrate with our ERP?",
     "ProcEaze is ERP plug-in ready. Integration with SAP and other ERPs is scoped during onboarding, so you can add ProcEaze without replacing your ERP."),
    ("How is ProcEaze set up for a new client?",
     "We issue client credentials, configure your catalogue and ARC prices, build your organisation hierarchy and approval chain, and assign a dedicated Key Account Manager."),
]


def pms_body():
    out = page_hero(
        [("Software", "platform.html"), ("Procurement Management Software", None)],
        "Procurement management software",
        "Procurement management software for the whole procurement function.",
        "ProcEaze is the system of record for indirect and MRO procurement: your vendors, rate contracts, catalogue, requests, "
        "approvals and spend, in one workspace with one login.",
        actions=hero_actions(),
        visual=M.browser("app.proceaze.in/dashboard", M.dashboard(), aria="Illustrative ProcEaze procurement dashboard"))

    out += _intro(
        "The basics", "What is procurement management software?",
        ["Procurement management software is where a company runs its procurement function. It holds the vendors you buy from, "
         "the prices you have agreed with them, the items people are allowed to order, the approval rules that apply and the record of what was bought.",
         "Without it, that information sits in different places: rate contracts in a spreadsheet, vendor details in someone's inbox, "
         "approvals on email and spend in month-end reports. Each piece works on its own. Together, they leave procurement without one version of the truth.",
         "ProcEaze brings it into one system. Your Key Account Manager (KAM) sets up your vendors' contracted prices, your catalogue and your "
         "approval hierarchy. From then on, every request, approval and purchase order runs through the same workspace, and every action is recorded."],
        [("Contracts in one file, vendors in another", "Nobody can see the agreed rate, the vendor and the approver in one place."),
         ("Rules that live in people's heads", "Who can approve what depends on who you ask."),
         ("Spend that arrives late", "Leadership sees what was bought only after it has been compiled.")],
        "Where procurement loses control")

    out += (f'<section class="section section-light"><div class="container">'
            + section_head("One system of record", "Everything your procurement function runs on.",
                           "Six parts of the function, managed in one procurement management system.", center=True)
            + feature_cards([
                dict(icon="store", title="Vendors & rate contracts", text="Your own vendors, with ARC prices, MOQs and validity loaded by your KAM.",
                     href="arc-pricing.html", cta="ARC contract pricing"),
                dict(icon="cart", title="Contracted catalogue", text="5,00,000+ products across 56+ categories, with your contract prices on the product.",
                     href="catalogue.html", cta="Catalogue & buying"),
                dict(icon="send", title="Requests", text="Purchase requisitions raised in one click from a validated cart."),
                dict(icon="network", title="Approvals", text="Chains of one to five levels that mirror your Delegation of Authority.",
                     href="approvals.html", cta="Approvals & DoA"),
                dict(icon="bar-chart", title="Visibility", text="Company-wide spend, ARC utilisation, category trends and approval turnaround, live.",
                     href="dashboards.html", cta="Spend management"),
                dict(icon="users", title="Roles & access", text="Directors, heads, managers, buyers and finance each see their own view, and only what their role allows.",
                     href="security.html", cta="Security & trust"),
            ]) + '</div></section>')

    out += _feature(
        "supplier-management", "Supplier management",
        "Supplier management: your vendors, on contract and on the record.",
        "Vendor management in ProcEaze starts with your own vendors and the prices you have agreed with them. "
        "Your KAM loads each vendor's ARC prices, MOQs and contract validity, and renewals are handled before contracts lapse. "
        "Every order and approval involving a vendor is kept in a permanent, time-stamped audit trail.",
        ["Your vendors' ARC prices, MOQs and validity loaded by your KAM",
         "Vendors supplying through ProcEaze verified with GSTIN, PAN, company registration and bank details",
         "Every vendor order and approval time-stamped in the audit trail",
         "Off-contract needs routed to RFQ, not to whoever answers the phone"],
        M.browser("app.proceaze.in/contracts", M.arc_contracts(), aria="Illustrative ARC contract register by vendor"),
        btn_link("vendor-portal.html", "Preview the Vendor Portal", "btn-primary btn-lg") + btn_link("vendors.html", "Become a vendor", "btn-secondary btn-lg"),
        after=_notice(f"<strong>What's next for supplier management.</strong> The Vendor Portal lets vendors receive "
                      f"RFQs matched to their categories, take part in reverse auctions and track awarded POs. The AI Price Negotiator "
                      f"{badge('early')} checks vendor GSTINs before it negotiates."))

    out += (f'<section class="section section-light"><div class="container">'
            + section_head("How it runs", "From contract to spend report, in one procurement management system.", None, center=True)
            + workflow([
                ("headset", "Set up", "KAM loads vendors, ARC prices and your hierarchy"),
                ("search", "Buy", "Teams order from the contracted catalogue"),
                ("send", "Request", "Requisition raised from a validated cart"),
                ("check-circle", "Approve", "Routed through your Delegation of Authority"),
                ("file-check", "Order", "PO issued to the vendor"),
                ("bar-chart", "Review", "Spend and compliance visible live"),
            ]) + '</div></section>')

    out += (f'<section class="section section-tight"><div class="container">'
            + section_head("Benefits", "What changes when procurement has a system of record.", None)
            + benefits([("eye", "One version of the truth", "Vendors, prices, approvals and spend in one place."),
                        ("lock", "Contracts that hold", "Catalogue orders go out at ARC rates."),
                        ("scale", "Policy built in", "Your Delegation of Authority is enforced, not remembered."),
                        ("history", "Audit-ready", "Every action is time-stamped and downloadable.")])
            + '</div></section>')

    out += _faq("pms-faq", PMS_FAQ, "Procurement management software, answered.")
    out += _related(PMS_KEY, ["platform.html", "dashboards.html", "vendor-portal.html"])
    return out


# ---------------------------------------------------------------------------
# 2. E-Procurement Software
# ---------------------------------------------------------------------------
EP_KEY = "e-procurement-software/"

EP_FAQ = [
    ("What is e-procurement software?",
     "E-procurement software moves buying online. Instead of requests on email or WhatsApp and prices in Excel, people order from a digital catalogue, raise requisitions and get approvals online, and source off-contract items through RFQs. ProcEaze is an e-procurement platform for industrial, MRO and indirect procurement."),
    ("What is the difference between e-procurement and e-sourcing?",
     "E-procurement covers the buying process: catalogue, requisitions, approvals and purchase orders. E-sourcing is the part that finds the supplier and price for a need, through RFQs, reverse auctions and negotiation. In ProcEaze, e-sourcing is brought together in the Sourcing Desk."),
    ("How many products are in the ProcEaze catalogue?",
     "5,00,000+ products across 56+ categories, including safety and PPE, MRO, electricals, fasteners, bearings and power transmission, office supplies, and IT and electronics."),
    ("Can buyers change the price when they order?",
     "No. Annual rate contract prices are loaded by your Key Account Manager and locked at the point of order. Items outside the contract go to RFQ instead of ad-hoc buying."),
    ("Are reverse auctions and AI negotiation available?",
     "Yes. Reverse auctions run in the Auction Portal, and you can try a simulation on the Reverse Auctions page. The AI Price Negotiator is in early access for selected clients."),
    ("Do our vendors need to use ProcEaze?",
     "Not to get started. Your Key Account Manager loads your vendors' contracted prices into your catalogue. The Vendor Portal gives vendors one place to receive RFQs, join auctions and track POs."),
]


def ep_body():
    out = page_hero(
        [("Software", "platform.html"), ("E-Procurement Software", None)],
        "E-procurement software",
        "E-procurement software that takes buying off email and WhatsApp.",
        "ProcEaze moves indirect and MRO buying online: a digital catalogue with your contracted prices, online requisitions and "
        "approvals, and e-sourcing for everything off-contract.",
        actions=hero_actions(),
        visual=M.browser("app.proceaze.in/catalogue", M.catalogue_arc(), aria="Illustrative digital catalogue with ARC-locked prices"))

    out += _intro(
        "The basics", "What is e-procurement software?",
        ["E-procurement software is the online version of how a company buys. People find items in a digital catalogue, see the "
         "agreed price, raise a request and get it approved, all in one online procurement system instead of across phones, inboxes and spreadsheets.",
         "In many plants and offices, buying still happens offline. A request comes in on WhatsApp, someone checks a rate in Excel, "
         "a vendor is called for a quote and the approval arrives by email. It works, but nobody can see the whole picture, and the contracted price rarely survives the trip.",
         "ProcEaze replaces that with one e-procurement platform. Your contracted catalogue, requisitions, approvals and purchase orders "
         "sit in one place, with one login, and every step is on the record."],
        [("Requests on WhatsApp", "No trail of who asked for what, or who said yes."),
         ("Rates in a spreadsheet", "Buyers can't see the ARC, so orders go out at whatever is quoted."),
         ("Quotes in inboxes", "Every RFQ ends in a comparison sheet built by hand.")],
        "What offline buying costs you")

    out += (f'<section class="section section-light"><div class="container">'
            + section_head("Offline vs online", "Email, WhatsApp and Excel, compared with an e-procurement platform.", None)
            + _table("Offline buying compared with ProcEaze e-procurement software",
                     ["Step", "Email, WhatsApp &amp; Excel", "ProcEaze"],
                     [("Finding items", "Separate vendors and portals for each category.", "One digital catalogue: 5,00,000+ products across 56+ categories."),
                      ("Price", "Looked up in a spreadsheet, or quoted again.", "ARC price on the product, locked at the point of order."),
                      ("Request", "A message or an email.", "A purchase requisition raised in one click from a validated cart."),
                      ("Approval", "Chased by phone, signed off on email.", "Routed through your one- to five-level hierarchy, with email notifications."),
                      ("Off-contract need", "Calls and emails to a few known vendors.", "RFQ, with reverse auctions and AI negotiation as options."),
                      ("Record", "Spread across inboxes and chats.", "A permanent, time-stamped, downloadable audit trail.")])
            + '</div></section>')

    out += (f'<section class="section"><div class="container">'
            + section_head("The online procurement system", "Every part of buying, online.", None, center=True)
            + feature_cards([
                dict(icon="search", title="Digital catalogue", text="Search every category from a single login.", href="catalogue.html", cta="Catalogue & buying"),
                dict(icon="lock", title="Contracted prices online", text="ARC prices, MOQ and validity shown on every product.", href="arc-pricing.html", cta="ARC contract pricing"),
                dict(icon="clipboard-check", title="Online requisitions", text="Carts are checked against price, MOQ and validity, then submitted in one click."),
                dict(icon="check-circle", title="Online approvals", text="Approve, reject or send back in one click, with comments.", href="approvals.html", cta="Approval workflows"),
                dict(icon="truck", title="Order tracking", text="Follow each requisition through approval, confirmation and delivery."),
                dict(icon="clipboard-list", title="E-sourcing", text="RFQs, quote comparison, NFAs and POs in one desk.", href="sourcing.html", cta="Sourcing Desk"),
            ]) + '</div></section>')

    out += _feature(
        "rfq-rfx-management", "RFQ / RFx management",
        "RFQ and RFx management: e-sourcing for everything off-contract.",
        "RFx is the family of sourcing requests: RFI, RFP and RFQ. In ProcEaze, e-sourcing is built around the RFQ. When an item isn't on "
        "contract, it goes to RFQ instead of an ad-hoc purchase. The Sourcing Desk brings RFQ creation, quote comparison, "
        "vendor selection, the Note for Approval (NFA) and the purchase order into one place.",
        ["Raise an RFQ from a requirement and invite vendors",
         "Compare quotes side by side with L1 / L2 / L3 ranking",
         "Raise an NFA with quotes and recommendation attached",
         "Approved NFAs become purchase orders"],
        M.browser("app.proceaze.in/sourcing/RFQ-2026-0318", M.sourcing_desk(), aria="Illustrative RFQ quote comparison screen"),
        btn_link("sourcing.html", "Explore the Sourcing Desk", "btn-primary btn-lg"),
        cls="section section-light", reverse=True,
        after=('<div class="mt-48">' + feature_cards([
            dict(icon="gavel", title="Reverse auctions", text="Live bidding with L1 / L2 / L3 ranking, reserve price and anti-sniping.",
                 status="coming", href="reverse-auction.html", cta="Try the simulation"),
            dict(icon="bot", title="AI Price Negotiator", text="An AI agent negotiates over chat or voice against your target price. The buyer decides.",
                 status="early", href="ai-negotiator.html", cta="AI Price Negotiator"),
            dict(icon="store", title="Vendor Portal", text="Vendors receive matched RFQs, join auctions and track awarded POs.",
                 status="coming", href="vendor-portal.html", cta="Vendor Portal"),
        ]) + '</div>'
            + _notice("<strong>Live today:</strong> NFAs route through the same approval hierarchy as requisitions, and purchase orders are "
                      "issued once they are approved. RFQs run through the Sourcing Desk, with reverse auctions and the Vendor Portal, and the "
                      "AI Price Negotiator is in early access.")))

    out += (f'<section class="section"><div class="container">'
            + section_head("Workflow", "From search to purchase order, online.", None, center=True)
            + workflow([
                ("search", "Search", "Find the item in the digital catalogue"),
                ("clipboard-check", "Validate", "Price, MOQ and validity checked in the cart"),
                ("send", "Requisition", "Submitted in one click"),
                ("check-circle", "Approve", "Routed through your hierarchy"),
                ("file-check", "Purchase order", "Issued to the vendor"),
                ("truck", "Delivery", "Tracked and kept on record"),
            ]) + '</div></section>')

    out += (f'<section class="section section-tight"><div class="container">'
            + section_head("Benefits", "What changes when buying moves online.", None)
            + benefits([("clock", "Minutes, not days", "Buyers find, add and submit without chasing prices."),
                        ("lock", "Contract prices hold", "Catalogue orders go out at ARC rates."),
                        ("grid", "One login", "Every category in one place."),
                        ("history", "Nothing lost", "Every request and approval stays on file.")])
            + '</div></section>')

    out += _faq("ep-faq", EP_FAQ, "E-procurement software, answered.")
    out += _related(EP_KEY, ["platform.html", "sourcing.html", "catalogue.html"])
    return out


# ---------------------------------------------------------------------------
# 3. Procurement Automation
# ---------------------------------------------------------------------------
PA_KEY = "procurement-automation/"

PA_FAQ = [
    ("What is procurement automation?",
     "Procurement automation means letting software handle the repeatable steps of buying: applying the contracted price, checking the order, sending it to the right approver, notifying people and raising the purchase order. ProcEaze automates these steps for indirect and MRO procurement, while people keep the decisions."),
    ("Which procurement tasks can be automated?",
     "In ProcEaze: ARC price application, cart validation against price, MOQ and validity, approval routing by your Delegation of Authority, email notifications to approvers, purchase order issue after approval, and a time-stamped audit trail of every action."),
    ("Does procurement automation replace approvers?",
     "No. Automation decides where a request goes, not whether it is approved. Approvers still approve, reject or send back every requisition and NFA, and every decision is recorded with their name and the time."),
    ("Can the approval workflow match our Delegation of Authority?",
     "Yes. Each client gets its own approval chain of one to five levels, configured during onboarding to mirror its Delegation of Authority."),
    ("Are approvers notified automatically?",
     "Yes. Email notifications are live, so approvers know when a request reaches them."),
    ("Can ProcEaze negotiate with vendors automatically?",
     "The AI Price Negotiator, in early access, negotiates with vendors over chat or voice within the target and policy you set. Exceptions are escalated, a buyer can take over at any time, and the award goes through your NFA approval."),
]


def pa_body():
    out = page_hero(
        [("Software", "platform.html"), ("Procurement Automation", None)],
        "Procurement automation",
        "Procurement automation for the steps that don't need a person.",
        "ProcEaze automates the routine work between a request and a purchase order: pricing, checks, routing, notifications and records. "
        "Your people keep the decisions.",
        actions=hero_actions(),
        visual=M.browser("app.proceaze.in/approvals", M.approvals(), aria="Illustrative automated approval chain"))

    out += _intro(
        "The basics", "What is procurement automation?",
        ["Procurement automation is software doing the repeatable parts of buying, so people don't have to. Most of the effort in "
         "indirect and MRO procurement goes into checking a price, finding the right approver, chasing a sign-off and retyping an order.",
         "None of those steps needs judgement. They need a rule, applied the same way every time. Procurement automation software "
         "applies the rule, and leaves the judgement to the people accountable for it.",
         "ProcEaze automates the path from cart to purchase order. Contract prices are applied for you, carts are checked before they are "
         "submitted, requests route themselves through your Delegation of Authority (DoA), and every action is written to the audit trail."],
        [("Checking prices by hand", "Every order needs someone to confirm the contracted rate."),
         ("Chasing approvals", "Requesters follow up by phone because nobody knows where a request sits."),
         ("Rebuilding the record", "Who approved what has to be pieced together later from email.")],
        "The manual work automation removes")

    out += (f'<section class="section section-light"><div class="container">'
            + section_head("What gets automated", "Six steps ProcEaze takes off your team's plate.", None, center=True)
            + feature_cards([
                dict(icon="lock", title="Price application", text="ARC prices are applied automatically and cannot be edited at order.", href="arc-pricing.html", cta="ARC contract pricing"),
                dict(icon="clipboard-check", title="Cart validation", text="Every line is checked against contract price, MOQ and validity before submission."),
                dict(icon="route", title="Approval routing", text="Requisitions and NFAs route through your DoA, from one level to five."),
                dict(icon="mail", title="Notifications", text="Approvers are emailed when a request reaches them."),
                dict(icon="file-check", title="PO generation", text="A purchase order is issued to the vendor once the request is fully approved."),
                dict(icon="history", title="Audit trail", text="Every order, approval and rejection is time-stamped, attributed and downloadable."),
            ]) + '</div></section>')

    out += _feature(
        "approval-workflows", "Approval workflows",
        "Approval workflows that route themselves by your Delegation of Authority.",
        "Approval workflow automation is the heart of procurement workflow automation. ProcEaze configures an approval chain for each client, "
        "from one level to five, to mirror its Delegation of Authority. Requisitions and NFAs move through it on their own, "
        "and every approver sees what is waiting in a role-specific queue.",
        ["Chains of one to five levels, configured per client",
         "Approve, reject or send back in one click, with comments",
         "NFAs route through the same hierarchy as requisitions",
         "Every decision time-stamped and attributed"],
        M.browser("app.proceaze.in/nfa/0091", M.nfa_note(), aria="Illustrative Note for Approval routed for approval"),
        btn_link("approvals.html", "Explore approval workflows", "btn-primary btn-lg"),
        reverse=True)

    out += (f'<section class="section section-light"><div class="container">'
            + section_head("Workflow", "Procurement workflow automation, step by step.", None, center=True)
            + workflow([
                ("cart", "Add to cart", "ARC price applied automatically"),
                ("clipboard-check", "Validate", "Price, MOQ and validity checked"),
                ("send", "Submit", "Requisition raised in one click"),
                ("route", "Route", "Sent to the right approver by your DoA"),
                ("check-circle", "Decide", "Approver approves, rejects or sends back"),
                ("file-check", "Purchase order", "Issued and recorded once approved"),
            ]) + '</div></section>')

    out += _split_lists(
        "Human in the loop", "What ProcEaze automates, and what your people still decide.",
        "Automation handles the rules. Accountability stays with people.",
        "Automated by ProcEaze",
        ["Applying the contracted price", "Checking MOQ and contract validity", "Routing to the right approver",
         "Notifying approvers by email", "Issuing the PO after approval", "Recording every action"],
        "Decided by your team",
        ["Whether a request is approved, rejected or sent back", "Which vendor wins an off-contract requirement",
         "Which prices and vendors go on contract", "How your approval chain and thresholds are set",
         "Whether to accept an offer from the AI Price Negotiator (early access)"],
        cls="section")

    out += (f'<section class="section section-tight"><div class="container">'
            + section_head("Benefits", "What changes when the routine runs itself.", None)
            + benefits([("clock", "Faster turnaround", "Requests reach the right approver immediately."),
                        ("repeat", "Consistency", "The same rule applied to every order."),
                        ("scale", "Policy enforced", "Your DoA is built in, not remembered."),
                        ("history", "A full record", "Nothing to reconstruct at audit time.")])
            + '</div></section>')

    out += _faq("pa-faq", PA_FAQ, "Procurement automation, answered.")
    out += _related(PA_KEY, ["platform.html", "approvals.html", "ai-negotiator.html"])
    return out


# ---------------------------------------------------------------------------
# 4. Procure-to-Pay Software
# ---------------------------------------------------------------------------
P2P_KEY = "procure-to-pay-software/"

P2P_FAQ = [
    ("What is procure-to-pay (P2P) software?",
     "Procure-to-pay software manages the chain from a purchase requisition through approval, purchase order and delivery to invoice and payment. ProcEaze covers requisition, approval, purchase order and delivery tracking on one record today. Payment and reconciliation are on the roadmap."),
    ("What is the difference between procure-to-pay and e-procurement?",
     "E-procurement is about moving buying online. Procure-to-pay looks at the whole transaction chain, from the first request to the final payment, and how each step connects to the next."),
    ("What is the difference between a purchase requisition and a purchase order?",
     "A purchase requisition is an internal request to buy, which goes for approval. A purchase order is the document issued to the vendor once the requisition is approved. In ProcEaze, both sit on the same record."),
    ("Does ProcEaze handle invoices and payments?",
     "Not yet. Payment and reconciliation, including payment gateway and invoice matching, are on the ProcEaze roadmap."),
    ("Can ProcEaze connect to our ERP for accounts payable?",
     "ProcEaze is ERP plug-in ready. Integration with SAP and other ERPs is scoped during onboarding, including what data moves and in which direction."),
    ("Can we track an order after the PO is issued?",
     "Yes. Each requisition can be followed through approval, confirmation and delivery, and every step is kept in the audit trail."),
]


def p2p_body():
    out = page_hero(
        [("Software", "platform.html"), ("Procure-to-Pay Software", None)],
        "Procure-to-pay software",
        "Procure-to-pay software that keeps every step on one record.",
        "From purchase requisition to approval, purchase order and delivery, ProcEaze keeps the P2P chain connected, priced at your "
        "contract and recorded for audit. Payment and reconciliation are on our roadmap.",
        actions=hero_actions(),
        visual=M.browser("app.proceaze.in/cart", M.cart_requisition(), aria="Illustrative cart and purchase requisition screen"))

    out += _intro(
        "The basics", "What is procure-to-pay (P2P) software?",
        ["Procure-to-pay, or P2P, is the chain of steps from the moment someone needs something to the moment the vendor is paid: "
         "requisition, approval, purchase order, delivery, invoice and payment. P2P software keeps those steps connected, so each one "
         "starts from the last instead of from a fresh email.",
         "When the chain is broken, the same order is typed three times, approvals can't be traced to the PO, and nobody can say "
         "whether the price paid matched the price agreed.",
         "ProcEaze keeps requisition, approval, purchase order and delivery on one record today, at your contracted price. "
         "Payment and reconciliation are on our roadmap, and we label them that way."],
        [("Retyped at every step", "The request, the approval and the PO live in different places."),
         ("Untraceable approvals", "Nobody can link a PO back to who approved it."),
         ("Price drift", "The rate on the PO isn't the rate in the contract.")],
        "Where the P2P chain breaks")

    live, road = badge("live"), badge("roadmap")
    out += (f'<section class="section section-light"><div class="container">'
            + section_head("The P2P cycle", "The procure-to-pay cycle in ProcEaze, stage by stage.",
                           "We label every stage honestly, so you can plan around it.")
            + _table("Procure-to-pay stages in ProcEaze and their status",
                     ["Stage", "What happens in ProcEaze", "Status"],
                     [("Purchase requisition", "Raised in one click from a cart checked against ARC price, MOQ and validity.", live),
                      ("Approval", "Routed through your one- to five-level Delegation of Authority.", live),
                      ("Purchase order", "Issued to the vendor once the requisition is fully approved.", live),
                      ("Delivery", "Tracked through confirmation and delivery, on the same record.", live),
                      ("Invoice matching", "Matching invoices to POs.", road),
                      ("Payment &amp; reconciliation", "Payment gateway and payment status on the record.", road)])
            + '</div></section>')

    out += _feature(
        "purchase-requisition-management", "Purchase requisition management",
        "Purchase requisition management: from cart to approved PR.",
        "Purchase requisition software should make the right request the easy one. In ProcEaze, a buyer builds a cart from the contracted "
        "catalogue, the cart is checked against contract price, MOQ and validity, and one click raises the purchase requisition (PR). "
        "The approval route is shown before it is submitted.",
        ["PR raised in one click from a validated cart",
         "ARC price, MOQ and validity checked per line",
         "Routed through your approval chain, with approve, reject or send back",
         "Choose ProcEaze as the vendor for Managed Procurement"],
        M.browser("app.proceaze.in/approvals", M.approvals(), aria="Illustrative requisition moving through approvals"),
        btn_link("catalogue.html", "Explore catalogue & buying", "btn-primary btn-lg") + btn_link("approvals.html", "Approval workflows", "btn-secondary btn-lg"),
        reverse=True)

    out += _feature(
        "purchase-order-management", "Purchase order management",
        "Purchase order management: POs on contracted terms, tracked to delivery.",
        "PO management in ProcEaze starts where approval ends. Once a requisition or NFA is fully approved, the purchase order is issued "
        "to the vendor at the contracted rate, with payment and delivery terms visible on the PO. The order is then tracked through "
        "confirmation and delivery, and the PO is stored securely with its approvals.",
        ["PO issued to the vendor after approval",
         "Catalogue orders priced at ARC rates",
         "Payment and delivery terms visible on each PO",
         "Tracked through confirmation and delivery, with a downloadable audit trail"],
        M.browser("app.proceaze.in/po", M.po_document(), aria="Illustrative purchase order document"),
        btn_link("arc-pricing.html", "How ARC prices reach the PO", "btn-primary btn-lg"),
        cls="section section-light")

    out += (f'<section class="section"><div class="container"><div class="split">'
            f'<div>{section_head("Invoice, payment and ERP", "Payment and reconciliation are on the roadmap.", None)}'
            + _prose("Today, ProcEaze covers the procure side of P2P: requisition, approval, purchase order and delivery tracking. "
                     "Payment and reconciliation, including payment gateway and invoice matching, are planned.",
                     "ProcEaze is ERP plug-in ready. Integration with SAP and other ERPs is scoped during onboarding, so purchase "
                     "data can flow to the system your finance team already uses for payables.")
            + f'<div class="btn-row mt-24">{btn_link("integrations.html", "Integration status", "btn-secondary btn-lg")}</div></div>'
            + '<div class="stack">' + "".join(
                f'<article class="card feature-card reveal" style="--d:{i}"><div class="card-head">{icon_tile(ic)}{badge(st, text=lab)}</div>'
                f'<h3>{t}</h3><p>{d}</p></article>'
                for i, (ic, t, st, lab, d) in enumerate([
                    ("wallet", "Payment &amp; reconciliation", "roadmap", None, "Payment status on the same record as the PO and delivery."),
                    ("banknote", "Invoice matching", "roadmap", None, "Invoices matched against purchase orders."),
                    ("database", "SAP &amp; other ERPs", "ready", "Plug-in ready", "ERP plug-in ready. Integration scoped during onboarding."),
                ])) + '</div>'
            + '</div></div></section>')

    out += (f'<section class="section section-light section-tight"><div class="container">'
            + section_head("Benefits", "What changes when P2P runs on one record.", None)
            + benefits([("layers", "Nothing retyped", "Requisition, approval and PO are one record."),
                        ("lock", "Price integrity", "Catalogue POs go out at ARC rates."),
                        ("eye", "Traceable", "Every PO links back to who approved it."),
                        ("download", "Audit on demand", "Export the record whenever finance asks.")])
            + '</div></section>')

    out += _faq("p2p-faq", P2P_FAQ, "Procure-to-pay software, answered.")
    out += _related(P2P_KEY, ["platform.html", "catalogue.html", "integrations.html"])
    return out


# ---------------------------------------------------------------------------
# Page registry
# ---------------------------------------------------------------------------
def _page(key, name, title, desc, body, faq):
    return dict(path=key, title=title, desc=desc, section="platform",
                crumbs=[("Software", "platform.html"), (name, None)], body=body, schemas=[_faq_schema(faq)])


PAGES = [
    _page(PMS_KEY, "Procurement Management Software",
          "Procurement Management Software for Enterprises | ProcEaze",
          "Procurement management software for Indian enterprises: your vendors, ARC contracts, a 5 lakh+ product catalogue, 1–5 level approvals and live spend.",
          pms_body, PMS_FAQ),
    _page(EP_KEY, "E-Procurement Software",
          "E-Procurement Software for Indian Enterprises | ProcEaze",
          "E-procurement software that moves buying online: a contracted digital catalogue, online requisitions and approvals, and RFQs instead of email and Excel.",
          ep_body, EP_FAQ),
    _page(PA_KEY, "Procurement Automation",
          "Procurement Automation Software for Indian Teams | ProcEaze",
          "Procurement automation software that applies ARC prices, validates carts, routes approvals by your DoA, issues POs and keeps a full audit trail.",
          pa_body, PA_FAQ),
    _page(P2P_KEY, "Procure-to-Pay Software",
          "Procure-to-Pay (P2P) Software for Enterprises | ProcEaze",
          "Procure-to-pay software that keeps requisition, approval, purchase order and delivery on one record at contract prices. Payment and reconciliation on roadmap.",
          p2p_body, P2P_FAQ),
]
