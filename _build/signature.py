"""
ProcEaze signature visual system — "The Procurement Control Plane".

01 Procurement grid      06 ARC lock
02 Intelligence nodes    07 Approval chain
03 Procurement paths     08 Auction pulse
04 Data capsules         09 AI negotiation thread
05 Product windows       10 Audit timeline

All figures inside these components are illustrative demo data.
"""
import math
from lib import (icon, icon_tile, badge, esc, L, section_head, btn_demo, btn_link, check_list, logo_mark, photo, APP_URL)
import mockups as M


def ic(name):
    return icon(name, "")


# ---------------------------------------------------------------------------
# 01–04  Hero: the Procurement Control Plane
# ---------------------------------------------------------------------------
CP_W, CP_H = 600, 400
CP_NODES = [
    # key, label, icon, x, y, status shown when the request reaches the node
    ("catalogue", "Catalogue", "grid", 80, 100, "ITEM SELECTED"),
    ("arc", "ARC pricing", "lock", 227, 100, "ARC VERIFIED"),
    ("approval", "Approval", "check-circle", 373, 100, "APPROVAL PASSED"),
    ("rfq", "RFQ", "clipboard-list", 520, 100, "RFQ LIVE"),
    ("auction", "Auction", "gavel", 520, 300, "AUCTION · L1 SET"),
    ("ai", "AI negotiation", "bot", 373, 300, "AI NEGOTIATION"),
    ("po", "Purchase order", "file-check", 227, 300, "PO READY"),
    ("spend", "Spend", "bar-chart", 80, 300, "SPEND UPDATED"),
]
CP_PATH = "M80 100 H520 C588 100 588 300 520 300 H80"


def control_plane():
    nodes = "".join(
        f'<div class="cp-node" data-node="{k}" data-status="{esc(st)}" style="--x:{x / CP_W * 100:.2f}%;--y:{y / CP_H * 100:.2f}%;--i:{i}">'
        f'<span class="cp-dot">{ic(ico)}</span><span class="cp-label">{esc(lab)}</span></div>'
        for i, (k, lab, ico, x, y, st) in enumerate(CP_NODES))
    segs = "".join("<i></i>" for _ in CP_NODES)
    svg = (f'<svg class="cp-svg" viewBox="0 0 {CP_W} {CP_H}" preserveAspectRatio="none" aria-hidden="true">'
           f'<defs><pattern id="cpGrid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="rgba(143,176,247,.09)"/></pattern>'
           f'<linearGradient id="cpFlow" x1="0" x2="1"><stop offset="0" stop-color="#8FB0F7"/><stop offset="1" stop-color="#4F7BE0"/></linearGradient>'
           f'<radialGradient id="cpGlow"><stop offset="0" stop-color="rgba(143,176,247,.9)"/><stop offset="1" stop-color="rgba(143,176,247,0)"/></radialGradient></defs>'
           f'<rect class="cp-grid" width="{CP_W}" height="{CP_H}" fill="url(#cpGrid)"/>'
           f'<path class="cp-aux" d="M227 100 C190 200 190 200 227 300"/><path class="cp-aux" d="M373 100 C410 200 410 200 373 300"/>'
           f'<path class="cp-base" d="{CP_PATH}"/>'
           f'<path class="cp-flow" d="{CP_PATH}" pathLength="1000" data-cp-path/>'
           f'<circle class="cp-halo" r="22" fill="url(#cpGlow)" cx="80" cy="100" data-cp-halo/>'
           f'<circle class="cp-packet" r="6" cx="80" cy="100" data-cp-packet/></svg>')
    status = (f'<div class="cp-status" data-cp-card><div class="cp-status-top"><span class="cp-req">REQ #PE-2048</span>'
              f'<span class="cp-time" data-cp-time>09:42:12</span></div>'
              f'<div class="cp-stage" data-cp-stage>PO READY</div>'
              f'<div class="cp-progress" data-cp-progress>{segs}</div>'
              f'<div class="cp-meta"><span>Nitrile gloves · 1,200 boxes</span><span data-cp-step>7 / 8</span></div></div>')
    panel = (f'<div class="cp-panel" role="img" aria-label="Procurement control plane: a request moves from catalogue through ARC pricing, approval, RFQ, auction, AI negotiation and purchase order to spend analytics.">'
             f'<div class="cp-head"><span class="cp-title">{ic("layers")}PROCUREMENT CONTROL PLANE</span>'
             f'<span class="cp-live"><i></i>Live simulation</span></div>'
             f'<div class="cp-stage-area">{svg}{nodes}{status}</div>'
             f'<div class="cp-foot"><span>{ic("shield-check")}Every step on the audit trail</span><span>Demo data</span></div></div>')
    caps = [("c1", "500000", "+", "5,00,000+", "Products"), ("c2", "56", "+", "56+", "Categories"),
            ("c3", "100", "%", "100%", "ARC-priced")]
    capsules = "".join(
        f'<div class="capsule {c}" style="--i:{i}"><strong><span data-count="{n}" data-suffix="{sfx}">{txt}</span></strong><span>{lab}</span></div>'
        for i, (c, n, sfx, txt, lab) in enumerate(caps))
    return f'<div class="control-plane" data-control-plane>{panel}{capsules}</div>'


def hero():
    return (
        '<section class="hero" data-hero><div class="hero-bg" aria-hidden="true"><div class="hero-grid-bg"></div>'
        '<div class="hero-orb o1"></div><div class="hero-orb o2"></div></div>'
        '<div class="container hero-layout"><div class="hero-copy">'
        '<p class="eyebrow hero-in" style="--d:0">Procurement Intelligence</p>'
        '<h1 class="hero-title"><span class="line"><span>Procurement software,</span></span>'
        '<span class="line"><span class="h-accent">under one view.</span></span></h1>'
        '<p class="lead hero-in" style="--d:2">A single B2B procurement workspace for your enterprise: catalogue to PO, RFQ to reverse auction, '
        'and AI-assisted vendor negotiation, all in one platform.</p>'
        f'<div class="btn-row hero-in" style="--d:3">{btn_demo("Contact Us", "btn-primary btn-lg magnetic")}'
        f'<a class="btn btn-secondary btn-lg" href="{L("how-it-works.html")}">See How It Works</a></div>'
        f'<p class="hero-sub hero-in" style="--d:4">{icon("sparkles")}Procurement, powered by AI.</p>'
        f'</div><div class="hero-visual">{control_plane()}</div></div></section>'
    )


# ---------------------------------------------------------------------------
# 8-stage lifecycle with live previews
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Fragmentation → Intelligence (signature moment) — shown connected only
# ---------------------------------------------------------------------------
CHAOS_TOOLS = [
    ("mail", "Email", "Requisitions in one workflow"),
    ("message-circle", "WhatsApp", "Every order on the record"),
    ("table", "Excel", "ARC locked at order"),
    ("globe", "Vendor portals", "Every category, one login"),
    ("network", "Approval chains", "1–5 level DoA routing"),
    ("file-text", "Manual reports", "Live role dashboards"),
]


def chaos_section(cls="section"):
    chips, lines = [], []
    n = len(CHAOS_TOOLS)
    for i, (ico, name, gain) in enumerate(CHAOS_TOOLS):
        a = math.radians(-90 + 360 / n * i)
        ax, ay = 50 + 36 * math.cos(a), 50 + 32 * math.sin(a)
        chips.append(
            f'<li class="chaos-chip" style="--ax:{ax:.1f}%;--ay:{ay:.1f}%;--i:{i}">'
            f'<span class="chaos-ico">{icon(ico)}</span><span class="chaos-text"><strong>{name}</strong>'
            f'<span class="chaos-gain">{icon("check", "icon icon-sm")}{gain}</span></span></li>')
        lines.append(f'<line x1="50" y1="50" x2="{ax:.1f}" y2="{ay:.1f}" pathLength="1"/>')
    stage = (f'<div class="chaos is-connected reveal-frame"><svg class="chaos-svg" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">'
             f'<g class="chaos-links">{"".join(lines)}</g></svg>'
             f'<div class="chaos-core" aria-hidden="true"><span class="chaos-core-ring"></span>'
             f'<img class="chaos-logo" src="{L("assets/logo/proceaze-logo.png")}" width="560" height="147" alt="">'
             f'<span class="chaos-core-label">One system of record</span></div>'
             f'<ul class="chaos-chips" aria-label="What ProcEaze connects">{"".join(chips)}</ul></div>')
    caption = ('<p class="chaos-caption">One connected system of record: catalogue, ARC prices, approvals, '
               'sourcing and spend, under one view.</p>')
    return (f'<section class="{cls} chaos-section" id="problem"><div class="container">'
            f'<div class="chaos-head">{section_head("With ProcEaze", "Industrial procurement is still run on email, WhatsApp and spreadsheets.", "Six problems every procurement team knows, and ProcEaze removes out of the box, with zero custom development.")}'
            f'<div class="chaos-controls reveal">{caption}</div></div>{stage}</div></section>')


def _pv_rows(rows):
    return "".join(f'<div class="pv-row"><span>{a}</span><b>{b}</b></div>' for a, b in rows)


LC_PREVIEWS = [
    lambda: (f'<div class="pv-search">{ic("search")}nitrile gloves 12"</div>'
             + _pv_rows([("Nitrile gloves, 12-inch, box of 100", f'₹392 <span class="m-lock">{ic("lock")}ARC</span>'),
                         ("Nitrile gloves, 9-inch, box of 100", f'₹318 <span class="m-lock">{ic("lock")}ARC</span>')])),
    lambda: (_pv_rows([("ARC price applied", '<span class="pv-ok">✓</span>'), ("MOQ met", '<span class="pv-ok">✓</span>'),
                       ("Contract valid", '<span class="pv-ok">✓</span>')]) + '<span class="m-btn pv-btn">Submit purchase requisition</span>'),
    lambda: _pv_rows([("Vendor B", "₹425 · L1"), ("Vendor A", "₹438 · L2"), ("Vendor C", "₹451 · L3"), ("Vendor D", "Awaited")]),
    lambda: ('<div class="pv-bars">' + "".join(f'<div><span>{r}</span><i style="--w:{w}%"></i><b>{p}</b></div>' for r, w, p in
                                                [("L1", 92, "₹980"), ("L2", 80, "₹995"), ("L3", 64, "₹1,020")]) + '</div>'
             + '<span class="m-chip amber">02:14 left</span>'),
    lambda: ('<div class="nego-msg ai pv-msg"><small>AI Negotiator</small>Volume commitment available. Target: ₹1,100.</div>'
             '<div class="nego-msg vendor pv-msg"><small>Vendor B</small>₹1,135 / unit</div>'),
    lambda: (_pv_rows([("Head · Plant 2", '<span class="m-chip green">Approved</span>'), ("Director · Operations", '<span class="m-chip amber">Pending</span>')])
             + '<span class="m-btn green pv-btn">Approve NFA</span>'),
    lambda: _pv_rows([("PO-24117", '<span class="m-chip blue">Released</span>'), ("Vendor", "Vendor B"), ("Terms", "30 days · ARC")]),
    lambda: (_pv_rows([("Delivery", '<span class="m-chip green">Confirmed</span>'), ("PO status", "Closed on record")])
             + f'<p class="pv-note">{badge("roadmap")} Payment gateway &amp; invoice matching</p>'),
]

LC_DATA = [
    ("Buyer", "Cart", "Live"), ("Buyer", "Purchase requisition", "Live"), ("Procurement", "Ranked quotes", "Sourcing Desk"),
    ("Procurement", "L1 / L2 / L3", "Live"), ("AI agent + buyer", "Shortlist", "Early access"),
    ("Approvers (1–5 levels)", "Approved NFA", "Live"), ("Procurement", "Purchase order", "Live"), ("Finance", "Closed record", "Roadmap: payments"),
]


def lifecycle(uid="lc"):
    import blocks as B
    nodes, panels = [], []
    for i, (ico, name, st, href, text, meta) in enumerate(B.STAGES):
        n = i + 1
        sel = i == 0
        mini = badge(st, "lc-mini-badge") if st else ""
        nodes.append(
            f'<li class="lc-step" role="presentation"><button class="lc-node" type="button" role="tab" id="{uid}-tab-{n}" '
            f'aria-controls="{uid}-panel-{n}" aria-selected="{"true" if sel else "false"}" tabindex="{0 if sel else -1}" style="--i:{i}">'
            f'<span class="lc-dot">{icon(ico)}</span><span class="lc-text"><span class="lc-num">{n:02d}</span>'
            f'<span class="lc-label">{esc(name)}</span>{mini}</span></button></li>')
        owner, output, status = LC_DATA[i]
        panels.append(
            f'<div class="lc-panel lc-panel-v2 tab-panel" role="tabpanel" id="{uid}-panel-{n}" aria-labelledby="{uid}-tab-{n}"{"" if sel else " hidden"}>'
            f'<div class="lc-copy"><span class="lc-panel-num">{n:02d}</span><h3>{esc(name)} {badge(st)}</h3><p>{text}</p>'
            f'<dl class="lc-data"><div><dt>Who</dt><dd>{esc(owner)}</dd></div><div><dt>Output</dt><dd>{esc(output)}</dd></div>'
            f'<div><dt>Status</dt><dd>{esc(status)}</dd></div></dl>'
            f'<a class="link-arrow" href="{L(href)}">Explore stage {icon("arrow-right")}</a></div>'
            f'<div class="lc-preview" aria-hidden="true"><div class="lc-preview-bar"><i></i><i></i><i></i><span>Stage {n:02d} · demo</span></div>'
            f'<div class="lc-preview-body">{LC_PREVIEWS[i]()}</div></div></div>')
    return (f'<div class="lifecycle" data-lifecycle data-tabs><div class="lc-line" aria-hidden="true"><span></span></div>'
            f'<ol class="lc-track" role="tablist" aria-label="The eight procurement stages">{"".join(nodes)}</ol>'
            f'<div class="lc-panels">{"".join(panels)}</div></div>')


def lifecycle_section(cls="section section-light"):
    return (f'<section class="{cls}" id="lifecycle"><div class="container">'
            + section_head("The platform", "From requisition to payment, in one connected flow.",
                           "ProcEaze digitises all eight stages of enterprise procurement, with no hand-off gaps. Select a stage to see it.", center=True)
            + lifecycle() + '</div></section>')


# ---------------------------------------------------------------------------
# 06  ARC lock
# ---------------------------------------------------------------------------
def arc_lock_visual():
    lock = ('<svg class="arc-lock-svg" viewBox="0 0 48 56" aria-hidden="true"><path class="arc-shackle" d="M14 26V16a10 10 0 0 1 20 0v10" '
            'fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"/><rect x="7" y="24" width="34" height="28" rx="7" fill="currentColor"/>'
            '<circle cx="24" cy="37" r="3.6" fill="#fff"/><path d="M24 39v5" stroke="#fff" stroke-width="3" stroke-linecap="round"/></svg>')
    details = [("MOQ", "50 pairs"), ("Validity", "till 31 Mar 2027"), ("Committed volume", "2,400 pairs / yr"),
               ("GST", "18% extra"), ("Contract", '<span class="m-chip green">Active</span>')]
    dl = "".join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in details)
    return (f'<div class="arc-lock" data-arc-lock><div class="arc-card">'
            f'<div class="arc-product"><span class="m-thumb">{ic("hard-hat")}</span><div><strong>Safety shoes, steel toe, ISI marked</strong>'
            f'<span>SKU PE-PPE-SS204 · Contract ARC-2026-009</span></div><span class="badge badge-demo">Demo data</span></div>'
            f'<div class="arc-prices"><div class="arc-row arc-vendor"><span>Vendor list price</span><b>₹1,240</b></div>'
            f'<div class="arc-row arc-contract"><span>Contract price (ARC)</span><b>₹1,080</b></div></div>'
            f'<div class="arc-display"><div class="arc-price"><span class="arc-cur">₹</span><span data-arc-price>1,080</span><small>/ pair</small></div>'
            f'<div class="arc-lockbox">{lock}<span class="arc-badge">ARC LOCKED</span></div></div>'
            f'<dl class="arc-details">{dl}</dl>'
            f'<div class="arc-foot">{ic("shield-check")}<span>Price applied from contract. It cannot be edited at order.</span>'
            f'<button class="arc-replay" type="button" data-arc-replay>{ic("rotate")}Replay</button></div></div></div>')


def arc_section(cls="section"):
    return (f'<section class="{cls}" id="arc"><div class="container"><div class="split">'
            f'<div>{section_head("Control · ARC contract pricing", "Your contracted price. Every order. Every time.", "Annual rate contracts are loaded into your catalogue. The vendor\'s list price never reaches the order: the ARC price is applied, locked and recorded.")}'
            f'<p class="statement reveal">Zero contract violations at the point of order.</p>'
            + check_list(["100% of catalogue requisitions priced at ARC rates", "MOQ, validity and GST shown on every item", "Off-contract needs routed to RFQ"])
            + f'<div class="btn-row mt-32">{btn_link("arc-pricing.html", "Explore ARC pricing", "btn-secondary btn-lg")}</div></div>'
            f'<div class="reveal-frame">{arc_lock_visual()}</div></div></div></section>')


# ---------------------------------------------------------------------------
# 07  Approval chain — interactive workflow engine
# ---------------------------------------------------------------------------
def approval_engine(uid="ae"):
    levels = "".join(f'<button type="button" aria-pressed="{"true" if n == 3 else "false"}" data-ae-levels="{n}">{n}</button>' for n in range(1, 6))
    return (f'<div class="ae" data-approval-engine id="{uid}-engine"><div class="ae-head">'
            f'<div><span class="ae-kicker">PR-31082 · ₹3.12 L + GST</span><strong>Armoured cable 4C × 16 sq mm, 500 m</strong></div>'
            f'<div class="ae-levels"><span id="{uid}-lv">Approval levels</span><div class="seg seg-sm" role="group" aria-labelledby="{uid}-lv">{levels}</div></div></div>'
            f'<ol class="ae-chain" data-ae-chain aria-label="Approval chain"></ol>'
            f'<div class="ae-actions"><p class="ae-acting" data-ae-acting aria-live="polite">Acting as Manager · Level 1</p>'
            f'<div class="ae-btns"><button class="btn btn-sm ae-approve" type="button" data-ae-act="approve">{icon("check")}Approve</button>'
            f'<button class="btn btn-sm ae-reject" type="button" data-ae-act="reject">{icon("x")}Reject</button>'
            f'<button class="btn btn-sm ae-back" type="button" data-ae-act="sendback">{icon("undo")}Send back</button>'
            f'<button class="btn btn-sm btn-ghost" type="button" data-ae-act="reset">{icon("rotate")}Reset</button></div></div>'
            f'<ol class="ae-log" data-ae-log aria-label="Audit log"></ol>'
            f'<p class="ae-note">{ic("info")}1–5 configurable approval levels. Roles shown are illustrative.</p></div>')


def approvals_section(cls="section section-light"):
    return (f'<section class="{cls}" id="approvals"><div class="container"><div class="split split-rev">'
            f'<div class="reveal-frame">{approval_engine()}</div>'
            f'<div>{section_head("Control · Delegation of Authority", "Approvals that mirror your organisation, and move at your speed.", "Director, department head, manager, buyer: set a chain of one to five levels for each client. Try it: approve, reject or send back the request.")}'
            + check_list(["1–5 configurable approval levels", "Approve, reject or send back in one click", "Every decision time-stamped and attributed"])
            + f'<div class="btn-row mt-32">{btn_link("approvals.html", "See approval workflows", "btn-secondary btn-lg")}</div></div>'
            f'</div></div></section>')


# ---------------------------------------------------------------------------
# Dashboard showcase (dark)
# ---------------------------------------------------------------------------
def dashboard_section(cls="section section-dark"):
    return (f'<section class="{cls}" id="intelligence"><div class="bg-dots" aria-hidden="true"></div><div class="container rel">'
            + section_head("Intelligence · Dashboards", "Every rupee of spend, live.",
                           "Procurement spend, category breakdown, ARC utilisation, approval turnaround and the order pipeline, updated as procurement happens.", center=True)
            + f'<div class="reveal-frame">{M.browser("app.proceaze.in/leadership", M.dashboard_pro(), aria="Illustrative leadership dashboard with spend trend, category breakdown, ARC utilisation gauge, approval turnaround and order pipeline", cls="on-dark")}</div>'
            + '</div></section>')


# ---------------------------------------------------------------------------
# 09  AI negotiation control tower
# ---------------------------------------------------------------------------
TOWER_VENDORS = [("A", "Ahmedabad", 1240, 92), ("B", "Vadodara", 1210, 88), ("C", "Surat", 1265, 74), ("D", "Pune", 1225, 81)]


def _tvendor(v, city, offer, rel):
    return (f'<div class="tv" data-tv="{v}"><div class="tv-top"><span class="tv-rank" data-tv-rank>—</span>'
            f'<strong>Vendor {v}</strong><span class="tv-city">{city}</span></div>'
            f'<div class="tv-offer"><span data-tv-offer>₹{offer:,}</span><small>/ unit</small></div>'
            f'<div class="tv-rel"><span>Reliability</span><div class="m-progress"><i style="--w:{rel}%"></i></div><b>{rel}</b></div>'
            f'<div class="tv-foot"><span class="m-chip grey" data-tv-status>Quoted</span><span class="tv-resp" data-tv-resp>Resp. —</span></div></div>')


def ai_tower(uid="tw", compact=False):
    left = _tvendor(*TOWER_VENDORS[0]) + _tvendor(*TOWER_VENDORS[1])
    right = _tvendor(*TOWER_VENDORS[2]) + _tvendor(*TOWER_VENDORS[3])
    core = (f'<div class="tower-core"><div class="tower-orb"><span class="ring r1"></span><span class="ring r2"></span>'
            f'<span class="tower-orb-in">{icon("bot")}<b>PROCEAZE AI</b></span></div>'
            f'<div class="tower-brief"><div><span>Requirement</span><b>Safety shoes · 2,500 pairs</b></div>'
            f'<div><span>Target</span><b>₹1,100</b></div><div><span>Benchmark</span><b>₹1,160</b></div></div>'
            f'<div class="tower-thread" data-tw-thread aria-live="polite"><div class="nego-msg sys">Press “Run negotiation” to start the simulation.</div></div></div>')
    foot = (f'<div class="tower-foot"><span class="control-note">{icon("hand")}<b>Buyer remains in control.</b> Awards, NFAs and POs are approved by people.</span>'
            f'<span class="tower-btns"><button class="btn btn-white btn-sm" type="button" data-tw-run>{icon("play")} Run negotiation</button>'
            f'<button class="btn btn-ghost-light btn-sm" type="button" data-tw-action="override">{icon("hand")} Take over</button></span></div>')
    return (f'<div class="tower{" tower-compact" if compact else ""}" data-tower{"" if compact else " data-autoplay"} id="{uid}-tower">'
            f'<div class="tower-head"><span>{icon("sparkles")}NEGOTIATION CONTROL TOWER</span><span>{badge("early")}<span class="tower-demo">Simulated data</span></span></div>'
            f'<div class="tower-grid"><div class="tower-col">{left}</div>{core}<div class="tower-col">{right}</div></div>{foot}</div>')


def ai_section(cls="section section-dark", title="An AI that negotiates with vendors on your behalf."):
    return (f'<section class="{cls}" id="ai"><div class="bg-grid" aria-hidden="true"></div><div class="container rel">'
            f'<div class="section-head center reveal"><div class="spotlight-badges" style="justify-content:center">{badge("early", "badge-lg")}</div>'
            f'<p class="eyebrow">Human + AI · AI Price Negotiator</p><h2>{title}</h2>'
            f'<p class="lead">Set a target. The AI agent negotiates with each vendor over chat or voice, ranks every offer and escalates what falls outside your policy. The decision stays with your buyer.</p></div>'
            f'<div class="reveal-frame">{ai_tower()}</div>'
            f'<div class="center mt-48">{btn_demo("Join AI early access", "btn-white btn-lg magnetic", "AI Negotiator")}</div></div></section>')


# ---------------------------------------------------------------------------
# 08  Auction pulse
# ---------------------------------------------------------------------------
def auction_section(cls="section section-light"):
    board = M.browser("app.proceaze.in/auctions/RA-2026-0157",
                      M.auction_board(full=True, autoplay=True, ceiling=1100, reserve=990, dec=5, duration=134, unit=" / pair",
                                      title="RA-2026-0157 · Lot 1", lot="Industrial safety shoes, steel toe · 5,000 pairs"))
    pts = ["English reverse auction and Japanese descending clock", "Live L1 / L2 / L3 ranking", "Reserve price and minimum decrement",
           "Anti-sniping time extension"]
    return (f'<section class="{cls}" id="auctions"><div class="container"><div class="split split-auction">'
            f'<div>'
            f'{section_head("Competition · Reverse Auction Portal", "Competitive bidding, designed for competitive savings.", "Vendors bid live and see only their rank. The clock protects against last-second sniping, and the reserve stays with the buyer.")}'
            + check_list(pts)
            + f'<div class="btn-row mt-32">{btn_link("reverse-auction.html", "Preview the Auction Portal", "btn-secondary btn-lg")}</div></div>'
            f'<div class="reveal-frame">{board}</div></div></div></section>')


# ---------------------------------------------------------------------------
# Category orbit
# ---------------------------------------------------------------------------
ORBIT_CATS = [
    ("hard-hat", "Safety & PPE", "Personal protective equipment for plants, sites and warehouses.", "Helmets · gloves · safety shoes · harnesses"),
    ("wrench", "MRO", "Maintenance, repair and operations supplies that keep equipment running.", "Spares · consumables · sealants"),
    ("zap", "Electricals", "Cables, switchgear, lighting and electrical consumables.", "Cables · switchgear · lighting"),
    ("nut", "Fasteners", "Bolts, nuts, screws, washers and anchors.", "Bolts · nuts · screws · anchors"),
    ("bearing", "Bearings & Power Transmission", "Bearings, belts, chains, couplings and housings.", "Bearings · belts · couplings"),
    ("notebook", "Paper & Stationery", "Copier paper, notebooks, files and everyday stationery.", "Paper · notebooks · files"),
    ("pen", "Office Supplies", "Office essentials for every desk, team and meeting room.", "Desk supplies · printer consumables"),
    ("laptop", "IT & Electronics", "Computing peripherals, networking accessories and electronics.", "Peripherals · networking · storage"),
    ("hammer", "Hand Tools", "Spanners, screwdrivers, pliers and tool kits.", "Spanners · pliers · tool kits"),
    ("cog", "Industrial Plants & Machinery", "Equipment and machinery for plant operations.", "Plant equipment · machinery spares"),
]


def category_orbit():
    n = len(ORBIT_CATS)
    items = []
    for i, (ico, name, desc, ex) in enumerate(ORBIT_CATS):
        ang = -90 + 360 / n * i
        a = math.radians(ang)
        x, y = 50 + 40 * math.cos(a), 50 + 40 * math.sin(a)
        items.append(f'<li><button class="orbit-item" type="button" style="--x:{x:.1f}%;--y:{y:.1f}%;--a:{ang + 90:.0f}deg" '
                     f'data-orbit-item data-name="{esc(name)}" data-desc="{esc(desc)}" data-ex="{esc(ex)}" aria-pressed="false">'
                     f'<span class="orbit-ico">{icon(ico)}</span><span class="orbit-name">{esc(name)}</span></button></li>')
    return (f'<div class="orbit" data-orbit><div class="orbit-rings" aria-hidden="true"><i></i><i></i><i></i></div>'
            f'<div class="orbit-ray" aria-hidden="true" data-orbit-ray></div>'
            f'<div class="orbit-core" aria-live="polite"><div class="orbit-core-in" data-orbit-core>'
            f'<span class="orbit-k">One login</span><strong>Every category</strong><span>One catalogue, at your contracted prices.</span></div></div>'
            f'<ul class="orbit-list" aria-label="Categories">{"".join(items)}</ul></div>')


# Category photography (assets/images/categories/<slug>.jpg). If a file is
# missing the image removes itself and the icon artwork shows instead.
CAT_SLUGS = {
    "Safety & PPE": "safety-ppe", "MRO": "mro", "Electricals": "electricals", "Fasteners": "fasteners",
    "Bearings & Power Transmission": "bearings", "Paper & Stationery": "paper-stationery",
    "Office Supplies": "office-supplies", "Office & Stationery Supplies": "office-supplies",
    "IT & Electronics": "it-electronics", "Hand Tools": "hand-tools", "Industrial Plants & Machinery": "machinery",
    "Plumbing & Pipe Fittings": "plumbing", "Welding Supplies": "welding", "Lubricants & Chemicals": "lubricants",
    "Packaging Materials": "packaging", "Housekeeping & Janitorial": "housekeeping", "Lighting & Fixtures": "lighting",
    "Material Handling": "material-handling", "Pumps & Valves": "pumps-valves", "Furniture": "furniture",
    "Pantry Supplies": "pantry",
}


# ProcEaze's own category banners (name and description are part of the image),
# shown uncropped with no overlaid text
BANNERS = {"safety-ppe", "mro", "electricals", "fasteners", "bearings", "paper-stationery",
           "office-supplies", "it-electronics", "hand-tools"}


def cat_slug(name):
    return CAT_SLUGS[name]


def is_banner(name):
    return cat_slug(name) in BANNERS


def cat_photo(name, cls="cat-photo"):
    alt = esc(f"{name} — product range") if is_banner(name) else ""
    return (f'<img class="{cls}" src="{L("assets/images/categories/" + cat_slug(name) + ".jpg")}" alt="{alt}" '
            f'width="1500" height="1000" loading="lazy" decoding="async" onerror="this.remove()">')


def category_tiles():
    """Auto-playing carousel of category tiles (shares the module carousel's track, dots and autoplay)."""
    n = len(ORBIT_CATS)
    slides = []
    for i, (ico, name, desc, ex) in enumerate(ORBIT_CATS):
        banner = " banner" if is_banner(name) else ""
        slides.append(f'<li class="mc-slide reveal" style="--d:{min(i, 3)}" role="group" aria-roledescription="slide" aria-label="{i + 1} of {n}: {esc(name)}">'
                      f'<a class="cat-tile{banner}" href="{L("categories.html")}#{cat_slug(name)}">'
                      f'{cat_photo(name, "cat-tile-img")}<span class="cat-tile-shade" aria-hidden="true"></span>'
                      f'<span class="cat-tile-ico" aria-hidden="true">{icon(ico)}</span>'
                      f'<span class="cat-tile-body"><strong>{esc(name)}</strong><span>{esc(ex)}</span></span>'
                      f'<span class="cat-tile-go" aria-hidden="true">{icon("arrow-right")}</span></a></li>')
    controls = (f'<div class="mc-controls">'
                f'<button class="mc-btn" type="button" data-mc-prev aria-label="Previous category">{icon("chevron-left")}</button>'
                f'<div class="mc-dots" data-mc-dots></div>'
                f'<button class="mc-btn" type="button" data-mc-next aria-label="Next category">{icon("chevron-right")}</button></div>')
    return (f'<div class="mod-carousel cat-carousel" data-carousel data-mc-item="category" aria-roledescription="carousel" aria-label="Categories">'
            f'<div class="mc-viewport"><ul class="mc-track" data-mc-track>{"".join(slides)}</ul></div>{controls}</div>')


def categories_section(cls="section"):
    return (f'<section class="{cls}" id="categories"><div class="container">'
            f'<div class="cat-tiles-head">{section_head("Categories", "Everything your sites need. One login.", "From safety gear to spares to stationery, for every site, plant and office, at your contracted prices.")}'
            f'<div class="btn-row">{btn_link("categories.html", "Browse all categories", "btn-secondary btn-lg")}</div></div>'
            f'{category_tiles()}</div></section>')


def photo_band():
    """Full-bleed industrial photograph under a navy overlay. Its stats complement the hero
    capsules (products, categories, ARC-priced, stages) rather than repeating them."""
    stats = [(None, "1–5", "Approval levels, set per client"), (None, "Permanent", "Audit trail on every order"),
             (None, "One", "Login for every site and category")]
    cells = "".join(
        f'<li class="reveal" style="--d:{i}"><strong>'
        + (f'<span data-count="{c}" data-suffix="{"+" if v.endswith("+") else ""}">{v}</span>' if c else v)
        + f'</strong><span>{t}</span></li>' for i, (c, v, t) in enumerate(stats))
    return (f'<section class="photo-band" aria-label="ProcEaze at a glance">'
            f'{photo("home-band", "", "photo-band-img", 2400, 1000)}<div class="photo-band-shade" aria-hidden="true"></div>'
            f'<div class="container"><div class="photo-band-copy reveal"><p class="eyebrow">Built for India\'s industrial enterprises</p>'
            f'<h2>From the shop floor to the boardroom, one procurement record.</h2></div>'
            f'<ul class="photo-band-stats">{cells}</ul></div></section>')


def orbit_section(cls="section"):
    return (f'<section class="{cls}" id="universe"><div class="container"><div class="split split-orbit">'
            f'<div>{section_head("Catalogue universe", "Every category, one catalogue.", "From the plant floor to the front office, every request starts in the same place. Select a category to explore.")}'
            f'<div class="btn-row"><a class="btn btn-secondary btn-lg" href="#safety-ppe">See category details</a></div></div>'
            f'<div class="reveal-frame">{category_orbit()}</div></div></div></section>')


# ---------------------------------------------------------------------------
# Industries — line-art compositions
# ---------------------------------------------------------------------------
def _art(kind):
    s = 'fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"'
    a = 'fill="none" stroke="#8FB0F7" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"'
    ground = '<path d="M20 250H460" stroke="currentColor" stroke-width="2" opacity=".35"/>'
    if kind == "manufacturing":
        body = (f'<path {s} d="M40 250V150l50 30v-30l50 30v-30l50 30v-60h40v130"/><path {s} d="M210 120V70h24v50"/>'
                f'<g class="art-spin" style="transform-origin:330px 150px"><circle {a} cx="330" cy="150" r="44"/><circle {a} cx="330" cy="150" r="16"/>'
                + "".join(f'<path {a} d="M{330 + 44 * math.cos(math.radians(t)):.1f} {150 + 44 * math.sin(math.radians(t)):.1f}L{330 + 56 * math.cos(math.radians(t)):.1f} {150 + 56 * math.sin(math.radians(t)):.1f}"/>' for t in range(0, 360, 30))
                + f'</g><path {s} d="M250 232h200M262 232v18M438 232v18"/><g class="art-belt">'
                + "".join(f'<rect {s} x="{270 + k * 40}" y="206" width="26" height="26" rx="3"/>' for k in range(4)) + '</g>'
                f'<path {a} d="M60 200h20M60 216h20M110 200h20M110 216h20M160 200h20M160 216h20"/>')
    elif kind == "energy":
        panels = "".join(f'<path {s} d="M{40 + k * 70} 250l14-60h56l-14 60z"/><path {s} d="M{68 + k * 70} 250l14-60M{47 + k * 70} 220h56"/>' for k in range(3))
        body = (panels + f'<path {s} d="M360 250V110"/><g class="art-spin" style="transform-origin:360px 106px">'
                f'<path {a} d="M360 106L360 40M360 106L417 139M360 106L303 139"/><circle {s} cx="360" cy="106" r="6"/></g>'
                f'<circle {a} cx="120" cy="70" r="24"/><path {a} d="M120 30v-10M120 120v-10M80 70H70M170 70h-10M92 42l-7-7M155 105l-7-7M148 42l7-7M85 105l7-7"/>'
                f'<path {s} d="M430 250V170M420 182h20M418 200h24"/>')
    elif kind == "logistics":
        stacks = "".join(f'<rect {s if (r + c) % 2 else a} x="{200 + c * 52}" y="{214 - r * 26}" width="48" height="24" rx="2"/>' for r in range(3) for c in range(4) if r < 3 - c % 2)
        body = (f'<path {s} d="M60 250V60M150 250V60M50 60h200M60 80l90-20M150 80L60 60"/><path {s} d="M230 60v40"/><rect {a} x="215" y="100" width="30" height="16" rx="2"/>'
                + stacks + f'<path {a} d="M20 270c40 10 80 10 120 0s80-10 120 0 80 10 120 0 60-10 100 0"/>'
                f'<path {s} d="M380 250l12-40h60l-6 40z"/><path {s} d="M400 210v-24h22v24"/>')
    elif kind == "infrastructure":
        grid = "".join(f'<path {s} d="M{250 + c * 40} 250V130"/>' for c in range(5)) + "".join(f'<path {s} d="M250 {250 - r * 30}H410"/>' for r in range(5))
        body = (f'<path {s} d="M90 250V50M80 50h220M90 70l200-20M90 50l20-20h0l-20 20"/><path {s} d="M90 90h-30v18h30"/>'
                f'<path {a} d="M260 50v60"/><rect {a} x="248" y="110" width="24" height="16" rx="2"/>' + grid
                + f'<path {a} d="M20 250c60-70 140-70 200 0" opacity=".9"/><path {a} d="M60 222v28M120 200v50M180 222v28"/>')
    else:  # facility / offices
        win = "".join(f'<rect {a if (r * 3 + c) % 4 == 0 else s} x="{88 + c * 30}" y="{70 + r * 30}" width="16" height="18" rx="2"/>' for r in range(6) for c in range(4))
        win2 = "".join(f'<rect {s} x="{278 + c * 30}" y="{140 + r * 28}" width="16" height="16" rx="2"/>' for r in range(3) for c in range(3))
        body = (f'<path {s} d="M70 250V50h140v200"/>' + win + f'<path {s} d="M260 250V120h110v130"/>' + win2
                + f'<path {s} d="M130 250v-22h20v22"/><circle {a} cx="420" cy="196" r="26"/><path {s} d="M420 222v28"/>')
    return (f'<svg class="ind-art" viewBox="0 0 480 290" role="img" aria-label="Illustration">'
            f'<defs><pattern id="indDots-{kind}" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="rgba(24,74,195,.16)"/></pattern></defs>'
            f'<rect width="480" height="290" fill="url(#indDots-{kind})"/>{ground}{body}</svg>')


INDUSTRY_SHOW = [
    ("manufacturing", "industries/manufacturing.html", "Manufacturing & Process Plants", "factory",
     "Thousands of MRO, safety and electrical items across plants, in one catalogue at ARC prices, with plant-wise approvals.",
     ["MRO", "Bearings & PT", "Fasteners", "Electricals", "Safety & PPE"]),
    ("energy", "industries/energy-renewables.html", "Energy & Renewables", "sun",
     "The same contracted catalogue and approval rules for every plant, substation and project site, with one view of spend.",
     ["Electricals", "Safety & PPE", "Hand Tools", "MRO"]),
    ("logistics", "industries/logistics.html", "Logistics, Ports & ICDs", "anchor",
     "Fast, controlled buying for terminals, yards and warehouses that run round the clock.",
     ["MRO", "Safety & PPE", "Electricals", "Bearings & PT"]),
    ("infrastructure", "industries/infrastructure.html", "Infrastructure & EPC", "construction",
     "Project-wise catalogues, prices and approvals, with live project-wise visibility for management.",
     ["Electricals", "Safety & PPE", "Hand Tools", "Fasteners"]),
    ("facility", "industries/facility-management.html", "Facility Management & Corporate Offices", "office",
     "Stationery, IT, electricals and maintenance supplies for every office and facility, from one catalogue.",
     ["Paper & Stationery", "Office Supplies", "IT & Electronics", "Electricals"]),
]


def industries_section(cls="section"):
    tabs, panels = [], []
    for i, (k, href, name, ico, text, cats) in enumerate(INDUSTRY_SHOW):
        sel = i == 0
        tabs.append(f'<button class="ind-tab" type="button" role="tab" id="ind-tab-{k}" aria-controls="ind-panel-{k}" aria-selected="{"true" if sel else "false"}" '
                    f'tabindex="{0 if sel else -1}">{icon(ico)}<span>{esc(name)}</span>{icon("arrow-right", "icon ind-arrow")}</button>')
        chips = "".join(f'<li>{esc(c)}</li>' for c in cats)
        panels.append(f'<div class="ind-panel tab-panel" role="tabpanel" id="ind-panel-{k}" aria-labelledby="ind-tab-{k}"{"" if sel else " hidden"}>'
                      f'<div class="ind-visual">{_art(k)}{photo("industry-" + k, name, "ind-photo")}</div><div class="ind-copy"><h3>{esc(name)}</h3><p>{text}</p>'
                      f'<ul class="cat-items">{chips}</ul><a class="link-arrow" href="{L(href)}">ProcEaze for {esc(name.split(" &")[0].split(",")[0])} {icon("arrow-right")}</a></div></div>')
    return (f'<section class="{cls}" id="industries"><div class="container">'
            + section_head("By industry", "Different sites. Different ways of buying.", "Procurement looks different on a shop floor, a solar park, a port and a project site. ProcEaze is configured for each.")
            + f'<div class="ind" data-tabs><div class="ind-tabs" role="tablist" aria-label="Industries" aria-orientation="vertical">{"".join(tabs)}</div>'
            + f'<div class="ind-stage">{"".join(panels)}</div></div></div></section>')


# ---------------------------------------------------------------------------
# Engagement switch — RUN IT vs RUN IT WITH US
# ---------------------------------------------------------------------------
ENGAGE_ROWS = [
    ("Buying from the catalogue", "you", "you", "Your teams order", "Your teams order"),
    ("Vendors", "you", "pe", "Your own vendors", "ProcEaze as the vendor"),
    ("Sourcing & pricing", "you", "pe", "RFQ, auctions, AI negotiation", "Handled by ProcEaze"),
    ("Fulfilment", "you", "pe", "By your vendors", "Handled by ProcEaze"),
    ("Approvals", "you", "you", "Your 1–5 level hierarchy", "Straight to purchase approval"),
    ("Dashboards & audit trail", "you", "you", "Role-based, live", "Role-based, live"),
    ("Key Account Manager", "pe", "pe", "Dedicated KAM", "Dedicated KAM"),
]


def engagement_switch():
    rows = "".join(
        f'<li class="es-row" data-run="{a}" data-with="{b}"><span class="es-label">{esc(t)}</span>'
        f'<span class="es-track"><span class="es-side es-you">Your team</span><span class="es-side es-pe">ProcEaze</span>'
        f'<span class="es-token"><span class="es-t-run">{esc(da)}</span><span class="es-t-with">{esc(db)}</span></span></span></li>'
        for t, a, b, da, db in ENGAGE_ROWS)
    return (f'<div class="es" data-engage data-mode="run">'
            f'<div class="es-switch" role="group" aria-label="Engagement model"><button type="button" aria-pressed="true" data-es-mode="run">'
            f'<b>RUN IT</b><span>ProcEaze Platform · SaaS</span></button><button type="button" aria-pressed="false" data-es-mode="with">'
            f'<b>RUN IT WITH US</b><span>ProcEaze Managed Procurement</span></button><span class="es-thumb" aria-hidden="true"></span></div>'
            f'<div class="es-body"><div class="es-copy">'
            f'<div class="es-pane es-pane-run"><h3>Your teams run procurement on ProcEaze.</h3><p>Catalogue, approvals, sourcing, auctions and POs, with your own vendors.</p>'
            f'<p class="es-best"><span>Best for</span>Enterprises with an in-house procurement team.</p></div>'
            f'<div class="es-pane es-pane-with"><h3>Let ProcEaze supply for you.</h3><p>Choose ProcEaze as the vendor for a requisition and it goes straight to purchase approval, while ProcEaze handles sourcing, pricing and fulfilment.</p>'
            f'<p class="es-best"><span>Best for</span>Companies wanting to outsource indirect / MRO buying.</p></div>'
            f'<div class="es-cta"><span>Pricing on request</span>{btn_demo("Contact Us", "btn-primary")}</div></div>'
            f'<ol class="es-rows" aria-label="Who does what">{rows}</ol></div></div>')


def engagement_section(cls="section section-light"):
    return (f'<section class="{cls}" id="engagement"><div class="container">'
            + '<div class="section-head-row">' + section_head("Engagement models", "Run it. Or run it with us.", "Two ways to work with ProcEaze, on the same platform. Flip the switch to see who does what.")
            + f'<a class="link-arrow reveal" href="{L("engagement-models.html")}">Compare procurement services {icon("arrow-right")}</a></div>'
            + f'<div class="reveal-frame">{engagement_switch()}</div></div></section>')


# ---------------------------------------------------------------------------
# Security vault + 10 Audit timeline
# ---------------------------------------------------------------------------
VAULT = [
    ("database", "Data isolation", "Each client's users, prices, vendors and documents are kept completely separate."),
    ("smartphone", "Passwordless OTP", "Users sign in with a one-time password. No passwords to leak or reuse."),
    ("users", "Role-based access", "Every user sees and does only what their role allows."),
    ("history", "Permanent audit trail", "Every order, approval and rejection is time-stamped, attributed and downloadable."),
    ("cloud", "Secure cloud storage", "Quotes, NFAs and POs stored securely, linked to each transaction."),
    ("key", "Encrypted tokens", "Sessions are secured with encrypted tokens tied to the user and role."),
]


def vault():
    n = len(VAULT)
    items = []
    for i, (ico, t, d) in enumerate(VAULT):
        ang = -90 + 360 / n * i
        a = math.radians(ang)
        x, y = 50 + 40 * math.cos(a), 50 + 40 * math.sin(a)
        items.append(f'<li><button class="vault-item" type="button" style="--x:{x:.1f}%;--y:{y:.1f}%;--a:{ang + 90:.0f}deg" data-orbit-item '
                     f'data-name="{esc(t)}" data-desc="{esc(d)}" aria-pressed="false"><span class="orbit-ico">{icon(ico)}</span><span class="orbit-name">{esc(t)}</span></button></li>')
    return (f'<div class="orbit vault" data-orbit><div class="orbit-rings" aria-hidden="true"><i></i><i></i><i></i></div>'
            f'<div class="orbit-ray" aria-hidden="true" data-orbit-ray></div>'
            f'<div class="orbit-core" aria-live="polite"><div class="orbit-core-in" data-orbit-core><span class="vault-shield">{icon("shield-check")}</span>'
            f'<strong>Your procurement vault</strong><span>Select a layer of control.</span></div></div>'
            f'<ul class="orbit-list" aria-label="Security controls">{"".join(items)}</ul></div>')


AUDIT = [
    ("09:42:12", "PR created", "Buyer · Maintenance", "PR-31082 raised from the catalogue. ARC price applied."),
    ("09:43:08", "Manager approved", "Manager · Maintenance", "Within Level 1 limit."),
    ("09:44:22", "RFQ created", "Procurement · Category lead", "Off-contract line routed to RFQ, 4 vendors invited."),
    ("10:01:17", "Vendor bid received", "Vendor B", "₹1,135 / unit, delivery in 10 days."),
    ("10:08:42", "NFA approved", "Head · Plant 2", "L1 recommended. Quotes and transcript attached."),
    ("10:10:03", "PO released", "System", "PO-24117 issued to Vendor B on contracted terms."),
]


def audit_trail(uid="at", dark=True):
    items = "".join(
        f'<li><button class="at-item" type="button" data-at-item aria-pressed="{"true" if i == 0 else "false"}" '
        f'data-user="{esc(u)}" data-action="{esc(a)}" data-time="{t}" data-remark="{esc(r)}">'
        f'<time>{t}</time><span class="at-dot" aria-hidden="true"></span><span class="at-action">{esc(a)}</span><span class="at-user">{esc(u)}</span></button></li>'
        for i, (t, a, u, r) in enumerate(AUDIT))
    t, a, u, r = AUDIT[0]
    detail = (f'<div class="at-detail" aria-live="polite" data-at-detail><dl>'
              f'<div><dt>User</dt><dd data-at-f="user">{esc(u)}</dd></div><div><dt>Action</dt><dd data-at-f="action">{esc(a)}</dd></div>'
              f'<div><dt>Timestamp</dt><dd data-at-f="time">14 Oct 2026, {t} IST</dd></div><div><dt>Remark</dt><dd data-at-f="remark">{esc(r)}</dd></div></dl>'
              f'<span class="at-stamp">{icon("lock")}Immutable record</span></div>')
    return (f'<div class="at{" at-dark" if dark else ""}" data-audit id="{uid}-audit"><div class="at-head"><span>{icon("history")}AUDIT TRAIL · PR-31082</span>'
            f'<button class="at-export" type="button" data-at-export>{icon("download")}Export</button></div>'
            f'<div class="at-body"><ol class="at-list">{items}</ol>{detail}</div></div>')


def trust_section(cls="section section-dark"):
    return (f'<section class="{cls}" id="trust"><div class="bg-grid" aria-hidden="true"></div><div class="container rel">'
            f'<div class="split split-trust"><div>{section_head("Trust · Security", "Enterprise-grade control, by design.", "Procurement data is commercially sensitive. Every client is isolated, every user authorised, and every action recorded.")}'
            f'<div class="reveal-frame">{vault()}</div></div>'
            f'<div><div class="section-head reveal"><p class="eyebrow">Audit trail</p><h2 class="h3-serif">Every action, on the record. Forever.</h2>'
            f'<p class="lead">Select any event to see who did what, when, and why.</p></div>'
            f'<div class="reveal-frame">{audit_trail()}</div>'
            f'<a class="link-arrow mt-24" href="{L("security.html")}">Read about security {icon("arrow-right")}</a></div></div></div></section>')


# ---------------------------------------------------------------------------
# KAM — technology that works with people
# ---------------------------------------------------------------------------
def kam_section(cls="section"):
    return (f'<section class="{cls}" id="kam"><div class="container"><div class="split">'
            f'<div>{section_head("Human + technology", "Technology that works with people.", "Every client gets a named Key Account Manager who configures your catalogue and ARC prices, and handles renewals, escalations and periodic spend reports.")}'
            + check_list(["Catalogue configuration", "ARC management and renewals", "Escalations, with one point of contact", "Periodic spend reports"])
            + f'</div><div class="reveal-frame kam-wrap">{M.kam_card()}</div></div></div></section>')


# ---------------------------------------------------------------------------
# How it works — scroll-driven three steps
# ---------------------------------------------------------------------------
HOW = [
    ("Onboard", "Workspace, catalogue, ARC prices, approval hierarchy and a dedicated KAM.",
     [("building", "Workspace"), ("grid", "Catalogue"), ("lock", "ARC"), ("network", "Hierarchy"), ("headset", "KAM")]),
    ("Buy & approve", "Teams order from the contracted catalogue. Requisitions route automatically for approval.",
     [("search", "Catalogue"), ("cart", "Requisition"), ("check-circle", "Approval")]),
    ("Source & control", "Off-contract needs go through RFQ, auction or AI negotiation, then NFA and PO. Leadership tracks everything live.",
     [("clipboard-list", "RFQ"), ("gavel", "Auction"), ("bot", "AI negotiation"), ("stamp", "NFA"), ("file-check", "PO")]),
]


def how_section(cls="section section-light", link=True):
    steps = "".join(
        f'<li class="how-step" data-how-step><span class="how-num">0{i + 1}</span><div class="how-body"><h3>{t.upper()}</h3><p>{d}</p>'
        f'<ol class="flow">' + "".join(f'<li><span class="flow-pill">{icon(ico)}{lab}</span>{icon("arrow-right", "flow-arrow")}</li>' for ico, lab in fl)
        + '</ol></div></li>' for i, (t, d, fl) in enumerate(HOW))
    more = f'<a class="btn btn-secondary btn-lg mt-32" href="{L("how-it-works.html")}">See detailed workflows {icon("arrow-right", "icon icon-arrow")}</a>' if link else ""
    return (f'<section class="{cls}" id="how-it-works"><div class="container"><div class="how" data-how>'
            f'<div class="how-intro">{section_head("How it works", "Live in three steps.", "From onboarding to purchase order. Scroll to follow the flow.")}{more}</div>'
            f'<ol class="how-steps"><span class="how-line" aria-hidden="true"><i data-how-line></i></span>{steps}</ol></div></div></section>')


# ---------------------------------------------------------------------------
# Network motif (final CTA, footer)
# ---------------------------------------------------------------------------
def network_svg(cls="net-svg"):
    pts = [(80, 60), (220, 140), (360, 50), (520, 160), (680, 70), (820, 150), (960, 60), (1100, 140), (1240, 70), (1360, 150),
           (150, 300), (300, 360), (470, 290), (640, 370), (800, 300), (980, 360), (1140, 290), (1300, 360)]
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (1, 10), (10, 11), (11, 12), (12, 13), (13, 14),
             (14, 15), (15, 16), (16, 17), (3, 12), (5, 14), (7, 16), (9, 17)]
    lines = "".join(f'<path d="M{pts[a][0]} {pts[a][1]}L{pts[b][0]} {pts[b][1]}" style="--i:{i}"/>' for i, (a, b) in enumerate(edges))
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="{4 if i % 3 else 6}" style="--i:{i}"/>' for i, (x, y) in enumerate(pts))
    return f'<svg class="{cls}" viewBox="0 0 1440 420" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><g class="net-lines">{lines}</g><g class="net-dots">{dots}</g></svg>'
