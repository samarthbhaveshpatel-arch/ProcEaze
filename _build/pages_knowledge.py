"""Procurement Knowledge Hub: hub, guides, glossary, blog, comparisons, whitepapers.

All links are produced inside body functions (render time), never at import.
Article content functions return (intro_html, [(id, heading, html), ...]).
"""
import re
from lib import (icon, icon_tile, badge, esc, L, section_head, page_hero, btn_demo, btn_link,
                 feature_cards, check_list, BASE_URL, SOFTWARE, SERVICES, KNOWLEDGE, TOOLS, PLATFORM, COMPANY)
from pages_misc import GLOSSARY, slug

DATE = "2026-11-12"
DATE_HUMAN = "12 November 2026"
HUB = "knowledge-hub/"
GUIDES = "knowledge-hub/procurement-guides/"
GLOSS = "knowledge-hub/procurement-glossary/"
BLOG = "knowledge-hub/blog/"
COMP = "knowledge-hub/procurement-comparisons/"
PAPERS = "knowledge-hub/whitepapers-reports/"
ARC_GUIDE = GUIDES + "annual-rate-contract-procurement/"
POST_LEAK = BLOG + "rate-contract-leakage/"
POST_DOA = BLOG + "procurement-approval-matrix/"
POST_MRO = BLOG + "mro-procurement-long-tail/"
CMP_EPROC = COMP + "e-procurement-vs-traditional-procurement/"
CMP_ARC = COMP + "rate-contract-vs-spot-buying/"
CMP_P2P = COMP + "procure-to-pay-vs-source-to-pay/"

AUTHOR = {"@type": "Organization", "name": "ProcEaze"}
PUBLISHER = {"@type": "Organization", "name": "ProcEaze",
             "logo": {"@type": "ImageObject", "url": BASE_URL + "/assets/logo/proceaze-logo-full.png"}}


# ---------------------------------------------------------------------------
# Glossary data: the shared GLOSSARY from pages_misc, extended
# ---------------------------------------------------------------------------
def term_id(term):
    return slug(term.split(" (")[0])


_TERMS = dict(GLOSSARY)
# KAM in pages_misc is ProcEaze-specific; give the general meaning here
_TERMS["KAM"] = ("Key Account Manager: the named person at a supplier or platform who manages a client's account. "
                 "At ProcEaze, your KAM loads your ARC prices and tracks renewals.")
_TERMS.update({
    "Anti-sniping": "A reverse-auction rule that extends the closing time when a bid arrives in the final minutes, so other bidders have a fair chance to respond.",
    "Approval matrix": "A table that sets who must approve a purchase, based on factors such as value, category and whether the item is on contract. It puts the Delegation of Authority into practice.",
    "Audit trail": "A time-stamped record of who did what, and when, on a requisition, approval, order or contract.",
    "Blanket purchase order": "A purchase order that covers repeated deliveries of agreed items over a period, often up to a value limit, with call-offs placed against it.",
    "Call-off": "An individual order placed against a rate contract or blanket purchase order.",
    "Catalogue buying": "Ordering from a pre-approved list of items with agreed prices and vendors, instead of sourcing each requirement separately.",
    "Category management": "Managing spend by groups of related items, such as electricals or PPE, with a plan for each category's vendors, contracts and demand.",
    "Comparative statement (CS)": "A table that sets vendor quotes side by side, line by line and on a like-for-like basis, used to identify L1 and to support the NFA.",
    "Contract compliance": "The extent to which purchases follow agreed contracts: the contracted vendor, the contracted item and the contracted rate.",
    "Cost centre": "A unit of the organisation, such as a department or site, to which spend is charged for budgeting and reporting.",
    "Debit note": "A document raised by a buyer to record an amount to be recovered from, or adjusted with, a vendor, for example for rejected goods or a short supply.",
    "Delivery challan": "A document that accompanies goods in transit when no tax invoice is issued at the time of movement, for example goods sent for job work.",
    "Direct procurement": "Buying the materials that go into the product a company makes, such as raw materials and components.",
    "E-invoice": "Under GST, a B2B invoice reported to the Invoice Registration Portal, which validates it and returns an Invoice Reference Number (IRN) and a QR code. It applies to businesses above a notified turnover threshold.",
    "E-procurement": "Running purchasing digitally, from requisition and approval through sourcing to purchase order, instead of on paper, email and spreadsheets.",
    "E-way bill": "An electronic document generated on the GST e-way bill portal before goods above a prescribed value are moved, recording the consignment, consignor, consignee and transport details.",
    "Earnest money deposit (EMD)": "A refundable deposit that some tenders require bidders to submit with their bid, as security that the bidder will honour it.",
    "Ex-works (EXW)": "A price basis where the vendor makes the goods available at its own premises, and the buyer arranges and pays for transport and bears the risk from there.",
    "FOR destination": "A price basis common in Indian contracts, where the vendor's rate includes delivery to the buyer's named site.",
    "GRN": "Goods receipt note: the record made when goods are received and checked at stores, confirming what arrived against the PO.",
    "GST": "Goods and Services Tax: India's tax on the supply of goods and services, levied as CGST with SGST (or UTGST) on supplies within a state or union territory, and as IGST on supplies between states.",
    "HSN code": "Harmonised System of Nomenclature code: the classification code for goods used on GST invoices and to determine the applicable tax rate.",
    "Incoterms": "Standard trade terms published by the International Chamber of Commerce that set out who pays for, and bears the risk of, each stage of delivery. Mostly used in import and export contracts.",
    "Indent": "A common Indian term for an internal request for material, raised by a user department or stores. Similar to a purchase requisition.",
    "Indicative quantity": "An estimate of the quantity to be bought over a contract period, shared with vendors for pricing, without a firm commitment to buy it.",
    "Indirect procurement": "Buying the goods and services that keep a business running but don't go into its product, such as MRO, office supplies, IT and facility services.",
    "Input tax credit (ITC)": "The GST paid on purchases that a registered business can set off against the GST it owes on its own supplies, subject to the conditions in GST law.",
    "Item master": "The list of item codes and descriptions in an ERP or procurement system. Duplicate or inconsistent entries make spend hard to analyse and contracts hard to enforce.",
    "Landed cost": "The total cost of getting an item to your site: the price plus freight, packing, insurance, duties and other charges.",
    "Lead time": "The time between placing an order and receiving the goods.",
    "Letter of intent (LOI)": "A document telling a vendor that you intend to award them an order or contract, issued before the formal PO or contract.",
    "Maverick spend": "Purchases made outside agreed contracts, vendors or processes. Also called off-contract spend.",
    "MSME": "Micro, small and medium enterprises, classified by investment and turnover and registered on the Udyam portal. Payments to micro and small suppliers are subject to time limits under the MSMED Act, 2006.",
    "PAN": "Permanent Account Number: the 10-character income-tax identifier, collected from vendors during onboarding.",
    "Payment terms": "When and how a vendor will be paid, for example a set number of days from receipt of goods or invoice.",
    "Price basis": "What a quoted rate includes, such as freight, packing, loading and insurance, and whether taxes are extra.",
    "Price-variation clause (PVC)": "A contract clause that adjusts a rate in line with an agreed index or base price, using a set formula and review frequency. Common for items linked to raw materials such as copper or steel.",
    "Procure-to-pay (P2P)": "The process from purchase requisition through approval, purchase order, goods receipt and invoice to payment.",
    "Rate contract": "An agreement that fixes rates for listed items for a period, without committing to a fixed quantity. When it runs for a year, it is called an annual rate contract (ARC).",
    "Request for information (RFI)": "An early request asking vendors to describe their capabilities, used to build a shortlist before an RFQ or RFP.",
    "Request for proposal (RFP)": "An invitation to vendors to propose both an approach and a price, used where the solution matters as much as the price.",
    "Segregation of duties": "Splitting key steps, such as requesting, approving, ordering and receiving, between different people, so no one person controls a purchase from end to end.",
    "Single source": "Buying from one chosen vendor even though others could supply. Different from sole source, where only one vendor can supply.",
    "Sole source": "A purchase where only one vendor can supply the item, for example a proprietary spare available only from the original manufacturer.",
    "Source-to-pay (S2P)": "The full process from spend analysis and sourcing through contracting and supplier management to procure-to-pay.",
    "Spend analysis": "Collecting and classifying purchase data by category, vendor, site and item, to see where money goes and where to act.",
    "Spend leakage": "Value lost when purchases don't follow negotiated contracts: the wrong vendor, a higher price than agreed, or an item bought outside the contract.",
    "Spend under management": "The share of spend covered by procurement processes such as contracts, approved vendors and competitive sourcing.",
    "Spot buying": "Buying each requirement as it arises, usually on fresh quotes, rather than under a standing contract.",
    "Supplier evaluation": "Assessing vendors against set criteria, such as quality, delivery, price, compliance and financial standing, before or during a contract.",
    "Tail spend": "The many small, infrequent purchases spread across many vendors. Individually low in value, but often where process cost is highest relative to what is bought.",
    "TDS on purchase of goods": "Tax deducted at source by a buyer on payments to a resident seller for goods, which applies when the buyer's turnover and the year's purchases from that seller cross thresholds set in income-tax law. Confirm the current rate, thresholds and section with your tax adviser.",
    "Techno-commercial evaluation": "Evaluating bids on technical compliance first and commercial terms second, often in a two-bid process where price bids are opened only for technically qualified vendors.",
    "Three-way match": "Checking that the PO, the goods receipt (GRN) and the vendor invoice agree on item, quantity and price before payment is released.",
    "Total cost of ownership (TCO)": "The full cost of an item over its life, including price, delivery, installation, maintenance, downtime and disposal.",
    "Vendor master": "The record of approved vendors in an ERP or procurement system, with details such as GSTIN, PAN, bank account and payment terms.",
    "Vendor onboarding": "Registering and verifying a new vendor, including documents such as GSTIN, PAN and bank details, before they can receive orders.",
    "Work order": "An order for services or works, used in place of a purchase order for jobs such as maintenance, installation or civil works.",
})

# Optional "read more" link per term: term -> (page key, label)
TERM_LINKS = {
    "ARC": (ARC_GUIDE, "Read the ARC procurement guide"),
    "Rate contract": (CMP_ARC, "Rate contract vs spot buying"),
    "Spot buying": (CMP_ARC, "Rate contract vs spot buying"),
    "Approval matrix": (POST_DOA, "Designing an approval matrix"),
    "DoA": (POST_DOA, "Designing an approval matrix"),
    "Spend leakage": (POST_LEAK, "Why negotiated rates leak"),
    "Maverick spend": (POST_LEAK, "Why negotiated rates leak"),
    "Tail spend": (POST_MRO, "MRO and the long tail"),
    "MRO": (POST_MRO, "MRO and the long tail"),
    "E-procurement": (CMP_EPROC, "E-procurement vs traditional procurement"),
    "Procure-to-pay (P2P)": (CMP_P2P, "Procure-to-pay vs source-to-pay"),
    "Source-to-pay (S2P)": (CMP_P2P, "Procure-to-pay vs source-to-pay"),
    "Reverse auction": ("reverse-auction.html", "Reverse auctions on ProcEaze"),
    "NFA": (ARC_GUIDE + "#approvals-and-nfa", "What goes into an NFA"),
    "Price-variation clause (PVC)": (ARC_GUIDE + "#commercial-terms", "ARC commercial terms"),
}

TERMS = sorted(_TERMS.items(), key=lambda kv: kv[0].lower())
TERM_IDS = {term_id(t) for t, _ in TERMS}
assert len(TERM_IDS) == len(TERMS), "duplicate glossary ids"

GLOSSARY_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "DefinedTermSet",
    "name": "Procurement glossary",
    "description": "Procurement terms used in Indian industrial, MRO and indirect procurement, explained.",
    "url": BASE_URL + "/" + GLOSS,
    "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d, "url": BASE_URL + "/" + GLOSS + "#" + term_id(t),
                        "inDefinedTermSet": BASE_URL + "/" + GLOSS} for t, d in TERMS],
}


# ---------------------------------------------------------------------------
# Small HTML helpers (render time only)
# ---------------------------------------------------------------------------
def a(key, text):
    return f'<a href="{L(key)}">{text}</a>'


def g(tid, text):
    """Link to a glossary term; fails loudly on a typo'd id."""
    if tid not in TERM_IDS:
        raise KeyError(f"unknown glossary id {tid!r}")
    return f'<a href="{L(GLOSS + "#" + tid)}">{text}</a>'


def P(*paras):
    return "".join(f"<p>{p}</p>" for p in paras)


def ul(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def ol(items):
    return ('<ol style="padding-left:1.3em;display:grid;gap:8px;margin-bottom:1em">'
            + "".join(f"<li>{i}</li>" for i in items) + "</ol>")


def h3(t, hid=None):
    return f'<h3{f" id={chr(34)}{hid}{chr(34)}" if hid else ""}>{t}</h3>'


def table(caption, heads, rows):
    """Side-by-side table using the site's .compare markup (row header + two columns)."""
    th = (f'<th scope="col">{heads[0]}</th>'
          + "".join(f'<th scope="col" class="col-head">{h}</th>' for h in heads[1:]))
    body = "".join(f'<tr><th scope="row">{r[0]}</th>' + "".join(f"<td>{c}</td>" for c in r[1:]) + "</tr>" for r in rows)
    return (f'<div class="compare-wrap" style="margin:1.4em 0 1.6em"><table class="compare"><caption class="sr-only">{caption}</caption>'
            f'<thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>')


def words(html):
    return len(re.sub(r"<[^>]+>", " ", html).split())


def cta(title="Put contracted buying under one view.",
        lead="See how ProcEaze handles catalogue buying, ARC pricing, approvals and purchase orders in one workspace."):
    return (f'<section class="section cta-band"><div class="bg-circle c1" aria-hidden="true"></div><div class="bg-circle c2" aria-hidden="true"></div>'
            f'<div class="container reveal"><h2>{title}</h2><p class="lead">{lead}</p>'
            f'<div class="btn-row">{btn_demo("Contact Us", "btn-white btn-lg")}'
            f'{btn_link("request-a-demo/", "Request a demo", "btn-ghost-light btn-lg")}</div></div></section>')


# ---------------------------------------------------------------------------
# Article content
# ---------------------------------------------------------------------------
def arc_guide_content():
    intro = P(
        f"An {g('arc', 'annual rate contract')} (ARC) is one of the most widely used tools in Indian industrial and indirect procurement, "
        "and one of the most frequently under-used. Negotiating good rates is the visible part of the work. Making sure those rates are "
        "used, by every buyer at every site, for the whole year, is where most of the value is won or lost.",
        "This guide walks through the full ARC cycle: deciding what belongs on a rate contract, preparing the item list, running the RFQ, "
        "agreeing commercial terms, getting approval, rolling the contract out, monitoring compliance and renewing it. It describes common "
        "practice; contract wording with legal or tax consequences should always be reviewed by your own legal and finance teams.")
    s = []
    s.append(("what-is-an-arc", "What is an annual rate contract?", P(
        f"An annual rate contract is an agreement with a vendor that fixes the price, and the main commercial terms, for a defined list of items "
        f"over a period, usually twelve months. It is often simply called a {g('rate-contract', 'rate contract')}. Unlike a normal "
        f"{g('po', 'purchase order')}, an ARC does not usually commit you to buy a fixed quantity. It commits the vendor to supply at the "
        "agreed rate whenever you order, within the terms of the contract.",
        f"In practice, an ARC sits between sourcing and buying. Procurement negotiates once, against a year's expected demand. Buyers and "
        f"plants then raise {g('pr', 'purchase requisitions')} and purchase orders against the contract as and when they need the items, "
        "without going back to the market each time. Each such order is sometimes called a call-off.",
        "Most organisations use ARCs for repeat, predictable items: safety and PPE, MRO spares, electricals, fasteners, bearings, lubricants, "
        "office supplies and IT consumables. These are the categories where the same items are bought again and again by many people across "
        "sites, and where negotiating every order separately costs more effort than it saves.",
        "A typical ARC records:")
        + ul(["the list of items, with specifications, make or approved equivalents, and unit of measure",
              f"the agreed rate per unit and what that rate includes (the {g('price-basis', 'price basis')})",
              "any price-variation clause",
              f"the {g('moq', 'MOQ')}, delivery lead time and delivery locations",
              "payment terms",
              "the validity period, and the conditions for renewal or termination",
              f"an {g('indicative-quantity', 'indicative annual quantity')}, where one is shared"])
        + P(f"Every abbreviation used in this guide is explained in the {a(GLOSS, 'procurement glossary')}.")))

    s.append(("arc-vs-spot-buying", "When to use an ARC, and when to buy spot", P(
        "An ARC is not the right tool for every purchase. It works best when four conditions hold:")
        + ul(["<strong>Repeat demand.</strong> The item is bought several times a year, not once.",
              "<strong>A stable specification.</strong> Everyone means the same item when they order it, so a single rate makes sense.",
              "<strong>Many buyers or sites.</strong> Orders spread across people and locations are where prices drift most without a contract.",
              "<strong>A reasonably predictable volume.</strong> You can give vendors an honest indicative quantity, which is what earns a better rate."])
        + P(f"{g('spot-buying', 'Spot buying')}, where you raise an {g('rfq', 'RFQ')} or buy against a fresh quotation for each requirement, "
            "usually suits one-off items, project-specific materials, items whose specification changes from order to order, and commodities "
            "whose prices move so fast that no vendor will hold a rate for long without adding a large risk margin.",
            "Most organisations end up with a mix: ARCs for the high-frequency core of their catalogue, and competitive spot buying for "
            f"everything else. The comparison {a(CMP_ARC, 'rate contract vs spot buying')} sets out the trade-offs side by side.",
            "A simple test is to list last year's purchase orders by item. Items that were ordered many times, by more than one person, at "
            "prices that varied between orders, are your strongest ARC candidates.")))

    s.append(("item-list-and-specifications", "Preparing the item list and specifications", P(
        "The item list is the foundation of the contract. If it is vague, vendors will price the vagueness in, buyers will find that items "
        "don't quite match what they need, and purchases will drift outside the contract.")
        + h3("Start from your own purchase history")
        + P("Pull twelve to twenty-four months of PO lines for the category. Group them by item, clean up duplicate descriptions (the same "
            "pair of gloves described five different ways is common), and note the quantity, number of orders, sites and the range of prices "
            "paid. This gives you an indicative annual quantity and shows where prices have varied most. If your "
            f"{g('item-master', 'item master')} has many duplicates, cleaning it up now will also make the contract easier to enforce later.")
        + h3("Write specifications vendors can price")
        + P("For each line, give the description, the technical specification or standard (such as the relevant IS or EN standard), the "
            f"make or list of approved makes, whether equivalents are acceptable, the pack size, the unit of measure and the {g('hsn-code', 'HSN code')}. "
            "Ambiguity in any of these is a common source of disputes later in the year.")
        + h3("Decide on brand or equivalent")
        + P("Locking a single brand gives users certainty but limits competition. Allowing approved equivalents widens the field, but someone, "
            "usually the user department or quality team, needs to approve which equivalents are acceptable before the RFQ, not after it.")
        + h3("Group items into lots")
        + P("Grouping related items into lots, such as all hand protection or all LT cables, lets specialist vendors quote for what they do "
            "well. Decide in advance whether you will award by line, by lot or for the whole list, and say so in the RFQ.")))

    s.append(("vendor-selection-and-rfq", "Vendor selection and the RFQ for an ARC", P(
        "An ARC RFQ is like any request for quotation, with one important difference: you are asking for a rate that will hold for a year, "
        "across sites, against an indicative rather than committed quantity. Vendors need enough information to price that risk properly.")
        + h3("Build the vendor list")
        + P("Invite vendors who can actually service the contract: the right categories, coverage of your delivery locations, the capacity "
            f"for your volumes, and a valid {g('gstin', 'GSTIN')}. For larger contracts, many organisations run a short "
            f"{g('supplier-evaluation', 'supplier evaluation')} covering quality, delivery record, financial standing and compliance documents "
            f"before inviting a vendor to quote. The {a('tools/supplier-evaluation-template/', 'supplier evaluation template')} gives you a "
            "weighted scoring structure to start from.")
        + h3("What the RFQ should contain")
        + ul(["the item list with specifications and indicative annual quantities by location",
              "the contract period and expected start date",
              "the price basis you want quoted",
              "your proposed terms on price variation, MOQ, lead time and payment",
              "a fixed response format, so quotes can be compared line by line",
              "the closing date and how clarifications will be handled",
              f"the evaluation method: lowest price, or a {g('techno-commercial-evaluation', 'techno-commercial evaluation')} that also weighs quality and service"])
        + P(f"The {a('tools/rfq-template-generator/', 'RFQ template generator')} produces a structured RFQ you can adapt for an ARC.")
        + h3("Evaluate and negotiate")
        + P(f"Put the quotes into a {g('comparative-statement', 'comparative statement')}, normalising for price basis, freight, taxes and "
            "payment terms so that you compare like with like. Identify the lowest quote, the "
            f"{g('l1-l2-l3', 'L1')}, by line or by lot. Negotiation usually follows, through direct discussion or a "
            f"{g('reverse-auction', 'reverse auction')}, and the final rates should be recorded alongside the original quotes.",
            "Some organisations also award a second vendor a smaller share as a backup source, at or near the L1 rate. If you plan to do this, "
            "state it in the RFQ so vendors can price accordingly.")))

    terms_table = table("Common ARC commercial terms", ["Term", "What to decide", "Common practice"], [
        ("Price basis", "What the rate includes: freight, packing, loading, insurance; GST extra or included", "Rate exclusive of GST, with delivery basis stated, often FOR destination"),
        ("Price variation", "Firm rate, or a formula linked to an index for volatile inputs", "Firm rates for most items; a PVC only for raw-material-linked items"),
        ("MOQ", "Minimum quantity or value per order, by item", "Set per item, in line with how sites actually consume it"),
        ("Validity", "Start and end dates; extension and termination", "Twelve months, with a short documented extension option"),
        ("Delivery", "Lead time, locations, documents", "Lead times by item or category, delivery to named sites"),
        ("Payment", "Days from receipt of goods, GRN or invoice", "Aligned to your accounts payable cycle and statutory MSME limits"),
    ])
    s.append(("commercial-terms", "Commercial terms: price basis, price variation, MOQ, validity, delivery and payment", P(
        "The terms around the rate matter as much as the rate itself. A good price with an impractical MOQ, a vague price basis or an "
        "unworkable lead time will not hold up in use. The summary below reflects common practice; your own terms will depend on the "
        "category, your sites and your policies.")
        + terms_table
        + h3("Price basis")
        + P(f"The price basis says what the rate includes. Two common options are {g('ex-works', 'ex-works')}, where you arrange and pay for "
            f"transport from the vendor's premises, and {g('for-destination', 'FOR destination')}, where the vendor delivers to your site and "
            "the rate includes freight. Spell out whether packing, loading, unloading and insurance are included, and whether GST is "
            "included or extra. Most B2B contracts quote rates exclusive of GST, with the applicable rate shown separately.")
        + h3("Price-variation clauses")
        + P("For items linked to volatile raw materials, such as copper or aluminium cables, steel products and some chemicals, vendors may not "
            f"be willing to hold a fixed rate for twelve months. A {g('price-variation-clause', 'price-variation clause')} links the rate to a "
            "published index or base price through an agreed formula.",
            "The usual design questions are: which index, what base date and base value, what share of the price is variable, whether there "
            "is a band within which no change is made, how often rates are revised, and whether a revision applies to orders already placed. "
            "For everything else, a firm rate for the contract period is simpler to administer and far easier to monitor.")
        + h3("MOQ and pack sizes")
        + P("A minimum order quantity protects the vendor from uneconomic small orders. Agree MOQs per item or per order value, and make sure "
            "buyers can see them when they order. An MOQ that is out of line with how a site actually consumes an item will push buyers "
            "towards local purchases.")
        + h3("Validity")
        + P("State the start and end dates, and what happens at the end: whether the contract can be extended at the same rates for a short "
            "period while a renewal is negotiated, and with how much notice. Avoid open-ended validity.")
        + h3("Delivery terms")
        + P(f"Agree {g('lead-time', 'lead times')} by item or category, the delivery locations, and the documents that must travel with the "
            f"goods: the invoice, test certificates where required and the {g('e-way-bill', 'e-way bill')} where applicable. Say how short "
            "or late deliveries will be handled. If you have many sites, specify whether lead times differ by location.")
        + h3("Payment terms")
        + P(f"{g('payment-terms', 'Payment terms')} are usually expressed as a number of days from receipt of goods, "
            f"{g('grn', 'GRN')} or invoice. Keep them consistent with your accounts payable process, and remember that payments to "
            f"registered micro and small suppliers are subject to statutory time limits (see {g('msme', 'MSME')}). Your finance team will "
            "know how these apply to you.")
        + h3("Other clauses to consider")
        + ul(["the quality inspection and rejection process", "warranty, for items where it applies",
              "periodic performance review, and the right to terminate for poor service",
              "how rates change if statutory tax rates change", "confidentiality of rates and volumes"])))

    s.append(("approvals-and-nfa", "Approvals and the NFA", P(
        f"Before an ARC is awarded, the decision normally needs approval under your {g('doa', 'Delegation of Authority')} (DoA). Because an "
        "ARC covers a year of spend, the approval level is usually set by the estimated annual contract value, not the value of a single order.",
        f"The approval document is commonly called a {g('nfa', 'Note for Approval')} (NFA). A good NFA lets an approver understand and "
        "approve the decision without opening another file. It typically includes:")
        + ul(["the requirement: category, items, sites and contract period",
              "the estimated annual value, and how it was estimated",
              "the vendors invited, those who responded, and any excluded, with reasons",
              "the comparative statement, with the L1 position by line or lot",
              "the negotiation history and the final rates",
              "a comparison with last purchase prices or the previous contract",
              "the key commercial terms, including any price-variation clause",
              "the recommendation and the reasons for it, especially where it is not L1 on every line"])
        + P(f"Record each approval with the approver's name and the date. When the contract is audited, the NFA and its "
            f"{g('audit-trail', 'audit trail')} are the first documents anyone will ask for. The article on "
            f"{a(POST_DOA, 'designing a procurement approval matrix')} covers how to set approval levels that protect the organisation "
            "without slowing routine buying down.")))

    s.append(("rolling-out-the-arc", "Rolling the ARC out to buyers", P(
        "Signing the ARC is only half the job. Many contracts under-deliver because the agreed rates never reach the people who place orders. "
        "A practical rollout covers five things:")
        + ol(["<strong>Publish the rates where buyers order.</strong> A PDF on a shared drive is easy to miss. The rates, MOQs and validity "
              "belong in the catalogue, ordering screen or item master that buyers actually use.",
              "<strong>Map items to item codes.</strong> If your ERP has several codes for the same item, link all of them to the contract, "
              "or clean them up.",
              "<strong>Brief the users.</strong> Tell buyers, stores and user departments what is covered, who the vendor is, the lead times "
              "and the process for anything that isn't covered.",
              "<strong>Set the exception route.</strong> Decide what a buyer should do when an item is needed urgently and the ARC vendor "
              "cannot deliver in time, and who approves that exception.",
              "<strong>Share contacts and escalation.</strong> Give sites the vendor contacts and a clear path for delivery or quality problems."])
        + P(f"{g('catalogue-buying', 'Catalogue buying')}, where contracted items and rates are the default choice on the ordering screen, is "
            "the most reliable way to make the contract the path of least resistance.")))

    s.append(("compliance-and-leakage", "Monitoring compliance and leakage", P(
        f"{g('spend-leakage', 'Leakage')} is the gap between the rates you negotiated and the prices you actually paid. It appears in a few "
        "predictable ways: contracted items bought from other vendors, contracted items bought at a higher rate, and items ordered under a "
        "slightly different description so they never match the contract at all. Spend that bypasses agreed contracts is often called "
        f"{g('maverick-spend', 'maverick spend')}.",
        "Track a small number of measures every month:")
        + ul(["<strong>ARC utilisation:</strong> the share of spend on contracted items that went through the contract",
              "<strong>Price compliance:</strong> PO lines on contracted items where the price differs from the ARC rate",
              "<strong>Off-contract purchases</strong> of contracted items, by site and by buyer",
              "<strong>Vendor performance:</strong> on-time delivery, short supply and rejections",
              "<strong>Consumption against the indicative quantity</strong>, so you know early if volumes are running well above or below plan"])
        + P("The point of monitoring is to find causes, not to blame buyers. If one site keeps buying locally, the reason is often a lead time, "
            "MOQ or service problem with the ARC vendor, and that is usually fixable. The post "
            f"{a(POST_LEAK, 'why negotiated rates don’t reach the purchase order')} looks at the causes and fixes in more detail.")))

    s.append(("renewals", "Renewals", P(
        "Start the renewal well before the contract expires. For most categories, two to three months ahead is a sensible minimum; allow longer "
        "for large or complex contracts, so there is time to go back to the market if needed. A renewal review should cover:")
        + ul(["actual consumption against the indicative quantity",
              "items to add, remove or re-specify, based on what was bought off-contract during the year",
              "the vendor's delivery and quality performance",
              "price movement in the market, and whether any price-variation clause worked as intended",
              "whether to extend, renegotiate with the incumbent or re-tender"])
        + P("If the renewal will not be ready in time, agree a short, documented extension at the existing rates rather than letting the "
            "contract lapse. A lapsed contract leaves buyers ordering without any agreed rate, and the leakage that follows can be hard to "
            "reverse.")))

    s.append(("common-mistakes", "Common mistakes", ul([
        "<strong>Vague specifications.</strong> Vendors price the uncertainty in, and disputes follow.",
        "<strong>Inflated indicative quantities.</strong> Overstating volume to win a lower rate damages trust when the volume doesn't "
        "arrive, and vendors remember it at the next tender.",
        "<strong>No stated price basis.</strong> Rates that don't say what they include cannot be compared, and freight or packing appears "
        "later as an extra.",
        "<strong>Contracts nobody can find.</strong> Rates that aren't visible at the point of order are, in practice, optional.",
        "<strong>No exception route.</strong> If there is no quick, approved way to handle urgent needs, buyers will create their own.",
        "<strong>Ignoring MOQs and lead times.</strong> A good rate with an impractical MOQ or lead time drives local buying.",
        "<strong>Letting contracts lapse.</strong> Expired rates quietly turn back into spot buying.",
        "<strong>Not measuring.</strong> Without utilisation and price-compliance figures, nobody knows whether the contract is working."])))

    s.append(("arc-checklist", "ARC checklist", check_list([
        "Purchase history analysed and ARC candidate items identified",
        "Item list cleaned, with specifications, makes, units and HSN codes",
        "Indicative annual quantities by site",
        "Vendor list prepared and vendors evaluated",
        "RFQ issued with a fixed response format, price basis and evaluation method",
        "Comparative statement prepared on a like-for-like basis",
        "Negotiation completed and final rates recorded",
        "Price basis, price variation, MOQ, validity, delivery and payment terms agreed",
        "NFA approved under your Delegation of Authority",
        "Contract signed and rates published where buyers order",
        "Buyers, stores and user departments briefed; exception route agreed",
        "Monthly utilisation, price-compliance and vendor performance reporting in place",
        "Renewal review scheduled well before expiry"])
        + P(f"For a ready structure, download the {a('tools/annual-rate-contract-template/', 'annual rate contract template')}.")))

    s.append(("how-proceaze-helps", "How ProcEaze helps", P(
        "ProcEaze is a procurement platform built around contracted buying. In short:")
        + ul(["Your Key Account Manager loads your ARC prices into one catalogue of 5,00,000+ products across 56+ categories, with MOQ and "
              "validity shown to buyers.",
              "ARC prices are locked at the point of order, and cart validation checks each order before it is submitted.",
              "Buyers raise purchase requisitions in one click. Approvals run from one to five levels to match your Delegation of Authority, "
              "with NFA approvals and purchase orders on the same record.",
              "Every action is kept in a permanent, downloadable audit trail, and role-based dashboards show spend analytics including ARC utilisation.",
              "Renewals are tracked by your KAM. If you would rather not run contracts yourself, the Managed Procurement option lets ProcEaze supply for you."])
        + P(f"Read more about {a('arc-pricing.html', 'ARC contract pricing on ProcEaze')}, or see "
            f"{a('services/arc-procurement-services/', 'ARC-based procurement services')} if you would like the contract set up, loaded and "
            "renewed for you.")))
    return intro, s


def leakage_content():
    intro = P(
        "Most procurement teams have been through this. A category is tendered, vendors are evaluated, rates are negotiated and approved, "
        "and an annual rate contract is signed. Six months later, someone looks at the purchase orders and finds the same items bought from "
        "other vendors, at other prices, at several sites.",
        f"This gap between the contract and the purchase order is usually called {g('spend-leakage', 'spend leakage')}. It is rarely the "
        "result of bad intent. It is almost always the result of how the contract was rolled out and how buying actually happens. That is "
        "good news, because it means it can be fixed.")
    s = []
    s.append(("what-leakage-looks-like", "What leakage looks like", P(
        "Leakage tends to show up in four forms:")
        + ul(["<strong>Wrong vendor.</strong> A contracted item is bought from a vendor who is not on the contract, often a local supplier.",
              "<strong>Wrong price.</strong> The right vendor is used, but the PO carries a different rate from the contract, usually an older or higher one.",
              "<strong>Wrong item.</strong> A near-identical item is ordered under a different description or item code, so it never matches the contract.",
              "<strong>No contract.</strong> The contract has expired and nobody noticed, so orders continue at whatever price is quoted."])
        + P(f"Each of these is a form of {g('maverick-spend', 'maverick spend')}, and each has a different cause. Treating them all as "
            "buyer discipline problems is the most common reason leakage persists.")))

    s.append(("why-it-happens", "Why it happens", h3("The rates are not visible where orders are placed")
        + P("If the contract lives in a PDF, an email or a spreadsheet on the procurement team's drive, a buyer at a plant has to know it "
            "exists, find it and look up the item before ordering. Under time pressure, many won't. The contract may be excellent, but in "
            "practice it is optional.")
        + h3("The item master doesn't match the contract")
        + P(f"When the same item has several codes or descriptions in the {g('item-master', 'item master')}, buyers can order a perfectly "
            "valid code that simply isn't linked to the contract. Nothing flags it, and the price is whatever the vendor quotes.")
        + h3("MOQ, lead time or service gaps")
        + P(f"Sometimes buyers go elsewhere for a good reason. The contracted vendor's {g('moq', 'MOQ')} may be larger than a site needs, the "
            f"{g('lead-time', 'lead time')} may be too long for a breakdown, or deliveries to a remote site may be unreliable. Each off-contract "
            "order is then a rational local decision, and the contract is the real problem.")
        + h3("Urgency without an exception route")
        + P("Breakdowns happen. If there is no quick, approved way to handle an urgent need, buyers create their own, and the workaround "
            "becomes the habit.")
        + h3("Contracts that lapse")
        + P("When a renewal is late, the old rates stop applying and nothing replaces them. Orders placed in the gap are effectively spot "
            "purchases, often at higher prices, and they can continue long after the new contract is signed.")
        + h3("Nobody is measuring")
        + P("If no one reports on contract utilisation and price compliance, leakage is invisible until an audit or a cost review finds it.")))

    s.append(("how-to-fix-it", "How to fix it", P(
        "Fixing leakage is mostly about making the contracted route the easiest route. In rough order of impact:")
        + ol(["<strong>Put contracted rates at the point of order.</strong> Load the items, rates, MOQs and validity into the catalogue, "
              "ordering screen or item master buyers actually use, so the contracted item is the default choice.",
              "<strong>Lock the price.</strong> Where a contract exists, the buyer shouldn't be able to edit the rate on the order. A "
              "price that can't be changed can't drift.",
              "<strong>Clean up item codes.</strong> Merge duplicate codes, or link every equivalent code to the contract line.",
              "<strong>Fix the contract, not just the behaviour.</strong> Where a site keeps buying locally, find out why. An MOQ, a lead "
              "time or a delivery location may need renegotiating.",
              "<strong>Create a fast exception route.</strong> Allow urgent off-contract purchases with a short, defined approval, and "
              "record the reason so you can see patterns.",
              "<strong>Track renewals.</strong> Keep a renewal calendar and start reviews two to three months before expiry, so contracts "
              "never lapse unnoticed.",
              "<strong>Report monthly.</strong> Share utilisation and price-compliance figures by site and category with the people who "
              "can act on them."])
        + P(f"The {a(ARC_GUIDE, 'annual rate contract procurement guide')} covers how to build these steps into the contract from the "
            "start, rather than fixing them afterwards.")))

    s.append(("what-to-measure", "What to measure", P(
        "You don't need a large set of measures. Four, tracked consistently, will tell you whether contracts are working:")
        + ul(["<strong>ARC utilisation:</strong> of all spend on contracted items, the share that went through the contract",
              "<strong>Price compliance:</strong> the number and value of PO lines on contracted items where the price differs from the contract rate",
              "<strong>Off-contract purchases by reason:</strong> urgency, MOQ, stock-out or no reason given",
              "<strong>Contracts expiring in the next 90 days</strong>, with renewal status"])
        + P("Read these by site and by category, not just in total. Leakage is usually concentrated in a few places, and that is where the "
            "fixes will pay off first.")))

    s.append(("where-software-helps", "Where software helps", P(
        f"Most of these fixes are process changes, but {g('e-procurement', 'e-procurement')} software makes them stick. On ProcEaze, ARC "
        "prices are loaded by your Key Account Manager and locked at the point of order, MOQ and validity are shown to buyers, cart "
        "validation checks orders before they go for approval, and dashboards show ARC utilisation. Renewals are tracked by your KAM. "
        f"See {a('arc-pricing.html', 'ARC contract pricing')} for how it works.")))
    return intro, s


def doa_content():
    intro = P(
        f"Every organisation needs a {g('doa', 'Delegation of Authority')} (DoA) for purchasing: a clear statement of who can approve what, "
        f"and up to which value. The {g('approval-matrix', 'approval matrix')} is how that delegation is applied to each purchase request.",
        "Designed well, an approval matrix protects the organisation from unauthorised or poorly justified spending without anyone noticing it "
        "is there. Designed badly, it becomes the reason a ₹2,000 spare takes two weeks to order, and buyers start finding ways around it. "
        "This article sets out how to design one that does the first and avoids the second.")
    s = []
    s.append(("what-an-approval-matrix-does", "What an approval matrix does", P(
        "An approval matrix answers three questions for every purchase request: does this need approval, who must approve it, and in what "
        "order? The answer usually depends on a few factors:")
        + ul(["the value of the request", "whether the item is on an existing contract or not",
              "the category, for example capital items, IT or hazardous materials",
              "the department, cost centre or site raising it",
              "whether the purchase is budgeted"])
        + P("The DoA is the policy; the matrix is the operating rule. Keeping the two aligned, and keeping the matrix simple enough to apply "
            "consistently, is most of the design work.")))

    s.append(("why-approvals-slow-buying", "Why approval matrices slow buying down", P(
        "Slow approvals are rarely caused by approvers being slow. They are usually built into the design:")
        + ul(["<strong>Too many levels for low-value requests.</strong> A routine consumable passes through the same chain as a large order.",
              "<strong>Approving transactions that were already approved.</strong> Each call-off against an approved rate contract goes "
              "through a full approval again, even though the vendor and price were approved when the contract was awarded.",
              "<strong>Serial chains.</strong> Every approver waits for the one before, so one absence holds up everything.",
              "<strong>No delegates.</strong> When an approver is travelling or on leave, requests simply wait.",
              "<strong>Unclear rules.</strong> If buyers can't predict who will approve a request, they can't plan for it."])))

    s.append(("design-principles", "Design principles", h3("Approve decisions, not transactions")
        + P(f"The most effective change in many organisations is to separate the sourcing decision from the order. When a rate contract is "
            f"awarded, the vendor, items and rates are approved once, through the {g('nfa', 'NFA')}. Orders placed against that contract, at "
            "the contracted rate, then need a lighter approval: usually budget and need, not price and vendor. Off-contract purchases carry "
            "the full chain, because the price and vendor have not been approved yet.")
        + h3("Use a small number of value bands")
        + P("Three to five value bands are usually enough. Each band should reflect a real step up in risk, and the thresholds should be "
            "reviewed periodically, not left unchanged for years while prices rise.")
        + h3("Keep levels proportionate")
        + P("Low-value requests should need one approver, typically the requester's manager or department head. Additional levels should be "
            "added only where they genuinely add judgement: finance for budget, a plant head for site impact, senior management for large or "
            "unusual commitments.")
        + h3("Set delegates and time limits")
        + P("Every approver should have a named delegate, and every level an expected turnaround time. Reminders and escalation after that "
            "time keep requests moving without anyone chasing.")
        + h3("Keep segregation of duties")
        + P(f"Whatever the design, {g('segregation-of-duties', 'segregation of duties')} still applies: the person requesting should not be the "
            "person approving, and approval should be separate from ordering and receiving.")
        + h3("Record everything")
        + P(f"Approvals should be recorded with the approver's name, the action, the date and any comments, in a permanent "
            f"{g('audit-trail', 'audit trail')}. That record is what makes a lighter process acceptable to auditors.")))

    s.append(("illustrative-structure", "An illustrative structure", P(
        "The table below shows the shape of a simple matrix. The value bands are examples only, not a recommendation. Set your own bands and "
        "approvers to match your DoA, your organisation's size and your risk appetite.")
        + table("Illustrative approval matrix structure", ["Value band (example only)", "On-contract (ARC rate)", "Off-contract"], [
            ("Up to ₹1 lakh", "Department head", "Department head, then procurement"),
            ("₹1 lakh to ₹10 lakh", "Department head", "Department head, procurement, then plant or function head"),
            ("₹10 lakh to ₹50 lakh", "Department head, then finance", "Department head, procurement, finance, then plant or function head"),
            ("Above ₹50 lakh", "Department head, finance, then senior management", "Full chain to senior management, with NFA"),
        ])
        + P("Notice the pattern: the on-contract route stays short at every value, because the commercial decision was approved when the "
            "contract was awarded. The off-contract route grows with value, because each request is a new commercial decision.")))

    s.append(("common-mistakes", "Common mistakes", ul([
        "<strong>Copying another organisation's matrix.</strong> Thresholds and approvers should reflect your structure, not someone else's.",
        "<strong>Splitting orders to stay under a threshold.</strong> If this happens often, the threshold is probably too low, and the "
        "matrix should also look at cumulative spend, not just single requests.",
        "<strong>Adding a level after every incident.</strong> Each addition feels safe, but together they produce a chain nobody can move through.",
        "<strong>Leaving the matrix on paper.</strong> If routing depends on people remembering the rules, they will be applied inconsistently."])))

    s.append(("review-annually", "Review it once a year", P(
        "Look at approval data once a year: average time per level, requests sent back or rejected, and how often each level actually "
        "changes an outcome. A level that approves everything it sees, quickly, may be adding little control. A level where requests wait "
        "longest may need a delegate or a lower threshold. Then update the DoA and the matrix together.")))

    s.append(("how-proceaze-helps", "How ProcEaze helps", P(
        "On ProcEaze, each client's approval chain is configured from one to five levels to match its Delegation of Authority. Approvers "
        "can approve, reject or send back a request in one click, NFA approvals run through the same hierarchy, and every action is kept "
        f"in a permanent, downloadable audit trail. Because {a('arc-pricing.html', 'ARC prices are locked at the point of order')}, "
        f"on-contract requests can safely follow a shorter route. Read more about {a('approvals.html', 'approval workflows')} or "
        f"{a('procurement-automation/', 'procurement automation')}.")))
    return intro, s


def mro_content():
    intro = P(
        f"{g('mro', 'MRO')} (maintenance, repair and operations) procurement covers the spares, consumables, tools and supplies that keep "
        "plants, warehouses and offices running: bearings, fasteners, electrical fittings, PPE, lubricants, hand tools, cleaning supplies. "
        "None of it goes into the product. Much of it is low in value per order. And because of that, it is easy to treat as unimportant.",
        "The problem is the shape of MRO spend. A relatively small number of items and vendors account for most of the value, and then "
        f"there is a long tail: thousands of items, many vendors, small orders, bought by many people. This {g('tail-spend', 'tail spend')} "
        "usually costs far more to manage than its value suggests.")
    s = []
    s.append(("what-is-the-long-tail", "What the long tail looks like", P(
        "If you list a year's MRO purchase lines by item and sort them by value, the pattern is familiar. The top of the list is a manageable "
        "set of high-value or high-frequency items. Below it runs a long list of items bought once or twice, in small quantities, from a "
        "wide spread of vendors, often local ones.",
        "Typical features of the tail:")
        + ul(["many vendors, each supplying a handful of items",
              "the same item bought from different vendors, at different prices, by different sites",
              f"inconsistent item descriptions and codes in the {g('item-master', 'item master')}",
              "urgent orders raised when something breaks down",
              "purchases made through petty cash or reimbursement, outside the procurement system"])))

    s.append(("why-it-costs-more", "Why it costs more than it looks", h3("Process cost per order")
        + P("Every purchase order carries a roughly similar process: a requisition, quotes, a comparison, approvals, a PO, receipt, an invoice "
            "and a payment. That effort is much the same for a ₹3,000 order as for a ₹3 lakh one. Across thousands of small orders, the "
            "people-time spent on the process can be large compared with the value of what is bought.")
        + h3("Price variation")
        + P("Without a contract, the same item is priced afresh each time. Different sites pay different prices for the same bearing or "
            "glove, and nobody sees the spread because no one report shows it.")
        + h3("Vendor sprawl")
        + P(f"Each additional vendor needs {g('vendor-onboarding', 'onboarding')}, a {g('vendor-master', 'vendor master')} record, GST and "
            "bank checks, and payment processing. A long list of occasional vendors multiplies that work and the compliance exposure that "
            "comes with it.")
        + h3("Duplicate stock and items")
        + P("When the same item exists under several codes, stores may hold it in several places, or order it while it is already on the "
            "shelf under another description.")
        + h3("Downtime risk")
        + P("The real cost of an MRO item is often not its price but the cost of not having it. A missing spare can stop a line. When tail "
            "items have no agreed source or lead time, every breakdown becomes an emergency purchase.")
        + h3("A weak audit trail")
        + P("Small purchases are the most likely to bypass the system altogether, through cash purchases or informal orders. That leaves "
            "gaps in records that auditors and finance teams have to reconstruct later.")))

    s.append(("signs-to-look-for", "Signs your MRO tail needs attention", P(
        "You don't need a full analysis to know whether the tail is a problem. A few signs usually show up first:")
        + ul(["buyers spend more of their week chasing quotes for small items than managing contracts or vendors",
              "the vendor master grows every quarter, and many vendors receive only one or two orders a year",
              "the same item appears at noticeably different prices on purchase orders from different sites",
              "stores report items on the shelf under one code while another code for the same item is being ordered",
              "emergency purchases after breakdowns are routine rather than rare",
              "finance regularly asks for supporting documents on small purchases that were made outside the system"])
        + P("If several of these sound familiar, the long tail is probably costing more in time, price and risk than its value suggests.")))

    s.append(("why-usual-fixes-fail", "Why the usual fixes fall short", P(
        "The common responses each solve part of the problem. Tightening approvals adds control but also adds process cost to every small "
        "order, which makes the original problem worse. Cutting the vendor list without giving buyers an alternative pushes purchases into "
        "cash and reimbursements. Running a large tender for the whole tail takes a long time and often struggles with poor item data.",
        "What works better is to reduce the number of separate buying decisions, not just to add checks to each of them.")))

    s.append(("how-to-bring-the-tail-under-control", "How to bring the tail under control", ol([
        f"<strong>Analyse the spend.</strong> Run a {g('spend-analysis', 'spend analysis')} of twelve to twenty-four months of MRO purchases "
        "by item, vendor, site and frequency. Clean up descriptions as you go.",
        "<strong>Split the tail.</strong> Separate items that recur (bought several times, by several sites) from genuine one-offs.",
        f"<strong>Contract the recurring items.</strong> Put recurring items on {a(ARC_GUIDE, 'annual rate contracts')}, grouped into "
        "category lots, with clear specifications, MOQs and lead times.",
        f"<strong>Make the catalogue the default.</strong> Publish contracted items and rates where buyers order, so "
        f"{g('catalogue-buying', 'catalogue buying')} is quicker than raising a fresh RFQ.",
        "<strong>Consolidate vendors.</strong> Fewer vendors with broader category coverage reduce onboarding and payment work, and "
        "make each relationship more valuable to both sides.",
        "<strong>Give one-offs a light, fast route.</strong> Use a simple RFQ process and a proportionate approval route for genuine "
        "one-off items.",
        "<strong>Measure and repeat.</strong> Track how much MRO spend goes through contracts, and move newly recurring items onto "
        "contracts at each renewal."])
        + P(f"The {a('tools/mro-procurement-checklist/', 'MRO procurement checklist')} sets out what to check before you buy, and "
            f"{a(CMP_ARC, 'rate contract vs spot buying')} helps decide which items belong on a contract.")))

    s.append(("how-proceaze-helps", "How ProcEaze helps", P(
        "ProcEaze gives buyers one catalogue of 5,00,000+ products across 56+ categories, including MRO, electricals, fasteners, bearings and "
        "power transmission, safety and PPE, and hand tools. Your ARC prices are loaded by your Key Account Manager and locked at the point of "
        "order, approvals run from one to five levels to match your Delegation of Authority, and spend analytics show where tail spend sits. "
        "If you would rather not manage the tail yourself, "
        f"{a('services/b2b-procurement-services/', 'B2B procurement services')} let ProcEaze supply for you.")))
    return intro, s


def eproc_content():
    intro = P(
        f"{g('e-procurement', 'E-procurement')} means running purchasing digitally, from requisition and approval through sourcing to "
        "purchase order. Traditional procurement means running the same steps on paper, email, phone calls and spreadsheets, often with an "
        "ERP used mainly to record the final purchase order.",
        "The steps are largely the same. What changes is where the information lives, who can see it, and how much of the checking is "
        "done by people versus by the system. This comparison sets out those differences side by side, and when each approach makes sense.")
    rows = [
        ("Requisitions", "Paper indents, emails or phone calls; details often incomplete", "Structured requisitions from a catalogue or form, with mandatory fields"),
        ("Approvals", "Physical signatures or email chains; hard to see where a request is", "Routed automatically by the approval matrix, with status visible to all"),
        ("Pricing", "Rates looked up in files or remembered; easy to use an old price", "Contracted rates shown, and often locked, at the point of order"),
        ("Sourcing and RFQs", "Quotes requested and collected by email; comparisons built by hand", "RFQs issued and quotes collected in one place; comparisons generated"),
        ("Purchase orders", "Typed or copied into the ERP, with manual errors", "Generated from the approved requisition, with no re-keying"),
        ("Records and audit", "Spread across inboxes, files and registers", "One permanent, time-stamped audit trail per request"),
        ("Spend visibility", "Monthly reports compiled by hand, usually late", "Dashboards updated as transactions happen"),
        ("Contract compliance", "Depends on buyers knowing and following the contract", "Contracted items and rates are the default route"),
        ("Set-up effort", "Little up front; effort is repeated on every order", "Catalogue, users and approval set-up up front; less effort per order"),
    ]
    s = []
    s.append(("the-two-approaches", "The two approaches", h3("Traditional procurement")
        + P("A user raises an indent on paper or by email. Procurement collects quotes by email or phone, builds a comparison in a "
            "spreadsheet, routes it for signatures, and keys the purchase order into the ERP. Records sit in inboxes, files and registers. "
            "It needs no new software and is familiar to everyone, but most of the control depends on people remembering and applying rules.")
        + h3("E-procurement")
        + P("Users raise requisitions in a system, usually from a catalogue of approved items. Approvals are routed automatically, contracted "
            "prices are applied, and the purchase order is generated from the approved request. Every step is recorded. The rules are "
            "built into the system, so they apply the same way every time.")))
    s.append(("side-by-side", "Side by side", table("E-procurement compared with traditional procurement",
                                                   ["Area", "Traditional procurement", "E-procurement"], rows)))
    s.append(("where-traditional-still-works", "Where traditional procurement still works", P(
        "Manual processes are not always wrong. A small organisation with a single site, a handful of buyers and a short vendor list may "
        "manage well with email and a spreadsheet, as long as approvals and records are kept consistently. Very occasional, highly "
        "specialised purchases, such as a one-off capital item, may also need a bespoke process whatever system you use.",
        "The case for e-procurement grows with scale: more sites, more buyers, more vendors, more contracts and more audit scrutiny. Those "
        "are the conditions in which manual control starts to break down.")))
    s.append(("what-changes-in-practice", "What changes in practice", P(
        "The most visible change is speed, but the more important ones are about control and information:")
        + ul([f"<strong>Contract compliance becomes the default.</strong> When contracted items and rates appear on the ordering screen, using the contract is the easiest choice. See {a(POST_LEAK, 'why negotiated rates don’t reach the purchase order')}.",
              f"<strong>Approvals become predictable.</strong> A configured {g('approval-matrix', 'approval matrix')} routes every request the same way, and everyone can see where it is.",
              f"<strong>Records are complete.</strong> The {g('audit-trail', 'audit trail')} is created as work happens, not reconstructed for audits.",
              "<strong>Spend data is usable.</strong> Clean, structured data replaces monthly reports compiled from several sources."])))
    s.append(("moving-to-e-procurement", "What to plan for when moving to e-procurement", ul([
        f"<strong>Item and vendor data.</strong> Clean the {g('item-master', 'item master')} and {g('vendor-master', 'vendor master')} first; a system amplifies whatever data it is given.",
        "<strong>Approval rules.</strong> Write down your Delegation of Authority in a form a system can apply. Gaps and contradictions show up quickly.",
        "<strong>ERP integration.</strong> Decide what flows between the e-procurement system and your ERP, and in which direction.",
        "<strong>Change management.</strong> Buyers and approvers need to see why the new route is easier, not just be told to use it.",
        "<strong>A phased start.</strong> Starting with a few high-volume categories usually works better than switching everything at once."])))
    s.append(("common-misconceptions", "Common misconceptions", ul([
        "<strong>“E-procurement means replacing the ERP.”</strong> Usually it doesn't. The ERP remains the system of record for "
        "finance and inventory; the e-procurement system handles requisitions, approvals and ordering, and the two are connected.",
        "<strong>“It removes judgement from buying.”</strong> It removes repetitive checking, such as looking up rates or routing "
        "approvals. Decisions about vendors, specifications and exceptions still sit with people.",
        "<strong>“It only suits large companies.”</strong> The case is strongest at scale, but mid-sized organisations with several "
        "sites or many buyers often feel the problems of manual procurement first.",
        "<strong>“Buyers will resist it.”</strong> Buyers resist systems that add steps. When ordering from a catalogue at a known "
        "price is faster than collecting quotes by email, most buyers adopt it quickly."])))
    s.append(("how-to-decide", "How to decide", P(
        "Ask three questions. How many people, sites and vendors are involved in buying? How much of your spend is under contract, and how "
        "confident are you that the contract rates are being used? And how long would it take you to answer an auditor's question about a "
        "purchase made eight months ago? If the answers worry you, the case for e-procurement is already there.",
        f"Read more about {a('e-procurement-software/', 'e-procurement software')} and {a('procure-to-pay-software/', 'procure-to-pay software')}. "
        "On ProcEaze, buyers order from one catalogue of 5,00,000+ products with ARC prices locked at order, raise requisitions in one click, "
        "and approvals run from one to five levels; ERP integration is plug-in ready and scoped at onboarding.")))
    return intro, s


def arc_vs_spot_content():
    intro = P(
        f"Most organisations buy in two ways. Some items are bought under a {g('rate-contract', 'rate contract')}, usually an "
        f"{g('arc', 'annual rate contract')} (ARC), where rates are agreed in advance and orders are placed against them through the year. "
        f"Everything else is bought through {g('spot-buying', 'spot buying')}: quotes are requested for each requirement as it arises.",
        "Neither is better in general. Each suits different kinds of items, and the real question is which items belong in which route. "
        "This comparison sets out the trade-offs and offers a simple way to decide.")
    rows = [
        ("Price", "Agreed in advance for the contract period; the same for every order", "Set by quotes on each occasion; varies with timing and vendor"),
        ("Effort per order", "Low; the commercial work was done when the contract was awarded", "Higher; quotes, comparison and approval each time"),
        ("Speed to order", "Fast; order straight from the contract", "Slower; depends on how quickly quotes come back"),
        ("Volume commitment", "Usually an indicative quantity, not a firm commitment", "None beyond the individual order"),
        ("Flexibility", "Fixed items, specifications and vendor for the period", "Free to change item, specification or vendor each time"),
        ("Market price movement", "Rate holds, or moves by an agreed formula (PVC)", "Each order reflects the market at that moment"),
        ("Vendor relationship", "Longer-term, with performance reviewed over the year", "Transactional"),
        ("Control and audit", "One approval for the contract; orders checked against it", "Each order needs its own justification and approval"),
        ("Best for", "Repeat, standard items bought by many people", "One-offs, changing specifications, volatile commodities"),
    ]
    s = []
    s.append(("definitions", "The two approaches", h3("Rate contract")
        + P("Procurement runs one sourcing exercise for a list of items, negotiates rates and terms, and gets the award approved, usually "
            f"through an {g('nfa', 'NFA')}. Buyers then order against the contract as needed, at the agreed rates, without returning to the "
            "market. The contract carries an indicative quantity but usually no firm commitment to buy it.")
        + h3("Spot buying")
        + P(f"Each requirement is sourced when it arises. The buyer raises an {g('rfq', 'RFQ')} or requests quotes, compares them, gets "
            "approval and issues a purchase order. There is no standing agreement, so each purchase is a fresh commercial decision.")))
    s.append(("side-by-side", "Side by side", table("Rate contract compared with spot buying",
                                                   ["Area", "Rate contract (ARC)", "Spot buying"], rows)))
    s.append(("when-a-rate-contract-wins", "When a rate contract wins", P(
        "Rate contracts are strongest where the same items are bought repeatedly, by many people, across sites. In that situation, spot "
        "buying repeats the same commercial work again and again, and produces different prices for the same item. An ARC does that work "
        "once, gives vendors a reason to offer a better rate in return for a year of business, and makes ordering faster.",
        "The catch is that a rate contract only delivers if buyers use it. Rates need to be visible and, ideally, locked at the point of "
        f"order. Otherwise, contracted items drift back into spot buying at other prices, which is the problem described in "
        f"{a(POST_LEAK, 'why negotiated rates don’t reach the purchase order')}.")))
    s.append(("when-spot-buying-wins", "When spot buying wins", P(
        "Spot buying is the better route for genuine one-off purchases, project-specific materials, items whose specification changes "
        "from order to order, and items whose prices move quickly. For volatile items, a vendor asked to hold a rate for a year will "
        "usually add a margin to cover the risk, so a well-run spot purchase can be the cheaper option.",
        "It is also the right route for new requirements that you don't yet understand well. A few spot purchases can establish the "
        "specification, the vendor field and the price range before you decide whether a contract makes sense.")))
    s.append(("the-hybrid", "The usual answer: both", P(
        "In practice, most organisations need both. A common pattern is a core of ARCs covering high-frequency items in categories such as "
        "PPE, MRO spares, electricals, fasteners and office supplies, with spot buying for everything else. Items that turn out to recur "
        "are moved onto contracts at the next renewal. For volatile but recurring items, a rate contract with a "
        f"{g('price-variation-clause', 'price-variation clause')} can combine the two: an agreed vendor and terms, with a rate that follows "
        "an index.")))
    s.append(("common-mistakes", "Common mistakes with each route", h3("With rate contracts")
        + ul(["putting items on contract that are bought once a year, so the contract adds administration without saving effort",
              "overstating the indicative quantity to win a lower rate, then disappointing the vendor",
              "loading rates where buyers can't see them, so orders drift back to spot buying",
              "letting contracts lapse without a documented extension"])
        + h3("With spot buying")
        + ul(["buying the same item spot, again and again, long after it should have moved onto a contract",
              "collecting too few quotes, or always from the same vendors, so the price is never really tested",
              "comparing quotes on different price bases, for example one including freight and one excluding it",
              "skipping the record of why a vendor was chosen, which leaves gaps at audit"])
        + P(f"Both routes depend on clean item data and a clear {g('approval-matrix', 'approval matrix')}: contracted orders can follow a "
            "short approval route, while spot purchases carry the full one.")))
    s.append(("how-to-decide", "A simple test", P("For each item or item group, ask:")
        + ol(["Was it ordered several times last year, by more than one person or site?",
              "Is the specification stable enough that everyone means the same item?",
              "Can you give vendors an honest indicative annual quantity?",
              "Is the price stable enough for a vendor to hold it, or to follow a simple index?"])
        + P(f"If the answer to all four is yes, it is a strong ARC candidate. The {a(ARC_GUIDE, 'annual rate contract procurement guide')} "
            f"covers how to set one up, and {a('arc-pricing.html', 'ARC contract pricing on ProcEaze')} shows how contracted rates are loaded "
            "and locked at the point of order, with MOQ and validity shown to buyers.")))
    return intro, s


def p2p_content():
    intro = P(
        f"{g('procure-to-pay', 'Procure-to-pay')} (P2P) and {g('source-to-pay', 'source-to-pay')} (S2P) are often used as if they meant the "
        "same thing. They don't. P2P covers the buying and paying of things you have already decided to buy, from a known source. S2P "
        "includes P2P, and adds everything that happens before it: understanding spend, sourcing, choosing vendors and agreeing contracts.",
        "The difference matters when you are deciding what to fix first, or what kind of software you need. This comparison sets out where "
        "each process starts and ends, who is involved and what each one controls.")
    rows = [
        ("Starts with", "A need: a purchase requisition or indent", "Spend analysis and a sourcing need"),
        ("Ends with", "Payment to the vendor", "Payment to the vendor, plus supplier performance review"),
        ("Main question", "Are we buying the approved thing, at the agreed price, correctly?", "Are we buying the right things, from the right vendors, on the right terms?"),
        ("Main steps", "Requisition, approval, PO, goods receipt, invoice, three-way match, payment", "Spend analysis, sourcing, RFQ or auction, award, contract, supplier management, then P2P"),
        ("Main users", "Requesters, buyers, approvers, stores, accounts payable", "All P2P users, plus category managers and sourcing teams"),
        ("Key documents", "PR, PO, GRN, invoice", "RFQ, comparative statement, NFA, contract, plus P2P documents"),
        ("Main controls", "Approvals, price compliance, three-way match", "Competitive sourcing, contract terms, vendor qualification, plus P2P controls"),
        ("Where value comes from", "Fewer errors, faster cycles, contract compliance", "Better prices and terms, plus everything P2P delivers"),
    ]
    s = []
    s.append(("definitions", "The two processes", h3("Procure-to-pay")
        + P(f"P2P begins when someone needs something. A {g('pr', 'purchase requisition')} is raised and approved, a {g('po', 'purchase order')} "
            f"is issued, goods are received and recorded on a {g('grn', 'GRN')}, the vendor's invoice is checked through a "
            f"{g('three-way-match', 'three-way match')}, and the vendor is paid. P2P assumes the vendor and price are already known, either "
            "from a contract or from a quote approved for this purchase.")
        + h3("Source-to-pay")
        + P(f"S2P starts earlier. It begins with {g('spend-analysis', 'spend analysis')} to understand what is bought and from whom, moves "
            f"through sourcing, {g('rfq', 'RFQs')} or {g('reverse-auction', 'reverse auctions')}, vendor selection and contracting, and "
            "includes ongoing supplier management. Only then does it hand over to P2P for day-to-day buying and payment.")))
    s.append(("side-by-side", "Side by side", table("Procure-to-pay compared with source-to-pay",
                                                   ["Area", "Procure-to-pay (P2P)", "Source-to-pay (S2P)"], rows)))
    s.append(("how-they-fit-together", "How they fit together", P(
        "The handover point between the two is the contract, or the approved sourcing decision. Sourcing decides which vendor supplies which "
        "item at what price and on what terms; P2P makes sure each purchase follows that decision.",
        "That is why weaknesses in one show up in the other. A strong sourcing process that agrees good rates delivers little if P2P lets "
        "buyers order at other prices. A tight P2P process can only enforce the rates and vendors it has been given; if sourcing never "
        "revisits them, P2P efficiently pays prices that may no longer be competitive.")))
    s.append(("worked-example", "A worked example", P(
        "Take a plant that needs safety gloves every month.",
        f"On the <strong>source-to-pay</strong> side, procurement reviews last year's glove purchases across sites, writes a specification, "
        "invites qualified vendors to quote, compares the responses, negotiates, and gets an annual rate contract approved through an "
        "NFA. The contract records the item, rate, MOQ, lead time and payment terms. Through the year, procurement reviews the vendor's "
        "delivery and quality, and decides at renewal whether to extend or re-tender.",
        f"On the <strong>procure-to-pay</strong> side, a stores officer raises a requisition for gloves each month. It is approved under "
        f"the {g('approval-matrix', 'approval matrix')}, a purchase order is issued at the contracted rate, the delivery is recorded on a "
        "GRN, the invoice is matched against the PO and GRN, and the vendor is paid.",
        "The sourcing work happens once a year. The P2P cycle runs twelve times. If the P2P side doesn't enforce the contract, the sourcing "
        "work is wasted; if the sourcing side is never revisited, P2P keeps paying last year's price.")))
    s.append(("common-misconceptions", "Common misconceptions", ul([
        "<strong>“P2P is just accounts payable.”</strong> Payment is the last step, but most of the control in P2P sits earlier: in "
        "requisitions, approvals, price compliance and goods receipt.",
        "<strong>“S2P replaces P2P.”</strong> It contains it. An organisation with strong sourcing still needs a reliable P2P process "
        "to turn sourcing decisions into correct orders and payments.",
        "<strong>“You must do everything at once.”</strong> Most organisations build in stages, and the order depends on where the "
        "biggest gaps are today."])))
    s.append(("which-to-fix-first", "Which to fix first", P(
        "There is no universal answer, but a few signs point one way or the other:")
        + ul(["<strong>Start with P2P</strong> if you already have contracts but can't tell whether they are used, approvals are slow or "
              "inconsistent, purchase orders are re-keyed by hand, or audit questions take days to answer.",
              "<strong>Start with sourcing</strong> if most spend is not under any contract, vendors have not been re-tendered in years, or "
              "you have little idea how prices compare across sites.",
              f"<strong>Do both in stages</strong> if you have many sites and categories. A common sequence is to put contracted, catalogue "
              f"buying in place first, then extend into sourcing. The {a(ARC_GUIDE, 'ARC procurement guide')} shows how the two meet in a rate contract."])))
    s.append(("software", "What this means for software", P(
        "Software is sold under both labels, and the scope varies widely. When comparing options, map them against the steps in the table "
        "above rather than the label: which steps are covered today, which are planned, and how each connects to your ERP.",
        "ProcEaze covers the buying side of P2P today: one catalogue with ARC prices locked at order, one-click purchase requisitions, one "
        "to five level approvals per your Delegation of Authority, NFA approvals, purchase orders and a permanent audit trail. On the "
        "sourcing side, the Sourcing Desk for RFQs, Reverse Auctions and the Vendor Portal cover sourcing, and the AI Price Negotiator is "
        "in early access. Payment and reconciliation are on the roadmap. ERP integration is plug-in ready and scoped at onboarding.",
        f"Read more about {a('procure-to-pay-software/', 'procure-to-pay software')}, {a('e-procurement-software/', 'e-procurement software')} "
        f"and the {a('sourcing.html', 'Sourcing Desk')}.")))
    return intro, s


# ---------------------------------------------------------------------------
# Article registry
# ---------------------------------------------------------------------------
ARTICLES = {
    ARC_GUIDE: dict(
        kind="guide", schema="Article", icon="lock",
        short="Annual Rate Contract Procurement",
        h1="Annual rate contract procurement: a practical guide",
        title="Annual Rate Contract (ARC) Procurement Guide | ProcEaze",
        desc="A practical guide to annual rate contract (ARC) procurement: item lists, RFQs, price-variation clauses, MOQ, approvals, rollout, leakage and renewals.",
        eyebrow="Procurement guide",
        lead="How to plan, negotiate, approve, roll out and renew an annual rate contract, so the rates you agree are the rates your buyers actually pay.",
        summary="The full ARC cycle: choosing items, writing specifications, running the RFQ, agreeing commercial terms, NFA approval, rollout, leakage monitoring and renewal, with a checklist.",
        content=arc_guide_content,
        aside=[(CMP_ARC, "Rate contract vs spot buying"), (POST_LEAK, "Why negotiated rates leak"),
               ("tools/annual-rate-contract-template/", "ARC template"), (GLOSS, "Procurement glossary")],
        more=["tools/annual-rate-contract-template/", "services/arc-procurement-services/", "arc-pricing.html",
              CMP_ARC, POST_LEAK, "tools/rfq-template-generator/"]),
    POST_LEAK: dict(
        kind="blog", schema="BlogPosting", icon="unlink",
        short="Why negotiated rates don't reach the PO",
        h1="Why negotiated rates don't reach the purchase order, and how to fix it",
        title="Rate Contract Leakage: Why Negotiated Rates Slip | ProcEaze",
        desc="Rate contract leakage explained: why negotiated ARC rates fail to reach purchase orders, the usual causes, and practical fixes procurement teams can apply.",
        eyebrow="Blog",
        lead="Rate contract leakage is rarely about bad intent. It is usually about where rates live, how items are coded and what buyers do when the contract doesn't fit.",
        summary="The four forms of rate contract leakage, the causes behind them, and seven practical fixes, from locking prices at order to tracking renewals.",
        content=leakage_content,
        aside=[(ARC_GUIDE, "ARC procurement guide"), (CMP_ARC, "Rate contract vs spot buying"), (GLOSS + "#spend-leakage", "Spend leakage, defined")],
        more=[ARC_GUIDE, "arc-pricing.html", CMP_ARC]),
    POST_DOA: dict(
        kind="blog", schema="BlogPosting", icon="network",
        short="Designing a procurement approval matrix",
        h1="How to design a procurement approval matrix (DoA) that doesn't slow buying down",
        title="Procurement Approval Matrix: Designing a DoA | ProcEaze",
        desc="How to design a procurement approval matrix (DoA) that keeps control without slowing buying: value bands, approval levels, delegates and on-contract routes.",
        eyebrow="Blog",
        lead="A procurement approval matrix should protect the organisation without anyone noticing it is there. Here is how to design one that does.",
        summary="Why approval chains slow buying, six design principles, an illustrative matrix structure, and the mistakes that turn a DoA into a bottleneck.",
        content=doa_content,
        aside=[(ARC_GUIDE + "#approvals-and-nfa", "Approvals and the NFA"), (GLOSS + "#doa", "DoA, defined"), (CMP_EPROC, "E-procurement vs traditional")],
        more=["approvals.html", "procurement-automation/", ARC_GUIDE]),
    POST_MRO: dict(
        kind="blog", schema="BlogPosting", icon="wrench",
        short="MRO procurement and the long tail",
        h1="MRO procurement: why the long tail costs more than it looks",
        title="MRO Procurement: The Hidden Cost of the Long Tail | ProcEaze",
        desc="MRO procurement and the long tail: why small, frequent purchases of spares and consumables cost more than they look, and how to bring them under control.",
        eyebrow="Blog",
        lead="Small MRO orders look harmless one at a time. Together, the long tail carries process cost, price variation, vendor sprawl and downtime risk.",
        summary="What MRO tail spend looks like, the six ways it costs more than its value, why the usual fixes fall short, and a seven-step plan to bring it under control.",
        content=mro_content,
        aside=[(ARC_GUIDE, "ARC procurement guide"), ("tools/mro-procurement-checklist/", "MRO procurement checklist"), (GLOSS + "#tail-spend", "Tail spend, defined")],
        more=["tools/mro-procurement-checklist/", "services/b2b-procurement-services/", CMP_ARC]),
    CMP_EPROC: dict(
        kind="comparison", schema="Article", icon="globe",
        short="E-procurement vs traditional procurement",
        h1="E-procurement vs traditional procurement: what actually changes",
        title="E-Procurement vs Traditional Procurement | ProcEaze",
        desc="E-procurement vs traditional procurement compared side by side: requisitions, approvals, pricing, sourcing, purchase orders, audit trail and spend visibility.",
        eyebrow="Procurement comparison",
        lead="The steps are largely the same. What changes is where information lives, who can see it, and how much checking is done by people versus the system.",
        summary="Nine areas compared side by side, where manual processes still work, and what to plan for when moving to e-procurement.",
        content=eproc_content,
        aside=[("e-procurement-software/", "E-procurement software"), (CMP_P2P, "P2P vs S2P"), (GLOSS + "#e-procurement", "E-procurement, defined")],
        more=["e-procurement-software/", "procure-to-pay-software/", POST_LEAK]),
    CMP_ARC: dict(
        kind="comparison", schema="Article", icon="scale",
        short="Rate contract vs spot buying",
        h1="Rate contract vs spot buying: which to use, and when",
        title="Rate Contract vs Spot Buying: When to Use Each | ProcEaze",
        desc="Rate contract vs spot buying compared: price certainty, effort, flexibility, risk and control, with a simple test for deciding which items belong on an ARC.",
        eyebrow="Procurement comparison",
        lead="Neither route is better in general. The real question is which items belong on a rate contract and which are better bought spot.",
        summary="Price, effort, speed, flexibility and control compared, when each route wins, and a four-question test for ARC candidates.",
        content=arc_vs_spot_content,
        aside=[(ARC_GUIDE, "ARC procurement guide"), ("arc-pricing.html", "ARC contract pricing"), (GLOSS + "#rate-contract", "Rate contract, defined")],
        more=[ARC_GUIDE, "arc-pricing.html", "tools/annual-rate-contract-template/"]),
    CMP_P2P: dict(
        kind="comparison", schema="Article", icon="route",
        short="Procure-to-pay vs source-to-pay",
        h1="Procure-to-pay vs source-to-pay: the difference explained",
        title="Procure-to-Pay vs Source-to-Pay: The Difference | ProcEaze",
        desc="Procure-to-pay vs source-to-pay explained: where each process starts and ends, who owns which steps, and how to decide which one to fix first.",
        eyebrow="Procurement comparison",
        lead="P2P makes sure each purchase follows the decision. S2P also makes the decision. Here is where one ends and the other begins.",
        summary="Where P2P and S2P start and end, the steps, users, documents and controls in each, and how to decide which to fix first.",
        content=p2p_content,
        aside=[("procure-to-pay-software/", "Procure-to-pay software"), (CMP_EPROC, "E-procurement vs traditional"), (GLOSS + "#procure-to-pay", "P2P, defined")],
        more=["procure-to-pay-software/", "e-procurement-software/", ARC_GUIDE]),
}

KIND_PARENT = {
    "guide": ("Procurement Guides", GUIDES),
    "blog": ("Blog", BLOG),
    "comparison": ("Procurement Comparisons", COMP),
}


def article_parts(key):
    intro, secs = ARTICLES[key]["content"]()
    html = intro + "".join(f"<h2>{h}</h2>{b}" for _, h, b in secs)
    return intro, secs, words(html)


def read_mins(key):
    return max(1, round(article_parts(key)[2] / 200))


def card_lookup():
    """key -> (name, description, icon) across the site lists and this module's articles."""
    lk = {r[0]: (r[1], r[2], r[3]) for r in SOFTWARE + SERVICES + KNOWLEDGE + TOOLS + COMPANY}
    lk.update({p[0]: (p[1], p[2], p[3]) for p in PLATFORM})
    lk.update({k: (v["short"], v["summary"], v["icon"]) for k, v in ARTICLES.items()})
    return lk


def keep_exploring(keys, title="Keep reading"):
    lk = card_lookup()
    cards = []
    for k in keys:
        n, d, ic = lk[k]
        cards.append(f'<a class="related-card reveal" href="{L(k)}">{icon_tile(ic)}<div><h3>{esc(n)}</h3><p>{esc(d)}</p></div></a>')
    return (f'<section class="section section-light section-tight"><div class="container">'
            f'<div class="section-head-row"><div class="section-head reveal"><p class="eyebrow">Keep exploring</p><h2>{title}</h2></div>'
            f'<a class="link-arrow reveal" href="{L(HUB)}">Knowledge hub {icon("arrow-right")}</a></div>'
            f'<div class="related-grid">{"".join(cards)}</div></div></section>')


def article_crumbs(key):
    v = ARTICLES[key]
    label, parent = KIND_PARENT[v["kind"]]
    return [("Knowledge Hub", HUB), (label, parent), (v["short"], None)]


def article_body(key):
    v = ARTICLES[key]

    def render():
        intro, secs, n = article_parts(key)
        hero = page_hero(article_crumbs(key), v["eyebrow"], v["h1"], v["lead"], compact=True)
        toc = "".join(f'<li><a href="#{sid}">{h}</a></li>' for sid, h, _ in secs)
        aside_links = "".join(f'<li><a href="{L(k)}">{esc(t)}</a></li>' for k, t in v["aside"])
        body = "".join(f'<h2 id="{sid}">{h}</h2>{b}' for sid, h, b in secs)
        meta = (f'<p class="small muted" style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">{icon("calendar", "icon icon-sm")}'
                f'<span>Published <time datetime="{DATE}">{DATE_HUMAN}</time></span><span aria-hidden="true">·</span>'
                f'{icon("clock", "icon icon-sm")}<span>{max(1, round(n / 200))} min read</span><span aria-hidden="true">·</span><span>By ProcEaze</span></p>')
        foot = (f'<div class="notice info mt-48">{icon("info")}<p>This article describes common procurement practice for general '
                f'information. It is not legal, tax or financial advice. For definitions of the terms used, see the '
                f'<a href="{L(GLOSS)}">procurement glossary</a>.</p></div>')
        return (hero + f'<section class="section"><div class="container"><div class="legal-layout">'
                f'<aside class="legal-toc"><h2>Contents</h2><ol>{toc}</ol><h2 class="mt-24">Related reading</h2>'
                f'<ul style="list-style:none;display:grid;gap:6px;font-size:.88rem">{aside_links}</ul></aside>'
                f'<article class="prose">{meta}{intro}{body}{foot}</article></div></div></section>'
                + keep_exploring(v["more"]) + cta())
    return render


def article_schema(key):
    v = ARTICLES[key]
    return {"@context": "https://schema.org", "@type": v["schema"], "headline": v["h1"], "description": v["desc"],
            "datePublished": DATE, "dateModified": DATE, "author": AUTHOR, "publisher": PUBLISHER,
            "inLanguage": "en-IN", "mainEntityOfPage": {"@type": "WebPage", "@id": BASE_URL + "/" + key},
            "url": BASE_URL + "/" + key}


def article_card(key, i=0, heading="h3"):
    v = ARTICLES[key]
    return (f'<article class="card card-hover reveal" style="--d:{i % 3};display:flex;flex-direction:column">'
            f'<div class="card-head">{icon_tile(v["icon"])}</div>'
            f'<p class="small muted" style="margin:0 0 8px"><time datetime="{DATE}">{DATE_HUMAN}</time> · {read_mins(key)} min read</p>'
            f'<{heading}>{esc(v["h1"])}</{heading}><p>{esc(v["summary"])}</p>'
            f'<a class="link-arrow" style="margin-top:auto" href="{L(key)}">Read {"the guide" if v["kind"] == "guide" else "more"} '
            f'<span class="sr-only">: {esc(v["short"])}</span>{icon("arrow-right")}</a></article>')


def keys_of(kind):
    return [k for k, v in ARTICLES.items() if v["kind"] == kind]


# ---------------------------------------------------------------------------
# Hub
# ---------------------------------------------------------------------------
def hub_body():
    hero = page_hero([("Knowledge Hub", None)], "Procurement resources", "Procurement Knowledge Hub",
                     "Practical procurement resources for Indian industrial, MRO and indirect buying teams: guides, a glossary, blog posts, "
                     "side-by-side comparisons and answers to common questions.",
                     actions=btn_link(ARC_GUIDE, "Read the ARC guide", "btn-primary btn-lg") + btn_link(GLOSS, "Browse the glossary"))
    sections = [
        dict(icon="clipboard-check", title="Procurement guides", text="Long-form, practical how-tos, starting with annual rate contract procurement.", href=GUIDES, cta="Browse guides"),
        dict(icon="book", title="Procurement glossary", text=f"{len(TERMS)} procurement terms explained plainly, from ARC and NFA to GRN and three-way match.", href=GLOSS, cta="Open the glossary"),
        dict(icon="newspaper", title="Blog", text="Short, practical articles on rate contracts, approvals and MRO buying.", href=BLOG, cta="Read the blog"),
        dict(icon="scale", title="Procurement comparisons", text="Procurement approaches compared side by side, with tables you can share.", href=COMP, cta="See comparisons"),
        dict(icon="message-circle", title="FAQs", text="Answers to common questions about ProcEaze, ARC pricing, approvals and onboarding.", href="faq.html", cta="Read the FAQs"),
        dict(icon="file-text", title="Whitepapers & reports", text="In-depth procurement reports. Our first reports are in preparation.", href=PAPERS, cta="Find out more"),
    ]
    out = hero
    out += (f'<section class="section"><div class="container">'
            + section_head("Browse the hub", "Procurement resources, by type.",
                           "Everything here is written for the people who run procurement day to day: buyers, procurement managers, department heads and finance.")
            + feature_cards(sections) + '</div></section>')

    # Featured guide
    g_key = ARC_GUIDE
    gv = ARTICLES[g_key]
    _, secs, n = article_parts(g_key)
    toc = check_list([h for _, h, _ in secs[:8]])
    out += (f'<section class="section section-light"><div class="container"><div class="split">'
            f'<div class="reveal"><p class="eyebrow">Featured guide</p><h2>{esc(gv["h1"])}</h2>'
            f'<p class="lead">{esc(gv["lead"])}</p><p class="small muted">{max(1, round(n / 200))} min read · includes a checklist</p>'
            f'<div class="btn-row mt-24">{btn_link(g_key, "Read the guide", "btn-primary btn-lg")}'
            f'{btn_link("tools/annual-rate-contract-template/", "Get the ARC template")}</div></div>'
            f'<div class="card reveal"><h3>What the guide covers</h3>{toc}</div></div></div></section>')

    # Latest posts
    posts = "".join(article_card(k, i) for i, k in enumerate(keys_of("blog")))
    out += (f'<section class="section"><div class="container">'
            f'<div class="section-head-row">{section_head("From the blog", "Latest posts.", None)}'
            f'<a class="link-arrow reveal" href="{L(BLOG)}">All posts {icon("arrow-right")}</a></div>'
            f'<div class="grid grid-3">{posts}</div></div></section>')

    # Comparisons
    comps = "".join(article_card(k, i) for i, k in enumerate(keys_of("comparison")))
    out += (f'<section class="section section-light"><div class="container">'
            f'<div class="section-head-row">{section_head("Side by side", "Procurement comparisons.", None)}'
            f'<a class="link-arrow reveal" href="{L(COMP)}">All comparisons {icon("arrow-right")}</a></div>'
            f'<div class="grid grid-3">{comps}</div></div></section>')

    # Glossary teaser
    pick = ["arc", "nfa", "doa", "l1-l2-l3", "grn", "three-way-match", "maverick-spend", "price-variation-clause"]
    by_id = {term_id(t): (t, d) for t, d in TERMS}
    chips = "".join(f'<a class="chip-btn" href="{L(GLOSS + "#" + i)}">{esc(by_id[i][0])}</a>' for i in pick)
    out += (f'<section class="section"><div class="container">'
            + section_head("Procurement glossary", "Procurement terms, explained.",
                           "Indian procurement has its own vocabulary. Start with the terms teams ask about most.")
            + f'<div class="chips reveal" style="flex-wrap:wrap">{chips}</div>'
            f'<p class="mt-24 reveal">{btn_link(GLOSS, "See all terms, A to Z", "btn-secondary")}</p></div></section>')

    out += keep_exploring(["tools/annual-rate-contract-template/", "tools/rfq-template-generator/", "tools/mro-procurement-checklist/"],
                          "Free procurement tools")
    out += cta("Ready to see contracted buying in practice?")
    return out


# ---------------------------------------------------------------------------
# Index pages
# ---------------------------------------------------------------------------
UPCOMING_GUIDES = [
    ("clipboard-list", "Running an RFQ for industrial and MRO items", "Specifications, vendor lists, response formats and comparative statements."),
    ("store", "Vendor onboarding and verification", "The documents, checks and records to keep before a vendor's first order."),
    ("bar-chart", "Spend analysis for indirect procurement", "Cleaning item data and finding where contracts will pay off first."),
]


def guides_body():
    hero = page_hero([("Knowledge Hub", HUB), ("Procurement Guides", None)], "Knowledge hub", "Procurement guides",
                     "Long-form, practical procurement guides for Indian buying teams. Each one walks through a process end to end, "
                     "with the decisions to make, the common mistakes and a checklist.", compact=True)
    v = ARTICLES[ARC_GUIDE]
    _, secs, n = article_parts(ARC_GUIDE)
    contents = "".join(f'<li><a href="{L(ARC_GUIDE + "#" + sid)}">{h}</a></li>' for sid, h, _ in secs)
    featured = (f'<article class="card reveal"><div class="card-head">{icon_tile(v["icon"])}<span class="small muted">'
                f'{max(1, round(n / 200))} min read</span></div>'
                f'<h2 style="font-size:clamp(1.6rem,1.2rem + 1.4vw,2.2rem)">{esc(v["h1"])}</h2><p class="lead">{esc(v["summary"])}</p>'
                f'<div class="grid grid-2 mt-24"><div><h3>Contents</h3><ol style="padding-left:1.3em;display:grid;gap:6px">{contents}</ol></div>'
                f'<div><h3>Use it with</h3>' + check_list([
                    f'<a href="{L("tools/annual-rate-contract-template/")}">Annual rate contract template</a>',
                    f'<a href="{L("tools/rfq-template-generator/")}">RFQ template generator</a>',
                    f'<a href="{L(CMP_ARC)}">Rate contract vs spot buying</a>',
                    f'<a href="{L("services/arc-procurement-services/")}">ARC-based procurement services</a>'])
                + f'<div class="btn-row mt-24">{btn_link(ARC_GUIDE, "Read the guide", "btn-primary btn-lg")}</div></div></div></article>')
    upcoming = "".join(
        f'<article class="placeholder-card reveal" style="--d:{i}"><div class="card-head">{icon_tile(ic)}</div>'
        f'<h3>{esc(t)}</h3><p class="muted">{esc(d)}</p><div class="placeholder-lines" aria-hidden="true"><i></i><i></i><i></i></div></article>'
        for i, (ic, t, d) in enumerate(UPCOMING_GUIDES))
    out = hero
    out += f'<section class="section"><div class="container">{featured}</div></section>'
    out += (f'<section class="section section-light"><div class="container">'
            + section_head("In preparation", "More guides on the way.", "These guides are being written now.")
            + f'<div class="grid grid-3">{upcoming}</div></div></section>')
    out += keep_exploring([GLOSS, COMP, BLOG], "More from the knowledge hub")
    out += cta()
    return out


def list_body(kind, crumb, eyebrow, h1, lead, list_title):
    def render():
        hero = page_hero([("Knowledge Hub", HUB), (crumb, None)], eyebrow, h1, lead, compact=True)
        cards = "".join(article_card(k, i) for i, k in enumerate(keys_of(kind)))
        others = [x for x in (GUIDES, GLOSS, BLOG, COMP) if x != {"blog": BLOG, "comparison": COMP}[kind]]
        return (hero + f'<section class="section"><div class="container">'
                + section_head(None, list_title, None)
                + f'<div class="grid grid-3">{cards}</div></div></section>'
                + keep_exploring(others, "More from the knowledge hub") + cta())
    return render


def glossary_body():
    hero = page_hero([("Knowledge Hub", HUB), ("Procurement Glossary", None)], "Knowledge hub",
                     "Procurement glossary: procurement terms, explained",
                     f"{len(TERMS)} procurement terms used in Indian industrial, MRO and indirect buying, from ARC and NFA to GRN, "
                     "e-way bill and three-way match, explained in plain language.", compact=True)
    groups = {}
    for t, d in TERMS:
        groups.setdefault(t[0].upper(), []).append((t, d))
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    jump = "".join(
        f'<a class="chip-btn" href="#letter-{c.lower()}">{c}</a>' if c in groups
        else f'<span class="chip-btn" aria-hidden="true" style="opacity:.35;pointer-events:none">{c}</span>'
        for c in letters)
    blocks = []
    for c in sorted(groups):
        items = []
        for t, d in groups[c]:
            link = ""
            if t in TERM_LINKS:
                k, lbl = TERM_LINKS[t]
                link = f'<a class="link-arrow small mt-8" href="{L(k)}">{esc(lbl)} {icon("arrow-right")}</a>'
            items.append(f'<div class="faq-item is-open" id="{term_id(t)}" style="padding:18px 20px;scroll-margin-top:110px">'
                         f'<h3 style="font-size:1rem;margin-bottom:4px">{esc(t)}</h3><p class="muted" style="margin:0">{esc(d)}</p>{link}</div>')
        blocks.append(f'<div id="letter-{c.lower()}" style="scroll-margin-top:110px;margin-top:40px">'
                      f'<h2 style="font-size:1.8rem">{c}</h2><div class="grid grid-2">{"".join(items)}</div></div>')
    out = hero
    out += (f'<section class="section"><div class="container">'
            f'<nav class="chips" aria-label="Jump to letter" style="flex-wrap:wrap">{jump}</nav>'
            f'<div class="notice info mt-24">{icon("info")}<p>Tax and legal definitions here are summaries for general understanding. '
            f'Thresholds and rules change, so confirm current requirements with your finance, tax or legal advisers.</p></div>'
            f'{"".join(blocks)}</div></section>')
    out += keep_exploring([ARC_GUIDE, POST_LEAK, CMP_P2P], "Put the terms in context")
    out += cta()
    return out


def papers_body():
    hero = page_hero([("Knowledge Hub", HUB), ("Whitepapers & Reports", None)], "Knowledge hub", "Procurement whitepapers and reports",
                     "In-depth procurement research for Indian industrial and indirect buying teams.", compact=True)
    out = hero
    out += (f'<section class="section"><div class="container container-narrow">'
            f'<div class="faq-empty reveal" style="padding:56px 24px">{icon_tile("file-text")}'
            f'<h2 class="mt-16" style="font-size:1.6rem">Our first reports are in preparation.</h2>'
            f'<p class="muted" style="max-width:560px;margin-inline:auto">There are no whitepapers or reports published yet. '
            f'Until the first ones are ready, our procurement guide, comparisons and glossary cover the practical side of the same topics. '
            f'If there is a subject you would like us to cover, tell us.</p>'
            f'<div class="btn-row mt-24" style="justify-content:center">{btn_demo("Contact Us", "btn-primary btn-lg")}</div>'
            f'</div></div></section>')
    out += keep_exploring([ARC_GUIDE, COMP, GLOSS], "Read these in the meantime")
    return out


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
HUB_SCHEMA = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Procurement Knowledge Hub",
              "url": BASE_URL + "/" + HUB, "inLanguage": "en-IN",
              "description": "Procurement guides, glossary, blog posts and comparisons for Indian procurement teams."}

PAGES = [
    dict(path=HUB, title="Procurement Knowledge Hub: Guides & Resources | ProcEaze",
         desc="The ProcEaze procurement knowledge hub: practical procurement resources for Indian teams, including an ARC guide, a glossary, blog posts and comparisons.",
         section="knowledge", crumbs=[("Knowledge Hub", None)], schemas=[HUB_SCHEMA], body=hub_body),
    dict(path=GUIDES, title="Procurement Guides for Indian Buying Teams | ProcEaze",
         desc="Practical procurement guides for Indian buying teams, starting with annual rate contract (ARC) procurement: process, terms, approvals and a checklist.",
         section="knowledge", crumbs=[("Knowledge Hub", HUB), ("Procurement Guides", None)], body=guides_body),
    dict(path=GLOSS, title="Procurement Glossary: Procurement Terms A to Z | ProcEaze",
         desc="Procurement glossary with procurement terms from A to Z: ARC, NFA, DoA, GRN, L1, e-way bill, three-way match and more, explained for Indian teams.",
         section="knowledge", crumbs=[("Knowledge Hub", HUB), ("Procurement Glossary", None)], schemas=[GLOSSARY_SCHEMA], body=glossary_body),
    dict(path=BLOG, title="Procurement Blog: Practical Insights for Buyers | ProcEaze",
         desc="The ProcEaze procurement blog: practical articles on rate contracts, approval matrices, MRO buying and controlling spend in Indian organisations.",
         section="knowledge", crumbs=[("Knowledge Hub", HUB), ("Blog", None)],
         body=list_body("blog", "Blog", "Knowledge hub", "Procurement blog",
                        "Practical, evergreen articles on the everyday problems of industrial, MRO and indirect procurement.", "Latest posts.")),
    dict(path=COMP, title="Procurement Comparisons: Approaches Side by Side | ProcEaze",
         desc="Procurement comparisons that set approaches side by side: e-procurement vs traditional, rate contract vs spot buying, and procure-to-pay vs source-to-pay.",
         section="knowledge", crumbs=[("Knowledge Hub", HUB), ("Procurement Comparisons", None)],
         body=list_body("comparison", "Procurement Comparisons", "Knowledge hub", "Procurement comparisons",
                        "Common procurement approaches compared side by side, with the trade-offs and a practical way to decide.", "All comparisons.")),
    dict(path=PAPERS, title="Procurement Whitepapers and Reports | ProcEaze",
         desc="Procurement whitepapers and reports from ProcEaze are in preparation. Meanwhile, read our ARC procurement guide, comparisons and procurement glossary.",
         section="knowledge", noindex=True, crumbs=[("Knowledge Hub", HUB), ("Whitepapers & Reports", None)], body=papers_body),
] + [
    dict(path=k, title=v["title"], desc=v["desc"], section="knowledge", crumbs=article_crumbs(k),
         schemas=[article_schema(k)], body=article_body(k), og_type="article")
    for k, v in ARTICLES.items()
]
