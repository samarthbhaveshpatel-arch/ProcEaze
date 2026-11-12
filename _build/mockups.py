"""
Reusable product-UI mockups (BrowserFrame, DashboardCard, ChartCard, Table,
StatCard, ApprovalCard, ProductCard, AuctionBoard, NegotiationPanel ...).

All figures shown inside mockups are DEMO VISUAL DATA ONLY and every frame
is labelled as such.
"""
from lib import icon, esc, logo_mark, L, badge

DEMO_LABEL = "Illustrative interface. Figures are demo data, not customer results."


def ic(name):
    """Small icon for dense mock UIs (sized by CSS of parent)."""
    return icon(name, "")


def browser(url, inner, glow=False, aria=None, note=True, cls=""):
    """BrowserFrame component. If aria is given the frame is exposed as one image."""
    role = f' role="img" aria-label="{esc(aria)}"' if aria else ""
    note_html = f'<span class="mock-note">{DEMO_LABEL}</span>' if note else ""
    return (f'<div class="browser-wrap {cls}"><div class="browser-frame{" glow" if glow else ""}"{role}>'
            f'<div class="bf-bar"><div class="bf-dots" aria-hidden="true"><span></span><span></span><span></span></div>'
            f'<div class="bf-url">{icon("lock")}{esc(url)}</div>'
            f'<span class="badge badge-demo">Demo data</span></div>'
            f'<div class="bf-body">{inner}</div></div>{note_html}</div>')


# --- primitives -----------------------------------------------------------
def kpi(label, value, delta="", tone="m-neutral", primary=False, icn=None):
    i = ic(icn) if icn else ""
    return (f'<div class="m-kpi{" primary" if primary else ""}"><div class="m-kpi-label">{i}{label}</div>'
            f'<div class="m-kpi-value">{value}</div><div class="m-kpi-delta {tone}">{delta}</div></div>')


def chip(text, color="blue"):
    return f'<span class="m-chip {color}">{text}</span>'


def bars(values, labels, hi=None):
    mx = max(values)
    bs = "".join(
        f'<div class="m-bar{" hi" if i == hi else ""}" style="--i:{i}"><i style="--h:{round(v / mx * 100)}%"></i></div>'
        for i, v in enumerate(values))
    ls = "".join(f"<span>{l}</span>" for l in labels)
    return f'<div class="anim-bars"><div class="m-bars">{bs}</div><div class="m-bar-labels">{ls}</div></div>'


DONUT_COLORS = ["#184AC3", "#4F7BE0", "#8FB0F7", "#0F2A6B", "#C9D7F7"]


def donut(segments):
    """segments: list of (label, pct)."""
    r, c = 36, 2 * 3.14159 * 36
    off, circles, legend = 0, [], []
    for i, (lab, pct) in enumerate(segments):
        col = DONUT_COLORS[i % len(DONUT_COLORS)]
        ln = c * pct / 100
        circles.append(f'<circle class="seg" cx="46" cy="46" r="{r}" stroke="{col}" '
                       f'stroke-dasharray="{ln - 1.5:.1f} {c:.1f}" stroke-dashoffset="{-off:.1f}"/>')
        off += ln
        legend.append(f'<li><i style="background:{col}"></i>{lab}<b>{pct}%</b></li>')
    return (f'<div class="m-donut-wrap"><svg class="m-donut" viewBox="0 0 92 92" aria-hidden="true">'
            f'<circle cx="46" cy="46" r="{r}" stroke="#EEF2FB"/>{"".join(circles)}</svg>'
            f'<ul class="m-legend">{"".join(legend)}</ul></div>')


def table(headers, rows, num_cols=()):
    num = ' class="num"'
    th = "".join(f'<th{num if i in num_cols else ""}>{h}</th>' for i, h in enumerate(headers))
    trs = ""
    for row in rows:
        tds = "".join(f'<td{num if i in num_cols else ""}>{c}</td>' for i, c in enumerate(row))
        trs += f"<tr>{tds}</tr>"
    return f'<table class="m-table"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'


def card(title, inner, meta="", cls=""):
    return f'<div class="m-card {cls}"><div class="m-card-title"><span>{title}</span><span>{meta}</span></div>{inner}</div>'


def progress(pct, color=""):
    return f'<div class="m-progress {color}"><i style="--w:{pct}%"></i></div>'


def sidebar(active="Overview", counts=None):
    counts = counts or {"Approvals": 18}
    items = [("Overview", "dashboard"), ("Catalogue", "grid"), ("Orders", "package"), ("Approvals", "check-circle"),
             ("Sourcing", "clipboard-list"), ("Vendors", "store"), ("Analytics", "bar-chart")]
    nav = "".join(
        f'<div class="m-nav-item{" active" if n == active else ""}">{ic(i)}{n}'
        f'{f"<span class=m-count>{counts[n]}</span>" if n in counts else ""}</div>' for n, i in items)
    return (f'<div class="m-side"><div class="m-side-brand">{logo_mark("")}ProcEaze</div>{nav}'
            f'<div class="m-side-foot"><span class="m-avatar">PH</span><span>Procurement Head<br>All plants</span></div></div>')


def app(main, active="Overview", counts=None):
    return f'<div class="m-app">{sidebar(active, counts)}<div class="m-main">{main}</div></div>'


def topbar(title, sub, right=""):
    return (f'<div class="m-topbar"><div><div class="m-title">{title}</div><div class="m-sub">{sub}</div></div>'
            f'<div style="display:flex;gap:8px;align-items:center">{right}</div></div>')


# --- Hero dashboard ------------------------------------------------------
def dashboard():
    kpis = ('<div class="m-kpis">'
            + kpi("Total procurement", "₹24.8 Cr", "FY 2026–27 to date", icn="rupee")
            + kpi("This month", "₹3.2 Cr", "▲ 6.4% vs last month", "m-up", icn="calendar")
            + kpi("Pending approvals", "18", "4 due today", "m-down", icn="clock")
            + kpi("ARC utilisation", "87%", "of catalogue spend", primary=True, icn="lock")
            + '</div>')
    spend = card("Monthly spend", bars([2.4, 2.9, 2.6, 3.4, 3.0, 3.6, 3.2], ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"], hi=6), "₹ Cr · demo")
    cats = card("Spend by category", donut([("MRO", 28), ("Electricals", 22), ("Safety &amp; PPE", 18), ("Bearings", 14), ("Others", 18)]))
    orders = card("Recent orders", table(
        ["Order", "Item", "Vendor", "Value", "Status"],
        [["<span class='strong'>PO-24117</span>", "<span class='m-ellipsis'>Ball bearing 6205-2RS</span>", "Vendor A", "₹1.84 L", chip("Delivered", "green")],
         ["<span class='strong'>PO-24116</span>", "<span class='m-ellipsis'>Safety helmet, ISI</span>", "Vendor C", "₹96,400", chip("In transit")],
         ["<span class='strong'>PR-31082</span>", "<span class='m-ellipsis'>Armoured cable 4C×16</span>", "—", "₹3.12 L", chip("Awaiting L2", "amber")],
         ["<span class='strong'>PO-24114</span>", "<span class='m-ellipsis'>Copier paper A4</span>", "ProcEaze", "₹42,800", chip("Confirmed")]],
        num_cols=(3,)), "View all")
    pipe = card("Approval pipeline", '<div class="m-pipe anim-bars">'
                + "".join(f'<div class="m-pipe-row"><span>{n}</span>{progress(p, c)}<b>{v}</b></div>' for n, p, c, v in [
                    ("Submitted", 100, "sky", 32), ("Manager", 46, "", 11), ("Dept. head", 24, "amber", 5), ("Director", 10, "green", 2)])
                + f'</div><div class="m-banner blue" style="margin-top:12px">{ic("history")}Every approval is time-stamped</div>')
    main = (topbar("Procurement overview", "All plants · FY 2026–27",
                   f'<div class="m-search m-hide-sm">{ic("search")}Search products…</div><span class="m-avatar">PH</span>')
            + kpis + f'<div class="m-row">{spend}{cats}</div><div class="m-row">{orders}<div class="m-hide-sm">{pipe}</div></div>')
    return app(main)


# --- ARC catalogue -------------------------------------------------------
def product(name, sku, price, unit, moq, valid, qty, icn, selected=False):
    return (f'<div class="m-product{" selected" if selected else ""}"><div class="m-thumb">{ic(icn)}</div>'
            f'<div style="min-width:0"><div class="m-product-name">{name}</div>'
            f'<div class="m-product-meta"><span>SKU <b>{sku}</b></span><span>MOQ <b>{moq}</b></span><span class="m-hide-sm">Valid till <b>{valid}</b></span></div>'
            f'<div class="m-product-meta"><span class="m-lock">{ic("lock")}ARC locked</span></div></div>'
            f'<div class="m-price"><strong>{price}</strong><span class="m-sub">per {unit} + GST</span>'
            f'<div style="display:flex;gap:6px;align-items:center;justify-content:flex-end;margin-top:6px">'
            f'<span class="m-qty m-hide-sm"><span>−</span><b>{qty}</b><span>+</span></span><span class="m-btn">{ic("cart")}Add to cart</span></div></div></div>')


def catalogue_arc():
    main = (topbar("Catalogue", "Contracted catalogue · Bearings &amp; Power Transmission",
                   f'<span class="m-pill">{ic("cart")}Cart · 3</span>')
            + f'<div class="m-search">{ic("search")}bearing 6205</div>'
            + '<div class="m-filters"><span class="m-filter">All categories</span><span class="m-filter active">Bearings &amp; PT</span>'
              '<span class="m-filter">ARC items only ✓</span><span class="m-filter m-hide-sm">MOQ ≤ 10</span></div>'
            + '<div class="m-products">'
            + product("Deep groove ball bearing 6205-2RS", "PE-BRG-6205", "₹186.00", "pc", "10", "31 Mar 2027", "40", "bearing", True)
            + product("Taper roller bearing 30208", "PE-BRG-30208", "₹642.00", "pc", "4", "31 Mar 2027", "8", "bearing")
            + product("Pillow block unit UCP 208", "PE-PT-UCP208", "₹1,128.00", "pc", "2", "31 Mar 2027", "4", "cog")
            + '</div>'
            + f'<div class="m-banner">{ic("shield-check")}ARC price applied from contract ARC-2026-014. Price cannot be edited at order.</div>')
    return app(main, "Catalogue", {"Approvals": 18})


# --- ARC contract register ----------------------------------------------
def arc_contracts():
    kpis = ('<div class="m-kpis" style="grid-template-columns:repeat(3,minmax(0,1fr))">'
            + kpi("Active contracts", "12", "Across 9 categories", icn="file-text")
            + kpi("Catalogue lines at ARC", "100%", "Locked at order", "m-up", primary=True, icn="lock")
            + kpi("Renewals due", "2", "Within 60 days", "m-down", icn="refresh") + '</div>')
    rows = [
        ("ARC-2026-014", "Bearings &amp; PT", "186", "31 Mar 2027", 82, "", chip("Active", "green")),
        ("ARC-2026-009", "Safety &amp; PPE", "240", "30 Nov 2026", 91, "amber", chip("Renewal due", "amber")),
        ("ARC-2026-021", "Electricals", "412", "31 Mar 2027", 67, "", chip("Active", "green")),
        ("ARC-2025-033", "Paper &amp; Stationery", "158", "31 Dec 2026", 74, "sky", chip("Active", "green")),
    ]
    tbl = table(["Contract", "Category", "Items", "Valid till", "Utilisation", "Status"],
                [[f"<span class='strong'>{a}</span>", b, c, d, f'<div style="min-width:70px">{progress(e, col)}</div>', s]
                 for a, b, c, d, e, col, s in rows], num_cols=(2,))
    main = (topbar("Rate contracts (ARC)", "Managed by your Key Account Manager", f'<span class="m-pill">{ic("headset")}KAM assigned</span>')
            + kpis + f'<div class="anim-bars">{card("Contract register", tbl, "Demo data")}</div>'
            + f'<div class="m-banner amber">{ic("bell")}ARC-2026-009 expires in 55 days. Renewal is with your KAM.</div>')
    return app(main, "Catalogue")


# --- Approval levels (1–5) -----------------------------------------------
CHAIN_ROLES = [("Buyer", "Requester", "cart"), ("Manager", "Level 1", "user-check"), ("Department head", "Level 2", "users"),
               ("Director", "Level 3", "crown"), ("Finance head", "Level 4", "landmark"), ("Managing director", "Level 5", "building")]


def chain_levels(n):
    nodes = CHAIN_ROLES[:n + 1]
    lis = "".join(f'<li><span class="flow-pill">{icon(i)}{w}<span class="small muted">· {lv}</span></span>{icon("arrow-right", "flow-arrow")}</li>'
                  for w, lv, i in nodes)
    return f'<ol class="flow">{lis}<li><span class="flow-pill solid">{icon("file-check")}PO issued</span></li></ol>'


# --- Cart / requisition -------------------------------------------------
def cart_requisition():
    checks = "".join(f'<div class="m-banner" style="background:#fff;border:1px solid var(--border-soft);color:var(--ink)">'
                     f'<span style="color:var(--success-ink);display:flex">{ic("check-circle")}</span>{t}</div>' for t in
                     ["ARC price applied to all 3 lines", "MOQ met for every item", "Contract valid till 31 Mar 2027"])
    rows = table(["Item", "Qty", "ARC price", "Line total"],
                 [["<span class='m-ellipsis'>Ball bearing 6205-2RS</span>", "40", "₹186.00", "₹7,440"],
                  ["<span class='m-ellipsis'>Taper roller bearing 30208</span>", "8", "₹642.00", "₹5,136"],
                  ["<span class='m-ellipsis'>Pillow block unit UCP 208</span>", "4", "₹1,128.00", "₹4,512"]], num_cols=(1, 2, 3))
    main = (topbar("Cart &amp; requisition", "Plant 2 · Maintenance", chip("Validating", "blue"))
            + card("Cart · 3 items", rows, "Subtotal ₹17,088 + GST")
            + f'<div class="m-row-even m-row">{card("Cart validation", "<div style=display:grid;gap:6px>" + checks + "</div>")}'
            + card("Approval route", '<div class="m-chain">'
                   + chain_step("Manager · Maintenance", "Level 1", "current", "clock")
                   + chain_step("Head · Plant 2", "Level 2", "", "user") + '</div>'
                   + '<div style="margin-top:10px"><span class="m-btn" style="width:100%">Submit purchase requisition</span></div>')
            + '</div>')
    return app(main, "Orders")


# --- Approvals -----------------------------------------------------------
def chain_step(who, role, state="", icn="user", right=""):
    dot_icon = "check" if state == "done" else icn
    return (f'<div class="m-chain-step {state}"><span class="m-step-dot">{ic(dot_icon)}</span>'
            f'<div><div class="who">{who}</div><div class="role">{role}</div></div><div>{right}</div></div>')


def approvals():
    pr = ('<div class="m-card"><div class="m-card-title"><span>PR-31082 · Armoured cable 4C × 16 sq mm, 500 m</span>'
          '<span>₹3.12 L + GST</span></div>'
          '<div class="m-product-meta" style="margin:0 0 10px"><span>Requested by <b>Buyer · Maintenance</b></span>'
          '<span>Plant <b>2</b></span><span>ARC <b>✓ applied</b></span></div>'
          '<div class="m-chain">'
          + chain_step("Director · Operations", "Level 3 · required above ₹2 L", "", "crown", chip("Waiting", "grey"))
          + chain_step("Head · Plant 2", "Level 2 · pending for 2 h", "current", "user", chip("Your action", "amber"))
          + chain_step("Manager · Maintenance", "Level 1 · approved 10:40", "done", "user", chip("Approved", "green"))
          + chain_step("Buyer · Maintenance", "Requester · submitted 09:12", "done", "user", chip("Submitted", "blue"))
          + '</div><div class="m-actions" style="margin-top:12px;justify-content:flex-end">'
          f'<span class="m-btn amber">{ic("undo")}Send back</span><span class="m-btn red">{ic("x")}Reject</span>'
          f'<span class="m-btn green">{ic("check")}Approve</span></div></div>')
    queue = card("My approval queue", table(
        ["Request", "Value", "Waiting"],
        [["<span class='strong'>PR-31082</span>", "₹3.12 L", chip("2 h", "amber")],
         ["<span class='strong'>PR-31079</span>", "₹84,600", chip("40 min")],
         ["<span class='strong'>NFA-0091</span>", "₹6.40 L", chip("1 d", "red")]], num_cols=(1,)), "3 pending", "m-hide-sm")
    main = (topbar("Approvals", "Delegation of Authority · 3-level chain", chip("Head · Plant 2", "blue"))
            + pr + queue
            + f'<div class="m-banner blue">{ic("history")}Every approval, rejection and send-back is time-stamped and attributed.</div>')
    return app(main, "Approvals", {"Approvals": 3})


# --- Analytics -----------------------------------------------------------
def analytics():
    kpis = ('<div class="m-kpis">'
            + kpi("Spend FY to date", "₹24.8 Cr", "All plants", icn="rupee")
            + kpi("ARC utilisation", "87%", "▲ 3 pts this quarter", "m-up", icn="lock")
            + kpi("Off-contract spend", "₹1.9 Cr", "Routed via RFQ", icn="clipboard-list")
            + kpi("Avg. approval time", "6.2 h", "▼ 1.4 h vs last qtr", "m-up", primary=True, icn="clock")
            + '</div>')
    depts = card("Spend by department", '<div class="m-pipe anim-bars">' + "".join(
        f'<div class="m-pipe-row" style="grid-template-columns:88px minmax(0,1fr) 46px"><span>{n}</span>{progress(p, c)}<b>{v}</b></div>'
        for n, p, c, v in [("Maintenance", 92, "", "₹8.6 Cr"), ("Production", 70, "sky", "₹6.5 Cr"),
                           ("Projects", 48, "", "₹4.4 Cr"), ("Admin &amp; IT", 30, "sky", "₹2.8 Cr"),
                           ("Safety", 26, "green", "₹2.5 Cr")]) + '</div>', "₹ · demo")
    trend = card("Category trend", bars([3.1, 3.4, 2.8, 3.9, 3.6, 4.2, 3.8, 4.4], ["MRO", "Elec", "PPE", "Brg", "Fast", "IT", "Tools", "Stat"], hi=5), "Q2 vs Q1")
    vendors = card("Top vendors", table(
        ["Vendor", "POs", "Spend", "On-time"],
        [[f'<span class="m-vendor"><span class="m-vendor-logo">VA</span>Vendor A</span>', "64", "₹3.8 Cr", chip("96%", "green")],
         [f'<span class="m-vendor"><span class="m-vendor-logo">VB</span>Vendor B</span>', "41", "₹2.6 Cr", chip("92%", "green")],
         [f'<span class="m-vendor"><span class="m-vendor-logo">PE</span>ProcEaze</span>', "38", "₹2.1 Cr", chip("98%", "green")]],
        num_cols=(1, 2)), "", "m-hide-sm")
    main = (topbar("Spend analytics", "All plants · FY 2026–27",
                   f'<span class="m-pill">{ic("download")}Export audit trail</span>')
            + kpis + f'<div class="m-row">{depts}{trend}</div>' + vendors)
    return app(main, "Analytics", {"Approvals": 18})


# --- Sourcing desk -------------------------------------------------------
def sourcing_desk():
    steps = '<div class="m-filters">' + "".join(
        f'<span class="m-filter{" active" if a else ""}">{t}</span>' for t, a in
        [("1 · RFQ", False), ("2 · Quotes 3/4", True), ("3 · Compare", False), ("4 · NFA", False), ("5 · PO", False)]) + '</div>'
    comp = table(["Vendor", "GSTIN", "Unit price", "Delivery", "Rank"],
                 [[f'<span class="m-vendor"><span class="m-vendor-logo">VB</span>Vendor B</span>', chip("Verified", "green"), "₹425", "10 days", chip("L1", "blue")],
                  [f'<span class="m-vendor"><span class="m-vendor-logo">VA</span>Vendor A</span>', chip("Verified", "green"), "₹438", "7 days", chip("L2", "grey")],
                  [f'<span class="m-vendor"><span class="m-vendor-logo">VC</span>Vendor C</span>', chip("Verified", "green"), "₹451", "14 days", chip("L3", "grey")],
                  [f'<span class="m-vendor"><span class="m-vendor-logo">VD</span>Vendor D</span>', chip("Pending", "amber"), "—", "—", chip("Awaited", "grey")]],
                 num_cols=(2,))
    main = (topbar("RFQ-2026-0318", "Nitrile gloves, 12-inch · 1,200 boxes", chip("Quotes open", "amber"))
            + steps + card("Quote comparison", comp, "Ex-GST")
            + f'<div class="m-actions" style="justify-content:flex-end"><span class="m-btn ghost">{ic("gavel")}Send to auction</span>'
            + f'<span class="m-btn ghost">{ic("bot")}Negotiate with AI</span><span class="m-btn">{ic("stamp")}Raise NFA</span></div>')
    return app(main, "Sourcing", {"Approvals": 18})


# --- Vendor portal -------------------------------------------------------
def vendor_portal():
    kpis = ('<div class="m-kpis">' + kpi("Open RFQs", "6", "2 close today", "m-down", icn="inbox")
            + kpi("Live auctions", "1", "Starts 15:00", icn="gavel")
            + kpi("Awarded POs", "14", "This quarter", "m-up", icn="file-check")
            + kpi("Deliveries due", "3", "This week", primary=True, icn="truck") + '</div>')
    rfqs = card("Matched RFQs", table(
        ["RFQ", "Category", "Closes", ""],
        [["<span class='strong'>RFQ-0318</span>", "Safety &amp; PPE", chip("Today", "amber"), '<span class="m-btn">Submit quote</span>'],
         ["<span class='strong'>RFQ-0321</span>", "Electricals", chip("2 days"), '<span class="m-btn ghost">View</span>'],
         ["<span class='strong'>RFQ-0322</span>", "Fasteners", chip("4 days"), '<span class="m-btn ghost">View</span>']]), "Matched to your categories")
    main = (topbar("Vendor workspace", "Supplier view", f'<span class="m-pill" style="color:var(--success-ink)">{ic("badge-check")}GSTIN verified</span>')
            + kpis + rfqs)
    side_items = [("Overview", "dashboard"), ("RFQs", "inbox"), ("Auctions", "gavel"), ("Purchase orders", "file-check"), ("Catalogue", "grid"), ("Profile", "id-card")]
    side = (f'<div class="m-side"><div class="m-side-brand">{logo_mark("")}Vendor Portal</div>'
            + "".join(f'<div class="m-nav-item{" active" if n == "Overview" else ""}">{ic(i)}{n}</div>' for n, i in side_items)
            + '<div class="m-side-foot"><span class="m-avatar">VS</span><span>Vendor admin</span></div></div>')
    return f'<div class="m-app">{side}<div class="m-main">{main}</div></div>'


# --- PO document / NFA ---------------------------------------------------
def po_document():
    rows = table(["Item", "Qty", "Rate", "Amount"],
                 [["Ball bearing 6205-2RS", "40", "₹186.00", "₹7,440.00"],
                  ["Taper roller bearing 30208", "8", "₹642.00", "₹5,136.00"],
                  ["Pillow block unit UCP 208", "4", "₹1,128.00", "₹4,512.00"]], num_cols=(1, 2, 3))
    trail = '<div class="m-chain">' + chain_step("Head · Plant 2", "Approved · 14 Oct, 11:02", "done") + chain_step("Manager · Maintenance", "Approved · 14 Oct, 10:40", "done") + '</div>'
    main = (topbar("Purchase Order PO-24117", "Issued against PR-31076 · ARC-2026-014",
                   f'<span class="m-pill">{ic("download")}PDF</span>')
            + f'<div class="m-row-even m-row"><div class="m-card"><div class="m-sub">Vendor</div><div class="m-title" style="font-size:12px">Vendor A</div>'
              f'<div class="m-sub">GSTIN verified · Payment terms 30 days</div></div>'
              f'<div class="m-card"><div class="m-sub">Deliver to</div><div class="m-title" style="font-size:12px">Plant 2 · Stores</div>'
              f'<div class="m-sub">Delivery within 7 days</div></div></div>'
            + card("Line items", rows, "₹17,088.00 + GST 18%")
            + card("Approval trail", trail, "Downloadable"))
    return app(main, "Orders")


def nfa_note():
    comp = table(["Rank", "Vendor", "Final price", "Source"],
                 [[chip("L1", "blue"), "Vendor B", "₹384", "AI negotiation"],
                  [chip("L2", "grey"), "Vendor A", "₹389", "AI negotiation"],
                  [chip("L3", "grey"), "Vendor C", "₹430", "RFQ quote"]], num_cols=(2,))
    main = (topbar("NFA-0091 · Note for Approval", "RFQ-2026-0318 · Nitrile gloves, 1,200 boxes", chip("Pending L2", "amber"))
            + card("Comparison", comp, "Per box, ex-GST")
            + card("Recommendation", '<div class="m-sub" style="font-size:11px;color:var(--ink)">Award to <b>Vendor B</b> at ₹384/box, two dispatches. '
                   'Buyer recommendation, attached transcript and quotes.</div>')
            + f'<div class="m-actions" style="justify-content:flex-end"><span class="m-btn amber">{ic("undo")}Send back</span>'
              f'<span class="m-btn red">{ic("x")}Reject</span><span class="m-btn green">{ic("check")}Approve NFA</span></div>')
    return app(main, "Sourcing")


# --- Reverse auction board (interactive; driven by main.js) ---------------
def inr(n):
    """Indian digit grouping: 650000 -> ₹6,50,000."""
    s = str(int(n))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        s = ",".join(parts) + "," + tail
    return "₹" + s


def auction_board(full=False, autoplay=None, ceiling=650000, reserve=540000, dec=2500, duration=180, unit="",
                  title="RA-2026-0142 · Lot 1", lot="Deep groove ball bearings 6205-2RS · 2,400 pcs"):
    autoplay = (not full) if autoplay is None else autoplay
    mm, ss = divmod(duration, 60)
    data = (f' data-ceiling="{ceiling}" data-reserve="{reserve}" data-dec="{dec}" data-duration="{duration}" data-unit="{esc(unit)}"'
            + (" data-autoplay" if autoplay else ""))
    mode_tabs = ""
    if full:
        mode_tabs = ('<div class="nego-channel" role="group" aria-label="Auction type">'
                     '<button type="button" aria-pressed="true" data-au-mode="english">English reverse</button>'
                     '<button type="button" aria-pressed="false" data-au-mode="japanese">Japanese clock</button></div>')
    controls = (f'<div class="au-controls"><button class="btn btn-primary btn-sm" type="button" data-au-toggle>{icon("play")} Start simulation</button>'
                f'<button class="btn btn-secondary btn-sm" type="button" data-au-reset>{icon("rotate")} Reset</button></div>')
    return (
        f'<div class="auction" data-auction{data}>'
        f'<div class="au-head"><div class="au-title">{esc(title)} <small>{esc(lot)}</small></div>'
        f'{mode_tabs}<span class="au-live idle" data-au-status>Ready</span>'
        f'<div class="au-timer" data-au-timer-wrap><small data-au-timer-label>Time left</small><span data-au-timer>{mm:02d}:{ss:02d}</span></div></div>'
        f'<div class="au-stats">'
        f'<div class="au-stat"><span data-au-label-ceiling>Ceiling price</span><strong data-au-ceiling>{inr(ceiling)}</strong></div>'
        f'<div class="au-stat"><span data-au-l1-label>Current L1</span><strong class="l1" data-au-l1>—</strong></div>'
        f'<div class="au-stat"><span>Min. decrement</span><strong data-au-dec>{inr(dec)}</strong></div>'
        f'<div class="au-stat"><span>Reserve (buyer only)</span><strong data-au-reserve>{inr(reserve)}</strong></div></div>'
        f'<div class="au-body"><div class="au-col"><div class="au-col-title"><span>Live ranking</span><span data-au-bids>0 bids</span></div>'
        f'<div class="au-clock" data-au-clock hidden><div class="au-clock-price" data-au-clock-price>{inr(ceiling)}</div>'
        f'<div class="au-clock-sub" data-au-clock-sub>Price drops every round. Bidders confirm to stay in.</div>'
        f'<div class="au-clock-bar"><i data-au-clock-bar></i></div></div>'
        f'<ol class="au-rank" data-au-rank>'
        + "".join(f'<li><span class="rk">—</span><span class="bidder">Bidder {b}<small>Waiting to bid</small></span><span class="amt">—</span></li>' for b in "ABCDE")
        + f'</ol></div>'
        f'<div class="au-col"><div class="au-col-title"><span>Bid history</span><span>IST</span></div>'
        f'<ol class="au-history" data-au-history><li><time>—</time><span>Auction opens when you start the simulation</span><b></b></li></ol>'
        f'<svg class="au-spark" viewBox="0 0 300 64" preserveAspectRatio="none" aria-hidden="true">'
        f'<defs><linearGradient id="auGrad" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="rgba(24,74,195,.18)"/><stop offset="1" stop-color="rgba(24,74,195,0)"/></linearGradient></defs>'
        f'<line x1="0" x2="300" y1="0" y2="0" data-au-reserve-line/><polygon class="area" data-au-area points=""/><polyline data-au-spark points=""/></svg>'
        f'</div></div>'
        f'<div class="au-foot"><div class="au-flags">'
        f'<span class="au-flag" data-au-flag-snipe>{ic("timer")}Anti-sniping: +60s if bid in last 30s</span>'
        f'<span class="au-flag" data-au-flag-reserve>{ic("target")}Reserve not met</span></div>{controls}</div>'
        f'<div class="au-result" data-au-result hidden></div>'
        f'</div>'
    )


# --- AI negotiator panel (interactive; driven by main.js) -----------------
def negotiator(full=False):
    channel = ('<div class="nego-channel" role="group" aria-label="Negotiation channel">'
               f'<button type="button" aria-pressed="true" data-nego-channel="chat">{ic("message")}Chat</button>'
               f'<button type="button" aria-pressed="false" data-nego-channel="voice">{ic("mic")}Voice</button></div>')
    head = (f'<div class="nego-head"><div class="nego-agent"><span class="nego-agent-icon">{ic("bot")}</span>'
            f'<div><strong>ProcEaze AI Negotiator</strong><small data-nego-state>Ready · RFQ-2026-0318</small></div></div>'
            f'{channel}</div>')
    brief = ('<div class="nego-brief">'
             '<div class="full"><span>Requirement</span><strong>Nitrile gloves, 12-inch, box of 100 · 1,200 boxes</strong></div>'
             '<div><span>Target price</span><strong>₹385</strong></div>'
             '<div><span>Benchmark</span><strong>₹410</strong></div></div>')
    steps = ('<ul class="nego-steps" data-nego-steps>'
             + "".join(f'<li data-step="{k}"><i>{ic("check")}</i>{t}</li>' for k, t in [
                 ("discover", "Vendor discovery"), ("verify", "GSTIN verification"), ("negotiate", "Negotiation"),
                 ("shortlist", "Shortlist"), ("decide", "Buyer decision")]) + '</ul>')
    pool = ('<ul class="nego-pool" data-nego-pool>'
            + "".join(f'<li data-vendor="{v}"><div><strong>Vendor {v}</strong><small>{c}</small></div>'
                      f'<span class="gst-pending" data-gst>GSTIN pending</span></li>'
                      for v, c in [("A", "Ahmedabad · PPE"), ("B", "Vadodara · PPE"), ("C", "Surat · PPE"), ("D", "Pune · PPE")])
            + '</ul>')
    transcript = (f'<div class="nego-voice" aria-hidden="true">{ic("phone")}<span data-nego-voice-who>Voice call</span>'
                  f'<span class="wave">' + "".join(f'<i style="--i:{i}"></i>' for i in range(22)) + '</span></div>'
                  f'<div class="nego-transcript" data-nego-transcript aria-live="polite">'
                  f'<div class="nego-msg sys">Press “Run negotiation” to start the demo.</div></div>')
    board = ('<ol class="nego-board" data-nego-board>'
             + "".join(f'<li data-vendor="{v}"><span class="pos">{i + 1}</span><div class="v"><strong>Vendor {v}</strong>'
                       f'<div class="rel">{progress(r)}<em>Reliability {r}</em></div></div>'
                       f'<span class="offer" data-offer>₹{o}<small class="m-neutral">Quoted</small></span></li>'
                       for i, (v, r, o) in enumerate([("B", 88, 425), ("A", 92, 438), ("C", 74, 451), ("D", 81, 446)]))
            + '</ol>')
    control = (f'<div class="nego-control"><strong>{ic("hand")}Buyer remains in control</strong>'
               f'<p>The AI negotiates and recommends. Awards, NFAs and POs are approved by people.</p>'
               f'<div class="m-actions"><button type="button" class="m-btn primary" data-nego-action="approve">Review shortlist</button>'
               f'<button type="button" class="m-btn" data-nego-action="escalate">Escalate</button>'
               f'<button type="button" class="m-btn" data-nego-action="override">Take over</button></div></div>')

    col_brief = f'<div class="nego-col"><div class="nego-label">Brief</div>{brief}<div class="nego-label">Pipeline</div>{steps}' + \
                (f'<div class="nego-label">Vendor pool <span>4 found</span></div>{pool}' if full else "") + '</div>'
    col_talk = f'<div class="nego-col"><div class="nego-label"><span>Negotiation transcript</span><span data-nego-with>—</span></div>{transcript}</div>'
    col_board = f'<div class="nego-col"><div class="nego-label">Live leaderboard <span>per box</span></div>{board}{control}</div>'
    body_cls = "nego-body" if full else "nego-body compact"
    cols = (col_brief + col_talk + col_board) if full else (col_talk + col_board)
    foot = (f'<div class="nego-foot"><span class="control-note">{ic("shield-check")}Final award is always made by the buyer.</span>'
            f'<span style="display:flex;gap:8px"><button class="btn btn-primary btn-sm" type="button" data-nego-run>{icon("play")} Run negotiation</button>'
            f'<button class="btn btn-secondary btn-sm" type="button" data-nego-reset>{icon("rotate")} Replay</button></span></div>')
    return f'<div class="nego" data-negotiator{" data-autoplay" if not full else ""} data-channel="chat">{head}<div class="{body_cls}">{cols}</div>{foot}</div>'


# --- Role widgets (home "Built for every role") ---------------------------
def role_widget(title, sub, kpis_, rows_title, rows):
    k = '<div class="m-kpis" style="grid-template-columns:repeat(3,minmax(0,1fr))">' + "".join(
        kpi(l, v, d, t, primary=(i == 0)) for i, (l, v, d, t) in enumerate(kpis_)) + '</div>'
    body = '<div class="m-pipe">' + "".join(
        f'<div class="m-pipe-row" style="grid-template-columns:minmax(0,1.3fr) minmax(0,1fr) auto"><span>{a}</span>{progress(p, c)}<b style="white-space:nowrap">{b}</b></div>'
        for a, p, c, b in rows) + '</div>'
    return f'<div class="m-main" style="background:#F6F8FD">{topbar(title, sub)}{k}{card(rows_title, body)}</div>'


ROLE_WIDGETS = {
    "director": ("Leadership dashboard", "Company-wide · live",
                 [("Spend FYTD", "₹24.8 Cr", "All entities", "m-neutral"), ("ARC utilisation", "87%", "▲ 3 pts", "m-up"), ("Active vendors", "42", "All entities", "m-neutral")],
                 "Category trends · this quarter", [("MRO", 82, "", "▲ 6%"), ("Electricals", 64, "sky", "▲ 3%"), ("Safety &amp; PPE", 44, "", "▼ 2%"), ("IT &amp; Electronics", 28, "sky", "▲ 1%")]),
    "procurement": ("Sourcing desk", "Procurement team",
                    [("Open RFQs", "12", "4 closing today", "m-down"), ("NFAs pending", "3", "Awaiting L2", "m-neutral"), ("POs this week", "41", "▲ 8", "m-up")],
                    "RFQ pipeline", [("Quotes received", 75, "", "9 / 12"), ("In comparison", 40, "sky", "5"), ("Sent to auction", 16, "amber", "2"), ("Raised to NFA", 24, "green", "3")]),
    "head": ("Approval queue", "Head · Plant 2",
             [("Pending", "5", "2 over 4 h", "m-down"), ("Team spend", "₹1.4 Cr", "This quarter", "m-neutral"), ("Avg. turnaround", "3.1 h", "▼ 0.8 h", "m-up")],
             "Team spend by section", [("Maintenance", 78, "", "₹62 L"), ("Utilities", 52, "sky", "₹41 L"), ("Stores", 30, "", "₹24 L"), ("Safety", 22, "green", "₹17 L")]),
    "buyer": ("My orders", "Buyer · Maintenance",
              [("My orders", "24", "This month", "m-neutral"), ("Approvals", "2", "At Level 1", "m-neutral"), ("Deliveries", "18", "This month", "m-up")],
              "My orders · status", [("PR-31082 · Cable", 66, "amber", "Awaiting L2"), ("PO-24117 · Bearings", 100, "green", "Delivered"), ("PO-24116 · Helmets", 80, "", "In transit"), ("PO-24114 · Paper", 40, "sky", "Confirmed")]),
    "finance": ("Compliance view", "Finance &amp; Accounts",
                [("Contract compliance", "100%", "Catalogue lines at ARC", "m-up"), ("PO terms", "312 POs", "Terms on every PO", "m-neutral"), ("Audit trail", "Ready", "CSV / PDF export", "m-neutral")],
                "PO terms by vendor", [("Vendor A · 30 days", 90, "", "64 POs"), ("Vendor B · 45 days", 62, "sky", "41 POs"), ("ProcEaze · 30 days", 56, "", "38 POs"), ("Vendor C · 30 days", 30, "sky", "22 POs")]),
    "vendor": ("Vendor workspace", "Supplier view",
               [("Matched RFQs", "6", "2 close today", "m-down"), ("Live auctions", "1", "15:00 IST", "m-neutral"), ("Awarded POs", "14", "This quarter", "m-up")],
               "Awarded POs · delivery", [("PO-24117", 100, "green", "Delivered"), ("PO-24121", 70, "", "Dispatched"), ("PO-24125", 35, "amber", "Packing"), ("PO-24128", 10, "sky", "Accepted")]),
}


def role_mock(key):
    t, s, k, rt, r = ROLE_WIDGETS[key]
    return browser("app.proceaze.in/" + key, role_widget(t, s, k, rt, r), aria=f"Illustrative {t} screen", note=False)


# --- KAM card --------------------------------------------------------------
def kam_card():
    items = [("grid", "Catalogue &amp; ARC configuration", "At onboarding"), ("refresh", "Contract renewals", "Before expiry"),
             ("package", "Catalogue updates", "On request"), ("alert-triangle", "Escalations", "Single point of contact"),
             ("bar-chart", "Periodic spend reports", "Scheduled")]
    lis = "".join(f'<li><span class="icon-tile">{icon(i)}</span><span>{t}</span><small>{s}</small></li>' for i, t, s in items)
    return (f'<div class="kam-card"><div class="kam-top"><span class="kam-avatar">{icon("headset")}</span>'
            f'<div><strong>Your Key Account Manager</strong><span>Named, dedicated to your account</span></div></div>'
            f'<ul class="kam-list">{lis}</ul>'
            f'<div class="m-banner blue" style="margin-top:14px;font-size:.82rem">{icon("message-circle", "")}Your KAM knows your catalogue, contracts and hierarchy.</div></div>')


# --- Security architecture -------------------------------------------------
def security_visual():
    tenants = "".join(f'<div class="tenant">{icon("folder-lock")}<strong>Client {c}</strong><span>Isolated workspace</span></div>' for c in "ABC")
    layers = [("smartphone", "Passwordless OTP sign-in", "No passwords to leak or reuse", "Access"),
              ("users", "Role-based access", "Users see only what their role allows", "Authorise"),
              ("key", "Encrypted session tokens", "Tied to the signed-in user and role", "Session"),
              ("history", "Permanent audit trail", "Every action time-stamped and attributed", "Record"),
              ("cloud", "Secure cloud document storage", "Quotes, POs and NFAs stored securely", "Store")]
    ls = "".join(f'<div class="sec-layer reveal" style="--d:{i}"><span class="icon-tile">{icon(a)}</span><div><strong>{b}</strong><span>{c}</span></div><em>{d}</em></div>'
                 for i, (a, b, c, d) in enumerate(layers))
    return (f'<div class="sec-visual"><div class="bg-grid" aria-hidden="true"></div><div class="tenants">{tenants}</div>'
            f'<div class="sec-layers">{ls}</div></div>')


# --- Integrations hub ------------------------------------------------------
def integrations_hub():
    nodes = [
        (50, 9, "database", "SAP &amp; other ERPs", "ready", "Plug-in ready"),
        (88, 32, "mail", "Email notifications", "live", None),
        (88, 72, "cloud", "Cloud document storage", "live", None),
        (50, 93, "code", "APIs for integration projects", "on-request", "On request"),
        (12, 72, "banknote", "Payment gateway &amp; invoice matching", "roadmap", None),
        (12, 32, "key", "Single sign-on (SSO)", "roadmap", None),
    ]
    paths = "".join(
        f'<path class="{"solid" if st == "live" else ""}" d="M50 50 L{x} {y}" vector-effect="non-scaling-stroke"/>'
        for x, y, _i, _t, st, _l in nodes)
    node_html = "".join(
        f'<div class="hub-node" style="left:{x}%;top:{y}%">{icon(i)}<strong>{t}</strong>{badge(st, text=lab)}</div>'
        for x, y, i, t, st, lab in nodes)
    return (f'<div class="hub"><svg class="hub-lines" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">{paths}</svg>'
            f'<div class="hub-center">{logo_mark("")}<div><strong>ProcEaze</strong></div></div>{node_html}</div>')


# --- Leadership dashboard (dark "Intelligence" section) --------------------
def line_chart(values, labels, w=520, h=150):
    mx, mn = max(values), min(values) * 0.8
    n = len(values)
    pts = [(round(i * (w / (n - 1)), 1), round(h - 12 - (v - mn) / (mx - mn) * (h - 30), 1)) for i, v in enumerate(values)]
    line = " ".join(f"{x},{y}" for x, y in pts)
    area = f"0,{h} " + line + f" {w},{h}"
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="3.5"/>' for x, y in pts)
    grid = "".join(f'<line x1="0" x2="{w}" y1="{y}" y2="{y}"/>' for y in (30, 70, 110))
    lab = "".join(f"<span>{l}</span>" for l in labels)
    return (f'<div class="lc-chart"><svg viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true">'
            f'<defs><linearGradient id="lcArea" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="rgba(143,176,247,.45)"/>'
            f'<stop offset="1" stop-color="rgba(143,176,247,0)"/></linearGradient></defs><g class="lc-grid">{grid}</g>'
            f'<polygon class="lc-area" points="{area}"/><polyline class="lc-stroke" points="{line}" pathLength="1"/><g class="lc-dots">{dots}</g></svg>'
            f'<div class="lc-labels">{lab}</div></div>')


def gauge(pct, label):
    c = 2 * 3.14159 * 52
    return (f'<div class="gauge"><svg viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="52" class="g-track"/>'
            f'<circle cx="60" cy="60" r="52" class="g-val" style="--len:{c * pct / 100:.1f};--c:{c:.1f}"/></svg>'
            f'<div class="gauge-in"><b>{pct}%</b><span>{label}</span></div></div>')


def dashboard_pro():
    kpis = ('<div class="m-kpis">'
            + kpi("Total procurement", "₹24.8 Cr", "FY 2026–27 to date", icn="rupee")
            + kpi("ARC utilisation", "87%", "▲ 3 pts this quarter", "m-up", icn="lock")
            + kpi("Pending approvals", "18", "4 due today", "m-down", icn="clock")
            + kpi("Purchase orders", "312", "FY to date", primary=True, icn="file-check") + '</div>')
    trend = card("Procurement spend", line_chart([1.9, 2.4, 2.9, 2.6, 3.4, 3.0, 3.6, 3.2], ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov"]), "₹ Cr · monthly")
    cats = card("Category breakdown", '<div class="m-pipe anim-bars">' + "".join(
        f'<div class="m-pipe-row" style="grid-template-columns:92px minmax(0,1fr) 34px"><span>{n}</span>{progress(p, c)}<b>{v}</b></div>'
        for n, p, c, v in [("MRO", 92, "", "28%"), ("Electricals", 72, "sky", "22%"), ("Safety &amp; PPE", 60, "", "18%"),
                           ("Bearings &amp; PT", 46, "sky", "14%"), ("Others", 60, "", "18%")]) + '</div>')
    arc = card("ARC utilisation", gauge(87, "of catalogue spend"), "Catalogue")
    turn = card("Approval turnaround", '<div class="m-pipe anim-bars">' + "".join(
        f'<div class="m-pipe-row" style="grid-template-columns:70px minmax(0,1fr) 34px"><span>{n}</span>{progress(p, c)}<b>{v}</b></div>'
        for n, p, c, v in [("Level 1", 30, "green", "1.8h"), ("Level 2", 52, "", "3.1h"), ("Level 3", 74, "amber", "4.6h")]) + '</div>', "Avg. hours")
    funnel = card("Order pipeline", '<div class="funnel anim-bars">' + "".join(
        f'<div class="fn-row" style="--w:{w}%"><span>{n}</span><i></i><b>{v}</b></div>'
        for n, w, v in [("Requisitions", 100, "128"), ("Approved", 84, "108"), ("PO released", 74, "95"), ("Delivered", 60, "77")]) + '</div>', "This month")
    main = (topbar("Leadership overview", "All plants · FY 2026–27", f'<span class="m-pill">{ic("download")}Export</span>')
            + kpis + f'<div class="m-row m-row-wide">{trend}{cats}</div><div class="m-row m-row-3">{arc}{turn}{funnel}</div>')
    return app(main, "Analytics")
