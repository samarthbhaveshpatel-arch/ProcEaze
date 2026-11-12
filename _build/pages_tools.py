"""Procurement Tools (SEO section 8): hub + five free tools.

Interactive logic lives in assets/js/tools.js (loaded via js=("tools",)).
Downloadable templates live in assets/downloads/. Every tool runs entirely in
the browser; nothing a visitor types is sent anywhere.
"""
import re
from lib import (icon, icon_tile, badge, esc, L, route, section_head, page_hero, btn_link, feature_cards,
                 check_list, related, BASE_URL, TOOLS)

ARC_GUIDE = "knowledge-hub/procurement-guides/annual-rate-contract-procurement/"
GLOSSARY = "knowledge-hub/procurement-glossary/"
DL = "assets/downloads/"
ARC_CSV = DL + "annual-rate-contract-item-schedule.csv"
ARC_DOC = DL + "annual-rate-contract-template.html"
SE_CSV = DL + "supplier-evaluation-template.csv"

TOOL_BY_KEY = {t[0]: t for t in TOOLS}


# ---------------------------------------------------------------------------
# Shared pieces (all link-producing helpers run inside body functions only)
# ---------------------------------------------------------------------------
def abs_url(key):
    return BASE_URL + "/" + route(key)


def faq_schema(items):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
                           for q, a in items]}


def app_schema(key, name, desc):
    return {"@context": "https://schema.org", "@type": "WebApplication", "name": name, "url": abs_url(key),
            "description": desc, "applicationCategory": "BusinessApplication",
            "operatingSystem": "Any (runs in a web browser)", "browserRequirements": "Requires JavaScript",
            "isAccessibleForFree": True, "inLanguage": "en-IN",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "INR"},
            "publisher": {"@type": "Organization", "name": "ProcEaze", "url": BASE_URL + "/"}}


def tool_hero(key, h1, lead, extra_actions=""):
    name = TOOL_BY_KEY[key][1]
    actions = (f'<a class="btn btn-primary btn-lg" href="#tool">Use the tool {icon("arrow-right", "icon icon-arrow")}</a>'
               + extra_actions)
    return page_hero([("Procurement Tools", "tools/"), (name, None)], "Free procurement tool", h1, lead,
                     actions=actions, badges=badge("live", text="Free, no sign-up"), compact=True)


def dl_btn(path, label, cls="btn-secondary btn-lg"):
    return f'<a class="btn {cls}" href="{L(path)}" download>{icon("download")} {label}</a>'


def noscript(text):
    return f'<noscript><div class="notice info mt-16">{icon("info")}<p>{text}</p></div></noscript>'


def privacy_note(text="Runs entirely in your browser. Nothing you type is sent to ProcEaze or anyone else."):
    return f'<p class="tool-private">{icon("lock")}<span>{text}</span></p>'


def prose_section(blocks, light=False, sid=None):
    """blocks: list of (h2, html) rendered in a readable two-column grid."""
    cls = "section section-light" if light else "section"
    sid_attr = f' id="{sid}"' if sid else ""
    cols = "".join(f'<div class="prose tool-prose"><h2>{h}</h2>{body}</div>' for h, body in blocks)
    return f'<section class="{cls}"{sid_attr}><div class="container"><div class="tool-prose-grid">{cols}</div></div></section>'


def tips_section(title, items, lead=None):
    return (f'<section class="section section-tight"><div class="container">'
            + section_head("Tips", title, lead)
            + f'<div class="tool-tips">{check_list(items)}</div></div></section>')


def inside_section(title, text, links):
    """links: list of (key, label, status or None)."""
    lis = "".join(f'<li><a class="link-arrow" href="{L(k)}">{esc(t)} {icon("arrow-right")}</a>{badge(st)}</li>'
                  for k, t, st in links)
    return (f'<section class="section section-light section-tight"><div class="container">'
            f'<div class="card card-flat tool-inside reveal"><div class="tool-inside-copy">{icon_tile("layers")}'
            f'<p class="eyebrow">Do this inside ProcEaze</p><h2>{title}</h2><p class="muted">{text}</p></div>'
            f'<ul class="tool-inside-links">{lis}</ul></div></div></section>')


def faq_section(prefix, items):
    qs = []
    for n, (q, a) in enumerate(items, 1):
        qs.append(f'<div class="faq-item"><h3 class="tool-faq-h"><button class="faq-q" type="button" aria-expanded="false" '
                  f'aria-controls="{prefix}-faq-a-{n}" id="{prefix}-faq-q-{n}">{esc(q)}<span class="faq-icon">{icon("plus")}</span></button></h3>'
                  f'<div class="faq-a" id="{prefix}-faq-a-{n}" role="region" aria-labelledby="{prefix}-faq-q-{n}"><div><p>{a}</p></div></div></div>')
    return (f'<section class="section" id="faq"><div class="container container-narrow">'
            + section_head("FAQ", "Frequently asked questions", None)
            + f'<div class="faq">{"".join(qs)}</div></div></section>')


def sibling_tools(current, extra=()):
    keys = [k for k, *_ in TOOLS if k not in ("tools/", current)]
    return related(keys + list(extra), "More free procurement tools")


def inr(n):
    """Indian digit grouping with ₹: 1234567 -> ₹12,34,567."""
    v = int(round(n))
    s = str(abs(v))
    last3, rest = s[-3:], s[:-3]
    if rest:
        last3 = "," + last3
        rest = re.sub(r"\B(?=(\d{2})+(?!\d))", ",", rest)
    return ("-" if v < 0 else "") + "₹" + rest + last3


def inr_short(n):
    if abs(n) >= 1e7:
        return f"₹{round(n / 1e7, 2):g} crore"
    if abs(n) >= 1e5:
        return f"₹{round(n / 1e5, 2 if abs(n) < 1e6 else 1):g} lakh"
    return inr(n)


# ---------------------------------------------------------------------------
# Hub: /tools/
# ---------------------------------------------------------------------------
HUB_FAQ = [
    ("Are these procurement tools free?",
     "Yes. Every tool and template on this page is free to use and download, with no sign-up."),
    ("Is my data sent to ProcEaze?",
     "No. The RFQ generator, supplier evaluation matrix, MRO checklist and savings calculator run entirely in your browser. "
     "Nothing you type is uploaded. The MRO checklist remembers your ticks in your own browser's local storage, on your device only."),
    ("Can I edit the templates?",
     "Yes. The CSV files open in Excel, Google Sheets or LibreOffice, and the contract structure template opens in any browser or word processor. "
     "Adapt them to your organisation's policies, and have contract templates reviewed by your legal team."),
    ("Who are these tools for?",
     "Procurement and purchase teams, plant and facility managers, and finance teams who buy indirect and MRO items such as "
     "spares, consumables, safety equipment, electricals and office supplies."),
]


def hub_body():
    hero = page_hero([("Procurement Tools", None)], "Procurement tools",
                     "Free procurement tools and templates.",
                     "Practical templates, a checklist and calculators for indirect and MRO procurement: write an RFQ, score suppliers, "
                     "structure an annual rate contract and estimate savings from your own numbers.",
                     actions='<a class="btn btn-primary btn-lg" href="#tools-list">Browse the tools ' + icon("arrow-right", "icon icon-arrow") + '</a>'
                             + btn_link("knowledge-hub/procurement-guides/", "Read the procurement guides", "btn-secondary btn-lg"),
                     badges=badge("live", text="Free, no sign-up"), compact=True)
    texts = {
        "tools/annual-rate-contract-template/": "The structure of an annual rate contract, a CSV item schedule and placeholder clauses to review with your legal team.",
        "tools/rfq-template-generator/": "Fill in your requirement, line items and terms, and get a formatted request for quotation to print, copy or download.",
        "tools/supplier-evaluation-template/": "A weighted scoring matrix for two to five suppliers, with live totals, ranking and CSV download.",
        "tools/mro-procurement-checklist/": "42 practical checks across six stages, from demand and specifications to inventory review, with progress saved on your device.",
        "tools/procurement-savings-calculator/": "Estimate price and process savings from your own spend, contract coverage and PO volumes, with the formula shown.",
    }
    cta = {"tools/annual-rate-contract-template/": "Get the template", "tools/rfq-template-generator/": "Build an RFQ",
           "tools/supplier-evaluation-template/": "Score suppliers", "tools/mro-procurement-checklist/": "Open the checklist",
           "tools/procurement-savings-calculator/": "Estimate savings"}
    cards = [dict(icon=ic, title=n, text=texts[k], href=k, cta=cta[k]) for k, n, _, ic in TOOLS if k != "tools/"]
    out = hero
    out += (f'<section class="section" id="tools-list"><div class="container">'
            + section_head("Five free tools", "Procurement templates you can use today.",
                           "Each tool runs in your browser. Nothing you enter is sent anywhere, and the downloads are plain CSV and HTML files you can edit.")
            + feature_cards(cards, cols=3) + '</div></section>')

    rows = [
        ("Annual Rate Contract Template", "You are setting up or renewing a rate contract for repeat items.", "Contract structure (HTML) and item schedule (CSV)"),
        ("RFQ Template Generator", "You need quotations for a new or off-contract requirement.", "A formatted RFQ to print, copy or download"),
        ("Supplier Evaluation Template", "Quotes are in and you need to compare suppliers fairly.", "Weighted scores, ranking and a CSV"),
        ("MRO Procurement Checklist", "You want to review how MRO buying works across its stages.", "A printable checklist with progress"),
        ("Procurement Savings Calculator", "You are building a case for contract coverage or process change.", "An estimate built from your own inputs"),
    ]
    trs = "".join(f'<tr><th scope="row">{esc(a)}</th><td>{esc(b)}</td><td>{esc(c)}</td></tr>' for a, b, c in rows)
    out += (f'<section class="section section-light"><div class="container">'
            + section_head("Which tool, when", "Pick the procurement tool for the job.",
                           "The tools follow the order most procurement work happens in: plan, source, evaluate, contract, buy and review.")
            + f'<div class="compare-wrap reveal"><table class="compare tool-compare"><caption class="sr-only">Which procurement tool to use, and what it produces</caption>'
              f'<thead><tr><th scope="col">Tool</th><th scope="col">Use it when</th><th scope="col">What you get</th></tr></thead><tbody>{trs}</tbody></table></div>'
            + '</div></section>')

    out += prose_section([
        ("Why free procurement templates?",
         "<p>Much of indirect and MRO procurement still runs on documents that each buyer writes from scratch: an RFQ in an email, "
         "a comparison in a spreadsheet, a rate contract copied from last year. Starting from a consistent template means every "
         "supplier gets the same information, every comparison uses the same criteria, and nothing important is left out.</p>"
         "<p>These templates are written for Indian procurement teams: rupees and lakh, GST and HSN codes, annual rate contracts, "
         "notes for approval (NFAs) and multi-site delivery.</p>"),
        ("How they fit together",
         "<p>Use the <strong>savings calculator</strong> to size the opportunity, the <strong>RFQ generator</strong> to collect quotes, "
         "the <strong>supplier evaluation template</strong> to compare them, and the <strong>annual rate contract template</strong> to "
         "lock in the result. The <strong>MRO checklist</strong> covers the whole cycle so you can spot gaps.</p>"
         f'<p>New to a term? The <a href="{L(GLOSSARY)}">procurement glossary</a> explains ARC, MOQ, NFA, L1 and more, and the '
         f'<a href="{L(ARC_GUIDE)}">guide to annual rate contract procurement</a> goes deeper on rate contracts.</p>'),
    ])
    out += faq_section("hub", HUB_FAQ)
    out += related(["knowledge-hub/procurement-guides/", GLOSSARY, "catalogue.html"], "Keep learning")
    return out


HUB_SCHEMA = {
    "@context": "https://schema.org", "@type": "ItemList", "name": "Free procurement tools and templates",
    "itemListElement": [{"@type": "ListItem", "position": i, "name": n, "url": BASE_URL + "/" + k}
                        for i, (k, n, _, _) in enumerate([t for t in TOOLS if t[0] != "tools/"], 1)],
}


# ---------------------------------------------------------------------------
# Annual Rate Contract Template
# ---------------------------------------------------------------------------
ARC_KEY = "tools/annual-rate-contract-template/"

ARC_SECTIONS = [
    ("users", "Parties", "Legal names, registered addresses, GSTIN and PAN of the buyer and supplier, and the authorised contacts on each side."),
    ("calendar", "Period and validity", "Start and end dates, whether POs issued inside the period are honoured after it ends, and that quantities are estimates."),
    ("table", "Item schedule", "Every item with its specification, make, unit of measure, HSN code, GST rate, MOQ, estimated annual quantity and rate."),
    ("rupee", "Price basis and taxes", "Whether rates include GST, freight, packing and insurance, and the delivery basis (for example FOR destination or ex-works)."),
    ("trending-up", "Price variation", "Fixed for the period, linked to a named index with a cap, or revised only on documented request and written approval."),
    ("truck", "Delivery", "Lead time from PO date, delivery locations, documents with each delivery, and when title and risk pass."),
    ("wallet", "Payment", "Credit period from receipt of accepted material and a correct invoice, statutory deductions and bank details."),
    ("badge-check", "Quality and rejection", "Conformance to specification, inspection rights, replacement of rejected items and warranty or shelf life."),
    ("alert-triangle", "Penalties", "Liquidated damages for late delivery, with a cap, and the right to buy elsewhere at the supplier's risk and cost."),
    ("x-circle", "Termination", "Notice period, termination for breach or repeated failures, and what happens to open purchase orders."),
    ("refresh", "Renewal", "How and when the contract is extended or renewed, and whether rates carry over."),
]

ARC_FIELDS = [
    ("Item code", "Your internal item master code, so the contract maps to the item your teams order.", "MRO-SAF-0012"),
    ("Item description", "A short, unambiguous name buyers will recognise.", "Safety helmet, ratchet type"),
    ("Specification / make / grade", "Standard, material, size and approved makes. This is what you inspect against.", "IS 2925, HDPE shell"),
    ("Unit of measure (UoM)", "The unit the rate applies to. State pack sizes explicitly.", "Nos; Box of 100"),
    ("HSN code and GST rate", "The tax classification and rate the supplier will invoice. Have your tax team confirm.", "As per the supplier's invoice and your tax team"),
    ("Minimum order quantity (MOQ)", "The smallest quantity the supplier accepts per order at this rate.", "50 Nos"),
    ("Estimated annual quantity", "An estimate from consumption history. Usually not a purchase commitment; say so in the contract.", "1,200 Nos"),
    ("Rate per UoM (₹, excl. GST)", "The contracted price. Keep taxes in their own column.", "Rate agreed after RFQ"),
    ("Price basis", "Where the price applies and what it includes: freight, packing, unloading.", "FOR destination, freight included"),
    ("Delivery lead time", "Days from PO date to delivery at your location.", "7 days"),
    ("Delivery location(s)", "Which plants, sites or warehouses the rate covers.", "Plant 1, Plant 2"),
    ("Rate valid from / to", "The validity window for this rate, usually the contract period.", "01-04 to 31-03"),
    ("Price variation clause", "Fixed, indexed or revisable on request, as agreed for this item.", "Fixed for contract period"),
]

ARC_FAQ = [
    ("What is an annual rate contract?",
     "An annual rate contract (ARC) is an agreement with a supplier that fixes the rates, terms and conditions for a list of items "
     "for a period, usually a year. You then order as and when you need the items, through purchase orders, at the agreed rates, "
     "without running a fresh RFQ each time."),
    ("Does an ARC commit us to buy a fixed quantity?",
     "Usually not. Most rate contracts state estimated annual quantities for planning and pricing, and say clearly that they are not "
     "a commitment. If you do agree a minimum offtake, write it into the contract explicitly. Your legal team should confirm the wording."),
    ("What should the item schedule include?",
     "For each item: item code, description, specification and make, unit of measure, HSN code and GST rate, MOQ, estimated annual quantity, "
     "rate excluding GST, price basis, delivery lead time, delivery locations and rate validity. The CSV template has a column for each."),
    ("How should price changes be handled during the contract?",
     "Choose one approach per item: rates fixed for the period, rates linked to a named index with a formula and a cap, or revisions "
     "only on documented request and written approval, applying to POs issued after the agreed date. Statutory GST changes follow the law."),
    ("Can I use this template as it is?",
     "No. It is a structural template with placeholder clauses, not legal advice. Use it to organise your contract and the commercial "
     "points to agree, then have your legal team draft or approve the final wording for your organisation."),
    ("When should we start renewing an ARC?",
     "Well before it expires. Review consumption, rejections and delivery performance, decide which items to retender, and leave enough "
     "time for an RFQ and approvals so buyers are not left without contracted rates."),
]


def arc_body():
    out = tool_hero(ARC_KEY, "Annual rate contract template, free to download.",
                    "A ready structure for an annual rate contract (ARC): the clauses to cover, a CSV item schedule and a field-by-field guide. "
                    "Built for indirect and MRO procurement in India.",
                    dl_btn(ARC_CSV, "Item schedule (CSV)"))
    # Downloads
    out += (f'<section class="section" id="tool"><div class="container">'
            + section_head("Downloads", "Download the annual rate contract template.",
                           "Two files: the item schedule, which carries your commercial terms item by item, and the contract structure with placeholder clauses.")
            + '<div class="grid grid-2">'
            + f'<article class="card tool-dl reveal"><div class="card-head">{icon_tile("table")}<span class="tool-file">CSV</span></div>'
              f'<h3>ARC item schedule</h3><p>Opens in Excel, Google Sheets or LibreOffice. Columns for item code, specification, UoM, HSN, GST rate, MOQ, '
              f'estimated quantity, rate, price basis, lead time, locations, validity and price variation. Two example rows to delete.</p>'
              f'<div class="btn-row mt-16">{dl_btn(ARC_CSV, "Download CSV", "btn-primary")}</div></article>'
            + f'<article class="card tool-dl reveal" style="--d:1"><div class="card-head">{icon_tile("file-text")}<span class="tool-file">HTML</span></div>'
              f'<h3>Contract structure template</h3><p>Fifteen sections from parties to renewal, with clauses in placeholder form and Annexure A for the item schedule. '
              f'Open it in a browser to print, or in Word to edit.</p>'
              f'<div class="btn-row mt-16">{dl_btn(ARC_DOC, "Download template", "btn-primary")}</div></article>'
            + '</div>'
            + f'<div class="notice mt-24 reveal">{icon("alert-triangle")}<p><strong>Template, not legal advice.</strong> '
              f'The contract structure is a starting point to organise the commercial terms. It has not been drafted for your organisation, '
              f'suppliers or jurisdiction. Your legal team must review and approve every clause before you use it.</p></div>'
            + '</div></section>')
    # Structure
    cards = "".join(f'<li class="tool-arc-step reveal" style="--d:{i % 3}"><span class="tool-arc-num">{i + 1:02d}</span>'
                    f'<div><h3>{esc(t)}</h3><p>{esc(d)}</p></div></li>' for i, (_, t, d) in enumerate(ARC_SECTIONS))
    out += (f'<section class="section section-light"><div class="container">'
            + section_head("Structure", "What goes into an annual rate contract.",
                           "Eleven parts every ARC should settle. The downloadable template follows the same order, plus definitions and general terms for your legal team.")
            + f'<ol class="tool-arc-steps">{cards}</ol></div></section>')
    # Field-by-field
    trs = "".join(f'<tr><th scope="row">{esc(f)}</th><td>{esc(w)}</td><td>{esc(e)}</td></tr>' for f, w, e in ARC_FIELDS)
    out += (f'<section class="section"><div class="container">'
            + section_head("Item schedule", "Field-by-field guide to the item schedule.",
                           "What to enter in each column of the CSV template. The examples are illustrations only.")
            + f'<div class="compare-wrap reveal"><table class="compare tool-compare"><caption class="sr-only">Annual rate contract item schedule fields</caption>'
              f'<thead><tr><th scope="col">Field</th><th scope="col">What to enter</th><th scope="col">Example</th></tr></thead><tbody>{trs}</tbody></table></div>'
            + '</div></section>')
    out += prose_section([
        ("What an annual rate contract does",
         "<p>An annual rate contract fixes the price and terms for items you buy repeatedly: safety equipment, fasteners, bearings, "
         "electrical consumables, stationery. Instead of collecting quotations for every order, you run one competitive process, agree "
         "rates for the year, and then order against the contract with purchase orders as needs arise.</p>"
         "<p>The value of an ARC depends on two things: how carefully the item schedule is written, and whether buyers actually order at "
         "the contracted rate. A vague specification lets a different make arrive at the same price; a missing price basis turns freight "
         "into an argument at invoice time.</p>"),
        ("How to use this template",
         "<ol><li>List the repeat items from your consumption history in the CSV and write a clear specification for each.</li>"
         "<li>Send the schedule with an RFQ to qualified suppliers and compare quotes on the same basis.</li>"
         "<li>Fill in the agreed rates, MOQ, lead times and validity.</li>"
         "<li>Use the contract structure to agree the commercial terms, then pass it to your legal team for drafting.</li>"
         "<li>Publish the contracted items where buyers order, and set a reminder for renewal.</li></ol>"
         f'<p>For a fuller walk-through, read the <a href="{L(ARC_GUIDE)}">guide to annual rate contract procurement</a>.</p>'),
    ], light=True)
    out += tips_section("Getting more from a rate contract.", [
        "Write specifications you can inspect against: standard, grade, size and approved makes, not just a product name.",
        "Keep GST, freight and packing in separate columns so quotes compare on the same basis.",
        "State that quantities are estimates unless you genuinely intend to commit to a minimum offtake.",
        "Agree a price-variation rule up front. Silence invites mid-year revision requests.",
        "Track how much spend actually goes through the contract. An ARC nobody orders against saves nothing.",
        "Start renewal early enough to retender and approve before the old rates expire.",
    ])
    out += inside_section("Contract prices, enforced at the point of order.",
                          "In ProcEaze, your Key Account Manager loads your ARC prices, MOQs and validity into one catalogue. Prices are locked at order, "
                          "and cart validation checks ARC price, MOQ and validity before a requisition goes for approval.",
                          [("arc-pricing.html", "ARC contract pricing", None), ("catalogue.html", "Catalogue and buying", None)])
    out += faq_section("arc", ARC_FAQ)
    out += sibling_tools(ARC_KEY, [GLOSSARY])
    return out


# ---------------------------------------------------------------------------
# RFQ Template Generator
# ---------------------------------------------------------------------------
RFQ_KEY = "tools/rfq-template-generator/"
RFQ_DESC = "Free RFQ template generator: build a request for quotation with line items, delivery, payment and evaluation terms, then print, copy or download it."

RFQ_FAQ = [
    ("What is an RFQ?",
     "A request for quotation (RFQ) is a document that asks suppliers to quote prices and terms for a defined requirement: what you need, "
     "how much, by when, where it must be delivered and on what commercial terms. It is used when you know exactly what you want to buy."),
    ("What should a good RFQ include?",
     "A unique RFQ number, a clear title, line items with specifications, quantities, units and required-by dates, the delivery location, "
     "the quote due date, payment and delivery terms, how quotes will be evaluated, and instructions on how suppliers should quote."),
    ("Is the information I enter sent anywhere?",
     "No. The generator runs entirely in your browser. Nothing is uploaded or stored by ProcEaze. When you download the RFQ, the file is "
     "created on your device."),
    ("Can I save my RFQ and edit it later?",
     "The page does not store your RFQ. Download it as an HTML file (opens in any browser or in Word) or as plain text, and keep that copy. "
     "Refreshing the page clears the form."),
    ("What is the difference between an RFQ, an RFP and a tender?",
     "An RFQ asks for prices on a clearly specified requirement. A request for proposal (RFP) asks suppliers to propose a solution when the "
     "approach is open. A tender is a formal, usually public, process with fixed rules for submission and opening of bids."),
    ("How many suppliers should receive an RFQ?",
     "Enough to make the comparison meaningful. Many organisations' purchase policies set a minimum number of quotations above a value "
     "threshold; follow your own policy and record why if fewer suppliers responded."),
]


def _rf(name, label, type_="text", ph="", full=False, attrs="", hint=None, value="", opt=True):
    fid = f"rfq-{name}"
    req = '<span class="opt">(optional)</span>' if opt else ""
    hint_html = f'<p class="field-hint" id="{fid}-hint">{hint}</p>' if hint else ""
    desc = f' aria-describedby="{fid}-hint"' if hint else ""
    val = f' value="{esc(value)}"' if value else ""
    phs = f' placeholder="{esc(ph)}"' if ph else ""
    return (f'<div class="field{" full" if full else ""}"><label for="{fid}">{label}{req}</label>'
            f'<input class="input" id="{fid}" type="{type_}" data-rfq-field="{name}"{phs}{val}{desc} {attrs}>{hint_html}</div>')


def _rfq_tool():
    uoms = ["Nos", "Kg", "Litre", "Metre", "Box", "Set", "Pair", "Roll", "Pack", "Sq. m"]
    pay = ["100% within 30 days of receipt of accepted material and invoice", "100% within 45 days of receipt of accepted material and invoice",
           "100% within 60 days of receipt of accepted material and invoice", "As per our standard purchase terms"]
    deliv = ["FOR destination, freight, packing and insurance included", "Ex-works, freight extra at actuals", "Door delivery to site, unloading by supplier"]
    evals = ["Lowest total landed cost (L1) among technically compliant quotes, for the whole RFQ",
             "Item-wise lowest landed cost (L1) among technically compliant quotes; orders may be split",
             "Weighted score on price, quality, delivery and technical compliance",
             "Price and delivery lead time, among technically compliant quotes"]
    dl = lambda i, opts: f'<datalist id="{i}">' + "".join(f'<option value="{esc(o)}"></option>' for o in opts) + '</datalist>'
    row_tpl = (
        '<template data-rfq-row><fieldset class="rfq-line" data-rfq-line>'
        '<legend>Line <span data-rfq-line-no>1</span></legend>'
        '<div class="field rfq-c-desc"><label data-for="desc">Description</label><input class="input" type="text" data-li="desc" placeholder="e.g. Safety helmet, ratchet type"></div>'
        '<div class="field rfq-c-spec"><label data-for="spec">Specification / make</label><input class="input" type="text" data-li="spec" placeholder="e.g. IS 2925, white"></div>'
        '<div class="field"><label data-for="qty">Qty</label><input class="input" type="number" min="0" step="any" inputmode="decimal" data-li="qty"></div>'
        '<div class="field"><label data-for="uom">UoM</label><input class="input" type="text" list="rfq-uom-list" data-li="uom" placeholder="Nos"></div>'
        '<div class="field"><label data-for="date">Required by</label><input class="input" type="date" data-li="date"></div>'
        f'<button class="btn btn-ghost btn-sm rfq-remove" type="button" data-rfq-remove>{icon("x")}<span>Remove</span></button>'
        '</fieldset></template>')
    sel = "".join(f'<option{" selected" if i == 0 else ""}>{esc(o)}</option>' for i, o in enumerate(evals))
    form = (
        f'<div class="form-card tool-form">'
        f'<h3 class="tool-h">1. Buyer and RFQ details</h3><div class="form-grid">'
        + _rf("company", "Buyer company", ph="Your company name", attrs='autocomplete="organization"')
        + _rf("number", "RFQ number", ph="e.g. RFQ/2026/014")
        + _rf("title", "RFQ title", ph="e.g. Safety equipment for Plant 2", full=True)
        + _rf("contact", "Contact name", ph="Who suppliers should reply to", attrs='autocomplete="name"')
        + _rf("email", "Contact email", "email", ph="name@company.com", attrs='autocomplete="email"')
        + _rf("phone", "Contact phone", "tel", ph="Phone number", attrs='autocomplete="tel"')
        + _rf("issued", "Date of issue", "date")
        + _rf("due", "Quote due date", "date", full=False)
        + _rf("validity", "Quote validity (days)", "number", ph="e.g. 90", attrs='min="0" step="1" inputmode="numeric"')
        + '</div>'
        f'<h3 class="tool-h">2. Line items</h3>'
        f'<div class="rfq-lines" data-rfq-items></div>{row_tpl}'
        f'<button class="btn btn-secondary btn-sm mt-16" type="button" data-rfq-add>{icon("plus")} Add line item</button>'
        f'<h3 class="tool-h">3. Delivery and commercial terms</h3><div class="form-grid">'
        f'<div class="field full"><label for="rfq-location">Delivery location<span class="opt">(optional)</span></label>'
        f'<textarea class="textarea rfq-short" id="rfq-location" data-rfq-field="location" placeholder="Site name and full delivery address"></textarea></div>'
        + _rf("payment", "Payment terms", ph="Choose or type your terms", full=True, attrs='list="rfq-pay-list"', hint="Pick a suggestion or type your own.")
        + _rf("delivery", "Delivery terms", ph="Choose or type your terms", full=True, attrs='list="rfq-del-list"')
        + f'<div class="field full"><label for="rfq-evaluation">Evaluation basis</label>'
          f'<select class="select" id="rfq-evaluation" data-rfq-field="evaluation">{sel}</select></div>'
        + f'<div class="field full"><label for="rfq-notes">Notes to suppliers<span class="opt">(optional)</span></label>'
          f'<textarea class="textarea" id="rfq-notes" data-rfq-field="notes" placeholder="e.g. Test certificates required with delivery; samples on request; site working hours"></textarea></div>'
        + '</div>' + dl("rfq-uom-list", uoms) + dl("rfq-pay-list", pay) + dl("rfq-del-list", deliv)
        + '</div>')
    actions = (
        '<div class="tool-actions" role="group" aria-label="RFQ actions">'
        f'<button class="btn btn-primary btn-sm" type="button" data-rfq-action="print">{icon("printer")} Print</button>'
        f'<button class="btn btn-secondary btn-sm" type="button" data-rfq-action="copy">{icon("file-text")} Copy as text</button>'
        f'<button class="btn btn-secondary btn-sm" type="button" data-rfq-action="txt">{icon("download")} .txt</button>'
        f'<button class="btn btn-secondary btn-sm" type="button" data-rfq-action="html">{icon("download")} .html</button>'
        f'<button class="btn btn-ghost btn-sm" type="button" data-rfq-action="reset">{icon("refresh")} Clear form</button></div>')
    preview = (
        f'<div class="tool-preview-wrap"><div class="tool-preview-head"><h3 class="tool-h" id="rfq-preview-h">Live preview</h3>{actions}</div>'
        f'<p class="small muted tool-status" role="status" aria-live="polite" data-rfq-status></p>'
        f'<div class="rfq-doc" data-rfq-preview role="region" aria-labelledby="rfq-preview-h" tabindex="0"></div></div>')
    return (f'<div class="tool-app" data-js-only data-rfq>{privacy_note()}<div class="tool-layout">{form}{preview}</div></div>'
            + noscript("The RFQ generator needs JavaScript. You can still use the RFQ checklist below to write your own, "
                       "or turn on JavaScript and reload the page."))


def rfq_body():
    out = tool_hero(RFQ_KEY, "RFQ template generator: build a complete RFQ in minutes.",
                    "Enter your requirement, line items and terms, and get a clean, consistent request for quotation to send to suppliers. "
                    "Print it, copy it or download it. Everything happens in your browser.")
    out += (f'<section class="section" id="tool"><div class="container">'
            + section_head("The generator", "Create your request for quotation.",
                           "Fill in as much as you need. The preview updates as you type, and empty fields show as placeholders so you can see what is missing.")
            + _rfq_tool() + '</div></section>')
    out += prose_section([
        ("What is an RFQ template?",
         "<p>A request for quotation asks suppliers to price a defined requirement on defined terms. A template makes sure every RFQ your team "
         "sends carries the same essentials: a reference number, line items with specifications and units, the delivery location, a due date, "
         "and the commercial terms you expect. Suppliers quote on the same basis, so you can compare like with like.</p>"
         "<p>This generator also adds standard instructions to suppliers: quote in rupees per unit with GST shown separately, state the make "
         "offered and any deviation from specification, give the lead time and quote validity, and include GSTIN and PAN.</p>"),
        ("How to use the generator",
         "<ol><li>Enter your company, an RFQ number your team can trace, and a short title.</li>"
         "<li>Add a line for each item. Be specific in the specification: standard, grade, size, approved makes.</li>"
         "<li>Set the delivery location, quote due date and quote validity.</li>"
         "<li>Choose or type your payment and delivery terms, and say how quotes will be evaluated.</li>"
         "<li>Check the preview, then print it, copy it into an email, or download it as .txt or .html.</li></ol>"
         "<p>The HTML download opens in any browser and in Word if you want to add your letterhead.</p>"),
    ], light=True)
    out += tips_section("Writing an RFQ suppliers can price accurately.", [
        "One requirement per line. Combining items in one line makes quotes impossible to compare.",
        "State the unit of measure and pack size explicitly: “Box of 100” is not the same as “Nos”.",
        "Tell suppliers how you will evaluate quotes. It reduces follow-up questions and makes the award easier to justify.",
        "Ask for GST, freight and packing separately, so you compare total landed cost.",
        "Give a realistic due date and stick to it. Late quotes accepted for one supplier are unfair to the rest.",
        "Keep the RFQ number on every quote, comparison and approval so the trail is easy to audit.",
    ])
    out += inside_section("RFQs, quotes and approvals on one desk.",
                          f"The ProcEaze Sourcing Desk, which brings RFQs, vendor selection, NFAs and POs into one place. "
                          f"Around it, ProcEaze runs catalogue buying at contracted prices with one-click purchase requisitions, 1–5 level approvals, "
                          f"POs and a downloadable audit trail.",
                          [("sourcing.html", "Sourcing Desk", None), ("e-procurement-software/", "E-procurement software", None),
                           ("procure-to-pay-software/", "Procure-to-pay software", None)])
    out += faq_section("rfq", RFQ_FAQ)
    out += sibling_tools(RFQ_KEY, [GLOSSARY])
    return out


# ---------------------------------------------------------------------------
# Supplier Evaluation Template
# ---------------------------------------------------------------------------
SE_KEY = "tools/supplier-evaluation-template/"
SE_DESC = "Free supplier evaluation template: score 2 to 5 suppliers on weighted criteria, see live totals and ranking, and download the matrix as CSV."

SE_CRITERIA = [
    ("Price / total cost", 30, "Landed cost: price plus freight, packing and taxes, and the effect of payment terms."),
    ("Quality", 20, "Conformance to specification, rejection history, test certificates."),
    ("Delivery reliability", 15, "On-time delivery record, lead time, ability to handle urgent orders."),
    ("Technical compliance", 15, "Meets every mandatory specification; deviations are listed and acceptable."),
    ("Payment terms", 5, "Credit period and conditions offered."),
    ("Service & support", 10, "Responsiveness, after-sales support, warranty handling."),
    ("Compliance & documentation", 5, "GSTIN, PAN, statutory registrations, authorisation letters, certificates."),
]

SE_FAQ = [
    ("What is a supplier evaluation template?",
     "A structured way to compare suppliers on the same criteria. Each criterion gets a weight that reflects how much it matters, each "
     "supplier gets a score per criterion, and the weighted total shows which supplier offers the best overall value, not just the lowest price."),
    ("How should I set the weights?",
     "Agree them with the people who use the item before you open the quotes. For commodity consumables, price usually carries more weight; "
     "for critical spares, quality, technical compliance and delivery reliability matter more. The weights must add up to 100%."),
    ("What do the scores from 1 to 5 mean?",
     "1 means the supplier does not meet the requirement, 2 partly meets it, 3 meets it, 4 exceeds it in some respects, and 5 clearly exceeds it. "
     "Write down what each score means for each criterion so different evaluators score consistently."),
    ("How is the weighted score calculated?",
     "For each supplier, multiply each criterion's weight by its score, add the results and divide by 100. With weights totalling 100%, "
     "the result is a score out of 5."),
    ("Does the highest score automatically win?",
     "Not necessarily. Treat mandatory requirements as pass or fail before scoring, and use the ranking as evidence for the decision, "
     "recorded in your note for approval (NFA) along with the quotes."),
    ("Is my evaluation saved?",
     "No. The matrix runs in your browser and nothing is sent anywhere or stored. Download it as CSV to keep a copy; refreshing the page resets it."),
]


def _se_tool():
    return (
        f'<div class="tool-app" data-js-only data-se>{privacy_note()}'
        f'<div class="se-bar"><p class="se-weight-total">Weights total: <strong data-se-total>100%</strong> <span class="muted small">(must equal 100%)</span></p>'
        f'<div class="tool-actions" role="group" aria-label="Matrix actions">'
        f'<button class="btn btn-secondary btn-sm" type="button" data-se-addcriterion>{icon("plus")} Add criterion</button>'
        f'<button class="btn btn-secondary btn-sm" type="button" data-se-addsupplier>{icon("plus")} Add supplier</button>'
        f'<button class="btn btn-primary btn-sm" type="button" data-se-csv>{icon("download")} Download CSV</button>'
        f'<button class="btn btn-ghost btn-sm" type="button" data-se-reset>{icon("refresh")} Reset</button></div></div>'
        f'<div class="notice mt-16" data-se-warn hidden>{icon("alert-triangle")}<p><span></span></p></div>'
        f'<div class="tool-table-wrap mt-16" data-se-table></div>'
        f'<div class="se-results"><h3 class="tool-h">Ranking</h3><ol class="se-rank" data-se-rank></ol>'
        f'<p class="small muted mt-16">Weighted score = sum of (weight × score) ÷ 100. Between two and five suppliers; '
        f'scores: 1 = does not meet, 3 = meets, 5 = clearly exceeds.</p></div>'
        f'<p class="sr-only" aria-live="polite" data-se-live></p></div>'
        + noscript("The interactive matrix needs JavaScript. Download the CSV template below instead: it has the same criteria "
                   "and weights, with formulas that calculate the weighted scores in Excel, Google Sheets or LibreOffice."))


def se_body():
    out = tool_hero(SE_KEY, "Supplier evaluation template with weighted scoring.",
                    "Compare two to five suppliers on the criteria that matter, weighted the way your organisation decides. "
                    "Live totals and ranking, and a CSV you can file with the approval.",
                    dl_btn(SE_CSV, "CSV template"))
    out += (f'<section class="section" id="tool"><div class="container">'
            + section_head("The matrix", "Score your suppliers.",
                           "Edit the criteria and weights, name your suppliers and score each one from 1 to 5. The weighted scores and ranking update as you go.")
            + _se_tool()
            + f'<div class="card card-flat tool-dl-inline mt-32 reveal">{icon_tile("table")}<div><h3>Prefer a spreadsheet?</h3>'
              f'<p>The CSV template has the same seven criteria and default weights, with formulas for the weight total and weighted scores.</p></div>'
              f'{dl_btn(SE_CSV, "Download CSV template", "btn-secondary")}</div>'
            + '</div></section>')
    rows = "".join(f'<tr><th scope="row">{esc(n)}</th><td>{w}%</td><td>{esc(d)}</td></tr>' for n, w, d in SE_CRITERIA)
    out += (f'<section class="section section-light"><div class="container">'
            + section_head("Default criteria", "Seven criteria to start from.",
                           "Sensible starting weights for indirect and MRO items. They are a starting point, not a standard: change them to suit the category before you score.")
            + f'<div class="compare-wrap reveal"><table class="compare tool-compare"><caption class="sr-only">Default supplier evaluation criteria and weights</caption>'
              f'<thead><tr><th scope="col">Criterion</th><th scope="col">Default weight</th><th scope="col">What to assess</th></tr></thead><tbody>{rows}</tbody></table></div>'
            + '</div></section>')
    out += prose_section([
        ("Why weighted supplier evaluation?",
         "<p>Choosing on price alone is quick, but it hides the cost of late deliveries, rejected batches and missing documents. A weighted "
         "evaluation makes the trade-offs explicit: everyone can see that price carried 30% of the decision and quality 20%, and how each "
         "supplier scored. That makes the award easier to explain to approvers and auditors, and fairer to suppliers.</p>"
         "<p>It works best when the criteria and weights are fixed before quotes are opened, and when more than one person scores.</p>"),
        ("How to use the template",
         "<ol><li>Review the criteria. Rename, add or remove them to fit the category.</li>"
         "<li>Set the weights so they total exactly 100%. The total is shown live.</li>"
         "<li>Name your suppliers (two to five) and score each criterion from 1 to 5.</li>"
         "<li>Read the weighted scores and ranking. Check any supplier with unscored criteria.</li>"
         "<li>Download the CSV and attach it to your comparison or note for approval.</li></ol>"),
    ])
    out += tips_section("Scoring suppliers consistently.", [
        "Treat mandatory requirements, such as a required certification, as pass or fail before you score.",
        "Write a one-line definition of 1, 3 and 5 for each criterion so evaluators score the same way.",
        "Score price on total landed cost, not the unit rate alone.",
        "Use delivery and quality records from past orders where you have them, rather than impressions.",
        "If two suppliers are within a few tenths of a point, look again at the highest-weighted criteria before deciding.",
    ])
    out += inside_section("From supplier comparison to approved purchase order.",
                          "Vendor selection is part of the ProcEaze Sourcing Desk, alongside NFA approvals "
                          "through 1–5 level approval chains, purchase orders and a downloadable audit trail.",
                          [("sourcing.html", "Sourcing Desk", None), ("approvals.html", "Approvals and delegation of authority", None)])
    out += faq_section("se", SE_FAQ)
    out += sibling_tools(SE_KEY, [GLOSSARY])
    return out


# ---------------------------------------------------------------------------
# MRO Procurement Checklist
# ---------------------------------------------------------------------------
MRO_KEY = "tools/mro-procurement-checklist/"
MRO_DESC = "Free MRO procurement checklist: 42 practical checks across demand, contracts, vendor selection, ordering, receipt and inventory, with saved progress."

MRO_STAGES = [
    ("demand", "Demand and specifications", [
        ("Consolidate demand across sites and departments", "So the same item is not bought separately by every site."),
        ("Review 12 months of consumption", "Use issues and purchase history to estimate annual quantities."),
        ("Write an inspectable specification for each item", "Standard, grade, size, material and approved makes."),
        ("Clean up item codes and descriptions", "One code per item; merge duplicates in the item master."),
        ("Classify items as critical, regular or one-off", "Criticality sets stock levels and sourcing effort."),
        ("Agree approved makes and equivalents with maintenance", "Avoids rejections by the user after the order."),
        ("Fix the unit of measure and pack size", "“Nos” versus “box of 100” causes wrong orders and wrong prices."),
    ]),
    ("contracts", "Catalogue and contracts", [
        ("Identify repeat, high-volume items for rate contracts", "These are the items worth an annual rate contract."),
        ("Run a competitive RFQ for contract items", "Same specification and terms to every supplier."),
        ("Agree rate, MOQ, lead time and validity per item", "Recorded in the item schedule, not in emails."),
        ("Fix the price basis", "GST, freight, packing and delivery location stated for every rate."),
        ("Agree a price-variation rule", "Fixed, indexed with a cap, or revisable only with written approval."),
        ("Publish contract items where buyers order", "A contract buyers cannot find will not be used."),
        ("Set renewal reminders before contracts expire", "Leave time to retender and approve."),
    ]),
    ("vendors", "Vendor selection", [
        ("Shortlist qualified suppliers for each category", "Follow your policy on the minimum number of quotations."),
        ("Verify GSTIN, PAN and bank details", "Before the first purchase order, not after the first invoice."),
        ("Check OEM or brand authorisation letters", "Where you require genuine or authorised supply."),
        ("Evaluate suppliers on weighted criteria", "Price, quality, delivery, compliance and service, agreed in advance."),
        ("Confirm delivery capability for every site", "Lead times can differ widely between locations."),
        ("Agree payment terms and documents up front", "Invoices, test certificates and warranty cards."),
        ("Keep a second source for critical items", "So one supplier's delay does not stop a line."),
    ]),
    ("ordering", "Ordering and approvals", [
        ("Raise a purchase requisition for every purchase", "No requisition, no order."),
        ("Order contract items at contract rates", "Check the rate, MOQ and validity at the time of order."),
        ("Route requisitions by your delegation of authority", "The right approver for the value and category."),
        ("Use a note for approval for off-contract or high-value buys", "Record quotes, comparison and recommendation."),
        ("Issue the purchase order before delivery", "Avoid post-facto POs for planned purchases."),
        ("Check PO terms against the contract", "Rate, taxes, delivery terms and payment terms."),
        ("Control emergency purchases", "Define who can authorise them and regularise them quickly."),
    ]),
    ("receipt", "Receipt and quality", [
        ("Match each delivery to the PO", "Item, quantity, make and PO number on the challan."),
        ("Inspect critical items against specification", "Check test certificates where required."),
        ("Record rejections with reasons", "Photos and rejection notes help resolve disputes."),
        ("Check the invoice against the PO", "Rate, quantity, GST rate and HSN code."),
        ("Record goods receipt promptly", "Late receipts delay payment and distort stock."),
        ("Track actual versus promised lead time", "The basis of delivery reliability scores."),
        ("Close or amend POs with short supply", "Do not leave open quantities hanging."),
    ]),
    ("review", "Inventory and review", [
        ("Set reorder levels for regular items", "Minimum and maximum levels based on usage and lead time."),
        ("Review slow-moving and non-moving stock", "Stop reordering what is not being used."),
        ("Track spend on contract versus off contract", "Shows whether contracts are actually used."),
        ("Review supplier performance periodically", "Delivery, quality, documentation and responsiveness."),
        ("Discuss off-contract buying with departments", "Find out why, and fix the catalogue or the contract."),
        ("Keep the full audit trail", "Requisition, approvals, PO, goods receipt and invoice, linked."),
        ("Feed lessons into the next contract cycle", "Update specifications, items and suppliers."),
    ]),
]
MRO_TOTAL = sum(len(items) for _, _, items in MRO_STAGES)

MRO_FAQ = [
    ("What is MRO procurement?",
     "MRO stands for maintenance, repair and operations. MRO procurement is the buying of the supplies that keep plants, sites and offices "
     "running but do not go into the finished product: spares, consumables, tools, safety equipment, lubricants, electricals and fasteners."),
    ("Why does MRO procurement need a checklist?",
     "MRO is typically many low-value items, bought often, by many people across sites. Small gaps such as vague specifications, duplicate "
     "item codes or buying outside contracts repeat across thousands of orders. A checklist helps you review every stage consistently."),
    ("Are my ticks saved?",
     "Yes, in your own browser's local storage on this device, so they are still there when you come back. Nothing is sent to ProcEaze. "
     "In private browsing, or if your browser blocks storage, ticks last only until you leave the page."),
    ("Can I print the checklist?",
     "Yes. Use the Print button to print just the checklist, with your current ticks, for a review meeting or a site audit."),
    ("How is MRO procurement different from direct procurement?",
     "Direct procurement buys the materials that go into what you make, usually in large volumes from a few suppliers. MRO procurement buys "
     "what keeps operations running, usually a long tail of items from many suppliers, which makes catalogues, rate contracts and approvals especially important."),
]


def _mro_tool():
    stages = []
    n = 0
    for si, (sk, title, items) in enumerate(MRO_STAGES, 1):
        lis = []
        for ii, (t, d) in enumerate(items, 1):
            n += 1
            iid = f"mro-{sk}-{ii}"
            lis.append(f'<li><label class="mro-item" for="{iid}"><input type="checkbox" id="{iid}" data-mro-item="{sk}-{ii}">'
                       f'<span><strong>{esc(t)}</strong><span class="mro-detail">{esc(d)}</span></span></label></li>')
        stages.append(f'<fieldset class="mro-stage" data-mro-stage><legend><h3 class="mro-stage-h"><span class="mro-num">{si:02d}</span>{esc(title)}'
                      f'<span class="mro-stage-count" data-mro-stage-count aria-hidden="true">{len(items)} items</span></h3></legend>'
                      f'<ul class="mro-list">{"".join(lis)}</ul></fieldset>')
    head = (f'<div class="mro-head" data-js-only>{privacy_note("Runs in your browser. Your ticks are saved on this device only and never sent anywhere.")}'
            f'<div class="mro-progress-row"><div class="mro-progress" role="progressbar" aria-label="Checklist progress" aria-valuemin="0" '
            f'aria-valuemax="{MRO_TOTAL}" aria-valuenow="0" data-mro-bar><span data-mro-fill></span></div>'
            f'<p class="mro-count" aria-live="polite" data-mro-count>0 of {MRO_TOTAL} items done (0%)</p></div>'
            f'<div class="tool-actions" role="group" aria-label="Checklist actions">'
            f'<button class="btn btn-primary btn-sm" type="button" data-mro-print>{icon("printer")} Print checklist</button>'
            f'<button class="btn btn-ghost btn-sm" type="button" data-mro-reset>{icon("refresh")} Reset</button></div></div>')
    return (f'<div class="mro" data-mro>{head}'
            f'<div class="mro-area" data-mro-print-area><p class="mro-print-title">MRO procurement checklist · ProcEaze</p>'
            f'<div class="mro-stages">{"".join(stages)}</div></div></div>'
            + noscript("Without JavaScript you can still tick the boxes and print the page with your browser, "
                       "but progress is not tracked or saved."))


def mro_body():
    out = tool_hero(MRO_KEY, "MRO procurement checklist, stage by stage.",
                    f"{MRO_TOTAL} practical checks for maintenance, repair and operations buying, from demand and specifications to inventory review. "
                    "Tick as you go; your progress stays on your device.")
    out += (f'<section class="section" id="tool"><div class="container">'
            + section_head("The checklist", "Six stages of MRO procurement.",
                           "Work through it for one category, one site or your whole MRO spend. Ticks are saved in this browser only.")
            + _mro_tool() + '</div></section>')
    out += prose_section([
        ("Why MRO buying needs its own checklist",
         "<p>MRO spend behaves differently from direct materials. Instead of a few large orders, it is thousands of small ones: a pack of gloves "
         "here, a bearing there, a cable drum for a shutdown. Requests come from maintenance, stores, projects, administration and every site. "
         "That spread is why small process gaps matter. A duplicate item code, a missing MOQ or one unapproved supplier repeats across hundreds of orders.</p>"
         "<p>The checklist follows the order the work happens in, so you can see which stage is weakest and fix that first.</p>"),
        ("How to use the checklist",
         "<ol><li>Pick a scope: one category, one site or all MRO.</li>"
         "<li>Go stage by stage and tick only what is genuinely in place today.</li>"
         "<li>Watch the stage counts: the stage with the fewest ticks is usually where to start.</li>"
         "<li>Print the checklist for a review meeting, and repeat it each quarter.</li></ol>"
         "<p>If you are not sure what a term means, see the "
         f'<a href="{L(GLOSSARY)}">procurement glossary</a>. For rate contracts, read the '
         f'<a href="{L(ARC_GUIDE)}">guide to annual rate contract procurement</a>.</p>'),
    ], light=True)
    out += tips_section("Quick wins in MRO procurement.", [
        "Start with item master hygiene. Clean codes and specifications make every later stage easier.",
        "Put the top repeat items on rate contracts first; the long tail can follow.",
        "Make the contracted catalogue the easiest way to buy, so buyers choose it without being told.",
        "Review off-contract purchases monthly with the departments that raise them.",
        "Keep requisition, approval, PO, receipt and invoice linked, so audits take hours rather than weeks.",
    ])
    out += inside_section("MRO buying in one catalogue, with approvals built in.",
                          "ProcEaze brings 5,00,000+ products across 56+ categories into one catalogue, with your ARC prices loaded and locked at order. "
                          "Cart validation, one-click purchase requisitions, 1–5 level approvals, POs and a downloadable audit trail cover the ordering stages of this checklist.",
                          [("catalogue.html", "Catalogue and buying", None), ("approvals.html", "Approvals and delegation of authority", None),
                           ("procure-to-pay-software/", "Procure-to-pay software", None)])
    out += faq_section("mro", MRO_FAQ)
    out += sibling_tools(MRO_KEY, [GLOSSARY])
    return out


# ---------------------------------------------------------------------------
# Procurement Savings Calculator
# ---------------------------------------------------------------------------
SAV_KEY = "tools/procurement-savings-calculator/"
SAV_DESC = "Free procurement savings calculator: estimate price and process savings from your own spend, contract coverage and PO volumes, with the formula shown."

# Neutral example values (not benchmarks): key, label, default, max, hint, prefix
SAV_INPUTS = [
    ("spend", "Annual indirect / MRO spend (₹)", 50000000, None, None, "₹"),
    ("current", "Share of spend on contract today (%)", 40, 100, "Spend bought at contracted (ARC) rates as a share of the total.", None),
    ("target", "Target share of spend on contract (%)", 70, 100, "The share you aim to buy on contract.", None),
    ("diff", "Price difference: contract vs off-contract (%)", 5, 100, "How much lower contract prices are, as a % of the off-contract price, on average.", None),
    ("pos", "Purchase orders per year", 2000, None, "Number of POs raised for this spend.", None),
    ("cpo", "Process cost per PO (₹)", 1500, None, None, "₹"),
    ("reduction", "Expected reduction in process cost (%)", 30, 100, "Your own estimate of how much the cost per PO could fall.", None),
]
SAV_DEF = {k: v for k, _, v, *_ in SAV_INPUTS}


def sav_calc(v):
    moved = v["spend"] * max(0, v["target"] - v["current"]) / 100
    price = moved * v["diff"] / 100
    process = v["pos"] * v["cpo"] * v["reduction"] / 100
    return dict(moved=moved, price=price, process=process, total=price + process, process_cost=v["pos"] * v["cpo"])


SAV_FAQ = [
    ("How does the procurement savings calculator work?",
     "It estimates two kinds of savings. Price savings: the extra spend you move onto contract, multiplied by how much cheaper contract prices are. "
     "Process savings: the number of POs, multiplied by the process cost per PO and by the reduction you expect. The total is the sum of the two. "
     "Every formula is shown with your numbers."),
    ("Where do I find the numbers to enter?",
     "Annual spend and the share on contract come from your ERP or purchase register. The price difference comes from comparing what you paid "
     "off contract with the contract rate for the same items. Process cost per PO is usually estimated from the time people spend on requisitions, "
     "approvals and POs."),
    ("Are the default values benchmarks?",
     "No. They are neutral example values to show how the calculator works. They are not industry figures and not ProcEaze results. Replace them with your own."),
    ("Why is the result only an estimate?",
     "Because it depends entirely on your assumptions, and real savings depend on which items move onto contract, supplier pricing, demand, "
     "and how processes actually change. Use it to size an opportunity, not as a forecast."),
    ("What does the calculator leave out?",
     "It does not include savings from renegotiating existing contracts, competitive bidding, demand reduction, inventory or working-capital effects, "
     "or the cost of making the change. Consider those separately."),
]


def _sav_tool():
    r = sav_calc(SAV_DEF)
    fields = []
    for k, label, val, mx, hint, prefix in SAV_INPUTS:
        fid = f"sav-{k}"
        hint_id = f"{fid}-hint"
        mx_attr = f' max="{mx}"' if mx is not None else ""
        attrs = f'min="0"{mx_attr} step="any" inputmode="decimal"'
        dyn = {"spend": f'{inr(val)} ({inr_short(val)})', "cpo": f'Current process cost: {inr(SAV_DEF["pos"]).replace("₹", "")} POs × {inr(val)} = {inr(r["process_cost"])} a year.'}
        hint_txt = dyn.get(k, hint)
        data_hint = f' data-sav-hint="{k}"' if k in dyn else ""
        inp = (f'<input class="input" id="{fid}" type="number" {attrs} value="{val}" data-sav-in="{k}" '
               f'aria-describedby="{hint_id} {fid}-err">')
        if prefix:
            inp = f'<div class="input-group"><span class="prefix" aria-hidden="true">{prefix}</span>{inp}</div>'
        fields.append(f'<div class="field{" full" if k == "spend" else ""}"><label for="{fid}">{label}</label>{inp}'
                      f'<p class="field-hint" id="{hint_id}"{data_hint}>{esc(hint_txt)}</p>'
                      f'<p class="field-error" id="{fid}-err">{icon("alert-circle")}<span></span></p></div>')
    form = (f'<div class="form-card tool-form"><h3 class="tool-h">Your numbers</h3>'
            f'<div class="notice info sav-example">{icon("info")}<p><strong>Example values, replace with your own.</strong> '
            f'The figures below are neutral examples to show how the calculator works. They are not benchmarks or ProcEaze results.</p></div>'
            f'<div class="form-grid mt-24">{"".join(fields)}</div>'
            f'<div class="tool-actions mt-24" role="group" aria-label="Calculator actions">'
            f'<button class="btn btn-secondary btn-sm" type="button" data-sav-reset>{icon("refresh")} Restore example values</button>'
            f'<button class="btn btn-ghost btn-sm" type="button" data-sav-clear>{icon("x")} Clear all</button></div></div>')
    res = (
        f'<div class="sav-results">'
        f'<div class="sav-total"><p class="sav-label">Estimated annual savings</p>'
        f'<p class="sav-big" data-sav-out="total-short">{inr_short(r["total"])}</p>'
        f'<p class="sav-full" data-sav-out="total">{inr(r["total"])}</p></div>'
        f'<div class="sav-split">'
        f'<div><p class="sav-label">Price savings</p><p class="sav-mid" data-sav-out="price-short">{inr_short(r["price"])}</p><p class="small muted" data-sav-out="price">{inr(r["price"])}</p></div>'
        f'<div><p class="sav-label">Process savings</p><p class="sav-mid" data-sav-out="process-short">{inr_short(r["process"])}</p><p class="small muted" data-sav-out="process">{inr(r["process"])}</p></div>'
        f'</div>'
        f'<div class="notice mt-16" data-sav-notes hidden>{icon("alert-triangle")}<p><span></span></p></div>'
        f'<h3 class="tool-h">How it is calculated</h3>'
        f'<dl class="sav-formula">'
        f'<div><dt>Spend moved onto contract = annual spend × (target share − current share)</dt><dd data-sav-out="f-moved">'
        f'{inr(SAV_DEF["spend"])} × ({SAV_DEF["target"]}% − {SAV_DEF["current"]}%) = {inr(r["moved"])}</dd></div>'
        f'<div><dt>Price savings = spend moved onto contract × price difference</dt><dd data-sav-out="f-price">'
        f'{inr(r["moved"])} × {SAV_DEF["diff"]}% = {inr(r["price"])}</dd></div>'
        f'<div><dt>Process savings = POs per year × process cost per PO × expected reduction</dt><dd data-sav-out="f-process">'
        f'{inr(SAV_DEF["pos"]).replace("₹", "")} POs × {inr(SAV_DEF["cpo"])} × {SAV_DEF["reduction"]}% = {inr(r["process"])}</dd></div>'
        f'<div><dt>Total = price savings + process savings</dt><dd data-sav-out="f-total">'
        f'{inr(r["price"])} + {inr(r["process"])} = {inr(r["total"])}</dd></div>'
        f'</dl>'
        f'<div class="notice mt-16">{icon("alert-triangle")}<p><strong>This is an estimate, not a forecast.</strong> It is calculated only from the numbers '
        f'and assumptions you enter. Actual results depend on your items, suppliers, prices and processes.</p></div>'
        f'<p class="sr-only" aria-live="polite" data-sav-live></p></div>')
    return (f'<div class="tool-app" data-js-only data-sav>{privacy_note()}<div class="tool-layout">{form}{res}</div></div>'
            + noscript("The calculator needs JavaScript. You can apply the same formulas by hand: they are set out under "
                       "“The formula” below."))


def sav_body():
    out = tool_hero(SAV_KEY, "Procurement savings calculator.",
                    "Estimate the annual price and process savings from moving more spend onto contract and making purchase orders cheaper to process. "
                    "Driven entirely by your own numbers, with the formula in plain sight.")
    out += (f'<section class="section" id="tool"><div class="container">'
            + section_head("The calculator", "Estimate your procurement savings.",
                           "Enter your own figures. Results update as you type and are shown in rupees, lakh and crore.")
            + _sav_tool() + '</div></section>')
    out += prose_section([
        ("The formula",
         "<p>The calculator estimates two separate effects and adds them together.</p>"
         "<ul><li><strong>Price savings</strong> = annual spend × (target share on contract − current share on contract) × price difference. "
         "The price difference is how much lower contract prices are, as a percentage of the off-contract price.</li>"
         "<li><strong>Process savings</strong> = purchase orders per year × process cost per PO × expected reduction in process cost.</li>"
         "<li><strong>Total</strong> = price savings + process savings.</li></ul>"
         "<p>If the target share is lower than the current share, price savings are taken as zero. Percentages above 100 are capped at 100.</p>"),
        ("Getting realistic inputs",
         "<p><strong>Spend and contract share:</strong> take the last 12 months of indirect and MRO purchases from your ERP or purchase register, "
         "and the part bought at contracted rates.</p>"
         "<p><strong>Price difference:</strong> compare off-contract purchase prices with the contract rate for the same items, and use a "
         "spend-weighted average rather than the best example.</p>"
         "<p><strong>Process cost per PO:</strong> estimate the time requesters, buyers, approvers and accounts spend per order, multiplied by "
         "their cost per hour. Be conservative about the reduction you expect.</p>"),
    ], light=True)
    out += tips_section("Using the estimate well.", [
        "Run it three times: cautious, expected and optimistic assumptions. Present the range, not one number.",
        "Only count spend that can realistically go on contract. One-off and specialised items often cannot.",
        "Process savings are usually time freed up, not cash, unless headcount or overtime actually changes.",
        "Write your assumptions next to the result when you share it, so others can challenge them.",
    ])
    out += inside_section("See your actual spend, not just an estimate.",
                          "ProcEaze gives role-based dashboards and spend analytics across your purchases, and loads your ARC prices so they are "
                          "locked at the point of order.",
                          [("dashboards.html", "Procurement spend management", None), ("arc-pricing.html", "ARC contract pricing", None)])
    out += faq_section("sav", SAV_FAQ)
    out += sibling_tools(SAV_KEY, [GLOSSARY])
    return out


# ---------------------------------------------------------------------------
# Page registry
# ---------------------------------------------------------------------------
_crumbs = lambda key: [("Procurement Tools", "tools/"), (TOOL_BY_KEY[key][1], None)]

PAGES = [
    dict(path="tools/", section="tools", crumbs=[("Procurement Tools", None)],
         title="Procurement Tools: Free Procurement Templates | ProcEaze",
         desc="Free procurement tools and templates: an annual rate contract template, RFQ generator, supplier evaluation matrix, MRO checklist and savings calculator.",
         body=hub_body, schemas=[HUB_SCHEMA, faq_schema(HUB_FAQ)]),
    dict(path=ARC_KEY, section="tools", crumbs=_crumbs(ARC_KEY),
         title="Annual Rate Contract Template (Free Download) | ProcEaze",
         desc="Free annual rate contract template: the structure of an ARC, a CSV item schedule with MOQ, rates and taxes, and placeholder clauses for legal review.",
         body=arc_body, schemas=[faq_schema(ARC_FAQ)], js=("tools",)),
    dict(path=RFQ_KEY, section="tools", crumbs=_crumbs(RFQ_KEY),
         title="RFQ Template Generator: Free Online Tool | ProcEaze",
         desc=RFQ_DESC, body=rfq_body, js=("tools",),
         schemas=[app_schema(RFQ_KEY, "RFQ Template Generator", RFQ_DESC), faq_schema(RFQ_FAQ)]),
    dict(path=SE_KEY, section="tools", crumbs=_crumbs(SE_KEY),
         title="Supplier Evaluation Template: Free Scoring Matrix | ProcEaze",
         desc=SE_DESC, body=se_body, js=("tools",),
         schemas=[app_schema(SE_KEY, "Supplier Evaluation Template", SE_DESC), faq_schema(SE_FAQ)]),
    dict(path=MRO_KEY, section="tools", crumbs=_crumbs(MRO_KEY),
         title="MRO Procurement Checklist: Free Interactive Checklist | ProcEaze",
         desc=MRO_DESC, body=mro_body, js=("tools",),
         schemas=[app_schema(MRO_KEY, "MRO Procurement Checklist", MRO_DESC), faq_schema(MRO_FAQ)]),
    dict(path=SAV_KEY, section="tools", crumbs=_crumbs(SAV_KEY),
         title="Procurement Savings Calculator: Estimate Savings | ProcEaze",
         desc=SAV_DESC, body=sav_body, js=("tools",),
         schemas=[app_schema(SAV_KEY, "Procurement Savings Calculator", SAV_DESC), faq_schema(SAV_FAQ)]),
]
