"""Platform pages: overview + nine capability pages."""
from lib import (icon, icon_tile, badge, esc, L, section_head, page_hero, hero_actions, btn_demo, btn_link,
                 feature_cards, workflow, benefits, challenge_list, check_list, related, status_legend,
                 PLATFORM, SOFTWARE, SOFTWARE_SCHEMA)
import mockups as M
import blocks as B
import signature as S


# ---------------------------------------------------------------------------
# Generic capability page template
# ---------------------------------------------------------------------------
def capability_page(d):
    status = d.get("status")
    badges = badge(status, "badge-lg") if status else ""
    actions = d.get("actions")
    actions = (actions() if callable(actions) else actions) or hero_actions(interest=d.get("interest"))
    out = page_hero([d.get("parent", ("Platform", "platform.html")), (d["name"], None)], d["eyebrow"], d["h1"], d["lead"],
                    actions=actions, visual=d.get("hero_visual", ""), badges=badges)

    if d.get("after_hero"):
        out += d["after_hero"]()

    # Problem
    out += (f'<section class="section"><div class="container"><div class="split">'
            f'<div>{section_head("The problem", d["problem"][0], d["problem"][1])}</div>'
            f'<div>{challenge_list(d["problem"][2])}</div></div></div></section>')

    # Solution + features
    sid = f' id="{d["features_id"]}"' if d.get("features_id") else ""
    out += (f'<section class="section section-light"{sid}><div class="container">'
            + section_head("The ProcEaze way", d["solution"][0], d["solution"][1], center=True)
            + feature_cards(d["features"]) + '</div></section>')

    # Product UI
    if d.get("ui"):
        title, text, pts, visual = d["ui"]
        out += (f'<section class="section"><div class="container">'
                + B.spotlight("Inside the product", title, text, pts, visual, btn_demo("See it in a demo", "btn-primary btn-lg"), reverse=True)
                + '</div></section>')

    if d.get("extra"):
        out += d["extra"]()

    # Workflow
    out += (f'<section class="section section-light"><div class="container">'
            + section_head("Workflow", d["workflow"][0], None, center=True)
            + workflow(d["workflow"][1]) + '</div></section>')

    # Benefits
    out += (f'<section class="section section-tight"><div class="container">'
            + section_head("Benefits", d.get("benefits_title", "What changes for your teams"), None)
            + benefits(d["benefits"]) + '</div></section>')

    out += related(d["related"])
    return out


def mk(path, title, desc, d):
    return dict(path=path, title=title, desc=desc, section="platform",
                crumbs=[d.get("parent", ("Platform", "platform.html")), (d["name"], None)], body=lambda: capability_page(d))


# ---------------------------------------------------------------------------
# Catalogue & Buying
# ---------------------------------------------------------------------------
CATALOGUE = dict(
    name="Catalogue & Buying", eyebrow="Catalogue & Buying",
    h1="5 lakh+ products. Ordered in minutes, at the right price.",
    lead="One catalogue for every site, plant and office, with your contracted prices pre-loaded and every order routed for approval.",
    hero_visual=M.browser("app.proceaze.in/catalogue", M.catalogue_arc(), aria="Illustrative catalogue with ARC-locked products"),
    problem=("Buying the basics shouldn't take a dozen emails.",
             "Indirect and MRO buying is high in volume and low in visibility. Most of the effort goes into finding items, prices and approvers.",
             [("Too many places to buy", "Separate vendors and portals for PPE, electricals, IT and stationery."),
              ("Prices are a guess", "Buyers can't see the contracted rate, so they ask, wait or pay more."),
              ("Orders vanish into inboxes", "Requests by email or WhatsApp leave no trail of who asked, who approved and what was ordered.")]),
    solution=("One catalogue. Contracted prices. Automatic approvals.",
              "ProcEaze brings every category into one searchable catalogue, configured for your company by your Key Account Manager."),
    features=[
        dict(icon="search", title="Unified search", text="Search every category from a single login."),
        dict(icon="lock", title="ARC prices pre-loaded", text="Contracted prices appear on the product. Buyers never have to look them up."),
        dict(icon="clipboard-check", title="Cart validation", text="Every cart is checked against contract price, MOQ and validity before it is submitted."),
        dict(icon="send", title="One-click requisition", text="Submit a purchase requisition from the cart. It routes to the right approver automatically."),
        dict(icon="truck", title="Order tracking", text="Follow each requisition through approval, confirmation and delivery."),
        dict(icon="store", title="ProcEaze as a vendor", text="Choose ProcEaze as the vendor on a requisition and it goes straight to purchase approval.",
             href="engagement-models.html", cta="Managed Procurement"),
    ],
    ui=("Cart validation before anything is submitted.",
        "The cart checks every line against the contract. If it passes, one click raises the requisition and shows the approval route.",
        ["ARC price, MOQ and validity checked per line", "Approval route shown before you submit", "Requisition, approvals and PO on one record"],
        M.browser("app.proceaze.in/cart", M.cart_requisition(), aria="Illustrative cart and requisition screen")),
    workflow=("From search to delivery, on one record.", [
        ("search", "Browse", "Search the contracted catalogue"),
        ("clipboard-check", "Cart validation", "Price, MOQ and validity checked"),
        ("send", "Submit PR", "One click from the cart"),
        ("check-circle", "Approval", "Routes through your hierarchy"),
        ("file-check", "Confirmation", "PO issued to the vendor"),
        ("truck", "Delivery & audit", "Delivery confirmed, record kept"),
    ]),
    benefits=[("clock", "Minutes, not days", "Buyers find, add and submit without chasing prices."),
              ("lock", "Contract compliance", "Catalogue orders go out at ARC rates."),
              ("grid", "One login", "Every category in one place."),
              ("history", "A full record", "Every request and approval stays on file.")],
    related=["arc-pricing.html", "approvals.html", "categories.html"],
)

# ---------------------------------------------------------------------------
# ARC Contract Pricing
# ---------------------------------------------------------------------------
ARC = dict(
    name="ARC Contract Pricing", eyebrow="ARC Contract Pricing",
    h1="Your contracted price. Every order. Every time.",
    lead="An annual rate contract is only worth what reaches the purchase order. ProcEaze locks your ARC prices into the catalogue, so every catalogue requisition is priced at the contracted rate.",
    hero_visual=M.browser("app.proceaze.in/contracts", M.arc_contracts(), aria="Illustrative ARC contract register"),
    problem=("Negotiated rates leak between the contract and the order.",
             "Procurement negotiates the rate. Then it has to survive every buyer, every site and every order for a year.",
             [("Rates live in spreadsheets", "Buyers can't see the ARC, so orders go out at whatever price is quoted."),
              ("Expiry goes unnoticed", "Contracts lapse quietly and orders continue at old or unagreed prices."),
              ("Compliance is hard to prove", "Finance can't show that orders matched the contract without manual checks.")]),
    solution=("Contract prices enforced at the point of order.",
              "Your Key Account Manager loads ARC prices, MOQs and validity into your catalogue. Buyers see them on every product and cannot change them at order."),
    features=[
        dict(icon="lock", title="Locked ARC price", text="The contracted price is applied automatically and cannot be edited at order."),
        dict(icon="package", title="MOQ on every product", text="Minimum order quantities are shown on the product and validated in the cart."),
        dict(icon="calendar", title="Contract validity", text="Each item shows how long its contract runs."),
        dict(icon="refresh", title="Renewals handled", text="Your KAM manages renewals and price updates before contracts lapse."),
        dict(icon="check-circle", title="100% ARC-priced requisitions", text="Every catalogue requisition is priced at ARC rates."),
        dict(icon="clipboard-list", title="Off-contract routed to RFQ", text="Items outside the contract go to RFQ, auction or AI negotiation instead of ad-hoc buying."),
    ],
    ui=("What the buyer sees: the price, locked.",
        "ARC items carry a locked-price badge, the MOQ and the contract validity. There is nothing to negotiate at order, and nothing to change.",
        ["Locked-price badge on every ARC item", "Contract reference applied automatically", "Price cannot be edited in the cart"],
        M.browser("app.proceaze.in/catalogue", M.catalogue_arc(), aria="Illustrative catalogue with ARC-locked products")),
    workflow=("From contract to purchase order, the rate holds.", [
        ("file-text", "Contract agreed", "ARC terms finalised with your vendors"),
        ("headset", "KAM configures", "Prices, MOQs and validity loaded"),
        ("cart", "Buyer orders", "ARC price applied automatically"),
        ("check-circle", "Approval", "Routes through your hierarchy"),
        ("file-check", "PO at ARC", "Issued at the contracted rate"),
        ("refresh", "Renewal", "Handled by your KAM"),
    ]),
    after_hero=lambda: S.arc_section("section section-light"),
    benefits=[("lock", "No leakage", "The negotiated rate reaches every catalogue order."),
              ("scale", "Audit-ready", "Show contract compliance from the record."),
              ("clock", "Faster ordering", "No price checks before buying."),
              ("refresh", "No silent lapses", "Renewals tracked by your KAM.")],
    related=["catalogue.html", "dashboards.html", "solutions/finance.html"],
)

# ---------------------------------------------------------------------------
# Approvals & DoA
# ---------------------------------------------------------------------------
def approval_levels_section():
    tabs, panels = [], []
    for n in range(1, 6):
        sel = n == 3
        tabs.append(f'<button class="tab" type="button" role="tab" id="lvl-tab-{n}" aria-controls="lvl-panel-{n}" '
                    f'aria-selected="{"true" if sel else "false"}" tabindex="{0 if sel else -1}">{n} level{"s" if n > 1 else ""}</button>')
        panels.append(f'<div class="tab-panel card" role="tabpanel" id="lvl-panel-{n}" aria-labelledby="lvl-tab-{n}"{"" if sel else " hidden"}>'
                      f'<p class="small muted" style="margin-bottom:16px">Illustrative {n}-level chain. Roles and value thresholds are configured to your Delegation of Authority.</p>'
                      f'{M.chain_levels(n)}</div>')
    return (f'<section class="section"><div class="container">'
            + section_head("Configurable hierarchy", "One level or five. Your chain, your rules.",
                           "Pick a chain length to see how a requisition travels. Each client gets its own hierarchy, set up during onboarding.", center=True)
            + f'<div data-tabs class="tabs-segment" style="text-align:center"><div class="tablist" role="tablist" aria-label="Number of approval levels">{"".join(tabs)}</div>'
            + f'<div class="tab-panels" style="text-align:left">{"".join(panels)}</div></div></div></section>')


APPROVALS = dict(
    name="Approvals & Delegation of Authority", eyebrow="Approvals & Delegation of Authority",
    h1="Approvals that mirror your organisation, and move at your speed.",
    lead="Build your own approval chain, from one level to five, and let requisitions and NFAs route themselves. Every approver sees what's waiting, and every decision is recorded.",
    hero_visual=M.browser("app.proceaze.in/approvals", M.approvals(), aria="Illustrative approval chain with approve, reject and send-back actions"),
    problem=("Approvals stall when they live in inboxes.",
             "Without a fixed route, requests wait, requesters chase, and nobody can say later who signed off.",
             [("No fixed route", "Nobody is sure who should approve what, or in which order."),
              ("No visibility", "Requests sit unseen, and requesters chase approvers by phone."),
              ("No record", "Sign-offs on email are hard to find and harder to audit.")]),
    solution=("Your Delegation of Authority, built into every request.",
              "ProcEaze configures an approval hierarchy for each client. Requests move through it automatically, with role-specific dashboards at every level."),
    features=[
        dict(icon="network", title="1–5 approval levels", text="Every client gets its own chain, configured to its Delegation of Authority."),
        dict(icon="check-circle", title="Approve, reject or send back", text="Approvers act in one click and can add comments for the requester."),
        dict(icon="dashboard", title="Role-specific dashboards", text="Directors, heads, managers and buyers each see their own queue and spend."),
        dict(icon="stamp", title="NFA approvals", text="Notes for Approval route through the same hierarchy with quotes and ranking attached."),
        dict(icon="mail", title="Email notifications", text="Approvers are notified when a request reaches them."),
        dict(icon="history", title="Permanent audit trail", text="Every approval, rejection and send-back is time-stamped and attributed."),
    ],
    after_hero=lambda: S.approvals_section("section section-light"),
    ui=("Every approver, one clear queue.",
        "Approvers see the request, the price basis and where it sits in the chain, then act in one click. Send-backs return to the requester with comments.",
        ["Director → Head → Manager → Buyer, or any chain you need", "Pending time visible for every request", "Decisions recorded with name and time"],
        M.browser("app.proceaze.in/nfa/0091", M.nfa_note(), aria="Illustrative Note for Approval screen")),
    workflow=("A requisition's journey through your hierarchy.", [
        ("send", "Buyer submits", "Requisition raised from the cart"),
        ("user-check", "Manager", "Level 1 approval"),
        ("users", "Department head", "Level 2 approval"),
        ("crown", "Director", "Level 3, where your DoA requires it"),
        ("file-check", "Purchase order", "Issued once fully approved"),
    ]),
    benefits=[("clock", "Faster turnaround", "Requests reach the right approver immediately."),
              ("eye", "Visibility", "Everyone can see where a request stands."),
              ("scale", "Policy built in", "Your DoA is enforced, not remembered."),
              ("history", "Audit-ready", "Every decision is on the record.")],
    related=["dashboards.html", "catalogue.html", "security.html"],
)

# ---------------------------------------------------------------------------
# Dashboards
# ---------------------------------------------------------------------------
DASHBOARDS = dict(
    name="Procurement Spend Management", eyebrow="Procurement spend management", parent=("Software", "platform.html"),
    h1="Procurement spend management that shows every rupee, live.",
    lead="Role-specific dashboards show spend, ARC utilisation, category trends and approval turnaround as they happen, from the director's view down to a single buyer's orders.",
    hero_visual=M.browser("app.proceaze.in/analytics", M.analytics(), aria="Illustrative spend analytics dashboard"),
    problem=("Spend visibility usually arrives a month late.",
             "When procurement runs on email and spreadsheets, the numbers only exist after someone compiles them.",
             [("Month-end surprises", "Spend is pieced together from bills and spreadsheets after it has happened."),
              ("No view of compliance", "Leadership can't see how much is bought on contract and how much isn't."),
              ("Hidden bottlenecks", "Slow approvals and stuck orders don't show up until someone complains.")]),
    solution=("Procurement reporting and analytics for every role.",
              "Every requisition, approval and PO runs through ProcEaze, so spend dashboards and reports are always current."),
    features_id="reporting-analytics",
    features=[
        dict(icon="rupee", title="Company-wide spend", text="Spend by plant, department, category and vendor."),
        dict(icon="lock", title="ARC utilisation", text="How much catalogue spend runs on contracted prices."),
        dict(icon="trending-up", title="Category trends", text="Spot shifts in what your sites are buying."),
        dict(icon="clock", title="Approval turnaround", text="See where requests wait, and for how long."),
        dict(icon="users", title="Role-specific views", text="Directors, heads, buyers and finance each see what matters to them."),
        dict(icon="download", title="Downloadable audit trail", text="Export the record whenever audit or finance asks."),
    ],
    ui=("A view for every role.",
        "Directors see the whole company. Department heads see their team. Buyers see their own orders. Finance sees contract compliance and PO terms.",
        ["Spend by plant, department and category", "Approval queues and turnaround", "Periodic spend reports from your KAM"],
        M.role_mock("director")),
    workflow=("From transaction to insight, without a spreadsheet.", [
        ("cart", "Requisition", "Raised in ProcEaze"),
        ("check-circle", "Approval", "Recorded with time and name"),
        ("file-check", "Purchase order", "Issued on contracted terms"),
        ("bar-chart", "Dashboard", "Updated as it happens"),
        ("headset", "Spend report", "Shared by your KAM periodically"),
    ]),
    extra=S.dashboard_section,
    benefits=[("gauge", "Decide on live data", "No waiting for month-end."),
              ("lock", "Compliance visible", "ARC utilisation at a glance."),
              ("hourglass", "Bottlenecks surfaced", "See where approvals wait."),
              ("download", "Reports on demand", "Export whenever needed.")],
    related=["approvals.html", "arc-pricing.html", "solutions/leadership.html"],
)

# ---------------------------------------------------------------------------
# Sourcing Desk
# ---------------------------------------------------------------------------
SOURCING = dict(
    name="Sourcing Desk", eyebrow="Sourcing Desk",
    h1="One desk for sourcing, from RFQ to purchase order.",
    lead="The Sourcing Desk brings RFQs, quote comparison, reverse auctions, AI negotiation, vendor selection, NFAs and POs into one place for your procurement team.",
    hero_visual=M.browser("app.proceaze.in/sourcing/RFQ-2026-0318", M.sourcing_desk(), aria="Illustrative RFQ quote comparison screen"),
    problem=("Sourcing runs across too many tools.",
             "Every off-contract requirement turns into a chain of emails, attachments and spreadsheets.",
             [("Quotes in inboxes", "RFQs go out by email and quotes come back in every format."),
              ("Manual comparisons", "Teams rebuild the same comparison sheet for every requirement."),
              ("Gaps between steps", "Vendor selection, NFA and PO are disconnected, so context gets lost.")]),
    solution=("Everything off-contract, handled in one flow.",
              "Raise the RFQ, compare quotes, run an auction or AI negotiation, then move straight to NFA and PO without leaving the desk."),
    features=[
        dict(icon="send", title="RFQ creation", text="Raise an RFQ from a requirement and invite vendors."),
        dict(icon="table", title="Quote comparison", text="Compare quotes side by side with L1 / L2 / L3 ranking."),
        dict(icon="gavel", title="Send to auction", text="Move a requirement to a reverse auction when competition helps.", href="reverse-auction.html", cta="Reverse auctions"),
        dict(icon="bot", title="Negotiate with AI", text="Hand a shortlist to the AI Price Negotiator.", status="early", href="ai-negotiator.html", cta="AI Price Negotiator"),
        dict(icon="stamp", title="NFA from the desk", text="Raise a Note for Approval with quotes and recommendation attached."),
        dict(icon="file-check", title="PO on approval", text="Approved NFAs become purchase orders."),
    ],
    ui=("From comparison to Note for Approval.",
        "When the best offer is clear, the NFA carries the ranking, quotes and recommendation to your approvers. Nothing is retyped.",
        ["L1 / L2 / L3 with source of each price", "Recommendation and attachments in one place", "Approve, reject or send back"],
        M.browser("app.proceaze.in/nfa/0091", M.nfa_note(), aria="Illustrative Note for Approval screen")),
    workflow=("The sourcing flow, end to end.", [
        ("clipboard-list", "Requirement", "Off-contract need raised"),
        ("send", "RFQ", "Sent to selected vendors"),
        ("table", "Compare", "Quotes ranked side by side"),
        ("gavel", "Auction or AI", "When it helps the price"),
        ("stamp", "NFA approval", "Through your hierarchy"),
        ("file-check", "Purchase order", "Issued to the vendor"),
    ]),
    benefits=[("layers", "One desk", "No more switching between tools."),
              ("table", "Clean comparisons", "Every quote in the same format."),
              ("history", "Context kept", "From RFQ to PO on one record."),
              ("clock", "Faster cycles", "Fewer hand-offs between steps.")],
    related=["reverse-auction.html", "ai-negotiator.html", "vendor-portal.html"],
)

# ---------------------------------------------------------------------------
# Reverse Auctions — interactive simulation
# ---------------------------------------------------------------------------
def auction_sim_section():
    types = [
        ("English reverse auction", "trending-down",
         "Bidders see the current L1 price and their own rank, and bid down in minimum decrements until the clock runs out. "
         "A bid in the final seconds extends the clock, so nobody wins by sniping."),
        ("Japanese descending clock", "timer",
         "The price starts at the ceiling and drops by a fixed decrement every round. Bidders confirm to stay in. "
         "The last bidder standing wins at the final price."),
    ]
    cards = "".join(f'<article class="card reveal" style="--d:{i}">{icon_tile(ic)}<h3 class="mt-16">{t}</h3><p>{d}</p></article>'
                    for i, (t, ic, d) in enumerate(types))
    return (f'<section class="section section-light" id="simulation"><div class="container">'
            + section_head("Interactive demonstration", "Run a simulated auction.",
                           "Choose an auction type and start the simulation. Bidders, prices and timings are simulated for illustration. This is not live data.", center=True)
            + f'<div class="reveal-frame" style="max-width:1080px;margin-inline:auto">{M.browser("app.proceaze.in/auctions/RA-2026-0142", M.auction_board(full=True))}</div>'
            + f'<div class="grid grid-2 mt-48" style="max-width:1080px;margin-inline:auto">{cards}</div>'
            + '</div></section>')


AUCTION = dict(
    name="Reverse Auctions", eyebrow="Reverse Auction Portal", interest="Auctions",
    h1="Live bidding that drives prices down.",
    lead="The ProcEaze Auction Portal runs live reverse auctions for your requirements: transparent ranking for vendors, full control for buyers. Try the simulation below.",
    actions=lambda: btn_demo("Contact Us", "btn-white btn-lg", "Auctions") + '<a class="btn btn-ghost-light btn-lg" href="#simulation">Try the simulation</a>',
    after_hero=auction_sim_section,
    problem=("Price discovery by email is slow and opaque.",
             "Sequential quote rounds take days and give vendors little reason to sharpen their price.",
             [("Round after round", "Revised quotes trickle in over days of follow-up."),
              ("No competitive tension", "Vendors can't see where they stand, so they hold their price."),
              ("Hard to defend", "The final choice is difficult to justify without a clear record of bids.")]),
    solution=("Live, transparent, and on the record.",
              "Invite qualified vendors, set the ceiling, reserve and decrement, and let the market find the price."),
    features=[
        dict(icon="rupee", title="Ceiling price", text="Set the opening price that bids must beat."),
        dict(icon="trending-down", title="Minimum decrement", text="Each new bid must improve on L1 by at least the decrement."),
        dict(icon="timer", title="Timer & anti-sniping", text="Bids in the final seconds extend the clock automatically."),
        dict(icon="bar-chart", title="L1 / L2 / L3 live ranking", text="Vendors see their rank, never each other's names."),
        dict(icon="target", title="Reserve price", text="A buyer-only reserve shows whether the result is acceptable."),
        dict(icon="history", title="Bid history", text="Every bid time-stamped, for the NFA and audit."),
    ],
    workflow=("From requirement to purchase order.", [
        ("clipboard-list", "Requirement", "Lot, quantity and specification"),
        ("users", "Invite vendors", "Qualified vendors only"),
        ("gavel", "Live auction", "English or Japanese format"),
        ("bar-chart", "Ranking", "L1 / L2 / L3 at close"),
        ("stamp", "NFA approval", "Your approvers decide"),
        ("file-check", "Purchase order", "Issued to the awarded vendor"),
    ]),
    benefits=[("trending-down", "Price discovery", "The market sets the price, live."),
              ("eye", "Transparency", "Every vendor sees a fair, ranked process."),
              ("clock", "Faster cycles", "Hours instead of rounds of follow-up."),
              ("history", "Defensible awards", "Every bid on the record.")],
    related=["sourcing.html", "ai-negotiator.html", "vendor-portal.html"],
)

# ---------------------------------------------------------------------------
# AI Price Negotiator (early access)
# ---------------------------------------------------------------------------
def nego_sim_section():
    return (f'<section class="section section-light" id="simulation"><div class="container">'
            + section_head("Inside a negotiation", "From vendor discovery to buyer decision.",
                           "The full pipeline: vendor discovery, GSTIN verification, chat or voice negotiation, live leaderboard and escalation. Press Run negotiation. Vendors and prices are illustrative.", center=True)
            + f'<div class="reveal-frame">{M.browser("app.proceaze.in/negotiator/RFQ-2026-0318", M.negotiator(full=True))}</div>'
            + '</div></section>')


def control_section():
    pts = ["Negotiates only within the target and policy you set",
           "Escalates exceptions, such as credit terms, to the buyer",
           "The buyer can take over any negotiation at any time",
           "A full transcript is kept for every conversation",
           "The final award goes through your NFA approval"]
    nodes = [("target", "Buyer sets target & policy", "Before any negotiation starts"),
             ("bot", "AI negotiates", "Chat or voice, within limits"),
             ("alert-triangle", "Exceptions escalated", "Anything outside policy"),
             ("hand", "Buyer decides", "Shortlist, override or award"),
             ("stamp", "NFA & PO", "Approved by people")]
    layers = "".join(f'<div class="sec-layer reveal" style="--d:{i}"><span class="icon-tile">{icon(a)}</span><div><strong>{b}</strong><span>{c}</span></div><em>{i + 1:02d}</em></div>'
                     for i, (a, b, c) in enumerate(nodes))
    return (f'<section class="section section-navy"><div class="bg-dots" aria-hidden="true"></div><div class="container" style="position:relative"><div class="split">'
            f'<div>{section_head("Human in the loop", "Buyer remains in control.", "The AI Price Negotiator is an assistant, not a decision-maker. It works within the targets you set, escalates what falls outside them and stops the moment a buyer takes over.")}'
            f'{check_list(pts)}</div>'
            f'<div class="sec-visual reveal-frame"><div class="sec-layers">{layers}</div></div></div></div></section>')


AI = dict(
    name="AI Price Negotiator", eyebrow="AI Price Negotiator", status="early", interest="AI Negotiator",
    h1="An AI that negotiates with vendors on your behalf.",
    lead="Set a target price and a vendor pool. The AI Price Negotiator verifies vendors, negotiates over chat or voice, and brings back a ranked shortlist with full transcripts. The buyer remains in control.",
    actions=lambda: btn_demo("Join early access", "btn-white btn-lg", "AI Negotiator") + '<a class="btn btn-ghost-light btn-lg" href="#simulation">Watch the demo</a>',
    after_hero=lambda: S.ai_section(title="Watch the negotiation control tower at work.") + nego_sim_section(),
    problem=("Negotiation is where buyers' time goes.",
             "Every quote invites a counter, and every counter is another call, email or WhatsApp thread.",
             [("Endless back-and-forth", "Buyers spend hours per requirement chasing revised quotes."),
              ("Inconsistent outcomes", "Results depend on who negotiates and how much time they have."),
              ("No record of the conversation", "Phone negotiations leave nothing to show approvers or auditors.")]),
    solution=("Consistent negotiation, at the scale of your requirements.",
              "The AI agent applies the same discipline to every vendor and every requirement, and documents all of it."),
    features=[
        dict(icon="search", title="Vendor discovery", text="Find vendors for the requirement from your vendor pool."),
        dict(icon="badge-check", title="GSTIN verification", text="Check vendor GSTINs before negotiation begins."),
        dict(icon="target", title="Target price & benchmark", text="Negotiate against your target, with a benchmark for context."),
        dict(icon="mic", title="Voice & chat negotiation", text="Negotiate with vendors over chat or voice."),
        dict(icon="file-text", title="Negotiation transcript", text="Every exchange recorded and attached to the requirement."),
        dict(icon="gauge", title="Reliability score", text="Each vendor's offer shown with a reliability score."),
        dict(icon="bar-chart", title="Live leaderboard", text="Offers ranked in real time as negotiations progress."),
        dict(icon="alert-triangle", title="Escalation", text="Anything outside your policy goes to the buyer."),
        dict(icon="hand", title="Buyer override", text="Take over any negotiation at any time. The AI pauses."),
    ],
    extra=control_section,
    workflow=("How a negotiation runs.", [
        ("search", "Discover", "Vendors matched to the requirement"),
        ("badge-check", "Verify", "GSTIN checked"),
        ("message", "Negotiate", "Chat or voice, against target"),
        ("bar-chart", "Rank", "Live leaderboard"),
        ("hand", "Buyer decides", "Shortlist, escalate or override"),
        ("stamp", "NFA & PO", "Approved through your hierarchy"),
    ]),
    benefits=[("clock", "Hours back", "Less manual back-and-forth for buyers."),
              ("repeat", "Consistency", "The same discipline on every requirement."),
              ("file-text", "Full transcripts", "Every conversation documented."),
              ("hand", "Human control", "People make every award.")],
    related=["sourcing.html", "reverse-auction.html", "approvals.html"],
)

# ---------------------------------------------------------------------------
# Vendor Portal
# ---------------------------------------------------------------------------
VENDOR_PORTAL = dict(
    name="Vendor Portal", eyebrow="Vendor Portal",
    h1="Receive RFQs, join auctions and track awarded POs in one portal.",
    lead="The ProcEaze Vendor Portal gives suppliers one place to respond to RFQs matched to their categories, take part in reverse auctions and follow awarded purchase orders.",
    actions=lambda: btn_demo("Contact Us", "btn-white btn-lg") + btn_link("vendors.html", "Register as a Vendor", "btn-ghost-light btn-lg"),
    hero_visual=M.browser("vendors.proceaze.in/overview", M.vendor_portal(), aria="Illustrative vendor portal overview"),
    problem=("Suppliers deserve a clear, fair process too.",
             "For vendors, enterprise procurement often means phone calls, scattered emails and little idea where a quote stands.",
             [("RFQs by phone and email", "Requirements arrive in every format, through every channel."),
              ("Opaque outcomes", "Vendors rarely know how their quote ranked or why."),
              ("PO follow-ups", "Tracking awarded orders means chasing buyers for updates.")]),
    solution=("One portal for every opportunity.",
              "Register once, get verified, and see RFQs, auctions and POs from ProcEaze clients in one place."),
    features=[
        dict(icon="inbox", title="Matched RFQs", text="RFQs routed to you based on the categories you supply."),
        dict(icon="send", title="Quote submission", text="Submit quotes in a consistent format, on time."),
        dict(icon="gavel", title="Auction participation", text="Bid in live reverse auctions with transparent ranking."),
        dict(icon="file-check", title="PO tracking", text="Follow awarded purchase orders through to delivery."),
        dict(icon="id-card", title="Profile & documents", text="GSTIN, PAN, registration and bank details kept on file."),
    ],
    workflow=("From registration to delivery.", [
        ("id-card", "Register", "Company and contact details"),
        ("badge-check", "Verification", "GSTIN, PAN and documents"),
        ("inbox", "Matched RFQs", "Based on your categories"),
        ("gavel", "Quote or bid", "RFQ response or live auction"),
        ("file-check", "PO awarded", "Tracked in the portal"),
        ("truck", "Deliver", "Delivery confirmed on record"),
    ]),
    benefits=[("inbox", "More opportunities", "RFQs matched to what you supply."),
              ("eye", "Transparency", "Know where you stand."),
              ("file-check", "Clear POs", "Awarded orders in one place.")],
    related=["vendors.html", "reverse-auction.html", "solutions/vendors.html"],
)

# ---------------------------------------------------------------------------
# Integrations
# ---------------------------------------------------------------------------
INTEGRATION_ITEMS = [
    ("database", "SAP & other ERPs", "ready", "Plug-in ready", "ERP plug-in ready. Integration scoped during onboarding."),
    ("key", "Single sign-on (SSO)", "roadmap", None, "SSO-ready architecture, with SSO on the roadmap. Today, users sign in with passwordless OTP."),
    ("mail", "Email notifications", "live", None, "Requesters and approvers are notified by email as requests move."),
    ("cloud", "Cloud document storage", "live", None, "Quotes, NFAs and POs stored securely in the cloud."),
    ("banknote", "Payment gateway & invoice matching", "roadmap", None, "Planned for the Payment & Reconciliation stage."),
    ("code", "APIs", "on-request", "On request", "Available for integration projects on request."),
]


def integrations_status_section():
    cards = "".join(
        f'<article class="card feature-card reveal" style="--d:{i % 3}"><div class="card-head">{icon_tile(ic)}{badge(st, text=lab)}</div>'
        f'<h3>{esc(t)}</h3><p>{d}</p></article>'
        for i, (ic, t, st, lab, d) in enumerate(INTEGRATION_ITEMS))
    return (f'<section class="section"><div class="container">'
            + section_head("Integration status", "What connects today, and what's next.", "We label every integration honestly, so you can plan around it.")
            + f'<div class="grid grid-3">{cards}</div>'
            + f'<p class="small muted mt-24">SAP is a trademark of its respective owner. ProcEaze does not claim an existing integration partnership with any ERP vendor; ERP connections are scoped and delivered per client.</p>'
            + '</div></section>')


def integrations_body():
    hero = page_hero([("Platform", "platform.html"), ("Integrations", None)], "Integrations",
                     "Fits into the systems you already run.",
                     "ProcEaze is ERP plug-in ready. Integration with SAP and other ERPs is scoped during onboarding, so you add ProcEaze without a rip-and-replace.",
                     actions=btn_demo("Discuss your integration", "btn-white btn-lg", "ERP integration") + btn_link("security.html", "Security & trust", "btn-ghost-light btn-lg"),
                     visual=f'<div class="dark-panel">{M.integrations_hub()}</div>')
    out = hero + integrations_status_section()
    out += (f'<section class="section section-light"><div class="container">'
            + section_head("How integration is scoped", "Agreed during onboarding, around your ERP.", None, center=True)
            + workflow([("search", "Discovery", "Your ERP, masters and data flows"),
                        ("clipboard-list", "Scope", "What syncs, in which direction, and when"),
                        ("plug", "Configure", "Plug-in set up for your ERP"),
                        ("check-circle", "Go live", "Tested with your team")])
            + '</div></section>')
    out += (f'<section class="section section-tight"><div class="container">'
            + section_head("Benefits", "Add ProcEaze, keep your ERP.", None)
            + benefits([("refresh", "No rip-and-replace", "ProcEaze works alongside your ERP."),
                        ("layers", "One flow", "Procurement in ProcEaze, finance in your ERP."),
                        ("clipboard-list", "Scoped to you", "Only the integrations you need."),
                        ("shield-check", "Secure by design", "Role-based access and audit trail.")])
            + '</div></section>')
    out += related(["security.html", "platform.html", "how-it-works.html"])
    return out


# ---------------------------------------------------------------------------
# Platform overview
# ---------------------------------------------------------------------------
FEATURE_TABS = [
    ("buy", "Buy", "cart", "Order from the contracted catalogue.",
     "Every category, ARC prices pre-loaded, cart validation and one-click requisitions.",
     ["ARC price locked at order", "MOQ and validity on every item", "Requisition routes itself"], "catalogue.html",
     lambda: M.browser("app.proceaze.in/catalogue", M.catalogue_arc(), aria="Illustrative catalogue screen", note=False)),
    ("approve", "Approve", "check-circle", "Approve through your own hierarchy.",
     "Chains of one to five levels, role-specific queues, and a permanent record of every decision.",
     ["Approve, reject or send back", "NFAs through the same chain", "Email notifications"], "approvals.html",
     lambda: M.browser("app.proceaze.in/approvals", M.approvals(), aria="Illustrative approvals screen", note=False)),
    ("source", "Source", "clipboard-list", "Source off-contract needs competitively.",
     "RFQs and quote comparison, with reverse auctions and AI negotiation when the price needs work.",
     ["Side-by-side quote comparison", "Reverse auctions", "AI Price Negotiator (early access)"], "sourcing.html",
     lambda: M.browser("app.proceaze.in/sourcing", M.sourcing_desk(), aria="Illustrative sourcing screen", note=False)),
    ("analyse", "Analyse", "bar-chart", "See it all, live.",
     "Spend, ARC utilisation, category trends and approval turnaround on role-specific dashboards.",
     ["Spend by plant, department and category", "ARC utilisation", "Downloadable audit trail"], "dashboards.html",
     lambda: M.browser("app.proceaze.in/analytics", M.analytics(), aria="Illustrative analytics screen", note=False)),
]


def feature_tabs_section():
    tabs, panels = [], []
    for i, (key, label, ic, h, text, pts, href, vis) in enumerate(FEATURE_TABS):
        sel = i == 0
        tabs.append(f'<button class="tab" type="button" role="tab" id="ft-tab-{key}" aria-controls="ft-panel-{key}" '
                    f'aria-selected="{"true" if sel else "false"}" tabindex="{0 if sel else -1}">{icon(ic)}{label}</button>')
        panels.append(f'<div class="role-panel tab-panel" role="tabpanel" id="ft-panel-{key}" aria-labelledby="ft-tab-{key}"{"" if sel else " hidden"}>'
                      f'<div><p class="role-kicker">{label}</p><h3>{h}</h3><p class="lead">{text}</p>{check_list(pts)}'
                      f'<a class="link-arrow mt-24" href="{L(href)}">Explore {label.lower()} {icon("arrow-right")}</a></div><div>{vis()}</div></div>')
    return (f'<section class="section"><div class="container">'
            + section_head("The platform in action", "Buy, approve, source and analyse in one place.", None, center=True)
            + f'<div data-tabs><div class="tablist reveal" role="tablist" aria-label="Platform capabilities" style="max-width:720px;margin-inline:auto">{"".join(tabs)}</div>'
            + f'<div class="tab-panels">{"".join(panels)}</div></div></div></section>')


def modules_section():
    mods = PLATFORM[1:]
    slides = []
    for i, (f, n, d, ic, st) in enumerate(mods):
        slides.append(f'<li class="mc-slide reveal" style="--d:{min(i, 3)}" role="group" aria-roledescription="slide" aria-label="{i + 1} of {len(mods)}: {esc(n)}">'
                      f'<a class="card module-card mc-card card-link" href="{L(f)}">'
                      f'<span class="mc-num" aria-hidden="true">{i + 1:02d}</span>'
                      f'<div class="card-head">{icon_tile(ic)}{badge(st)}</div><h3>{esc(n)}</h3><p>{esc(d)}.</p>'
                      f'<span class="link-arrow">Explore {icon("arrow-right")}</span></a></li>')
    controls = (f'<div class="mc-controls">'
                f'<button class="mc-btn" type="button" data-mc-prev aria-label="Previous capability">{icon("chevron-left")}</button>'
                f'<div class="mc-dots" data-mc-dots></div>'
                f'<button class="mc-btn" type="button" data-mc-next aria-label="Next capability">{icon("chevron-right")}</button></div>')
    return (f'<section class="section section-mc"><div class="container">'
            + '<div class="section-head-row">' + section_head("Capabilities", "Nine capabilities. One workspace.", "Each capability is marked with its status, so you always know what's live.")
            + f'<div class="reveal">{status_legend()}</div></div>'
            + f'<div class="mod-carousel" data-carousel aria-roledescription="carousel" aria-label="Platform capabilities">'
            + f'<div class="mc-viewport"><ul class="mc-track" data-mc-track>{"".join(slides)}</ul></div>'
            + f'{controls}</div></div></section>')


def goals_section():
    items = [('<span data-count="100" data-suffix="%">100%</span>', "of catalogue requisitions priced at ARC rates", None),
             ('<span>0%</span>', "manual email or WhatsApp ordering", "The platform goal"),
             ('<span data-count="8">8</span>', "connected stages, from catalogue to payment", None),
             ("1–5", "approval levels, configured per client", None)]
    cards = "".join(f'<div class="stat-card reveal" style="--d:{i}"><div class="stat-value">{v}</div><div class="stat-label">{l}</div>'
                    f'{f"<span class=stat-note>{n}</span>" if n else ""}</div>' for i, (v, l, n) in enumerate(items))
    return (f'<section class="section section-tight section-light"><div class="container">'
            + section_head("Designed for control", "The standard ProcEaze is built to hold.", None)
            + f'<div class="stat-grid stat-grid-light">{cards}</div></div></section>')


def software_section():
    """The other Software Solutions pages, which sit alongside this one."""
    cards = "".join(f'<a class="related-card reveal" href="{L(f)}">{icon_tile(ic)}<div><h3>{esc(n)}</h3><p>{esc(d)}</p></div></a>'
                    for f, n, d, ic in SOFTWARE[1:])
    return (f'<section class="section section-light" id="software-solutions"><div class="container">'
            + section_head("Software solutions", "One B2B procurement platform, for every way you buy.",
                           "The same platform, seen through the job you need it to do.")
            + f'<div class="related-grid">{cards}</div></div></section>')


# Platform features live as sections on the software page they belong to
FEATURES_INDEX = [
    ("store", "Supplier management", "Your vendors and their contracted prices, in one place.", "procurement-management-software/#supplier-management"),
    ("clipboard-list", "RFQ / RFx management", "Requests for quotation, compared side by side.", "e-procurement-software/#rfq-rfx-management"),
    ("send", "Purchase requisition management", "One-click requisitions from a validated cart.", "procure-to-pay-software/#purchase-requisition-management"),
    ("network", "Approval workflows", "One to five levels, mirroring your Delegation of Authority.", "procurement-automation/#approval-workflows"),
    ("file-check", "Purchase order management", "POs issued on contracted terms once approved.", "procure-to-pay-software/#purchase-order-management"),
    ("bar-chart", "Procurement reporting & analytics", "Live spend, ARC utilisation and approval turnaround.", "dashboards.html#reporting-analytics"),
    ("plug", "Integrations", "ERP plug-in ready, scoped during onboarding.", "integrations.html"),
]


def features_index_section():
    items = [dict(icon=ic, title=t, text=d, href=h, cta="See how it works") for ic, t, d, h in FEATURES_INDEX]
    return (f'<section class="section" id="platform-features"><div class="container">'
            + section_head("Platform features", "Procurement platform features, from supplier to report.", None, center=True)
            + feature_cards(items) + '</div></section>')


def platform_body():
    hero = page_hero([("B2B Procurement Platform", None)], "B2B procurement platform", "One B2B procurement platform, from catalogue to purchase order.",
                     "ProcEaze connects every stage of indirect and MRO procurement: contracted catalogue buying, approvals, sourcing, auctions, "
                     "AI negotiation and purchase orders, with live visibility for leadership.",
                     actions=hero_actions(), visual=M.browser("app.proceaze.in/dashboard", M.dashboard(), aria="Illustrative ProcEaze dashboard"))
    return (hero + S.lifecycle_section() + software_section() + feature_tabs_section() + features_index_section() + modules_section())


PAGES = [
    dict(path="platform.html", title="B2B Procurement Platform for Indian Enterprises | ProcEaze",
         desc="ProcEaze is a B2B procurement platform from catalogue to purchase order: ARC-locked buying, 1–5 level approvals, POs and live spend analytics.",
         section="platform", crumbs=[("B2B Procurement Platform", None)], schemas=[SOFTWARE_SCHEMA], body=platform_body),
    mk("catalogue.html", "Catalogue & Buying: 5 Lakh+ Products | ProcEaze",
       "MRO procurement platform with 5,00,000+ products across 56+ categories, ARC prices pre-loaded, cart validation and one-click purchase requisitions.", CATALOGUE),
    mk("arc-pricing.html", "ARC Rate Contract Management Software | ProcEaze",
       "Rate contract management that locks ARC prices at the point of order. 100% of catalogue requisitions priced at contracted rates, with renewals handled by your KAM.", ARC),
    mk("approvals.html", "Approval Workflow & Delegation of Authority | ProcEaze",
       "Approval workflow software with 1–5 configurable levels, approve, reject or send back, NFA approvals and a permanent audit trail.", APPROVALS),
    mk("dashboards.html", "Procurement Spend Management Software | ProcEaze",
       "Procurement spend management software with live spend analytics: company-wide spend, ARC utilisation, category trends and approval turnaround by role.", DASHBOARDS),
    mk("sourcing.html", "Sourcing Desk: RFQ to Purchase Order | ProcEaze",
       "Sourcing software with one desk for RFQs, side-by-side quote comparison, reverse auctions, AI negotiation, NFAs and purchase orders, in one place.", SOURCING),
    mk("reverse-auction.html", "Reverse Auction Software India | ProcEaze",
       "Reverse auction software for Indian enterprises: English and Japanese formats, L1/L2/L3 ranking, reserve price, anti-sniping and bid history. Try the simulation.", AUCTION),
    mk("ai-negotiator.html", "AI Price Negotiator: AI Procurement Software | ProcEaze",
       "An AI agent that negotiates with vendors over chat or voice against your target price, with GSTIN verification, transcripts and buyer control. Early access.", AI),
    mk("vendor-portal.html", "Vendor Management Portal | ProcEaze",
       "A vendor portal to receive matched RFQs, join reverse auctions and track awarded purchase orders in one place.", VENDOR_PORTAL),
    dict(path="integrations.html", title="Integrations: ERP Plug-in Ready | ProcEaze",
         desc="ProcEaze is ERP plug-in ready. Integration with SAP and other ERPs is scoped during onboarding. Email notifications and cloud document storage are live.",
         section="platform", crumbs=[("Platform", "platform.html"), ("Integrations", None)], body=integrations_body),
]
