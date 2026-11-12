"""Reusable marketing sections shared by several pages."""
from lib import (icon, icon_tile, badge, esc, L, section_head, btn_demo, btn_link, check_list, workflow)
import mockups as M

# ---------------------------------------------------------------------------
# 8-stage lifecycle (interactive tabs)
# ---------------------------------------------------------------------------
STAGES = [
    ("search", "Catalogue & Search", None, "catalogue.html",
     "Search every category in your contracted catalogue, with ARC prices pre-loaded.",
     "Live · Catalogue & Buying"),
    ("cart", "Cart & Requisition", None, "catalogue.html",
     "Carts validate contract price, MOQ and validity. One click raises a purchase requisition that routes itself for approval.",
     "Live · ARC-locked"),
    ("clipboard-list", "RFQ Management", None, "sourcing.html",
     "Off-contract needs go out as RFQs to your vendors. Quotes come back for side-by-side comparison.",
     "Sourcing Desk"),
    ("gavel", "Reverse Auction", None, "reverse-auction.html",
     "Run English or Japanese reverse auctions with live L1/L2/L3 ranking, reserve price and anti-sniping.",
     "Auction Portal"),
    ("bot", "AI Price Negotiator", "early", "ai-negotiator.html",
     "An AI agent counters vendor quotes over chat or voice and brings back the best offer. The buyer decides.",
     "Buyer remains in control"),
    ("stamp", "NFA Approval", None, "approvals.html",
     "The Note for Approval routes through your Delegation of Authority with quotes, ranking and recommendation attached.",
     "1–5 approval levels"),
    ("file-check", "Purchase Order", None, "approvals.html",
     "Approved requisitions and NFAs become purchase orders on contracted terms, issued to the vendor and kept on record.",
     "Permanent audit trail"),
    ("wallet", "Payment & Reconciliation", "roadmap", "integrations.html",
     "Delivery, PO and payment status stay on one record. Payment gateway and invoice matching are on the roadmap.",
     "Payment gateway on roadmap"),
]


def lifecycle(uid="lc"):
    nodes, panels = [], []
    for i, (ic, name, st, href, text, meta) in enumerate(STAGES):
        n = i + 1
        sel = "true" if i == 0 else "false"
        mini = badge(st, "lc-mini-badge") if st else ""
        nodes.append(
            f'<li class="lc-step" role="presentation"><button class="lc-node" type="button" role="tab" id="{uid}-tab-{n}" '
            f'aria-controls="{uid}-panel-{n}" aria-selected="{sel}" tabindex="{0 if i == 0 else -1}" style="--i:{i}">'
            f'<span class="lc-dot">{icon(ic)}</span><span class="lc-text"><span class="lc-num">{n:02d}</span>'
            f'<span class="lc-label">{esc(name)}</span>{mini}</span></button></li>')
        panels.append(
            f'<div class="lc-panel tab-panel" role="tabpanel" id="{uid}-panel-{n}" aria-labelledby="{uid}-tab-{n}"{"" if i == 0 else " hidden"}>'
            f'<span class="lc-panel-num">{n:02d}</span><div><h3>{esc(name)} {badge(st)}</h3><p>{text}</p></div>'
            f'<div class="lc-panel-meta"><span>{esc(meta)}</span><a class="link-arrow" href="{L(href)}">Explore stage {icon("arrow-right")}</a></div></div>')
    return (f'<div class="lifecycle" data-lifecycle data-tabs><div class="lc-line" aria-hidden="true"><span></span></div>'
            f'<ol class="lc-track" role="tablist" aria-label="The eight procurement stages">{"".join(nodes)}</ol>'
            f'<div class="lc-panels">{"".join(panels)}</div></div>')


def lifecycle_section(cls="section section-light", head=True):
    h = section_head("The procurement lifecycle", "From requisition to payment, in one connected flow.",
                     "ProcEaze digitises all eight stages of enterprise procurement, with no hand-off gaps.", center=True) if head else ""
    return f'<section class="{cls}" id="lifecycle"><div class="container">{h}{lifecycle()}</div></section>'


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------
STATS = [
    ('<span data-count="500000" data-suffix="+">5,00,000+</span>', "Products on the catalogue", None),
    ('<span data-count="56" data-suffix="+">56+</span>', "Categories", None),
    ('<span data-count="8">8</span>', "Connected procurement stages", None),
    ("1–5", "Configurable approval levels", None),
    ('<span data-count="100" data-suffix="%">100%</span>', "Catalogue requisitions priced at ARC rates", None),
    ("Permanent", "Audit trail on every order, approval and rejection", None),
    ("ERP", "Plug-in ready", "Scoped at onboarding"),
]


def stats_section(cls="section section-navy"):
    cards = "".join(
        f'<div class="stat-card reveal" style="--d:{i % 4}"><div class="stat-value">{v}</div>'
        f'<div class="stat-label">{l}</div>{f"<span class=stat-note>{n}</span>" if n else ""}</div>'
        for i, (v, l, n) in enumerate(STATS))
    return (f'<section class="{cls}" aria-labelledby="stats-title"><div class="bg-dots" aria-hidden="true"></div><div class="container" style="position:relative">'
            + section_head("ProcEaze in numbers", "Built for procurement at industrial scale.", None, title_id="stats-title")
            + f'<div class="stat-grid">{cards}</div></div></section>')


# ---------------------------------------------------------------------------
# Problems
# ---------------------------------------------------------------------------
PROBLEMS = [
    ("mail", "Manual PO flows",
     "Requisitions travel by email and WhatsApp. POs are typed up by hand and nobody can see where an order stands.",
     "Requisition to PO in one digital flow"),
    ("unlink", "ARC leakage",
     "Contracted rates sit in spreadsheets. Orders go out at other prices and the negotiated rate never reaches the PO.",
     "ARC price locked at the point of order"),
    ("hourglass", "Approval bottlenecks",
     "Approvals wait in inboxes, with no fixed chain, no visibility of who is holding them and no record of sign-off.",
     "1–5 level chains that move automatically"),
    ("puzzle", "Fragmented category tools",
     "Separate vendors, portals and logins for PPE, electricals, IT and stationery. Nothing sits in one place.",
     "Every category in one catalogue, one login"),
    ("eye-off", "Zero management visibility",
     "Leadership sees spend only after month-end, stitched together from vendor bills and spreadsheets.",
     "Live dashboards for every role"),
    ("database", "No client data isolation",
     "Shared tools blur the boundary around your users, prices and documents.",
     "Complete data isolation per client"),
]


def problems_section(cls="section"):
    cards = "".join(
        f'<article class="card card-hover problem-card reveal" style="--d:{i % 3}"><span class="num" aria-hidden="true">{i + 1:02d}</span>'
        f'{icon_tile(ic)}<h3>{t}</h3><p>{d}</p><p class="fix">{icon("check-circle")}<span>{fx}</span></p></article>'
        for i, (ic, t, d, fx) in enumerate(PROBLEMS))
    return (f'<section class="{cls}" id="problem"><div class="container">'
            + section_head("The problem", "Industrial procurement is still run on email, WhatsApp and spreadsheets.",
                           "Six problems every procurement team knows, and ProcEaze removes out of the box, with zero custom development.")
            + f'<div class="grid grid-3">{cards}</div></div></section>')


# ---------------------------------------------------------------------------
# Differentiators (bento)
# ---------------------------------------------------------------------------
def differentiators_section(cls="section"):
    mini = ('<div class="nego" style="border-radius:16px;overflow:hidden;box-shadow:0 30px 60px -30px rgba(0,0,0,.6)" aria-hidden="true">'
            '<div style="padding:14px;display:flex;flex-direction:column;gap:8px">'
            '<div class="nego-msg vendor"><small>Vendor B</small>Our best price is ₹405 per box.</div>'
            '<div class="nego-msg ai"><small>AI Negotiator</small>Can you reach ₹386 for two dispatches a week apart?</div>'
            '<div class="nego-msg vendor"><small>Vendor B</small>Two dispatches: ₹384 per box, GST extra.</div>'
            '<div class="nego-msg sys ok">Below target. Shortlisted for buyer review.</div></div></div>')
    small = [
        ("package", "One catalogue", "One login for industrial categories including bearings, electricals, fasteners, PPE, hand tools, IT, stationery and more.", "categories.html", "Browse categories"),
        ("plug", "ERP plug-in ready", "Designed to connect with SAP and other ERPs without a rip-and-replace. Integration is scoped during onboarding.", "integrations.html", "See integrations"),
        ("network", "Customised hierarchy", "Every client gets its own approval chain, from one level to five.", "approvals.html", "See approvals"),
        ("users", "Delegation of Authority", "Role-specific dashboards for directors, managers and buyers.", "approvals.html", "Explore DoA"),
        ("history", "Permanent audit trail", "Every order, approval and rejection is time-stamped, attributed and downloadable.", "security.html", "Security & trust"),
    ]
    cards = "".join(
        f'<article class="card card-hover feature-card reveal" style="--d:{i % 3}">{icon_tile(ic)}<h3>{t}</h3><p>{d}</p>'
        f'<a class="link-arrow" href="{L(h)}">{c} {icon("arrow-right")}</a></article>'
        for i, (ic, t, d, h, c) in enumerate(small))
    hero = (f'<article class="card bento-hero reveal"><div><div class="spotlight-badges">{badge("early")}</div>'
            f'<span class="icon-tile on-blue" style="margin-bottom:18px">{icon("bot")}</span>'
            f'<h3>AI Price Negotiator</h3><p>An AI agent that negotiates with vendors on your behalf, countering quotes and closing the best price '
            f'without manual back-and-forth.</p><a class="link-arrow mt-16" href="{L("ai-negotiator.html")}">Join early access {icon("arrow-right")}</a></div>{mini}</article>')
    return (f'<section class="{cls}" id="different"><div class="container">'
            + section_head("Why ProcEaze", "What makes ProcEaze different", "Built around how Indian industrial enterprises actually buy: contracted prices, layered approvals and many categories.")
            + f'<div class="bento">{hero}{cards}</div></div></section>')


# ---------------------------------------------------------------------------
# Built for every role (tabs)
# ---------------------------------------------------------------------------
ROLE_TABS = [
    ("director", "CXO", "crown", "solutions/leadership.html", None,
     "Company-wide spend, ARC utilisation and category trends in real time.",
     "See every rupee of procurement spend as it happens, not after month-end.",
     ["Spend by plant, department and category", "ARC utilisation and off-contract spend", "Approval turnaround across the organisation"]),
    ("procurement", "Procurement", "clipboard-list", "solutions/procurement.html", None,
     "One desk for RFQs, auctions, vendor selection, NFAs and POs.",
     "Run sourcing end to end without switching between email, spreadsheets and portals.",
     ["Side-by-side quote comparison", "Reverse auctions and AI negotiation when you need them", "NFAs routed through your Delegation of Authority"]),
    ("head", "Department Head", "users", "solutions/department-heads.html", None,
     "Approval queues, team spend and turnaround at a glance.",
     "Know what your team is buying and keep approvals moving.",
     ["Approve, reject or send back in one click", "Team spend by section and category", "Every decision time-stamped on the record"]),
    ("buyer", "Buyer", "cart", "solutions/buyers.html", None,
     "Order from your contracted catalogue in minutes, with prices pre-loaded.",
     "No price hunting, no email chains. Search, add to cart, submit.",
     ["Search the whole catalogue in one place", "ARC price locked at the point of order", "Track every requisition through to delivery"]),
    ("finance", "Finance", "landmark", "solutions/finance.html", None,
     "Contract-compliant pricing, PO terms and a downloadable audit trail.",
     "Clean records from requisition to purchase order, ready when audit asks.",
     ["100% of catalogue requisitions priced at ARC rates", "PO terms visible on every order", "Download the audit trail at any time"]),
    ("vendor", "Vendor", "store", "solutions/vendors.html", None,
     "Receive RFQs, join auctions and track awarded POs in one portal.",
     "A transparent, digital way to win business from industrial enterprises.",
     ["RFQs matched to your categories", "Transparent live auction ranking", "Awarded PO and delivery tracking"]),
]


def roles_section(cls="section section-light"):
    tabs, panels = [], []
    for i, (key, label, ic, href, st, h, sub, pts) in enumerate(ROLE_TABS):
        sel = i == 0
        tabs.append(f'<button class="tab" type="button" role="tab" id="role-tab-{key}" aria-controls="role-panel-{key}" '
                    f'aria-selected="{"true" if sel else "false"}" tabindex="{0 if sel else -1}">{icon(ic)}{label}</button>')
        st_html = f'<div class="spotlight-badges">{badge(st)}<span class="small muted">Vendor Portal</span></div>' if st else ""
        panels.append(
            f'<div class="role-panel tab-panel" role="tabpanel" id="role-panel-{key}" aria-labelledby="role-tab-{key}"{"" if sel else " hidden"}>'
            f'<div><p class="role-kicker">{label}</p>{st_html}<h3>{h}</h3><p class="lead">{sub}</p>{check_list(pts)}'
            f'<a class="link-arrow mt-24" href="{L(href)}">ProcEaze for {"Leadership" if label == "CXO" else label} {icon("arrow-right")}</a></div>'
            f'<div>{M.role_mock(key)}</div></div>')
    return (f'<section class="{cls}" id="roles"><div class="container">'
            + section_head("Built for every role", "Everyone sees what they need.", "Select a role. The dashboard changes with it.", center=True)
            + f'<div data-tabs><div class="tablist reveal" role="tablist" aria-label="Roles">{"".join(tabs)}</div>'
            + f'<div class="tab-panels">{"".join(panels)}</div></div></div></section>')


# ---------------------------------------------------------------------------
# Feature spotlights
# ---------------------------------------------------------------------------
def spotlight(eyebrow, title, lead, points, visual, cta, reverse=False, status=None, tag="h2"):
    b = f'<div class="spotlight-badges">{badge(status, "badge-lg")}</div>' if status else ""
    return (f'<div class="spotlight{" reverse" if reverse else ""}"><div class="spotlight-copy reveal">{b}'
            f'<p class="eyebrow">{eyebrow}</p><{tag} class="display">{title}</{tag}><p class="lead">{lead}</p>{check_list(points)}'
            f'<div class="btn-row">{cta}</div></div><div class="spotlight-visual reveal-frame">{visual}</div></div>')


def spotlights_section(cls="section"):
    arc = spotlight("ARC-locked buying", "Your contracted price. Every order. Every time.",
                    "Annual rate contracts are loaded into your catalogue. Buyers see the ARC price, MOQ and contract validity, and the price cannot be changed at order.",
                    ["Contract prices enforced at the point of order", "MOQ and validity shown on every product", "Off-contract needs routed to RFQ"],
                    M.browser("app.proceaze.in/catalogue", M.catalogue_arc(), aria="Illustrative catalogue screen with ARC-locked prices"),
                    btn_link("arc-pricing.html", "Explore ARC pricing", "btn-primary btn-lg"), tag="h3")
    appr = spotlight("Approvals & Delegation of Authority", "Approvals that mirror your organisation, and move at your speed.",
                     "Set an approval chain of one to five levels for each client. Requisitions route automatically, and every approver can approve, reject or send back in one click.",
                     ["Director → Head → Manager → Buyer, or any chain you need", "Approve, reject or send back with comments", "Every action time-stamped and attributed"],
                     M.browser("app.proceaze.in/approvals", M.approvals(), aria="Illustrative approval chain screen"),
                     btn_link("approvals.html", "See approval workflows", "btn-primary btn-lg"), reverse=True, tag="h3")
    auc = spotlight("Reverse auctions", "Competitive bidding, designed for competitive savings.",
                    "Invite vendors to a live reverse auction. Everyone sees their rank, not each other's names, and the clock protects against last-second sniping.",
                    ["Live L1 / L2 / L3 ranking", "Reserve price and minimum decrement", "Anti-sniping time extension"],
                    M.browser("app.proceaze.in/auctions/RA-2026-0142", M.auction_board()),
                    btn_link("reverse-auction.html", "Preview the Auction Portal", "btn-primary btn-lg"), tag="h3")
    ai = spotlight("AI Price Negotiator", "An AI that negotiates with vendors on your behalf.",
                   "Set a target price. The AI agent finds and verifies vendors, negotiates over chat or voice, and brings back a ranked shortlist. The award stays with you.",
                   ["Target price and benchmark built in", "Vendor reliability score on every offer", "Full transcript for every negotiation"],
                   M.browser("app.proceaze.in/negotiator", M.negotiator()),
                   btn_demo("Join early access", "btn-primary btn-lg", "AI Negotiator"), reverse=True, status="early", tag="h3")
    return (f'<section class="{cls}" id="features"><div class="container">'
            + section_head("Feature spotlights", "Control at every step, from contract price to final award.", None, center=True)
            + arc + appr + auc + ai + '</div></section>')


# ---------------------------------------------------------------------------
# How it works — three steps
# ---------------------------------------------------------------------------
THREE_STEPS = [
    ("Onboard", "We set up your workspace, catalogue, ARC prices and approval hierarchy. A dedicated Key Account Manager is assigned.",
     [("building", "Workspace"), ("lock", "ARC prices"), ("network", "Hierarchy"), ("headset", "KAM")]),
    ("Buy & approve", "Your teams order from the contracted catalogue; requisitions route automatically for approval.",
     [("search", "Search"), ("cart", "Cart"), ("check-circle", "Approve")]),
    ("Source & control", "Off-contract needs go through RFQ, auction or AI negotiation, then NFA and PO. Leadership tracks everything live.",
     [("clipboard-list", "RFQ"), ("gavel", "Auction"), ("bot", "AI"), ("file-check", "PO")]),
]


def three_steps_section(cls="section section-light", link=True):
    cards = "".join(
        f'<article class="step-card reveal" style="--d:{i}"><div class="step-num">0<span>{i + 1}</span></div><h3>{t}</h3><p>{d}</p>'
        f'<div class="step-visual"><ol class="flow">' + "".join(
            f'<li><span class="flow-pill">{icon(ic)}{lab}</span>{icon("arrow-right", "flow-arrow")}</li>' for ic, lab in fl)
        + '</ol></div></article>'
        for i, (t, d, fl) in enumerate(THREE_STEPS))
    more = f'<div class="center mt-48 reveal"><a class="btn btn-secondary btn-lg" href="{L("how-it-works.html")}">See detailed workflows {icon("arrow-right", "icon icon-arrow")}</a></div>' if link else ""
    return (f'<section class="{cls}" id="how-it-works"><div class="container">'
            + section_head("How it works", "Live in three steps", None, center=True)
            + f'<div class="steps">{cards}</div>{more}</div></section>')


# ---------------------------------------------------------------------------
# Engagement models
# ---------------------------------------------------------------------------
def engagement_cards():
    saas = (f'<article class="engage-card featured reveal"><span class="engage-kicker">SaaS</span>'
            f'<h3 class="engage-name">ProcEaze Platform</h3>'
            f'<p>Your teams run procurement on ProcEaze: catalogue, approvals, sourcing, auctions and POs, with your own vendors.</p>'
            + check_list(["Your contracted catalogue and ARC prices", "Your own vendors and approval hierarchy", "Dashboards for every role", "Dedicated Key Account Manager"])
            + f'<div class="engage-best"><span>Best for</span>Enterprises with an in-house procurement team.</div>'
            f'<div class="engage-price mt-24"><span>Pricing on request</span>{btn_demo("Contact Us", "btn-white", "Platform SaaS")}</div></article>')
    managed = (f'<article class="engage-card reveal" style="--d:1"><span class="engage-kicker">Managed</span>'
               f'<h3 class="engage-name">ProcEaze Managed Procurement</h3>'
               f'<p>Let ProcEaze supply for you. Choose ProcEaze as the vendor for a requisition and it goes straight to purchase approval, '
               f'while ProcEaze handles sourcing, pricing and fulfilment.</p>'
               + check_list(["ProcEaze as the vendor on a requisition", "Sourcing, pricing and fulfilment handled", "Your approvals stay in control", "Dedicated Key Account Manager"])
               + f'<div class="engage-best"><span>Best for</span>Companies wanting to outsource indirect / MRO buying.</div>'
               f'<div class="engage-price mt-24"><span>Pricing on request</span>{btn_demo("Contact Us", "btn-primary", "Managed Procurement")}</div></article>')
    return f'<div class="engage-grid">{saas}{managed}</div>'


def engagement_section(cls="section"):
    return (f'<section class="{cls}" id="engagement"><div class="container">'
            + '<div class="section-head-row">'
            + section_head("Engagement models", "Run it yourself, or let ProcEaze supply for you.", "Two ways to work with ProcEaze. Both run on the same platform.")
            + f'<a class="link-arrow reveal" href="{L("engagement-models.html")}">Compare procurement services {icon("arrow-right")}</a></div>'
            + engagement_cards() + '</div></section>')


# ---------------------------------------------------------------------------
# Security & KAM
# ---------------------------------------------------------------------------
SECURITY_POINTS = [
    ("database", "Complete data isolation per client", "Each client's users, prices, documents and records are kept separate."),
    ("smartphone", "Passwordless OTP sign-in", "Users sign in with a one-time password. No passwords to leak or reuse."),
    ("users", "Role-based access", "Every user sees and does only what their role allows."),
    ("history", "Permanent audit trail", "Every order, approval and rejection is time-stamped, attributed and downloadable."),
    ("cloud", "Secure cloud document storage", "Quotes, NFAs and purchase orders are stored securely in the cloud."),
]


def security_section(cls="section section-light"):
    items = "".join(f'<li class="reveal" style="--d:{i}">{icon_tile(ic)}<div><strong>{t}</strong><span>{d}</span></div></li>'
                    for i, (ic, t, d) in enumerate(SECURITY_POINTS))
    return (f'<section class="{cls}" id="security"><div class="container"><div class="split">'
            f'<div>{section_head("Security & trust", "Enterprise-grade control, by design.", "Procurement data is commercially sensitive. ProcEaze is built so that every client, user and action is separated, authorised and recorded.")}'
            f'<ul class="challenge-list sec-list">{items}</ul>'
            f'<a class="link-arrow mt-24 reveal" href="{L("security.html")}">Read about security {icon("arrow-right")}</a></div>'
            f'<div class="reveal-frame">{M.security_visual()}</div></div></div></section>')


def kam_section(cls="section"):
    return (f'<section class="{cls}" id="kam"><div class="container"><div class="split">'
            f'<div class="reveal-frame">{M.kam_card()}</div>'
            f'<div>{section_head("Key Account Management", "A dedicated expert for your account.", "Every client gets a named Key Account Manager who configures your catalogue and ARC prices, and handles renewals, catalogue updates, escalations and periodic spend reports.")}'
            + check_list(["Catalogue and ARC prices configured for you", "Renewals and catalogue updates handled", "One escalation point for your team", "Periodic spend reports"])
            + f'<div class="btn-row mt-32">{btn_demo("Meet the team in a demo", "btn-primary btn-lg")}</div></div></div></div></section>')


# ---------------------------------------------------------------------------
# What you get (replaces social proof)
# ---------------------------------------------------------------------------
GET = [("layers", "One unified platform"), ("lock", "ARC-locked pricing"), ("network", "Configurable approval chains"),
       ("gavel", "Reverse auctions"), ("bot", "AI negotiation"), ("headset", "Dedicated KAM")]


def what_you_get_section(cls="section section-tight section-border"):
    lis = "".join(f'<li class="reveal" style="--d:{i % 3}">{icon_tile(ic)}{t}</li>' for i, (ic, t) in enumerate(GET))
    return (f'<section class="{cls}"><div class="container">'
            + section_head("What you get with ProcEaze", "Everything procurement needs, under one view.", None, center=True)
            + f'<ul class="get-list">{lis}</ul></div></section>')
