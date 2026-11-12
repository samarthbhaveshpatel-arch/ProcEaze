"""FAQ, Careers and Legal pages. GLOSSARY is extended and rendered by pages_knowledge.py."""
import re
from lib import (icon, icon_tile, badge, esc, L, section_head, page_hero, btn_demo, btn_link, feature_cards, photo_frame)

# ---------------------------------------------------------------------------
# FAQ — answers are drawn only from approved product facts
# ---------------------------------------------------------------------------
FAQ = [
    ("general", "General", [
        ("What is ProcEaze?", "ProcEaze is a B2B procurement intelligence and e-procurement platform for industrial, MRO and indirect procurement. It brings catalogue buying, approvals, sourcing, reverse auctions, AI price negotiation and purchase orders into one workspace."),
        ("Who is ProcEaze for?", "Indian enterprises with industrial, MRO and indirect spend, including manufacturing and process plants, automotive and auto components, infrastructure and construction, energy and renewables, logistics, ports and ICDs, and facility management and corporate offices. Inside a company, it serves leadership, procurement, department heads, buyers, finance and vendors."),
        ("Who is behind ProcEaze?", "ProcEaze was built by a team that runs industrial supply-chain operations in Ahmedabad, India, and started as an in-house procurement tool before becoming a platform for every enterprise."),
        ("What engagement models are available?", "ProcEaze Platform (SaaS), where your teams run procurement on ProcEaze with your own vendors, and ProcEaze Managed Procurement, where you choose ProcEaze as the vendor for a requisition and ProcEaze handles sourcing, pricing and fulfilment."),
        ("How much does ProcEaze cost?", "Pricing is on request and depends on your engagement model and scope. Contact us and our team will discuss it with you."),
        ("What support do clients get?", "Every client gets a named Key Account Manager who handles configuration, renewals, catalogue updates, escalations and periodic spend reports."),
    ]),
    ("catalogue", "Catalogue", [
        ("How many products and categories are on ProcEaze?", "5,00,000+ products across 56+ categories, including safety & PPE, MRO, electricals, fasteners, bearings & power transmission, paper & stationery, office supplies, IT & electronics, hand tools, and industrial plants & machinery."),
        ("Who keeps our catalogue up to date?", "Your dedicated Key Account Manager configures your catalogue and ARC prices, and handles renewals and catalogue updates."),
        ("Can we buy from ProcEaze directly?", "Yes. With Managed Procurement, choose ProcEaze as the vendor on a requisition. It goes straight to purchase approval in your hierarchy."),
    ]),
    ("arc", "ARC Pricing", [
        ("What is ARC pricing?", "ARC stands for annual rate contract. ProcEaze loads your contracted prices into the catalogue and locks them at the point of order, so 100% of catalogue requisitions are priced at ARC rates."),
        ("Can a buyer change the price at order?", "No. ARC prices are applied automatically and cannot be edited at order. Items outside the contract go through RFQ, reverse auction or AI negotiation instead."),
        ("What happens when a contract is due for renewal?", "Your Key Account Manager handles renewals and price updates."),
    ]),
    ("approvals", "Approvals", [
        ("How many approval levels can we have?", "Each client gets its own approval chain, configured from one level to five to match your Delegation of Authority."),
        ("What can approvers do?", "Approve, reject or send back a request in one click. Every action is time-stamped and attributed in a permanent audit trail."),
        ("Do different roles see different dashboards?", "Yes. ProcEaze provides role-specific dashboards for directors, department heads, managers, buyers and finance."),
        ("Are approvers notified?", "Yes. Email notifications are live, so approvers know when a request reaches them."),
    ]),
    ("sourcing", "Sourcing", [
        ("How are off-contract requirements handled?", "Off-contract needs go through RFQ, reverse auction or AI negotiation, then NFA approval and purchase order."),
        ("What is the Sourcing Desk?", "The Sourcing Desk brings RFQs, auctions, vendor selection, NFAs and POs into one desk for procurement teams."),
        ("What is an NFA?", "A Note for Approval. In ProcEaze, it carries the quotes, ranking and recommendation through your approval hierarchy before a purchase order is issued."),
    ]),
    ("auctions", "Auctions", [
        ("Are reverse auctions available?", "Yes. The Reverse Auction Portal runs live reverse auctions, and you can try a simulation on the Reverse Auctions page."),
        ("Which auction formats will be supported?", "English reverse auctions and Japanese descending-clock auctions, with ceiling price, minimum decrement, a timer, L1 / L2 / L3 live ranking, reserve price, anti-sniping and bid history."),
    ]),
    ("ai", "AI Negotiator", [
        ("What does the AI Price Negotiator do?", "It is an AI agent that negotiates with vendors on your behalf, over chat or voice, countering quotes against your target price and bringing back a ranked shortlist with full transcripts."),
        ("Does the AI make purchasing decisions?", "No. The buyer remains in control. The AI negotiates and recommends, exceptions are escalated to the buyer, buyers can take over at any time, and awards go through your NFA approval."),
        ("Is the AI Price Negotiator available now?", "It is in early access for selected clients. You can ask to join through the demo request form."),
    ]),
    ("vendors", "Vendors", [
        ("How do vendors join ProcEaze?", "Register once on the Become a Vendor page. During verification you'll be asked for GSTIN, PAN, company registration, bank details, a product catalogue or price list, and authorisation letters where applicable."),
        ("What is the Vendor Portal?", "The Vendor Portal is where vendors receive RFQs matched to their categories, take part in auctions and track awarded purchase orders."),    ]),
    ("security", "Security", [
        ("How is our data protected?", "Each client's data is completely isolated. Users sign in with passwordless OTP, access is role-based, sessions use encrypted tokens, every action is recorded in a permanent audit trail, and documents are stored securely in the cloud."),
        ("Is single sign-on (SSO) supported?", "SSO is on the roadmap. Today, users sign in with passwordless OTP."),
    ]),
    ("integrations", "Integrations", [
        ("Does ProcEaze integrate with SAP or other ERPs?", "ProcEaze is ERP plug-in ready. Integration with SAP and other ERPs is scoped during onboarding. APIs are available for integration projects on request."),
        ("Do we need to replace our ERP?", "No. ProcEaze is designed to connect with your ERP without a rip-and-replace."),
        ("Are payment gateway and invoice matching available?", "Not yet. Payment gateway and invoice matching are on the roadmap."),
        ("How does onboarding work?", "We issue client credentials, configure your catalogue and ARC prices, build your organisation hierarchy and assign a dedicated Key Account Manager."),
    ]),
]


def faq_body():
    hero = page_hero([("Knowledge Hub", "knowledge-hub/"), ("FAQs", None)], "FAQs", "Procurement software FAQs, answered.",
                     "Everything you might want to know about ProcEaze, from catalogue and pricing to auctions, AI and security.", compact=True)
    chips = '<button class="chip-btn" type="button" data-faq-topic="all" aria-pressed="true">All topics</button>' + "".join(
        f'<button class="chip-btn" type="button" data-faq-topic="{k}" aria-pressed="false">{esc(t)}</button>' for k, t, _ in FAQ)
    toc = "".join(f'<a href="#faq-{k}">{esc(t)}</a>' for k, t, _ in FAQ)
    groups = []
    n = 0
    for k, t, items in FAQ:
        qs = []
        for q, a in items:
            n += 1
            qs.append(f'<div class="faq-item"><h3 style="margin:0;font-size:inherit"><button class="faq-q" type="button" aria-expanded="false" '
                      f'aria-controls="faq-a-{n}" id="faq-q-{n}">{esc(q)}<span class="faq-icon">{icon("plus")}</span></button></h3>'
                      f'<div class="faq-a" id="faq-a-{n}" role="region" aria-labelledby="faq-q-{n}"><div><p>{esc(a)}</p></div></div></div>')
        groups.append(f'<div class="faq-group" data-topic="{k}"><h2 id="faq-{k}">{esc(t)}</h2><div class="faq">{"".join(qs)}</div></div>')
    tools = (f'<div class="faq-tools"><div class="faq-search"><label class="sr-only" for="faq-search">Search questions</label>{icon("search")}'
             f'<input class="input" id="faq-search" type="search" placeholder="Search questions, e.g. ARC, auction, SSO" data-faq-search autocomplete="off"></div>'
             f'<div class="chips" role="group" aria-label="Filter by topic">{chips}</div>'
             f'<p class="small muted" aria-live="polite" data-faq-count>{n} questions</p></div>')
    out = hero
    out += (f'<section class="section"><div class="container">{tools}<div class="faq-layout">'
            f'<nav class="faq-toc" aria-label="FAQ topics">{toc}</nav><div>{"".join(groups)}'
            f'<div class="faq-empty" data-faq-empty hidden>No questions match your search. Try another term, or '
            f'<a href="{L("contact.html")}">ask us directly</a>.</div></div></div></div></section>')
    return out


FAQ_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                   for _, _, items in FAQ for q, a in items],
}


# ---------------------------------------------------------------------------
# Resources (phase 2)
# ---------------------------------------------------------------------------
GLOSSARY = [
    ("ARC", "Annual rate contract: prices agreed with a vendor for a period, usually a year."),
    ("DoA", "Delegation of Authority: who in the organisation can approve what, and up to which value."),
    ("GSTIN", "Goods and Services Tax Identification Number: the 15-character GST registration number of a business."),
    ("KAM", "Key Account Manager: your named point of contact at ProcEaze."),
    ("L1 / L2 / L3", "The lowest, second-lowest and third-lowest bids or quotes for a requirement."),
    ("MOQ", "Minimum order quantity for an item."),
    ("MRO", "Maintenance, repair and operations: the supplies that keep plants and facilities running."),
    ("NFA", "Note for Approval: the document that seeks approval for a sourcing decision before a PO is issued."),
    ("PO", "Purchase order: the formal order issued to a vendor."),
    ("PR", "Purchase requisition: an internal request to buy, raised before a PO."),
    ("RFQ", "Request for quotation: an invitation to vendors to quote for a requirement."),
    ("Reverse auction", "An auction where vendors bid prices down, and the lowest bid ranks first."),
]


# ---------------------------------------------------------------------------
# Careers (phase 2)
# ---------------------------------------------------------------------------
def careers_body():
    hero = page_hero([("Careers", None)], "Careers", "Careers at ProcEaze.",
                     "We're building procurement software for India's industrial enterprises, as a team that runs supply chains every day.",
                     visual=photo_frame("careers-team", "A team working together in an office"))
    areas = [dict(icon="code", title="Product & engineering", text="Building the platform: catalogue, approvals, sourcing, auctions and AI negotiation."),
             dict(icon="headset", title="Key account management", text="Working with clients on catalogues, contracts and procurement outcomes."),
             dict(icon="truck", title="Supply & operations", text="Sourcing, pricing and fulfilment for Managed Procurement.")]
    out = hero
    out += (f'<section class="section"><div class="container">'
            f'<div class="faq-empty reveal" style="padding:56px 24px;margin-bottom:56px">{icon_tile("briefcase")}'
            f'<h2 class="mt-16" style="font-size:1.6rem">Opportunities will be listed here.</h2>'
            f'<p class="muted" style="max-width:520px;margin-inline:auto">There are no open roles listed right now. Please check back later.</p></div>'
            + section_head("What we work on", "The teams behind ProcEaze.", None)
            + feature_cards(areas) + '</div></section>')
    return out


# ---------------------------------------------------------------------------
# Legal (placeholder structure — wording to be finalised by legal counsel)
# ---------------------------------------------------------------------------
LEGAL = {
    "privacy": ("Privacy Policy", "How ProcEaze collects, uses and protects personal data submitted through this website.", [
        ("Who we are", "Identify the data fiduciary / controller for this website. Legal entity name, registered address and contact details to be confirmed by legal counsel."),
        ("Information we collect", "Through the Contact Us form: name, work email, phone, company, designation, company size, procurement spend band, areas of interest and message. Through the vendor registration form: company and contact details, GSTIN, PAN, location, categories supplied and message. Describe any technical data collected by the website host."),
        ("How we use information", "To respond to demo requests, verify and onboard vendors, and communicate about ProcEaze. State any other purposes explicitly."),
        ("Consent and legal basis", "Describe the consent obtained through the website forms and the applicable legal basis under Indian law, including the Digital Personal Data Protection Act, 2023 and its rules, as advised by counsel."),
        ("Sharing", "List categories of recipients (for example group companies and service providers) and the safeguards applied. Confirm whether any data is transferred outside India."),
        ("Retention", "State how long each category of data is kept, and why."),
        ("Security", "Summarise the measures used to protect submitted data."),
        ("Your rights", "Explain how individuals can access, correct or erase their data, withdraw consent and raise grievances, including grievance officer details if required."),
        ("Cookies", "Refer to the Cookie Policy."),
        ("Changes to this policy", "Explain how updates are published and the effective date."),
        ("Contact", "Contact details for privacy queries, to be confirmed by legal counsel."),
    ]),
    "terms": ("Terms of Use", "The terms that govern use of the ProcEaze marketing website.", [
        ("Acceptance", "Use of this website constitutes acceptance of these terms. Define who 'we' and 'you' are."),
        ("About this website", "This website describes the ProcEaze platform. Use of the platform itself (app.proceaze.in) is governed by a separate client agreement."),
        ("Feature status", "Capabilities on this website are labelled Live, Early access or Roadmap. Early access and roadmap items may change and are not commitments."),
        ("Illustrative content", "Product screens and simulations on this website use demo data for illustration and do not represent customer results."),
        ("Acceptable use", "Prohibit misuse of the website and forms, including false submissions and automated scraping."),
        ("Intellectual property", "ProcEaze name, logo and website content ownership. Third-party trademarks, including ERP names, belong to their owners."),
        ("Disclaimers and limitation of liability", "To be drafted by legal counsel."),
        ("Governing law and jurisdiction", "To be confirmed by legal counsel."),
        ("Changes", "How and when these terms may be updated."),
        ("Contact", "Contact details to be confirmed by legal counsel."),
    ]),
    "cookies": ("Cookie Policy", "How this website uses cookies and similar technologies.", [
        ("What cookies are", "Explain cookies and similar technologies such as local storage."),
        ("How this website uses them", "At the time of writing, this website does not set its own cookies or use analytics or advertising trackers. Web fonts are loaded from Google Fonts. Update this section before adding analytics or other tools."),
        ("Third-party services", "List any third-party services that may set cookies, with links to their policies."),
        ("Managing cookies", "Explain how visitors can control cookies in their browser settings, and any consent mechanism adopted."),
        ("Changes", "How updates to this policy are published."),
        ("Contact", "Contact details to be confirmed by legal counsel."),
    ]),
    "vendor-terms": ("Vendor Terms", "Terms for vendors registering to supply through ProcEaze.", [
        ("Eligibility", "Who may register as a vendor, including GST registration requirements."),
        ("Registration and verification", "Information and documents required for verification: GSTIN, PAN, company registration, bank details, product catalogue / price list and authorisation letters where applicable. Explain the right to accept or decline registrations."),
        ("Accuracy of information", "Vendors must keep their details, documents and price lists accurate and current."),
        ("RFQs and quotations", "Rules for responding to RFQs, validity of quotes and confidentiality of buyer requirements."),
        ("Reverse auctions", "Auction rules, including bid validity, minimum decrements, anti-sniping extensions and prohibited conduct such as collusion. To be finalised before the Auction Portal launches."),
        ("AI-assisted negotiation", "Disclosure that vendors may negotiate with an AI agent acting for a buyer, that transcripts are recorded, and that final awards are made by the buyer."),
        ("Purchase orders and fulfilment", "How POs are issued, accepted and fulfilled, and how delivery is confirmed."),
        ("Payment terms", "Payment terms are set out in each purchase order. Details to be confirmed."),
        ("Confidentiality", "Obligations regarding buyer information, prices and documents."),
        ("Suspension and termination", "Grounds and process for suspending or removing a vendor."),
        ("Contact", "Vendor support and legal contact details to be confirmed."),
    ]),
}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def legal_body(key):
    title, lead, sections = LEGAL[key]

    def render():
        hero = page_hero([("Legal", ""), (title, None)], "Legal", title, lead, compact=True)
        toc = "".join(f'<li><a href="#{slug(h)}">{esc(h)}</a></li>' for h, _ in sections)
        body = "".join(f'<h2 id="{slug(h)}">{i + 1}. {esc(h)}</h2><p>{esc(t)}</p>' for i, (h, t) in enumerate(sections))
        others = "".join(f'<li><a href="{L(k + ".html")}">{esc(v[0])}</a></li>' for k, v in LEGAL.items() if k != key)
        return (hero + f'<section class="section"><div class="container"><div class="legal-layout">'
                f'<aside class="legal-toc"><h2>Contents</h2><ol>{toc}</ol><h2 class="mt-24">Other policies</h2><ul style="list-style:none;display:grid;gap:6px;font-size:.88rem">{others}</ul></aside>'
                f'<article class="prose"><div class="notice">{icon("alert-triangle")}<p><strong>Draft structure for legal review.</strong> '
                f'This page sets out the intended structure only. Final wording must be reviewed and approved by legal counsel before publication.</p></div>'
                f'{body}<p class="small muted mt-32">Last updated: to be confirmed on publication.</p></article></div></div></section>')
    return render


PAGES = [
    dict(path="faq.html", title="Procurement Software FAQs | ProcEaze",
         desc="Procurement software FAQs: catalogue and ARC pricing, approvals, sourcing, reverse auctions, AI negotiation, security, integrations and Managed Procurement.",
         section="knowledge", crumbs=[("Knowledge Hub", "knowledge-hub/"), ("FAQs", None)], schemas=[FAQ_SCHEMA], body=faq_body),
    dict(path="careers.html", title="Careers at ProcEaze",
         desc="Careers at ProcEaze: build procurement software for India's industrial enterprises across product, engineering, key accounts and supply operations.",
         section="company", crumbs=[("Careers", None)], body=careers_body),
] + [
    # Draft legal pages stay out of search until counsel approves final wording
    dict(path=f"{k}.html", title=f"{v[0]} | ProcEaze", desc=v[1], section="company", noindex=True,
         crumbs=[("Legal", ""), (v[0], None)], body=legal_body(k))
    for k, v in LEGAL.items()
]
