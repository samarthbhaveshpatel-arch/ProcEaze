"""Solutions by role and by industry."""
from lib import (icon, icon_tile, badge, esc, L, section_head, page_hero, hero_actions, btn_demo, btn_link,
                 feature_cards, benefits, challenge_list, related, photo, photo_frame)
import mockups as M
import blocks as B
import signature as S

CATEGORY_ICONS = {
    "Safety & PPE": "hard-hat", "MRO": "wrench", "Electricals": "zap", "Fasteners": "nut",
    "Bearings & Power Transmission": "bearing", "Paper & Stationery": "notebook",
    "Office & Stationery Supplies": "pen", "IT & Electronics": "laptop", "Hand Tools": "hammer",
    "Industrial Plants & Machinery": "cog",
}


# ---------------------------------------------------------------------------
# Role pages
# ---------------------------------------------------------------------------
def role_page(d):
    lazy = lambda v: v() if callable(v) else v
    out = page_hero([("Solutions", "solutions.html"), (d["name"], None)], d["eyebrow"], d["h1"], d["lead"],
                    actions=lazy(d.get("actions")) or hero_actions(), visual=d["hero_visual"], badges=d.get("badges", ""))
    out += (f'<section class="section"><div class="container"><div class="split">'
            f'<div>{section_head("Challenges", d["challenges"][0], d["challenges"][1])}</div>'
            f'<div>{challenge_list(d["challenges"][2])}</div></div></div></section>')
    out += (f'<section class="section section-light"><div class="container">'
            + section_head("How ProcEaze helps", d["helps"][0], d["helps"][1], center=True)
            + feature_cards(d["helps"][2]) + '</div></section>')
    t, txt, pts, vis = d["ui"]
    out += (f'<section class="section"><div class="container">'
            + B.spotlight("Your view in ProcEaze", t, txt, pts, vis, lazy(d.get("ui_cta")) or btn_demo("See it in a demo", "btn-primary btn-lg"), reverse=True)
            + '</div></section>')
    out += (f'<section class="section section-tight section-light"><div class="container">'
            + section_head("Benefits", d.get("benefits_title", "What changes for you"), None) + benefits(d["benefits"]) + '</div></section>')
    out += related(d["related"], "Related")
    return out


def mk_role(path, title, desc, d):
    return dict(path=path, title=title, desc=desc, section="solutions",
                crumbs=[("Solutions", "solutions.html"), (d["name"], None)], body=lambda: role_page(d))


LEADERSHIP = dict(
    name="Leadership / CXO", eyebrow="For leadership & CXOs",
    h1="See and control every rupee of procurement spend, live.",
    lead="ProcEaze gives directors and CXOs a live, company-wide view of procurement: spend by plant and category, ARC utilisation and approval turnaround, with control built into every order.",
    hero_visual=M.browser("app.proceaze.in/dashboard", M.dashboard(), aria="Illustrative leadership dashboard"),
    challenges=("Procurement control shouldn't depend on month-end reports.", "What leadership typically faces before ProcEaze.",
                [("Spend seen too late", "Numbers arrive after month-end, compiled by hand."),
                 ("Contract leakage", "Negotiated ARC rates don't always reach the order."),
                 ("Policy depends on people", "The Delegation of Authority lives in a document, not in the process."),
                 ("No single source of truth", "Each plant and category runs on its own tools.")]),
    helps=("Visibility and control, by design.", "Everything that happens in procurement happens in ProcEaze, so leadership sees it as it happens.", [
        dict(icon="dashboard", title="Company-wide dashboard", text="Spend by plant, department, category and vendor, live.", href="dashboards.html", cta="Dashboards"),
        dict(icon="lock", title="ARC utilisation", text="See how much catalogue spend runs on contracted prices."),
        dict(icon="network", title="DoA enforced", text="Approval chains of one to five levels, configured to your policy.", href="approvals.html", cta="Approvals"),
        dict(icon="history", title="Permanent audit trail", text="Every order, approval and rejection on the record."),
        dict(icon="headset", title="Periodic spend reports", text="Your Key Account Manager shares spend reports on a regular schedule."),
        dict(icon="trending-down", title="Competitive price discovery", text="Reverse auctions and the AI Price Negotiator (early access) for off-contract buying."),
    ]),
    ui=("Company-wide spend, ARC utilisation and category trends in real time.",
        "One dashboard for the whole organisation, with the detail a click away.",
        ["Spend by plant, department and category", "Off-contract spend and where it goes", "Approval turnaround across the organisation"],
        M.browser("app.proceaze.in/analytics", M.analytics(), aria="Illustrative spend analytics")),
    benefits=[("shield-check", "Control", "Policy enforced in the process."), ("eye", "Visibility", "Live and company-wide."),
              ("lock", "Compliance", "Contract prices on every catalogue order."), ("history", "Accountability", "Every decision attributed.")],
    related=["dashboards.html", "arc-pricing.html", "approvals.html"],
)

PROCUREMENT = dict(
    name="Procurement & Purchase", eyebrow="For procurement & purchase teams",
    h1="One desk for sourcing, from RFQ to purchase order.",
    lead="Run catalogue buying, RFQs, auctions, AI negotiation, NFAs and POs in one platform, with contracted prices enforced and every step on the record.",
    hero_visual=M.browser("app.proceaze.in/sourcing/RFQ-2026-0318", M.sourcing_desk(), aria="Illustrative sourcing desk"),
    challenges=("Your team's time goes to admin, not sourcing.", "The usual friction in an email-and-spreadsheet procurement function.",
                [("Email-driven RFQs", "Quotes arrive in every format and comparison is manual."),
                 ("Constant price follow-ups", "Negotiation takes hours of calls and messages."),
                 ("ARC enforcement by hand", "Checking every order against the contract isn't possible."),
                 ("Approvals that stall", "NFAs wait in inboxes with no visibility.")]),
    helps=("Routine buying runs itself. Sourcing gets your attention.", "ProcEaze takes catalogue orders off your desk, so your team can focus on what needs sourcing.", [
        dict(icon="lock", title="ARC-locked catalogue", text="Routine buying runs at contracted prices, without your involvement."),
        dict(icon="table", title="Quote comparison", text="RFQ responses ranked side by side, L1 to L3.", href="sourcing.html", cta="Sourcing Desk"),
        dict(icon="gavel", title="Reverse auctions", text="Live competitive bidding when competition helps.", href="reverse-auction.html", cta="Try the simulation"),
        dict(icon="bot", title="AI Price Negotiator", text="An AI agent that negotiates on your behalf, within your targets.", status="early", href="ai-negotiator.html", cta="Watch the demo"),
        dict(icon="stamp", title="NFAs through your DoA", text="Notes for Approval route automatically with quotes attached."),
        dict(icon="headset", title="A dedicated KAM", text="Catalogue, ARC prices and renewals managed with you."),
    ]),
    ui=("From quote comparison to Note for Approval.", "Every price has a source, every recommendation has a record, and approvers see it all.",
        ["L1 / L2 / L3 with the source of each price", "Recommendation with attachments", "Approval through your hierarchy"],
        M.browser("app.proceaze.in/nfa/0091", M.nfa_note(), aria="Illustrative Note for Approval")),
    benefits=[("clock", "Time back", "Less admin, more sourcing."), ("trending-down", "Sharper prices", "Competition and negotiation where it counts."),
              ("history", "Clean records", "Every step documented."), ("layers", "Fewer hand-offs", "RFQ to PO in one flow.")],
    related=["sourcing.html", "reverse-auction.html", "ai-negotiator.html"],
)

HEADS = dict(
    name="Department Heads", eyebrow="For department heads & managers",
    h1="Approve in one click. Know your team's spend.",
    lead="See every request waiting for you, approve, reject or send back in one click, and track what your team is buying.",
    hero_visual=M.browser("app.proceaze.in/approvals", M.approvals(), aria="Illustrative approval queue"),
    challenges=("Approving shouldn't mean digging through inboxes.", "What managers deal with when approvals run on email.",
                [("Approvals across channels", "Requests arrive by email, WhatsApp and in person."),
                 ("No context when approving", "Is this the contract price? Who asked for it, and why?"),
                 ("No view of team spend", "Spend is visible only when finance reports it."),
                 ("Chasing and being chased", "Requesters follow up because they can't see status.")]),
    helps=("Everything you need to decide, in one place.", "Your queue, your team's spend and the full context of each request.", [
        dict(icon="inbox", title="One approval queue", text="Every request waiting for you, with how long it has waited."),
        dict(icon="check-circle", title="Approve, reject or send back", text="Act in one click, with comments for the requester."),
        dict(icon="lock", title="Price basis shown", text="See whether each line is at the ARC price before you approve."),
        dict(icon="bar-chart", title="Team spend", text="Spend by section and category for your team."),
        dict(icon="mail", title="Email notifications", text="Know when a request reaches you."),
        dict(icon="history", title="Decisions on record", text="Every approval is time-stamped and attributed."),
    ]),
    ui=("Approval queues, team spend and turnaround at a glance.", "Your dashboard shows what's pending, what your team spends and how quickly requests move.",
        ["Pending requests with waiting time", "Team spend by section", "Average approval turnaround"], M.role_mock("head")),
    benefits=[("clock", "Faster decisions", "Everything in one queue."), ("eye", "Full context", "Price basis and history on every request."),
              ("bar-chart", "Spend awareness", "Know what your team buys."), ("message-circle", "Fewer follow-ups", "Requesters see status themselves.")],
    related=["approvals.html", "dashboards.html", "catalogue.html"],
)

BUYERS = dict(
    name="Buyers & Requesters", eyebrow="For buyers & requesters",
    h1="Order what you need in minutes, at the right price.",
    lead="Search 5,00,000+ products in your contracted catalogue, add to cart at ARC prices and submit a requisition that routes itself for approval.",
    hero_visual=M.browser("app.proceaze.in/catalogue", M.catalogue_arc(), aria="Illustrative catalogue"),
    challenges=("Buying the basics takes too long.", "What requesters run into without a procurement platform.",
                [("Hunting for items", "Different vendors and portals for every category."),
                 ("Not knowing the price", "Waiting for quotes on items that are already under contract."),
                 ("Chasing approvals", "No way to see where a request is stuck."),
                 ("Re-typing orders", "The same details copied from email to spreadsheet to PO.")]),
    helps=("Search, add to cart, submit. Done.", "ProcEaze takes the guesswork and the follow-ups out of ordering.", [
        dict(icon="search", title="One search", text="The whole catalogue, every category.", href="categories.html", cta="Browse categories"),
        dict(icon="lock", title="Prices pre-loaded", text="ARC prices on every contracted item."),
        dict(icon="clipboard-check", title="Cart validation", text="Price, MOQ and validity checked before you submit."),
        dict(icon="send", title="One-click requisition", text="Your PR routes to the right approver automatically."),
        dict(icon="eye", title="Status at every step", text="See where your request is, from approval to delivery."),
        dict(icon="store", title="ProcEaze as vendor", text="Choose ProcEaze as the vendor on a requisition when that suits you.", href="engagement-models.html", cta="Managed Procurement"),
    ]),
    ui=("Order from your contracted catalogue in minutes, with prices pre-loaded.", "The cart checks everything before you submit, and shows who will approve.",
        ["ARC price, MOQ and validity per line", "Approval route shown up front", "Track to delivery"],
        M.browser("app.proceaze.in/cart", M.cart_requisition(), aria="Illustrative cart and requisition")),
    benefits=[("clock", "Minutes, not days", "No price hunting."), ("lock", "Right price", "ARC applied automatically."),
              ("eye", "Always know the status", "No chasing."), ("grid", "One login", "Every category.")],
    related=["catalogue.html", "categories.html", "approvals.html"],
)

FINANCE = dict(
    name="Finance & Accounts", eyebrow="For finance & accounts",
    h1="Contract-compliant spend with clean records.",
    lead="Contract-compliant pricing, clear PO terms and a permanent, downloadable audit trail for every order.",
    hero_visual=M.browser("app.proceaze.in/orders/PO-24117", M.po_document(), aria="Illustrative purchase order with approval trail"),
    challenges=("Audit shouldn't be an archaeology project.", "Where finance teams lose time when procurement runs on email.",
                [("Price compliance unproven", "Checking orders against contracts is manual."),
                 ("Missing approvals", "Approvals on email are hard to find at audit time."),
                 ("Inconsistent PO terms", "Terms vary by buyer and by vendor."),
                 ("Scattered documents", "Quotes, NFAs and POs saved in different places.")]),
    helps=("Every order, compliant and documented.", "ProcEaze builds the record as procurement happens.", [
        dict(icon="lock", title="ARC-priced requisitions", text="100% of catalogue requisitions priced at ARC rates."),
        dict(icon="file-check", title="PO terms on every order", text="Payment and delivery terms visible on each PO."),
        dict(icon="download", title="Downloadable audit trail", text="Every order, approval and rejection, time-stamped and attributed."),
        dict(icon="cloud", title="Secure document storage", text="Quotes, NFAs and POs stored securely in the cloud."),
        dict(icon="users", title="Role-based access", text="Finance sees what it needs, without editing rights it doesn't."),
        dict(icon="banknote", title="Payment & invoice matching", text="Payment gateway and invoice matching are on the roadmap.", status="roadmap"),
    ]),
    ui=("Contract-compliant pricing, PO terms and a downloadable audit trail.", "A compliance view built for finance: what was bought, at what price, on what terms, approved by whom.",
        ["ARC compliance on catalogue lines", "PO terms by vendor", "Audit exports on demand"], M.role_mock("finance")),
    benefits=[("scale", "Compliance shown", "Not reconstructed."), ("history", "Audit-ready", "Every decision on record."),
              ("file-check", "Consistent POs", "Terms on every order."), ("folder-lock", "Documents in one place", "Stored securely.")],
    related=["arc-pricing.html", "security.html", "integrations.html"],
)


VENDORS = dict(
    name="Vendors", eyebrow="For vendors & suppliers",
    h1="Win more business with transparent, digital sourcing.",
    lead="Supply to India's industrial enterprises through ProcEaze. Register once, receive RFQs matched to your categories, take part in auctions and track awarded POs.",
    actions=lambda: btn_link("vendors.html", "Register as a Vendor", "btn-white btn-lg") + btn_link("vendor-portal.html", "Preview the Vendor Portal", "btn-ghost-light btn-lg"),
    hero_visual=M.browser("vendors.proceaze.in/overview", M.vendor_portal(), aria="Illustrative vendor portal"),
    challenges=("Selling to large enterprises is hard to do well.", "What suppliers tell us gets in the way.",
                [("Opportunities depend on contacts", "Hard to reach the right buyer at a large enterprise."),
                 ("Opaque evaluations", "No visibility on how quotes were compared."),
                 ("Slow PO follow-ups", "Chasing buyers for order and delivery updates."),
                 ("Paperwork, repeated", "The same documents submitted to every customer.")]),
    helps=("A fair, digital route to industrial buyers.", "ProcEaze gives vendors the same clarity it gives buyers.", [
        dict(icon="id-card", title="Register once", text="Your GSTIN, PAN, registration and bank details on file.", href="vendors.html", cta="Register"),
        dict(icon="inbox", title="Matched RFQs", text="RFQs routed to you based on the categories you supply."),
        dict(icon="gavel", title="Fair, ranked auctions", text="See your rank live, never your competitors' names."),
        dict(icon="file-check", title="PO tracking", text="Follow awarded orders through to delivery."),
        dict(icon="store", title="Vendor Portal", text="RFQs, auctions and POs in one place.", href="vendor-portal.html", cta="Preview"),
    ]),
    ui=("Receive RFQs, join auctions and track awarded POs in one portal.", "Your workspace shows what's open, what's live and what's been awarded.",
        ["RFQs matched to your categories", "Live auction schedule", "Awarded PO and delivery status"], M.role_mock("vendor"),
    ),
    ui_cta=lambda: btn_link("vendors.html", "Register as a Vendor", "btn-primary btn-lg"),
    benefits=[("inbox", "More opportunities", "RFQs matched to what you supply."), ("eye", "Transparency", "Know where you stand."),
              ("file-check", "Clear POs", "Awarded orders in one place.")],
    related=["vendors.html", "vendor-portal.html", "reverse-auction.html"],
)


# ---------------------------------------------------------------------------
# Industry pages
# ---------------------------------------------------------------------------
def basket(title, cats):
    chips = "".join(f'<li class="cat-chip">{icon_tile(CATEGORY_ICONS[c])}{esc(c)}</li>' for c in cats)
    return (f'<div class="form-card basket"><p class="tl-kicker">Typical category basket</p>'
            f'<p class="basket-title">{esc(title)}</p>'
            f'<ul class="basket-list">{chips}</ul>'
            f'<div class="m-banner blue" style="margin-top:18px;font-size:.84rem">{icon("lock", "")}All at your contracted prices, in one catalogue.</div></div>')


IND_PHOTO = {
    "Manufacturing & Process Plants": "industry-manufacturing", "Energy & Renewables": "industry-energy",
    "Logistics, Ports & ICDs": "industry-logistics", "Infrastructure & Construction": "industry-infrastructure",
    "Facility Management & Corporate Offices": "industry-facility",
    # No dedicated automotive photo yet; the plant-floor photo is the closest match
    "Automotive & Auto Components": "industry-manufacturing",
}


def industry_page(d):
    visual = photo_frame(IND_PHOTO[d["name"]], d["name"], f'<div class="photo-float">{basket(d["name"], d["cats"])}</div>')
    out = page_hero([("Industries", "industries.html"), (d["name"], None)], "Industries · " + d["name"], d["h1"], d["lead"],
                    actions=hero_actions(), visual=visual)
    out += (f'<section class="section"><div class="container"><div class="split">'
            f'<div>{section_head("Challenges", d["challenges"][0], d["challenges"][1])}</div>'
            f'<div>{challenge_list(d["challenges"][2])}</div></div></div></section>')
    out += (f'<section class="section section-light"><div class="container">'
            + section_head("How ProcEaze helps", d["helps"][0], None, center=True)
            + feature_cards(d["helps"][1]) + '</div></section>')
    out += related(d["related"], "Related")
    return out


def mk_ind(path, title, desc, d):
    return dict(path=path, title=title, desc=desc, section="industries",
                crumbs=[("Industries", "industries.html"), (d["name"], None)], body=lambda: industry_page(d))


def std_helps(first_text, approvals_text, sourcing_text, dash_text):
    return [
        dict(icon="grid", title="One catalogue", text=first_text, href="catalogue.html", cta="Catalogue & Buying"),
        dict(icon="lock", title="ARC prices everywhere", text="The same contracted price at every site, locked at the point of order."),
        dict(icon="network", title="Approvals that fit", text=approvals_text, href="approvals.html", cta="Approvals"),
        dict(icon="clipboard-list", title="Off-contract, handled", text=sourcing_text, href="sourcing.html", cta="Sourcing Desk"),
        dict(icon="bar-chart", title="Live visibility", text=dash_text, href="dashboards.html", cta="Dashboards"),
        dict(icon="headset", title="A dedicated KAM", text="A named Key Account Manager configures your catalogue, ARC prices and renewals."),
    ]


MANUFACTURING = dict(
    name="Manufacturing & Process Plants",
    h1="Manufacturing procurement software that keeps plants running.",
    lead="Manufacturing and process plants buy thousands of MRO, safety and electrical items across sites. ProcEaze puts them in one catalogue at ARC prices, with plant-wise approvals and live visibility for leadership.",
    cats=["MRO", "Bearings & Power Transmission", "Fasteners", "Electricals", "Safety & PPE", "Hand Tools"],
    challenges=("Plant procurement is high-volume and high-stakes.", "Small items, bought often, that stop a line when they're missing.",
                [("High-volume, low-value MRO", "Thousands of spares and consumables, each with its own vendor and price."),
                 ("Multiple plants, different practices", "Each site buys and approves its own way."),
                 ("Urgent breakdown buys", "Unplanned requirements bypass contracts and approvals."),
                 ("Safety compliance", "PPE has to be the right specification, every time.")]),
    helps=("Plant procurement, standardised.", std_helps(
        "MRO, bearings, fasteners, electricals, PPE and tools for every plant, in one place.",
        "Plant-wise and department-wise chains of one to five levels.",
        "Urgent and non-catalogue needs go through RFQ, auction or AI negotiation instead of ad-hoc buying.",
        "Spend and ARC utilisation by plant, department and category.")),
    related=["catalogue.html", "arc-pricing.html", "solutions/procurement.html"],
)

ENERGY = dict(
    name="Energy & Renewables",
    h1="Procurement for sites spread across the map.",
    lead="Energy and renewables operators run plants, substations and project sites far from head office. ProcEaze gives every site the same contracted catalogue and approval rules, and gives leadership one view of spend.",
    cats=["Electricals", "Safety & PPE", "Hand Tools", "MRO", "Fasteners", "IT & Electronics"],
    challenges=("Distance makes procurement harder to control.", "When sites are remote, local buying becomes the default.",
                [("Remote, dispersed sites", "Site teams order through local vendors at local prices."),
                 ("Safety-critical items", "PPE and electricals must meet specification."),
                 ("Project and O&M spend mixed", "Hard to separate and track by site."),
                 ("Approvers in other places", "Requests wait while approvers travel between sites.")]),
    helps=("Every site, the same standard.", std_helps(
        "Electricals, PPE, tools and MRO for every plant and site, in one catalogue.",
        "Online approvals through your hierarchy, wherever approvers are.",
        "Site-specific needs go through RFQ, auction or AI negotiation, not local shopping.",
        "Spend by site and category for operations and leadership.")),
    related=["approvals.html", "dashboards.html", "solutions/leadership.html"],
)

LOGISTICS = dict(
    name="Logistics, Ports & ICDs",
    h1="Procurement that keeps terminals and depots moving.",
    lead="Ports, ICDs and logistics operators run round the clock across terminals, yards and warehouses. ProcEaze brings MRO, safety and office buying into one contracted catalogue, with approvals that match each location.",
    cats=["MRO", "Safety & PPE", "Electricals", "Bearings & Power Transmission", "Fasteners", "Office & Stationery Supplies"],
    challenges=("Operations that never stop need procurement that keeps up.", "Downtime costs more than the part.",
                [("Round-the-clock operations", "Requirements come up at all hours, and approvals can't wait."),
                 ("Equipment uptime", "Spares and consumables must arrive fast and at the right price."),
                 ("Many locations", "Terminals, yards and warehouses buy separately."),
                 ("Safety across the yard", "PPE is in constant demand across teams.")]),
    helps=("Fast, controlled buying at every location.", std_helps(
        "Spares, PPE, electricals and office supplies for every terminal and warehouse.",
        "Location-wise approval chains, with email notifications so requests keep moving.",
        "Non-catalogue spares go through RFQ, auction or AI negotiation.",
        "Spend by location and category, live.")),
    related=["catalogue.html", "approvals.html", "dashboards.html"],
)

INFRA = dict(
    name="Infrastructure & Construction",
    h1="Construction procurement, controlled from site to head office.",
    lead="Infrastructure, construction and EPC companies buy for many projects at once. ProcEaze gives each project its catalogue, prices and approvals, and gives management live, project-wise visibility of spend.",
    cats=["Electricals", "Safety & PPE", "Hand Tools", "Fasteners", "Industrial Plants & Machinery", "MRO"],
    challenges=("Every project is its own procurement operation.", "Control slips when each site buys on its own.",
                [("Many projects, many sites", "Each project buys independently, often from local vendors."),
                 ("Cost control by project", "Spend is hard to attribute to the right project."),
                 ("Contracts don't reach site", "Site teams don't see head-office rate contracts."),
                 ("Urgent site needs", "Requirements can't wait for long quote cycles.")]),
    helps=("Head-office control, site-level speed.", std_helps(
        "Electricals, PPE, tools, fasteners and machinery for every project site.",
        "Project-wise approval chains of one to five levels.",
        "Project requirements go through RFQ, auction or AI negotiation, then NFA and PO.",
        "Spend by project, site and category, live.")),
    related=["sourcing.html", "reverse-auction.html", "solutions/leadership.html"],
)

FM = dict(
    name="Facility Management & Corporate Offices",
    h1="Every office and facility, supplied from one catalogue.",
    lead="Facility managers and corporate admin teams buy stationery, IT, electricals and maintenance supplies across many locations. ProcEaze standardises it with contracted prices, simple ordering and clean records.",
    cats=["Paper & Stationery", "Office & Stationery Supplies", "IT & Electronics", "Electricals", "Safety & PPE", "Hand Tools"],
    challenges=("Small orders add up to a big admin load.", "Frequent purchases, many locations, little visibility.",
                [("Many small orders", "Frequent, low-value orders create heavy admin."),
                 ("Location-by-location buying", "Each office or facility uses its own vendors."),
                 ("Little spend visibility", "Spend by location and category is hard to see."),
                 ("Approval overhead", "Even small orders need a sign-off trail.")]),
    helps=("Simple ordering, standard prices, clean records.", std_helps(
        "Stationery, office supplies, IT, electricals and maintenance items in one place.",
        "Simple one- or two-level approvals for routine orders, longer chains where you need them.",
        "One-off requirements go through RFQ instead of local buying.",
        "Spend by office, facility and category.")),
    related=["catalogue.html", "engagement-models.html", "solutions/buyers.html"],
)

AUTOMOTIVE = dict(
    name="Automotive & Auto Components",
    h1="Automotive procurement for plants that run to the minute.",
    lead="Automotive OEM and auto component plants buy a long tail of MRO spares, tooling, fasteners and safety supplies to keep production lines on schedule. ProcEaze puts them in one catalogue at ARC prices, with plant-wise approvals and live spend visibility.",
    cats=["MRO", "Bearings & Power Transmission", "Fasteners", "Hand Tools", "Safety & PPE", "Electricals"],
    challenges=("Indirect buying can't hold up the line.", "When a spare or consumable is missing, production waits.",
                [("Line-critical spares", "Bearings, belts and maintenance spares are needed fast, at the agreed price."),
                 ("Many plants and shifts", "Each plant and shift raises its own requirements and approvals."),
                 ("Price drift on repeat items", "The same consumables are bought again and again, often at different rates."),
                 ("Shop-floor safety", "PPE has to be the right specification for every line and every shift.")]),
    helps=("Plant-floor procurement, standardised.", std_helps(
        "MRO spares, bearings, fasteners, hand tools, PPE and electricals for every plant, in one place.",
        "Plant-wise and department-wise chains of one to five levels, so urgent requests reach the right approver.",
        "Non-catalogue and urgent spares go through RFQ, auction or AI negotiation instead of ad-hoc buying.",
        "Spend and ARC utilisation by plant, department and category.")),
    related=["industries/manufacturing.html", "arc-pricing.html", "approvals.html"],
)


PAGES = [
    mk_role("solutions/leadership.html", "Procurement Software for Leadership & CXOs | ProcEaze",
            "See and control every rupee of procurement spend, live: company-wide dashboards, ARC utilisation, DoA approvals and a permanent audit trail.", LEADERSHIP),
    mk_role("solutions/procurement.html", "Procurement Software for Purchase Teams | ProcEaze",
            "One desk for sourcing from RFQ to purchase order: ARC-locked catalogue, quote comparison, reverse auctions, AI price negotiation and NFAs.", PROCUREMENT),
    mk_role("solutions/department-heads.html", "Approval Software for Department Heads | ProcEaze",
            "Approve in one click and know your team's spend: one approval queue, price basis on every request and live team dashboards.", HEADS),
    mk_role("solutions/buyers.html", "Purchase Requisition Software for Buyers | ProcEaze",
            "Order from 5,00,000+ products in minutes at contracted ARC prices, with cart validation and one-click purchase requisitions.", BUYERS),
    mk_role("solutions/finance.html", "Procurement Compliance for Finance Teams | ProcEaze",
            "Contract-compliant spend with clean records: ARC-priced requisitions, PO terms on every order and a downloadable audit trail.", FINANCE),
    mk_role("solutions/vendors.html", "Sell to Industrial Enterprises: Vendors | ProcEaze",
            "Win business from India's industrial enterprises: register once, receive matched RFQs, join reverse auctions and track awarded POs.", VENDORS),
    mk_ind("industries/manufacturing.html", "Procurement Software for Manufacturing | ProcEaze",
           "Procurement software for manufacturing and process plants: MRO, bearings, fasteners and PPE in one catalogue at ARC prices, with plant-wise approvals.", MANUFACTURING),
    mk_ind("industries/automotive/", "Procurement Software for Automotive & Auto Components | ProcEaze",
           "Procurement software for automotive and auto component plants: MRO spares, bearings, fasteners, tools and PPE at ARC prices, with plant-wise approvals.", AUTOMOTIVE),
    mk_ind("industries/energy-renewables.html", "Procurement for Energy & Renewables | ProcEaze",
           "One contracted catalogue and approval standard for every plant, substation and project site, with one view of spend.", ENERGY),
    mk_ind("industries/logistics.html", "Procurement for Logistics, Ports & ICDs | ProcEaze",
           "Fast, controlled procurement for terminals, yards and warehouses: MRO, PPE and electricals at contracted prices with location-wise approvals.", LOGISTICS),
    mk_ind("industries/infrastructure.html", "Procurement Software for Infrastructure & Construction | ProcEaze",
           "Construction and infrastructure procurement software: project-wise site catalogues at ARC prices, project approval chains and live project spend for EPC companies.", INFRA),
    mk_ind("industries/facility-management.html", "Procurement for Facility Management & Offices | ProcEaze",
           "Stationery, IT, electricals and maintenance supplies for every office and facility from one contracted catalogue.", FM),
]


# ---------------------------------------------------------------------------
# Hubs: solutions.html and industries.html
# ---------------------------------------------------------------------------
from lib import ROLES, INDUSTRIES  # noqa: E402


def solutions_hub():
    hero = page_hero([("Solutions", None)], "Solutions", "Everyone sees what they need.",
                     "One procurement platform, with a view for every role that touches procurement: leadership, procurement, department heads, buyers, finance and vendors.",
                     actions=hero_actions(("industries.html", "Solutions by industry")),
                     visual=M.role_mock("director"))
    slides = "".join(
        f'<li class="mc-slide reveal" style="--d:{min(i, 3)}" role="group" aria-roledescription="slide" aria-label="{i + 1} of {len(ROLES)}: {esc(n)}">'
        f'<a class="role-card mc-card" href="{L(f)}"><span class="mc-num" aria-hidden="true">{i + 1:02d}</span>'
        f'<span class="role-card-top">{icon_tile(ic)}</span>'
        f'<h3>{esc(n)}</h3><p>{esc(d)}.</p><span class="link-arrow">Explore {icon("arrow-right")}</span></a></li>'
        for i, (f, n, d, ic) in enumerate(ROLES))
    controls = (f'<div class="mc-controls">'
                f'<button class="mc-btn" type="button" data-mc-prev aria-label="Previous role">{icon("chevron-left")}</button>'
                f'<div class="mc-dots" data-mc-dots></div>'
                f'<button class="mc-btn" type="button" data-mc-next aria-label="Next role">{icon("chevron-right")}</button></div>')
    out = hero
    out += (f'<section class="section section-mc"><div class="container">'
            + section_head("By role", "Six roles. One record.", "Each role gets its own dashboard, queue and controls, on the same data.")
            + f'<div class="mod-carousel" data-carousel data-mc-item="role" aria-roledescription="carousel" aria-label="Roles">'
            + f'<div class="mc-viewport"><ul class="mc-track" data-mc-track>{slides}</ul></div>{controls}</div>'
            + '</div></section>')
    out += B.roles_section("section section-light")
    return out


def industries_hub():
    hero = page_hero([("Industries", None)], "Industries", "Built for India's industrial enterprises.",
                     "Manufacturing and automotive plants, construction projects, energy sites, ports and ICDs, and corporate offices all buy differently. ProcEaze is configured around how each one works.",
                     actions=hero_actions(("categories.html", "Browse categories")), bg="industry-logistics")
    out = hero + S.industries_section("section")
    cards = "".join(
        f'<a class="cat-tile reveal {"wide" if i < len(INDUSTRIES) % 3 else "third"}" style="--d:{i % 3}" href="{L(f)}">'
        f'{photo(IND_PHOTO[n], "", "cat-tile-img")}<span class="cat-tile-shade" aria-hidden="true"></span>'
        f'<span class="cat-tile-ico" aria-hidden="true">{icon(ic)}</span>'
        f'<span class="cat-tile-body"><strong>{esc(n)}</strong><span>Challenges, categories and how ProcEaze helps</span></span>'
        f'<span class="cat-tile-go" aria-hidden="true">{icon("arrow-right")}</span></a>'
        for i, (f, n, ic) in enumerate(INDUSTRIES))
    out += (f'<section class="section section-light"><div class="container">'
            + section_head("Industry pages", "Go deeper into your industry.", None)
            + f'<div class="cat-tiles">{cards}</div></div></section>')
    return out


PAGES += [
    dict(path="solutions.html", title="Solutions by Role | ProcEaze",
         desc="Procurement solutions for leadership, procurement teams, department heads, buyers, finance and vendors: one platform, a view for every role.",
         section="solutions", crumbs=[("Solutions", None)], body=solutions_hub),
    dict(path="industries.html", title="Procurement Software by Industry | ProcEaze",
         desc="Procurement software by industry: manufacturing, automotive, infrastructure & construction, energy, logistics, ports & ICDs and facility management in India.",
         section="industries", crumbs=[("Industries", None)], body=industries_hub),
]
