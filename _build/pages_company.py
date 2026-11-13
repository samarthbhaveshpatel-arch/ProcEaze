"""Categories, How It Works, Security, Become a Vendor, About, Why ProcEaze, Request a Demo, Contact.

COMPARE (Platform vs Managed Procurement) is rendered on the Procurement Services hub, pages_services.py."""
from lib import (icon, icon_tile, badge, esc, L, section_head, page_hero, hero_actions, btn_demo, btn_link, feature_cards, workflow, benefits, check_list, related, demo_form, f_input, f_phone, f_select,
                 f_checks, f_textarea, f_consent, success_panel, APP_URL, photo_frame)
import mockups as M
import blocks as B
import signature as S

# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------
CONFIRMED = [
    ("hard-hat", "Safety & PPE", "Personal protective equipment for plants, sites and warehouses.", ["Safety helmets", "Gloves", "Safety shoes", "Eye protection", "Harnesses"]),
    ("wrench", "MRO", "Maintenance, repair and operations supplies that keep equipment running.", ["Maintenance spares", "Consumables", "Adhesives & sealants", "Tapes"]),
    ("zap", "Electricals", "Cables, switchgear, lighting and electrical consumables.", ["Cables & wires", "Switchgear", "Lighting", "Panel accessories"]),
    ("nut", "Fasteners", "Bolts, nuts, screws, washers and anchors in standard grades.", ["Bolts & nuts", "Screws", "Washers", "Anchors"]),
    ("bearing", "Bearings & Power Transmission", "Bearings, belts, chains, couplings and housings.", ["Ball bearings", "Roller bearings", "Belts & chains", "Couplings"]),
    ("notebook", "Paper & Stationery", "Copier paper, notebooks, files and everyday stationery.", ["Copier paper", "Notebooks", "Files & folders", "Writing instruments"]),
    ("pen", "Office & Stationery Supplies", "Office essentials for every desk, team and meeting room.", ["Desk supplies", "Printer consumables", "Organisers", "Whiteboard supplies"]),
    ("laptop", "IT & Electronics", "Computing peripherals, networking accessories and electronics.", ["Peripherals", "Networking accessories", "Storage", "Cables & adapters"]),
    ("hammer", "Hand Tools", "Spanners, screwdrivers, pliers and tool kits for maintenance teams.", ["Spanners", "Screwdrivers", "Pliers", "Tool kits"]),
    ("cog", "Industrial Plants & Machinery", "Equipment and machinery for plant operations.", ["Plant equipment", "Machinery spares", "Workshop equipment"]),
]

def categories_body():
    hero = page_hero([("Categories", None)], "Categories", "5 lakh+ products. 56+ categories. One login.",
                     "Everything your sites, plants and offices need, at your contracted prices.",
                     actions=btn_demo("Contact Us", "btn-white btn-lg") + btn_link("catalogue.html", "See how buying works", "btn-ghost-light btn-lg"), bg="about-operations")
    art = lambda ic, n: f'<div class="cat-art has-photo{" banner" if S.is_banner(n) else ""}">{S.cat_photo(n)}{icon_tile(ic)}</div>'
    card = lambda ic, n, d, items, anchor: (
        f'<li><article class="cat-card"{(' id="' + S.cat_slug(n) + '"') if anchor else ""}>{art(ic, n)}<h3>{esc(n)}</h3><p>{d}</p>'
        f'<ul class="cat-items" aria-label="Typical items">{"".join(f"<li>{esc(x)}</li>" for x in items)}</ul></article></li>')

    # Two auto-scrolling rows running in opposite directions. Each track holds its
    # cards twice so the loop is seamless; the copy is hidden from assistive tech.
    def row(cats, reverse):
        real = "".join(card(*c, anchor=True) for c in cats)
        copy = "".join(card(*c, anchor=False) for c in cats)
        return (f'<div class="cat-marquee{" reverse" if reverse else ""} reveal">'
                f'<div class="cat-marquee-track"><ul class="cat-marquee-list">{real}</ul>'
                f'<ul class="cat-marquee-list" aria-hidden="true">{copy}</ul></div></div>')
    half = (len(CONFIRMED) + 1) // 2
    cards = row(CONFIRMED[:half], reverse=False) + row(CONFIRMED[half:], reverse=True)
    out = hero + S.orbit_section("section section-light")
    out += (f'<section class="section"><div class="container">'
            + section_head("Confirmed categories", "The core of your contracted catalogue.", "Typical items are shown for orientation. Your catalogue is configured for your company by your Key Account Manager.")
            + f'<div class="cat-marquees">{cards}</div></div></section>')
    out += (f'<section class="section"><div class="container">'
            + section_head("Set up for you", "Your catalogue, configured around your contracts.", None, center=True)
            + feature_cards([
                dict(icon="headset", title="Configured by your KAM", text="Your Key Account Manager sets up the catalogue for your company, sites and categories."),
                dict(icon="lock", title="ARC prices loaded", text="Contracted prices, MOQs and validity appear on every ARC item."),
                dict(icon="refresh", title="Updates on request", text="New items, price changes and renewals are handled by your KAM."),
            ]) + '</div></section>')
    return out


# ---------------------------------------------------------------------------
# How it works
# ---------------------------------------------------------------------------
def how_body():
    hero = page_hero([("How It Works", None)], "How it works", "From onboarding to purchase order, step by step.",
                     "How ProcEaze goes live for your company, and how ordering, approvals and sourcing work once it does.",
                     actions=btn_demo("Contact Us", "btn-white btn-lg") + '<a class="btn btn-ghost-light btn-lg" href="#onboarding">See the workflows</a>')
    out = hero + S.how_section("section", link=False)

    onboarding = [
        ("01", "Client credentials issued", "Your workspace is created and credentials are issued to your administrators."),
        ("02", "Catalogue & ARC configured", "Your catalogue, contracted ARC prices, MOQs and validity are loaded."),
        ("03", "Org hierarchy built", "Departments, users, roles and approval chains of one to five levels are set up."),
        ("04", "Dedicated KAM assigned", "A named Key Account Manager becomes your single point of contact."),
    ]
    tl = "".join(f'<li class="tl-item reveal" style="--d:{i}"><span class="tl-dot">{n}</span>'
                 f'<div class="tl-body"><h3>{t}</h3><p>{d}</p></div></li>' for i, (n, t, d) in enumerate(onboarding))
    out += (f'<section class="section section-light" id="onboarding"><div class="container"><div class="split">'
            f'<div>{section_head("Client onboarding", "We set you up. Your KAM stays with you.", "For enterprises onboarded by the ProcEaze team, these are the four steps to go live.")}'
            f'</div><ol class="timeline">{tl}</ol></div></div></section>')

    out += (f'<section class="section"><div class="container">'
            + section_head("Self-service onboarding", "Or set up your organisation yourself.", "The self-service path, from first sign-in to a working department dashboard.", center=True)
            + workflow([("mail", "Work email + OTP", "Sign in with a one-time password"),
                        ("building", "Organisation details", "Company, sites and departments"),
                        ("users", "Create users", "Invite your team"),
                        ("network", "Set approval roles", "Who approves what"),
                        ("dashboard", "Department dashboard", "Ready to order")])
            + '</div></section>')

    out += (f'<section class="section section-blue"><div class="bg-dots" aria-hidden="true"></div><div class="container" style="position:relative">'
            + section_head("Order workflow", "How a catalogue order moves.", "Every step is recorded, from the first search to delivery.", center=True)
            + workflow([("search", "Browse", "Search the contracted catalogue"),
                        ("clipboard-check", "Cart validation", "ARC price, MOQ and validity"),
                        ("send", "Submit PR", "One click from the cart"),
                        ("check-circle", "Approval", "Through your hierarchy"),
                        ("file-check", "Confirmation", "PO issued to the vendor"),
                        ("truck", "Delivery & audit", "Delivered and on record")])
            + '</div></section>')

    paths = [
        ("clipboard-list", "Through RFQ", None, "Raise an RFQ to your vendors, compare quotes side by side and choose the best offer."),
        ("gavel", "Through reverse auction", None, "Run a live auction with L1/L2/L3 ranking, reserve price and anti-sniping."),
        ("store", "ProcEaze as vendor", None, "Choose ProcEaze as the vendor. The requisition goes straight to purchase approval and ProcEaze handles sourcing, pricing and fulfilment."),
    ]
    cards = "".join(f'<article class="card card-hover feature-card reveal" style="--d:{i}"><div class="card-head">{icon_tile(ic)}{badge(st)}</div>'
                    f'<h3>{t}</h3><p>{d}</p></article>' for i, (ic, t, st, d) in enumerate(paths))
    out += (f'<section class="section"><div class="container">'
            + section_head("Managed procurement & sourcing", "Three routes for off-contract needs.", "Whichever route you take, the result goes through NFA approval and becomes a purchase order.", center=True)
            + f'<div class="grid grid-3">{cards}</div>'
            + f'<div class="center mt-48 reveal" style="display:flex;justify-content:center">'
            + '<ol class="flow">' + "".join(f'<li><span class="flow-pill{" solid" if t == "Purchase order" else ""}">{icon(ic)}{t}</span>{icon("arrow-right", "flow-arrow")}</li>'
                                            for ic, t in [("clipboard-list", "RFQ / Auction / ProcEaze"), ("stamp", "NFA approval"), ("file-check", "Purchase order")])
            + '</ol></div></div></section>')

    return out


# ---------------------------------------------------------------------------
# Engagement models
# ---------------------------------------------------------------------------
COMPARE = [
    ("What it is", "Your teams run procurement on ProcEaze: catalogue, approvals, sourcing, auctions and POs, with your own vendors.",
     "ProcEaze supplies for you. Choose ProcEaze as the vendor for a requisition and it goes straight to purchase approval."),
    ("Best for", "Enterprises with an in-house procurement team.", "Companies wanting to outsource indirect / MRO buying."),
    ("Catalogue", "Your contracted catalogue, with your vendors' ARC prices.", "ProcEaze's own catalogue, with ProcEaze as the vendor."),
    ("Sourcing tools", "RFQs run by your team, plus reverse auctions and the AI Price Negotiator (early access).",
     "ProcEaze handles sourcing, pricing and fulfilment for requisitions placed with ProcEaze."),
    ("Approvals", "Your one- to five-level hierarchy for every requisition, NFA and PO.", "Requisitions go straight to purchase approval in your hierarchy."),
    ("Dashboards", "Role-specific dashboards and spend analytics.", "The same dashboards, including spend placed with ProcEaze."),
    ("KAM", "Dedicated Key Account Manager.", "Dedicated Key Account Manager."),
    ("Commercials", "Pricing on request.", "Pricing on request."),
]


# ---------------------------------------------------------------------------
# Security
# ---------------------------------------------------------------------------
PILLARS = [
    ("database", "Complete data isolation per client", "Each client's users, catalogue, ARC prices, vendors, documents and records are kept separate from every other client.",
     ["A separate workspace for each client", "No shared pricing or catalogue data between clients", "Client-specific hierarchy and roles"]),
    ("smartphone", "Passwordless OTP sign-in", "Users sign in with a one-time password. There are no passwords to steal, reuse or reset.",
     ["One-time password at sign-in", "No passwords to leak or reuse", "Accounts tied to the user's email"]),
    ("users", "Role-based access", "What each user can see and do is defined by their role in your organisation.",
     ["Buyers see their orders", "Approvers see their queue", "Leadership and finance views by role"]),
    ("history", "Permanent audit trail", "Every order, approval and rejection is time-stamped, attributed and downloadable.",
     ["Who did what, and when", "Approvals, rejections and send-backs", "Export whenever audit asks"]),
    ("cloud", "Secure cloud document storage", "Quotes, NFAs and purchase orders are stored securely in the cloud, linked to the transaction they belong to.",
     ["Documents linked to each transaction", "No attachments lost in inboxes", "Access follows role permissions"]),
    ("key", "Encrypted tokens", "Sessions are secured with encrypted tokens, tied to the signed-in user and their role.",
     ["Encrypted session tokens", "Access tied to user and role", "Signed-in state verified by the platform"]),
]


def security_body():
    hero = page_hero([("Security & Trust", None)], "Security & trust", "Enterprise-grade control, by design.",
                     "Procurement data is commercially sensitive: prices, vendors, contracts and approvals. ProcEaze separates every client, authorises every user and records every action.",
                     actions=btn_demo("Contact Us", "btn-white btn-lg") + btn_link("integrations.html", "Integrations", "btn-ghost-light btn-lg"),
                     visual=M.security_visual())
    cards = "".join(f'<article class="card card-hover reveal" style="--d:{i % 2}"><div class="card-head">{icon_tile(ic, "solid")}</div>'
                    f'<h3>{t}</h3><p>{d}</p>{check_list(pts)}</article>' for i, (ic, t, d, pts) in enumerate(PILLARS))
    out = hero + S.trust_section()
    out += (f'<section class="section"><div class="container">'
            + section_head("Six layers of control", "How ProcEaze protects procurement data.", None)
            + f'<div class="grid grid-2">{cards}</div></div></section>')
    out += (f'<section class="section section-light"><div class="container"><div class="split">'
            f'<div>{section_head("Straight answers", "We only claim what is true today.", "Security reviews deserve precise answers. We label roadmap items as roadmap, and we don\'t list certifications or hosting commitments on this website.")}</div>'
            f'<div class="stack">'
            f'<div class="notice info reveal">{icon("info")}<p><strong>Single sign-on (SSO)</strong> is on the roadmap. Today, users sign in with passwordless OTP. {badge("roadmap")}</p></div>'
            f'<div class="notice info reveal">{icon("info")}<p><strong>Security questionnaires.</strong> If your evaluation includes one, share it with our team during your demo.</p></div>'
            f'<div class="notice info reveal">{icon("info")}<p><strong>ERP integration</strong> is scoped during onboarding, including what data moves and in which direction. {badge("ready", text="Plug-in ready")}</p></div>'
            f'</div></div></div></section>')
    out += related(["approvals.html", "integrations.html", "solutions/finance.html"], "Related")
    return out


# ---------------------------------------------------------------------------
# Become a vendor
# ---------------------------------------------------------------------------
STATES = ["Andaman and Nicobar Islands", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chandigarh", "Chhattisgarh",
          "Dadra and Nagar Haveli and Daman and Diu", "Delhi", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jammu and Kashmir",
          "Jharkhand", "Karnataka", "Kerala", "Ladakh", "Lakshadweep", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya",
          "Mizoram", "Nagaland", "Odisha", "Puducherry", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
          "Uttar Pradesh", "Uttarakhand", "West Bengal"]
BUSINESS_TYPES = ["Proprietorship", "Partnership", "LLP", "Private Limited", "Public Limited", "Other"]
DOCS = [("id-card", "GSTIN", "GST registration certificate"), ("id-card", "PAN", "Company or proprietor PAN"),
        ("building", "Company registration", "Incorporation or registration certificate"),
        ("banknote", "Bank details", "Cancelled cheque or bank letter"),
        ("file-text", "Product catalogue / price list", "What you supply, and at what price"),
        ("stamp", "Authorisation letters", "From OEMs or brands, where applicable")]


def vendor_form():
    p = "vr"
    cats = [c[1] for c in CONFIRMED]
    return (
        f'<div class="form-card form-wrap" id="register">'
        f'<h2 style="font-size:1.6rem">Register as a Vendor</h2><p class="muted" style="margin-bottom:24px">Takes about five minutes. Fields marked * are required.</p>'
        f'<form data-form="vendor" novalidate data-toast="Vendor registration received. Our vendor team will be in touch.">'
        f'<div class="form-grid">'
        + f_input(p, "company", "Company name", auto="organization", placeholder="Registered company name", full=True)
        + f_input(p, "contact", "Contact name", auto="name", placeholder="Full name")
        + f_input(p, "email", "Email", "email", auto="email", placeholder="name@company.com", rule="email")
        + f_phone(p)
        + f_input(p, "gstin", "GSTIN", placeholder="24ABCDE1234F1Z5", rule="gstin", attrs='maxlength="15" autocapitalize="characters" spellcheck="false"',
                  hint="15 characters, as on your GST registration.")
        + f_input(p, "city", "City", auto="address-level2", placeholder="City")
        + f_select(p, "state", "State / UT", STATES)
        + f_checks(p, "categories", "Categories you supply", cats, required=True)
        + f_input(p, "brands", "Brands", required=False, placeholder="Brands you manufacture or are authorised for")
        + f_input(p, "website", "Website", "url", required=False, auto="url", placeholder="https://")
        + f_textarea(p, "message", "Message", placeholder="Locations you serve, capacity, anything else we should know")
        + (f'<div class="field full"><label class="consent" for="{p}-docs"><input type="checkbox" id="{p}-docs" name="documents" required aria-describedby="{p}-docs-err">'
           f'<span>I can share GSTIN, PAN, company registration, bank details and a product catalogue / price list during verification<span class="req" aria-hidden="true">*</span></span></label>'
           f'<p class="field-error" id="{p}-docs-err">{icon("alert-circle")}<span></span></p></div>')
        + f_consent(p, f'I agree to be contacted and accept the <a href="{L("privacy.html")}">Privacy Policy</a> and <a href="{L("vendor-terms.html")}">Vendor Terms</a>')
        + f'</div><div class="form-actions mt-16"><span class="form-note">{icon("lock")} Documents are requested only during verification.</span>'
        f'<button class="btn btn-primary btn-lg" type="submit">Register as a Vendor {icon("arrow-right", "icon icon-arrow")}</button></div></form>'
        + success_panel("Thank you for registering!", "Our vendor team will review your details and contact you about verification and next steps.",
                        f'<button class="btn btn-secondary mt-24" type="button" data-form-again>Register another company</button>')
        + '</div>'
    )


def vendors_body():
    hero = page_hero([("Become a Vendor", None)], "Become a vendor", "Supply to India's industrial enterprises through ProcEaze.",
                     "Register once to receive RFQs matched to your categories, take part in reverse auctions and track awarded purchase orders.",
                     actions='<a class="btn btn-white btn-lg" href="#register">Register as a Vendor ' + icon("arrow-right", "icon icon-arrow") + '</a>'
                             + btn_link("vendor-portal.html", "Preview the Vendor Portal", "btn-ghost-light btn-lg"),
                     visual=photo_frame("vendor-dispatch", "Goods being loaded for dispatch at a warehouse"))
    out = hero
    out += (f'<section class="section"><div class="container">'
            + section_head("How it works for vendors", "Four steps to your first order.", None, center=True)
            + workflow([("id-card", "Register once", "Company, contact and categories"),
                        ("inbox", "Receive matched RFQs", "Based on what you supply"),
                        ("gavel", "Participate in auctions", "Live, ranked and fair"),
                        ("file-check", "Track POs", "From award to delivery")])
            + f'<p class="center small muted mt-32">Register once to receive RFQs, join reverse auctions and track your purchase orders in the Vendor Portal.</p>'
            + '</div></section>')
    docs = "".join(f'<li class="reveal" style="--d:{i}">{icon_tile(ic)}<div><strong>{t}</strong><span>{d}</span></div></li>' for i, (ic, t, d) in enumerate(DOCS))
    out += (f'<section class="section section-light"><div class="container"><div class="split" style="align-items:start">'
            f'<div>{section_head("Documents needed", "Keep these ready for verification.", "You don\'t need to upload anything to register. Our vendor team will ask for these during verification.")}'
            f'<ul class="challenge-list sec-list">{docs}</ul>'
            f'</div>'
            f'{vendor_form()}</div></div></section>')
    out += related(["solutions/vendors.html", "vendor-portal.html", "reverse-auction.html"], "Related")
    return out


# ---------------------------------------------------------------------------
# About
# ---------------------------------------------------------------------------
def about_body():
    hero = page_hero([("About Us", None)], "About ProcEaze", "Built by people who run supply chains.",
                     "ProcEaze was built inside working supply-chain operations in Ahmedabad, by a team that buys, stores and moves industrial goods every day.",
                     actions=btn_demo("Contact Us", "btn-white btn-lg") + btn_link("platform.html", "Explore the platform", "btn-ghost-light btn-lg"),
                     visual=photo_frame("about-operations", "Warehouse racking stocked with industrial goods",
                                        f'<div class="photo-chip">{icon("factory")}Built from real procurement operations</div>'))
    story = [
        ("Origin", "Built for our own operations", "ProcEaze started as an in-house tool for procurement across our own supply-chain operations in Ahmedabad.", None),
        ("RProc", "The first version", "The first version, RProc, ran our own procurement: catalogue buying, approvals and purchase orders, replacing email and spreadsheets.", None),
        ("ProcEaze", "A platform for every enterprise", "RProc evolved into ProcEaze: a multi-client platform with complete data isolation, configurable approval hierarchies and a dedicated Key Account Manager for every client.", None),
        ("Today", "Sourcing, auctions and AI", "The Sourcing Desk, Reverse Auction Portal and Vendor Portal bring sourcing onto the platform. The AI Price Negotiator is in early access.", None),
    ]
    tl = "".join(f'<li class="tl-item reveal" style="--d:{i}"><span class="tl-dot">{i + 1:02d}</span>'
                 f'<div class="tl-body"><span class="tl-kicker">{k}</span><h3>{t} {badge(st)}</h3><p>{d}</p></div></li>'
                 for i, (k, t, d, st) in enumerate(story))
    out = hero
    out += (f'<section class="section"><div class="container"><div class="split" style="align-items:start">'
            f'<div>{section_head("Our story", "From an internal tool to a procurement platform.", None)}'
            f'<div class="stack reveal"><p class="lead">We didn\'t start with software. We started with procurement: thousands of industrial items, many sites, contracted prices that didn\'t always reach the order, and approvals that lived in inboxes.</p>'
            f'<p class="muted">So we built the tool we needed. Because it was built by people who run supply chains, it follows how industrial procurement actually works in India: annual rate contracts, layered approvals, NFAs and a long tail of MRO categories.</p></div></div>'
            f'<ol class="timeline">{tl}</ol></div></div></section>')
    principles = [
        dict(icon="factory", title="Built from operations", text="Every workflow comes from procurement we have run ourselves."),
        dict(icon="badge-check", title="Honest about status", text="We label what's live, in early access and on the roadmap."),
        dict(icon="shield-check", title="Control by design", text="Data isolation, role-based access and a permanent audit trail from day one."),
        dict(icon="headset", title="Service, not just software", text="Every client gets a named Key Account Manager."),
    ]
    out += (f'<section class="section section-light"><div class="container">'
            + section_head("How we work", "What we hold ourselves to.", None, center=True)
            + feature_cards(principles, cols=4) + '</div></section>')
    out += related(["why-proceaze/", "careers.html", "security.html"], "More about ProcEaze")
    return out


# ---------------------------------------------------------------------------
# Contact Us
# ---------------------------------------------------------------------------
def contact_body():
    hero = page_hero([("Contact Us", None)], "Contact Us", "Talk to the ProcEaze team.",
                     "Questions about the platform, pricing or a demo? Send us a message and our team will get back to you.",
                     compact=True)
    nxt = [("clock", "Within one business day", "Our team gets back to you by email or phone."),
           ("layers", "A 30-minute walkthrough", "Configured around your categories, contracts and approval hierarchy."),
           ("message-circle", "Your questions answered", "Engagement model, integration and pricing (on request).")]
    tl = "".join(f'<li class="tl-item"><span class="tl-dot">{icon(ic)}</span><div class="tl-body"><h3 style="font-size:1rem">{t}</h3><p>{d}</p></div></li>'
                 for ic, t, d in nxt)
    side = (f'<aside class="stack">'
            f'<div class="card card-flat"><h2 style="font-size:1.35rem">What happens next</h2><ol class="timeline mt-24">{tl}</ol></div>'
            f'<div class="card card-flat"><div class="card-head">{icon_tile("log-in")}</div><h3>Already a client?</h3>'
            f'<p>Sign in to your workspace.</p><a class="link-arrow" href="{APP_URL}" rel="nofollow">Sign in {icon("arrow-right")}</a></div>'
            f'<div class="card card-flat"><div class="card-head">{icon_tile("store")}</div><h3>Are you a vendor?</h3>'
            f'<p>Register to supply through ProcEaze.</p><a class="link-arrow" href="{L("vendors.html")}">Become a Vendor {icon("arrow-right")}</a></div>'
            f'</aside>')
    out = hero
    out += (f'<section class="section"><div class="container"><div class="split split-form">'
            f'<div class="form-card"><h2 style="font-size:1.6rem">Contact Us</h2>'
            f'<p class="muted" style="margin-bottom:24px">Tell us a little about your company. Fields marked * are required.</p>{demo_form("ct")}</div>'
            f'{side}</div></div></section>')
    return out


# ---------------------------------------------------------------------------
# Why ProcEaze
# ---------------------------------------------------------------------------
WHY = [
    dict(icon="factory", title="Built from real operations", text="ProcEaze began as the tool our own supply-chain operations in Ahmedabad needed. Every workflow comes from procurement we have run ourselves.", href="about.html", cta="Our story"),
    dict(icon="lock", title="Contract prices that reach the order", text="ARC prices are locked at the point of order, so every catalogue requisition goes out at the contracted rate.", href="arc-pricing.html", cta="ARC pricing"),
    dict(icon="network", title="Approvals that mirror your DoA", text="One to five levels, configured to your Delegation of Authority, with approve, reject and send back in one click.", href="approvals.html", cta="Approval workflows"),
    dict(icon="grid", title="Every category, one login", text="5,00,000+ products across 56+ categories, from PPE and MRO spares to stationery and IT.", href="categories.html", cta="Browse categories"),
    dict(icon="briefcase", title="Run it, or run it with us", text="Use the platform with your own vendors, or choose ProcEaze as the vendor through Managed Procurement.", href="services/", cta="Procurement services"),
    dict(icon="headset", title="A named Key Account Manager", text="Every client gets a KAM who configures the catalogue, loads ARC prices and handles renewals.", href="how-it-works.html", cta="How onboarding works"),
    dict(icon="shield-check", title="Control by design", text="Complete data isolation per client, passwordless OTP sign-in, role-based access and a permanent audit trail.", href="security.html", cta="Security & trust"),
    dict(icon="badge-check", title="Honest about status", text="Every capability is labelled live, early access or roadmap, so you can plan around what's real.", href="platform.html", cta="See the platform"),
]

USUAL_WAY = [
    ("Ordering", "Requests by email, phone and WhatsApp", "One-click requisitions from a validated cart"),
    ("Prices", "Buyers ask for the rate, or pay what's quoted", "ARC price shown on the product and locked at order"),
    ("Approvals", "Sign-offs scattered across inboxes", "Your 1–5 level chain, with every decision recorded"),
    ("Categories", "A different vendor and portal per category", "56+ categories in one catalogue, one login"),
    ("Visibility", "Spend compiled from spreadsheets at month-end", "Role-based spend dashboards, live"),
    ("Audit", "Hunting for emails when audit asks", "A downloadable, time-stamped audit trail"),
]


def why_body():
    hero = page_hero([("Why ProcEaze", None)], "Why ProcEaze", "Why ProcEaze: procurement software built by people who buy.",
                     "Most procurement software is designed around a process diagram. ProcEaze was designed around a working procurement desk: "
                     "annual rate contracts, layered approvals and a long tail of industrial categories.",
                     actions=btn_demo("Request a Demo", "btn-primary btn-lg magnetic") + btn_link("platform.html", "Explore the platform", "btn-secondary btn-lg"),
                     visual=photo_frame("about-operations", "Warehouse racking stocked with industrial goods",
                                        f'<div class="photo-chip">{icon("factory")}Built from real procurement operations</div>'))
    rows = "".join(f'<tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td></tr>' for a, b, c in USUAL_WAY)
    table = (f'<div class="compare-wrap reveal"><table class="compare"><caption class="sr-only">Procurement on email and spreadsheets compared with procurement on ProcEaze</caption>'
             f'<thead><tr><th scope="col">Compare</th><th scope="col" class="col-head">Email, WhatsApp &amp; Excel</th>'
             f'<th scope="col" class="col-head">ProcEaze</th></tr></thead><tbody>{rows}</tbody></table></div>')
    out = hero
    out += (f'<section class="section"><div class="container">'
            + section_head("Eight reasons", "Why procurement teams choose ProcEaze.", None, center=True)
            + feature_cards(WHY, cols=4) + '</div></section>')
    out += (f'<section class="section section-light" id="compare"><div class="container">'
            + section_head("The usual way vs ProcEaze", "What changes when procurement moves onto one platform.", None)
            + table + '</div></section>')
    out += S.kam_section()
    out += related(["platform.html", "services/", "request-a-demo/"], "Next steps")
    return out


# ---------------------------------------------------------------------------
# Request a Demo
# ---------------------------------------------------------------------------
def demo_body():
    hero = page_hero([("Request a Demo", None)], "Request a demo", "Request a demo of ProcEaze procurement software.",
                     "A 30-minute walkthrough, configured around your categories, contracts and approval hierarchy. No generic slide deck.",
                     compact=True)
    see = ["Catalogue buying with your ARC prices locked at order",
           "Your approval chain, from one level to five, with NFAs",
           "Role-based dashboards and spend analytics",
           "Managed Procurement, if you'd like ProcEaze to supply for you",
           "What's live and what's in early access, clearly labelled"]
    bring = ["Your main categories (for example PPE, MRO, electricals, stationery)",
             "How approvals work today, and who signs off what",
             "Whether you already have annual rate contracts",
             "The ERP you use, if integration matters"]
    side = (f'<aside class="stack">'
            f'<div class="card card-flat"><h2 style="font-size:1.35rem">What you\'ll see</h2>{check_list(see)}</div>'
            f'<div class="card card-flat"><h2 style="font-size:1.35rem">Helpful to bring</h2>{check_list(bring)}</div>'
            f'<div class="card card-flat"><div class="card-head">{icon_tile("message-circle")}</div><h3>Just have a question?</h3>'
            f'<p>Send us a message instead.</p><a class="link-arrow" href="{L("contact.html")}">Contact Us {icon("arrow-right")}</a></div>'
            f'</aside>')
    out = hero
    out += (f'<section class="section"><div class="container"><div class="split split-form">'
            f'<div class="form-card"><h2 style="font-size:1.6rem">Book your demo</h2>'
            f'<p class="muted" style="margin-bottom:24px">Our team replies within one business day. Fields marked * are required.</p>'
            f'{demo_form("rd", "Request a Demo")}</div>{side}</div></div></section>')
    out += (f'<section class="section section-light"><div class="container">'
            + section_head("How it works", "From request to walkthrough.", None, center=True)
            + workflow([("send", "Request", "Tell us about your company"),
                        ("phone", "Short call", "We confirm your scope and attendees"),
                        ("layers", "Tailored demo", "30 minutes on your categories and approvals"),
                        ("route", "Next steps", "Onboarding plan and commercials on request")])
            + '</div></section>')
    return out


PAGES = [
    dict(path="why-proceaze/", title="Why ProcEaze | Procurement Software Built From Operations",
         desc="Why procurement teams choose ProcEaze: ARC prices locked at order, approvals that mirror your DoA, 56+ categories in one catalogue and a dedicated KAM.",
         section="company", crumbs=[("Why ProcEaze", None)], body=why_body),
    dict(path="request-a-demo/", title="Request a Demo: Procurement Software Walkthrough | ProcEaze",
         desc="Request a 30-minute demo of ProcEaze procurement software, configured around your categories, ARC contracts and approval hierarchy.",
         section="company", crumbs=[("Request a Demo", None)], body=demo_body),
    dict(path="categories.html", title="Categories: 5 Lakh+ Industrial Products | ProcEaze",
         desc="5 lakh+ products across 56+ categories: safety & PPE, MRO, electricals, fasteners, bearings, stationery, IT, hand tools and more, at your contracted prices.",
         section="categories", crumbs=[("Categories", None)], body=categories_body),
    dict(path="how-it-works.html", title="How It Works: Onboarding & Procurement Workflows | ProcEaze",
         desc="How ProcEaze goes live in three steps, with detailed client onboarding, self-service onboarding, order workflow and managed procurement flows.",
         section="how", crumbs=[("How It Works", None)], body=how_body),
    dict(path="security.html", title="Security & Trust | ProcEaze",
         desc="Complete data isolation per client, passwordless OTP sign-in, role-based access, encrypted tokens, secure cloud storage and a permanent audit trail.",
         section="company", crumbs=[("Security & Trust", None)], body=security_body),
    dict(path="vendors.html", title="Become a Vendor: Supply Through ProcEaze",
         desc="Register as a vendor to supply India's industrial enterprises: receive matched RFQs, join reverse auctions and track purchase orders.",
         section="company", crumbs=[("Become a Vendor", None)], body=vendors_body),
    dict(path="about.html", title="About ProcEaze: Built by People Who Run Supply Chains",
         desc="ProcEaze was built inside working supply-chain operations in Ahmedabad, by a team that buys, stores and moves industrial goods every day.",
         section="company", crumbs=[("About Us", None)], body=about_body),
    dict(path="contact.html", title="Contact Us | ProcEaze",
         desc="Contact ProcEaze about procurement software, managed procurement services or supplying as a vendor. Our team replies within one business day.",
         section="company", crumbs=[("Contact", None)], body=contact_body),
]
