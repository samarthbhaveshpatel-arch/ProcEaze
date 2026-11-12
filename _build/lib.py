"""
ProcEaze static site generator — shared building blocks.

Every page is rendered to plain static HTML (no runtime dependency).
Edit content in the pages_*.py modules, shared chrome here, then run:

    python _build/build.py
"""
from urllib.parse import quote
import json
import html as _html

BASE_URL = "https://www.proceaze.in"
APP_URL = "https://proceaze.in/login"

# Render context (set per page by build.py)
CTX = {"root": "", "path": "index.html", "section": ""}

# ---------------------------------------------------------------------------
# URL structure
# ---------------------------------------------------------------------------
# The site uses clean folder URLs (/platform/, /services/...). Older pages are
# still keyed by their original file names throughout the page modules; ROUTES
# maps each such key to its public URL. Pages added with the SEO structure use
# their folder URL as the key directly (e.g. "e-procurement-software/").
# build.py writes a redirect page at every old .html location in this table.
ROUTES = {
    "index.html": "",
    # Software solutions + platform capabilities
    "platform.html": "platform/",
    "dashboards.html": "procurement-spend-management/",
    "catalogue.html": "platform/catalogue/",
    "arc-pricing.html": "platform/rate-contract-management/",
    "approvals.html": "platform/approval-workflows/",
    "sourcing.html": "platform/sourcing-desk/",
    "reverse-auction.html": "platform/reverse-auction/",
    "ai-negotiator.html": "platform/ai-price-negotiator/",
    "vendor-portal.html": "platform/vendor-portal/",
    "integrations.html": "platform/integrations/",
    # Services (engagement models now live on the services hub)
    "engagement-models.html": "services/",
    # Solutions by role
    "solutions.html": "solutions/",
    "solutions/leadership.html": "solutions/leadership/",
    "solutions/procurement.html": "solutions/procurement/",
    "solutions/department-heads.html": "solutions/department-heads/",
    "solutions/buyers.html": "solutions/buyers/",
    "solutions/finance.html": "solutions/finance/",
    "solutions/vendors.html": "solutions/vendors/",
    # Industries
    "industries.html": "industries/",
    "industries/manufacturing.html": "industries/manufacturing/",
    "industries/infrastructure.html": "industries/infrastructure-construction/",
    "industries/energy-renewables.html": "industries/energy-renewables/",
    "industries/logistics.html": "industries/logistics/",
    "industries/facility-management.html": "industries/facility-management/",
    # Knowledge hub
    "resources.html": "knowledge-hub/",
    "faq.html": "knowledge-hub/faqs/",
    # Company
    "about.html": "about/",
    "contact.html": "contact/",
    "security.html": "security/",
    "vendors.html": "become-a-vendor/",
    "careers.html": "careers/",
    "categories.html": "categories/",
    "how-it-works.html": "how-it-works/",
    # Legal
    "privacy.html": "privacy-policy/",
    "terms.html": "terms-of-use/",
    "cookies.html": "cookie-policy/",
    "vendor-terms.html": "vendor-terms/",
}


def route(key):
    """Public URL path for a page key: no leading slash, '' for the home page."""
    return ROUTES.get(key, key)


def L(path):
    """Relative link from the current page to a page key or site-root path."""
    if path.startswith(("http", "#", "mailto:", "tel:")):
        return path
    cut = min([i for i in (path.find("?"), path.find("#")) if i >= 0], default=len(path))
    url = CTX["root"] + route(path[:cut])
    return (url or "./") + path[cut:]


def esc(s):
    return _html.escape(str(s), quote=True)


# ---------------------------------------------------------------------------
# Icons (Lucide-style, 24px grid, stroke-based)
# ---------------------------------------------------------------------------
ICONS = {
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "arrow-up": '<path d="m5 12 7-7 7 7M12 19V5"/>',
    "chevron-down": '<path d="m6 9 6 6 6-6"/>',
    "chevron-right": '<path d="m9 18 6-6-6-6"/>',
    "chevron-left": '<path d="m15 18-6-6 6-6"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "check-circle": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "x-circle": '<circle cx="12" cy="12" r="10"/><path d="m15 9-6 6M9 9l6 6"/>',
    "alert-circle": '<circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/>',
    "alert-triangle": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4M12 17h.01"/>',
    "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>',
    "cart": '<circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/>',
    "bag": '<path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/>',
    "file-text": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8M16 13H8M16 17H8"/>',
    "file-check": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="m9 15 2 2 4-4"/>',
    "clipboard-list": '<rect width="8" height="4" x="8" y="2" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M12 11h4M12 16h4M8 11h.01M8 16h.01"/>',
    "clipboard-check": '<rect width="8" height="4" x="8" y="2" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/>',
    "gavel": '<path d="m14.5 12.5-8 8a2.12 2.12 0 1 1-3-3l8-8"/><path d="m16 16 6-6"/><path d="m8 8 6-6"/><path d="m9 7 8 8"/><path d="m21 11-8-8"/>',
    "bot": '<path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2M20 14h2M15 13v2M9 13v2"/>',
    "sparkles": '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/>',
    "stamp": '<path d="M5 22h14"/><path d="M19.27 13.73A2.5 2.5 0 0 0 17.5 13h-11A2.5 2.5 0 0 0 4 15.5V17a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-1.5c0-.66-.26-1.3-.73-1.77Z"/><path d="M14 13V8.5C14 7 15 7 15 5a3 3 0 0 0-6 0c0 2 1 2 1 3.5V13"/>',
    "wallet": '<path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/>',
    "rupee": '<path d="M6 3h12M6 8h12M6 13l8.5 8M6 13h3M9 13c6.667 0 6.667-10 0-10"/>',
    "lock": '<rect width="18" height="11" x="3" y="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>',
    "shield-check": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "key": '<path d="m15.5 7.5 2.3 2.3a1 1 0 0 0 1.4 0l2.1-2.1a1 1 0 0 0 0-1.4L19 4"/><path d="m21 2-9.6 9.6"/><circle cx="7.5" cy="15.5" r="5.5"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    "user": '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "user-check": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="m16 11 2 2 4-4"/>',
    "headset": '<path d="M3 11h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-5Zm0 0a9 9 0 1 1 18 0m0 0v5a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3Z"/><path d="M21 16v2a4 4 0 0 1-4 4h-5"/>',
    "building": '<rect width="16" height="20" x="4" y="2" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M16 6h.01M12 6h.01M12 10h.01M12 14h.01M16 10h.01M16 14h.01M8 10h.01M8 14h.01"/>',
    "office": '<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2M10 6h4M10 10h4M10 14h4M10 18h4"/>',
    "factory": '<path d="M2 20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8l-7 5V8l-7 5V4a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M17 18h1M12 18h1M7 18h1"/>',
    "zap": '<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
    "hard-hat": '<path d="M10 10V5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5"/><path d="M14 6a6 6 0 0 1 6 6v3"/><path d="M4 15v-3a6 6 0 0 1 6-6"/><rect x="2" y="15" width="20" height="4" rx="1"/>',
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    "hammer": '<path d="m15 12-8.373 8.373a1 1 0 1 1-3-3L12 9"/><path d="m18 15 4-4"/><path d="m21.5 11.5-1.914-1.914A2 2 0 0 1 19 8.172V7l-2.26-2.26a6 6 0 0 0-4.202-1.756L9 2.96l.92.82A6.18 6.18 0 0 1 12 8.4V10l2 2h1.172a2 2 0 0 1 1.414.586L18.5 14.5"/>',
    "nut": '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><circle cx="12" cy="12" r="3.5"/>',
    "bearing": '<circle cx="12" cy="12" r="9.5"/><circle cx="12" cy="12" r="3.5"/><circle cx="12" cy="5.7" r="1.3"/><circle cx="12" cy="18.3" r="1.3"/><circle cx="5.7" cy="12" r="1.3"/><circle cx="18.3" cy="12" r="1.3"/>',
    "cog": '<path d="M12 20a8 8 0 1 0 0-16 8 8 0 0 0 0 16Z"/><path d="M12 14a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z"/><path d="M12 2v2M12 22v-2M17 20.66l-1-1.73M11 10.27 7 3.34M20.66 17l-1.73-1M3.34 7l1.73 1M14 12h8M2 12h2M20.66 7l-1.73 1M3.34 17l1.73-1M17 3.34l-1 1.73M11 13.73l-4 6.93"/>',
    "notebook": '<path d="M2 6h4M2 10h4M2 14h4M2 18h4"/><rect width="16" height="20" x="4" y="2" rx="2"/><path d="M16 2v20"/>',
    "pen": '<path d="M21.17 6.81a1 1 0 0 0-3.99-3.99L3.84 16.17a2 2 0 0 0-.5.83l-1.32 4.35a.5.5 0 0 0 .62.62l4.35-1.32a2 2 0 0 0 .83-.5z"/><path d="m15 5 4 4"/>',
    "printer": '<path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><path d="M6 9V3a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v6"/><rect x="6" y="14" width="12" height="8" rx="1"/>',
    "laptop": '<path d="M20 16V7a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v9m16 0H4m16 0 1.28 2.55a1 1 0 0 1-.9 1.45H3.62a1 1 0 0 1-.9-1.45L4 16"/>',
    "package": '<path d="M11 21.73a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73z"/><path d="M12 22V12"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="m7.5 4.27 9 5.15"/>',
    "truck": '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
    "warehouse": '<path d="M22 8.35V20a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V8.35A2 2 0 0 1 3.26 6.5l8-3.2a2 2 0 0 1 1.48 0l8 3.2A2 2 0 0 1 22 8.35Z"/><path d="M6 18h12M6 14h12"/><rect width="12" height="12" x="6" y="10"/>',
    "bar-chart": '<path d="M3 3v16a2 2 0 0 0 2 2h16"/><path d="M18 17V9M13 17V5M8 17v-3"/>',
    "pie-chart": '<path d="M21 12c.552 0 1.005-.449.95-.998a10 10 0 0 0-8.953-8.951c-.55-.055-.998.398-.998.95v8a1 1 0 0 0 1 1z"/><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/>',
    "trending-down": '<path d="M22 17 13.5 8.5l-5 5L2 7"/><path d="M16 17h6v-6"/>',
    "trending-up": '<path d="M22 7 13.5 15.5l-5-5L2 17"/><path d="M16 7h6v6"/>',
    "dashboard": '<rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "timer": '<path d="M10 2h4M12 14l3-3"/><circle cx="12" cy="14" r="8"/>',
    "hourglass": '<path d="M5 22h14M5 2h14M17 22v-4.172a2 2 0 0 0-.586-1.414L12 12l-4.414 4.414A2 2 0 0 0 7 17.828V22M7 2v4.172a2 2 0 0 0 .586 1.414L12 12l4.414-4.414A2 2 0 0 0 17 6.172V2"/>',
    "bell": '<path d="M10.27 21a2 2 0 0 0 3.46 0"/><path d="M3.26 15.33A1 1 0 0 0 4 17h16a1 1 0 0 0 .74-1.67C19.41 13.96 18 12.5 18 8A6 6 0 0 0 6 8c0 4.5-1.41 5.96-2.74 7.33"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "message": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "message-circle": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "mic": '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2M12 19v3"/>',
    "workflow": '<rect width="8" height="8" x="3" y="3" rx="2"/><path d="M7 11v4a2 2 0 0 0 2 2h4"/><rect width="8" height="8" x="13" y="13" rx="2"/>',
    "network": '<rect x="16" y="16" width="6" height="6" rx="1"/><rect x="2" y="16" width="6" height="6" rx="1"/><rect x="9" y="2" width="6" height="6" rx="1"/><path d="M5 16v-3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3M12 12V8"/>',
    "plug": '<path d="M12 22v-5M9 8V2M15 8V2M18 8v5a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4V8Z"/>',
    "cloud": '<path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/>',
    "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14a9 3 0 0 0 18 0V5"/><path d="M3 12a9 3 0 0 0 18 0"/>',
    "code": '<path d="m16 18 6-6-6-6M8 6l-6 6 6 6"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20M2 12h20"/>',
    "briefcase": '<path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/><rect width="20" height="14" x="2" y="6" rx="2"/>',
    "list-checks": '<path d="m3 17 2 2 4-4M3 7l2 2 4-4M13 6h8M13 12h8M13 18h8"/>',
    "filter": '<path d="M22 3H2l8 9.46V19l4 2v-8.54L22 3z"/>',
    "calendar": '<path d="M8 2v4M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/>',
    "map-pin": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    "landmark": '<path d="M3 22h18M6 18v-7M10 18v-7M14 18v-7M18 18v-7M12 2l9 5H3z"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>',
    "anchor": '<path d="M12 22V8M5 12H2a10 10 0 0 0 20 0h-3"/><circle cx="12" cy="5" r="3"/>',
    "construction": '<rect x="2" y="6" width="20" height="8" rx="1"/><path d="M17 14v7M7 14v7M17 3v3M7 3v3M10 14 2.3 6.3M14 6l7.7 7.7M8 6l8 8"/>',
    "refresh": '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
    "send": '<path d="M14.536 21.686a.5.5 0 0 0 .937-.024l6.5-19a.496.496 0 0 0-.635-.635l-19 6.5a.5.5 0 0 0-.024.937l7.93 3.18a2 2 0 0 1 1.112 1.11z"/><path d="m21.854 2.147-10.94 10.939"/>',
    "undo": '<path d="M9 14 4 9l5-5"/><path d="M4 9h10.5a5.5 5.5 0 0 1 0 11H11"/>',
    "eye": '<path d="M2.06 12.35a1 1 0 0 1 0-.7 10.75 10.75 0 0 1 19.88 0 1 1 0 0 1 0 .7 10.75 10.75 0 0 1-19.88 0"/><circle cx="12" cy="12" r="3"/>',
    "eye-off": '<path d="M10.733 5.076a10.744 10.744 0 0 1 11.205 6.575 1 1 0 0 1 0 .696 10.747 10.747 0 0 1-1.444 2.49"/><path d="M14.084 14.158a3 3 0 0 1-4.242-4.242"/><path d="M17.479 17.499a10.75 10.75 0 0 1-15.417-5.151 1 1 0 0 1 0-.696 10.75 10.75 0 0 1 4.446-5.143"/><path d="m2 2 20 20"/>',
    "history": '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5M12 7v5l4 2"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5M12 15V3"/>',
    "inbox": '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>',
    "layers": '<path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>',
    "grid": '<rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/>',
    "scale": '<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10M12 3v18M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "gauge": '<path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/>',
    "log-in": '<path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><path d="m10 17 5-5-5-5M15 12H3"/>',
    "book-open": '<path d="M12 7v14"/><path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z"/>',
    "newspaper": '<path d="M15 18h-5M18 14h-8"/><path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-4 0v-9a2 2 0 0 1 2-2h2"/><rect width="8" height="4" x="10" y="6" rx="1"/>',
    "book": '<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20"/>',
    "table": '<path d="M12 3v18"/><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M3 9h18M3 15h18"/>',
    "puzzle": '<path d="M19.439 7.85c-.049.322.059.648.289.878l1.568 1.568c.47.47.706 1.087.706 1.704s-.235 1.233-.706 1.704l-1.611 1.611a.98.98 0 0 1-.837.276c-.47-.07-.802-.48-.968-.925a2.501 2.501 0 1 0-3.214 3.214c.446.166.855.497.925.968a.979.979 0 0 1-.276.837l-1.61 1.61a2.404 2.404 0 0 1-1.705.707 2.402 2.402 0 0 1-1.704-.706l-1.568-1.568a1.026 1.026 0 0 0-.877-.29c-.493.074-.84.504-1.02.968a2.5 2.5 0 1 1-3.237-3.237c.464-.18.894-.527.967-1.02a1.026 1.026 0 0 0-.289-.877l-1.568-1.568A2.402 2.402 0 0 1 1.998 12c0-.617.236-1.234.706-1.704L4.23 8.77c.24-.24.581-.353.917-.303.515.077.877.528 1.073 1.01a2.5 2.5 0 1 0 3.259-3.259c-.482-.196-.933-.558-1.01-1.073-.05-.336.062-.676.303-.917l1.525-1.525A2.402 2.402 0 0 1 12 1.998c.617 0 1.234.236 1.704.706l1.568 1.568c.23.23.556.338.877.29.493-.074.84-.504 1.02-.968a2.5 2.5 0 1 1 3.237 3.237c-.464.18-.894.527-.967 1.02Z"/>',
    "unlink": '<path d="m18.84 12.25 1.72-1.71h-.02a5.004 5.004 0 0 0-.12-7.07 5.006 5.006 0 0 0-6.95 0l-1.72 1.71M5.17 11.75l-1.71 1.71a5.004 5.004 0 0 0 .12 7.07 5.006 5.006 0 0 0 6.95 0l1.71-1.71M8 2v3M2 8h3M16 19v3M19 16h3"/>',
    "external": '<path d="M15 3h6v6M10 14 21 3M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
    "droplet": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/>',
    "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>',
    "flask": '<path d="M14 2v6a2 2 0 0 0 .245.96l5.51 10.08A2 2 0 0 1 18 22H6a2 2 0 0 1-1.755-2.96l5.51-10.08A2 2 0 0 0 10 8V2"/><path d="M6.453 15h11.094M8.5 2h7"/>',
    "bulb": '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5M9 18h6M10 22h4"/>',
    "armchair": '<path d="M19 9V6a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v3"/><path d="M3 16a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-5a2 2 0 0 0-4 0v1.5a.5.5 0 0 1-.5.5h-9a.5.5 0 0 1-.5-.5V11a2 2 0 0 0-4 0z"/><path d="M5 18v2M19 18v2"/>',
    "coffee": '<path d="M10 2v2M14 2v2M16 8a1 1 0 0 1 1 1v8a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V9a1 1 0 0 1 1-1h14a4 4 0 1 1 0 8h-1M6 2v2"/>',
    "store": '<path d="m2 7 4.41-4.41A2 2 0 0 1 7.83 2h8.34a2 2 0 0 1 1.42.59L22 7"/><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><path d="M15 22v-4a2 2 0 0 0-2-2h-2a2 2 0 0 0-2 2v4"/><path d="M2 7h20"/><path d="M22 7v3a2 2 0 0 1-2 2 2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 16 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 12 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 8 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 4 12a2 2 0 0 1-2-2V7"/>',
    "crown": '<path d="M11.562 3.266a.5.5 0 0 1 .876 0L15.39 8.87a1 1 0 0 0 1.516.294L21.183 5.5a.5.5 0 0 1 .798.519l-2.834 10.246a1 1 0 0 1-.956.734H5.81a1 1 0 0 1-.957-.734L2.02 6.02a.5.5 0 0 1 .798-.519l4.276 3.664a1 1 0 0 0 1.516-.294z"/><path d="M5 21h14"/>',
    "id-card": '<path d="M16 10h2M16 14h2"/><path d="M6.17 15a3 3 0 0 1 5.66 0"/><circle cx="9" cy="11" r="2"/><rect x="2" y="5" width="20" height="14" rx="2"/>',
    "banknote": '<rect width="20" height="12" x="2" y="6" rx="2"/><circle cx="12" cy="12" r="2"/><path d="M6 12h.01M18 12h.01"/>',
    "badge-check": '<path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"/><path d="m9 12 2 2 4-4"/>',
    "upload": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m17 8-5-5-5 5M12 3v12"/>',
    "repeat": '<path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>',
    "route": '<circle cx="6" cy="19" r="3"/><path d="M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15"/><circle cx="18" cy="5" r="3"/>',
    "fingerprint": '<path d="M12 10a2 2 0 0 0-2 2c0 1.02-.1 2.51-.26 4"/><path d="M14 13.12c0 2.38 0 6.38-1 8.88"/><path d="M17.29 21.02c.12-.6.43-2.3.5-3.02"/><path d="M2 12a10 10 0 0 1 18-6"/><path d="M2 16h.01"/><path d="M21.8 16c.2-2 .131-5.354 0-6"/><path d="M5 19.5C5.5 18 6 15 6 12a6 6 0 0 1 .34-2"/><path d="M8.65 22c.21-.66.45-1.32.57-2"/><path d="M9 6.8a6 6 0 0 1 9 5.2v2"/>',
    "smartphone": '<rect width="14" height="20" x="5" y="2" rx="2"/><path d="M12 18h.01"/>',
    "folder-lock": '<rect width="8" height="5" x="14" y="17" rx="1"/><path d="M10 20H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h3.9a2 2 0 0 1 1.69.9l.81 1.2a2 2 0 0 0 1.67.9H20a2 2 0 0 1 2 2v2.5"/><path d="M20 17v-2a2 2 0 1 0-4 0v2"/>',
    "list": '<path d="M3 12h.01M3 18h.01M3 6h.01M8 12h13M8 18h13M8 6h13"/>',
    "pause": '<rect x="14" y="4" width="4" height="16" rx="1"/><rect x="6" y="4" width="4" height="16" rx="1"/>',
    "play": '<polygon points="6 3 20 12 6 21 6 3"/>',
    "rotate": '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/>',
    "hand": '<path d="M18 11V6a2 2 0 0 0-2-2a2 2 0 0 0-2 2"/><path d="M14 10V4a2 2 0 0 0-2-2a2 2 0 0 0-2 2v2"/><path d="M10 10.5V6a2 2 0 0 0-2-2a2 2 0 0 0-2 2v8"/><path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.82L7 15"/>',
    "arrow-up-right": '<path d="M7 7h10v10M7 17 17 7"/>',
    "percent": '<path d="M19 5 5 19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
}


def icon(name, cls="icon", label=None):
    body = ICONS.get(name, ICONS["info"])
    aria = f'role="img" aria-label="{esc(label)}"' if label else 'aria-hidden="true"'
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" {aria} focusable="false">{body}</svg>')


def icon_tile(name, extra=""):
    return f'<span class="icon-tile {extra}">{icon(name)}</span>'


# Brand mark: shopping-bag outline forming a "P" monogram
LOGO_MARK_PATHS = (
    '<path d="M17 15.5V11a7 7 0 0 1 14 0v4.5"/>'
    '<path d="M9.5 44V16H25a7.75 7.75 0 0 1 0 15.5H9.5"/>'
    '<path d="M25 16h10.5l3.5 26H19.5v-5.5"/>'
)


def logo_mark(cls="brand-mark"):
    return (f'<svg class="{cls}" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="3.6" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{LOGO_MARK_PATHS}</svg>')


def brand(extra_cls=""):
    return (f'<a class="brand {extra_cls}" href="{L("index.html")}" aria-label="ProcEaze — home">'
            f'<img class="brand-logo" src="{L("assets/logo/proceaze-logo.png")}" width="560" height="147" '
            f'alt="ProcEaze — Procurement Intelligence"></a>')


# ---------------------------------------------------------------------------
# Status badges
# ---------------------------------------------------------------------------
STATUS = {
    "early": ("badge-early", "Early access"),
    "roadmap": ("badge-roadmap", "Roadmap"),
    "live": ("badge-live", "Live"),
    "ready": ("badge-ready", "Plug-in ready"),
    "sso-ready": ("badge-roadmap", "Roadmap"),
    "verify": ("badge-verify", "Catalogue verification required"),
    "on-request": ("badge-ready", "On request"),
}


def badge(status, extra="", text=None):
    if not status or status not in STATUS:
        return ""
    cls, label = STATUS[status]
    return f'<span class="badge {cls} {extra}">{esc(text or label)}</span>'


# ---------------------------------------------------------------------------
# Navigation data
# ---------------------------------------------------------------------------
PLATFORM = [
    # file, name, short description, icon, status
    ("platform.html", "Platform Overview", "One workspace from catalogue to purchase order", "dashboard", None),
    ("catalogue.html", "Catalogue & Buying", "One contracted catalogue, ARC prices pre-loaded", "cart", None),
    ("arc-pricing.html", "ARC Contract Pricing", "Contract prices enforced at the point of order", "lock", None),
    ("approvals.html", "Approvals & Delegation of Authority", "Approval chains from one level to five", "network", None),
    ("dashboards.html", "Procurement Spend Management", "Spend, ARC utilisation and category trends", "bar-chart", None),
    ("sourcing.html", "Sourcing Desk", "RFQs, vendor selection, NFAs and POs", "clipboard-list", None),
    ("reverse-auction.html", "Reverse Auctions", "Live competitive bidding with anti-sniping", "gavel", None),
    ("ai-negotiator.html", "AI Price Negotiator", "An AI agent that negotiates on your behalf", "bot", "early"),
    ("vendor-portal.html", "Vendor Portal", "RFQs, auctions and POs for suppliers", "store", None),
    ("integrations.html", "Integrations", "ERP plug-in ready, scoped at onboarding", "plug", None),
]
PLATFORM_BY_FILE = {p[0]: p for p in PLATFORM}

ROLES = [
    ("solutions/leadership.html", "Leadership / CXO", "Company-wide spend and control, live", "crown"),
    ("solutions/procurement.html", "Procurement & Purchase", "One desk from RFQ to purchase order", "clipboard-list"),
    ("solutions/department-heads.html", "Department Heads", "Approvals and team spend at a glance", "users"),
    ("solutions/buyers.html", "Buyers & Requesters", "Order in minutes at contracted prices", "cart"),
    ("solutions/finance.html", "Finance & Accounts", "Contract-compliant spend, clean records", "landmark"),
    ("solutions/vendors.html", "Vendors", "Transparent, digital sourcing", "store"),
]

INDUSTRIES = [
    ("industries/manufacturing.html", "Manufacturing & Process Plants", "factory"),
    ("industries/infrastructure.html", "Infrastructure & Construction", "construction"),
    ("industries/automotive/", "Automotive & Auto Components", "cog"),
    ("industries/energy-renewables.html", "Energy & Renewables", "sun"),
    ("industries/logistics.html", "Logistics, Ports & ICDs", "anchor"),
    ("industries/facility-management.html", "Facility Management & Corporate Offices", "office"),
]

# SEO structure: section 2, Software Solutions (key, name, short description, icon)
SOFTWARE = [
    ("platform.html", "B2B Procurement Platform", "One workspace from catalogue to purchase order", "dashboard"),
    ("procurement-management-software/", "Procurement Management Software", "Suppliers, contracts, requests and approvals in one system", "layers"),
    ("e-procurement-software/", "E-Procurement Software", "Digital catalogue buying, RFQs and approvals", "globe"),
    ("procurement-automation/", "Procurement Automation", "Validation, routing and approvals without the chasing", "workflow"),
    ("procure-to-pay-software/", "Procure-to-Pay Software", "Requisition, approval and PO on one record", "route"),
    ("dashboards.html", "Procurement Spend Management", "Live spend, ARC utilisation and category trends", "pie-chart"),
]

# Section 3, Procurement Services
SERVICES = [
    ("services/", "Procurement Services", "Run procurement yourself, or let ProcEaze supply for you", "briefcase"),
    ("services/end-to-end-procurement-services/", "End-to-End Procurement Services", "Sourcing, pricing and fulfilment handled by ProcEaze", "repeat"),
    ("services/b2b-procurement-services/", "B2B & Corporate Procurement Services", "Indirect and MRO buying for companies, managed", "building"),
    ("services/arc-procurement-services/", "ARC-Based Procurement Services", "Annual rate contracts set up, loaded and renewed", "lock"),
]

COMPANY = [
    ("about.html", "About Us", "Built by people who run supply chains", "building"),
    ("why-proceaze/", "Why ProcEaze", "What sets ProcEaze apart", "badge-check"),
    ("contact.html", "Contact Us", "Get in touch with our team", "message-circle"),
    ("request-a-demo/", "Request a Demo", "A 30-minute walkthrough, configured for you", "calendar"),
    ("security.html", "Security & Trust", "Enterprise-grade control, by design", "shield-check"),
    ("vendors.html", "Become a Vendor", "Supply through ProcEaze", "store"),
    ("careers.html", "Careers", "Work on procurement intelligence", "users"),
]

# Section 6, Procurement Knowledge Hub
KNOWLEDGE = [
    ("knowledge-hub/", "Knowledge Hub", "Guides and insights for procurement teams", "book-open"),
    ("knowledge-hub/procurement-guides/", "Procurement Guides", "Practical how-tos for procurement teams", "clipboard-check"),
    ("knowledge-hub/procurement-glossary/", "Procurement Glossary", "Procurement terms, explained", "book"),
    ("knowledge-hub/blog/", "Blog", "Perspectives on industrial procurement", "newspaper"),
    ("faq.html", "FAQs", "Answers to common questions", "message-circle"),
    ("knowledge-hub/procurement-comparisons/", "Procurement Comparisons", "Approaches compared side by side", "scale"),
    ("knowledge-hub/whitepapers-reports/", "Whitepapers & Reports", "In-depth procurement research", "file-text"),
]

# Section 8, Procurement Tools
TOOLS = [
    ("tools/", "Procurement Tools", "Free templates, checklists and calculators", "wrench"),
    ("tools/annual-rate-contract-template/", "Annual Rate Contract Template", "A ready ARC structure to download", "file-text"),
    ("tools/rfq-template-generator/", "RFQ Template Generator", "Build a complete RFQ in minutes", "clipboard-list"),
    ("tools/supplier-evaluation-template/", "Supplier Evaluation Template", "Weighted scoring for vendor selection", "list-checks"),
    ("tools/mro-procurement-checklist/", "MRO Procurement Checklist", "Everything to check before you buy MRO", "clipboard-check"),
    ("tools/procurement-savings-calculator/", "Procurement Savings Calculator", "Estimate savings from your own numbers", "percent"),
]


# ---------------------------------------------------------------------------
# Forms
# ---------------------------------------------------------------------------
def _err(fid):
    return f'<p class="field-error" id="{fid}-err">{icon("alert-circle")}<span></span></p>'


def f_input(p, name, label, type_="text", required=True, auto=None, placeholder="", rule=None, full=False, hint=None, attrs=""):
    fid = f"{p}-{name}"
    req = '<span class="req" aria-hidden="true">*</span>' if required else '<span class="opt">(optional)</span>'
    ac = f' autocomplete="{auto}"' if auto else ""
    rl = f' data-rule="{rule}"' if rule else ""
    ph = f' placeholder="{esc(placeholder)}"' if placeholder else ""
    hint_html = f'<p class="field-hint" id="{fid}-hint">{hint}</p>' if hint else ""
    desc = f"{fid}-err" + (f" {fid}-hint" if hint else "")
    return (f'<div class="field{" full" if full else ""}"><label for="{fid}">{label}{req}</label>'
            f'<input class="input" id="{fid}" name="{name}" type="{type_}"{ac}{ph}{rl}{" required" if required else ""} '
            f'aria-describedby="{desc}" {attrs}>{hint_html}{_err(fid)}</div>')


def f_phone(p, required=True):
    fid = f"{p}-phone"
    req = '<span class="req" aria-hidden="true">*</span>' if required else ""
    return (f'<div class="field"><label for="{fid}">Phone{req}</label><div class="input-group">'
            f'<span class="prefix" aria-hidden="true">+91</span>'
            f'<input class="input" id="{fid}" name="phone" type="tel" inputmode="numeric" autocomplete="tel-national" '
            f'placeholder="98765 43210" maxlength="11" data-rule="phone-in"{" required" if required else ""} aria-describedby="{fid}-err"></div>{_err(fid)}</div>')


def f_select(p, name, label, options, required=True, full=False):
    fid = f"{p}-{name}"
    req = '<span class="req" aria-hidden="true">*</span>' if required else '<span class="opt">(optional)</span>'
    opts = '<option value="">Select…</option>' + "".join(f'<option>{esc(o)}</option>' for o in options)
    return (f'<div class="field{" full" if full else ""}"><label for="{fid}">{label}{req}</label>'
            f'<select class="select" id="{fid}" name="{name}"{" required" if required else ""} aria-describedby="{fid}-err">{opts}</select>{_err(fid)}</div>')


def f_textarea(p, name, label, required=False, placeholder=""):
    fid = f"{p}-{name}"
    req = '<span class="req" aria-hidden="true">*</span>' if required else '<span class="opt">(optional)</span>'
    return (f'<div class="field full"><label for="{fid}">{label}{req}</label>'
            f'<textarea class="textarea" id="{fid}" name="{name}" placeholder="{esc(placeholder)}"{" required" if required else ""} '
            f'aria-describedby="{fid}-err"></textarea>{_err(fid)}</div>')


def f_checks(p, name, legend, options, required=False):
    fid = f"{p}-{name}"
    items = "".join(
        f'<label class="check"><input type="checkbox" name="{name}" value="{esc(o)}" data-interest="{esc(o)}"> {esc(o)}</label>'
        for o in options)
    req = ' data-required-group="true"' if required else ""
    reqmark = '<span class="req" aria-hidden="true">*</span>' if required else '<span class="opt">(select any)</span>'
    return (f'<fieldset class="field full" id="{fid}"{req} aria-describedby="{fid}-err"><legend>{legend}{reqmark}</legend>'
            f'<div class="check-grid">{items}</div>{_err(fid)}</fieldset>')


def f_consent(p, text=None):
    fid = f"{p}-consent"
    text = text or f'I agree to be contacted and accept the <a href="{L("privacy.html")}">Privacy Policy</a>'
    return (f'<div class="field full"><label class="consent" for="{fid}"><input type="checkbox" id="{fid}" name="consent" required '
            f'aria-describedby="{fid}-err"><span>{text}<span class="req" aria-hidden="true">*</span></span></label>{_err(fid)}</div>')


INTERESTS = ["Platform SaaS", "Managed Procurement", "Auctions", "AI Negotiator", "ERP integration"]
COMPANY_SIZES = ["1–50 employees", "51–200 employees", "201–1,000 employees", "1,001–5,000 employees", "5,000+ employees"]
SPEND_BANDS = ["Under ₹5 Cr", "₹5–25 Cr", "₹25–100 Cr", "₹100–500 Cr", "Above ₹500 Cr", "Prefer not to say"]


def success_panel(title, text, extra=""):
    return (f'<div class="form-success" data-form-success hidden tabindex="-1">'
            f'<div class="success-icon">{icon("check")}</div><h3>{title}</h3><p>{text}</p>{extra}</div>')


def demo_form(p, submit_label="Send Message", modal=False):
    """The 'Contact Us' form (used in modal and on the contact page)."""
    return (
        f'<div class="form-wrap">'
        f'<form class="demo-form" data-form="demo" novalidate data-toast="Demo request received. We will be in touch within one business day.">'
        f'<div class="form-grid">'
        + f_input(p, "name", "Full name", auto="name", placeholder="Your full name")
        + f_input(p, "email", "Work email", "email", auto="email", placeholder="name@company.com", rule="work-email")
        + f_phone(p)
        + f_input(p, "company", "Company name", auto="organization", placeholder="Company name")
        + f_input(p, "designation", "Designation", auto="organization-title", placeholder="e.g. Head of Procurement")
        + f_select(p, "size", "Company size", COMPANY_SIZES)
        + f_select(p, "spend", "Annual procurement spend", SPEND_BANDS, full=True)
        + f_checks(p, "interest", "Interested in", INTERESTS)
        + f_textarea(p, "message", "Message", placeholder="Tell us about your categories, sites or approval structure")
        + f_consent(p)
        + f'</div><div class="form-actions mt-16"><span class="form-note">{icon("lock")} Your details are used only to arrange your demo.</span>'
        f'<button class="btn btn-primary btn-lg" type="submit">{submit_label} {icon("arrow-right", "icon icon-arrow")}</button></div>'
        f'</form>'
        + success_panel("Thank you.", "Our team will get back to you within one business day.",
                        '<button class="btn btn-secondary mt-24" type="button" data-modal-close>Close</button>' if modal else
                        '<button class="btn btn-secondary mt-24" type="button" data-form-again>Send another request</button>')
        + '</div>'
    )


# ---------------------------------------------------------------------------
# Section helpers
# ---------------------------------------------------------------------------
def section_head(eyebrow=None, title="", lead=None, center=False, tag="h2", title_id=None):
    eb = f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else ""
    ld = f'<p class="lead">{lead}</p>' if lead else ""
    tid = f' id="{title_id}"' if title_id else ""
    return f'<div class="section-head{" center" if center else ""} reveal">{eb}<{tag}{tid}>{title}</{tag}>{ld}</div>'


def bg_hero_deco(particles=False):
    parts = '<div class="bg-particles" aria-hidden="true">' + "<span></span>" * 6 + "</div>" if particles else ""
    lines = ('<svg class="bg-lines" aria-hidden="true" preserveAspectRatio="none" viewBox="0 0 1440 800">'
             '<path d="M0 620 H380 L460 540 H900" stroke="rgba(255,255,255,.10)" fill="none"/>'
             '<path d="M1440 180 H1120 L1060 240 H760" stroke="rgba(255,255,255,.08)" fill="none"/>'
             '<circle cx="900" cy="540" r="3" fill="rgba(143,176,247,.7)"/><circle cx="760" cy="240" r="3" fill="rgba(143,176,247,.6)"/></svg>')
    return (f'<div class="bg-grid" aria-hidden="true"></div><div class="bg-dots" aria-hidden="true"></div>'
            f'<div class="bg-circle c1" aria-hidden="true"></div><div class="bg-circle c2" aria-hidden="true"></div>{lines}{parts}')


def light_deco():
    """Light hero backdrop: procurement grid, soft orbs and a faint node path."""
    path = ('<svg class="hero-path" viewBox="0 0 600 300" aria-hidden="true" preserveAspectRatio="xMaxYMin meet">'
            '<path d="M20 60 H260 C320 60 320 200 380 200 H580" pathLength="1"/>'
            '<circle cx="20" cy="60" r="5"/><circle cx="140" cy="60" r="5"/><circle cx="260" cy="60" r="5"/>'
            '<circle cx="380" cy="200" r="5"/><circle cx="480" cy="200" r="5"/><circle class="hp-end" cx="580" cy="200" r="7"/></svg>')
    return ('<div class="hero-bg" aria-hidden="true"><div class="hero-grid-bg"></div><div class="hero-orb o1"></div>'
            f'<div class="hero-orb o2"></div></div>{path}')


def breadcrumbs(items):
    """items: list of (label, href or None). Home is prepended."""
    lis = [f'<li><a href="{L("index.html")}">Home</a></li>']
    for label, href in items:
        if href:
            lis.append(f'<li><a href="{L(href)}">{esc(label)}</a></li>')
        elif href == "":
            lis.append(f'<li><span>{esc(label)}</span></li>')
        else:
            lis.append(f'<li><span aria-current="page">{esc(label)}</span></li>')
    return f'<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>{"".join(lis)}</ol></nav>'


def page_hero(crumbs, eyebrow, title, lead, actions="", visual="", badges="", compact=False, bg=None):
    grid_cls = "page-hero-grid" + ("" if visual else " single")
    vis = f'<div class="page-hero-visual reveal-frame">{visual}</div>' if visual else ""
    bdg = f'<div class="hero-badges">{badges}</div>' if badges else ""
    act = f'<div class="btn-row">{actions}</div>' if actions else ""
    # bg: a photo from assets/images/photos/, faded to white behind the copy
    deco = (f'<div class="page-hero-bg" aria-hidden="true">{photo(bg, cls="page-hero-img", w=1600, h=1067, eager=True)}'
            f'<span class="page-hero-shade"></span></div>') if bg else light_deco()
    cls = "page-hero" + (" page-hero-compact" if compact else "") + (" page-hero-photo" if bg else "")
    return (
        f'<section class="{cls}">{deco}'
        f'<div class="container">{breadcrumbs(crumbs)}'
        f'<div class="{grid_cls}"><div class="page-hero-copy reveal">{bdg}<p class="eyebrow">{eyebrow}</p>'
        f'<h1>{title}</h1><p class="lead">{lead}</p>{act}</div>{vis}</div></div></section>'
    )


def btn_demo(label="Contact Us", cls="btn-primary btn-lg", interest=None):
    q = f'?interest={quote(interest)}' if interest else ""
    return f'<a class="btn {cls}" href="{L("contact.html")}{q}">{label} {icon("arrow-right", "icon icon-arrow")}</a>'


def photo(name, alt="", cls="photo", w=1600, h=1067, eager=False):
    """Site photography from assets/images/photos/. A missing file removes
    itself so the container's own background/artwork shows instead."""
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img class="{cls}" src="{L("assets/images/photos/" + name + ".jpg")}" alt="{esc(alt)}" '
            f'width="{w}" height="{h}" {load} decoding="async" onerror="this.remove()">')


def photo_frame(name, alt, extra=""):
    """A rounded photo panel used as a page-hero visual."""
    return f'<figure class="photo-frame">{photo(name, alt, eager=True)}{extra}</figure>'


def btn_link(href, label, cls="btn-secondary btn-lg", ic=None):
    i = icon(ic) if ic else ""
    return f'<a class="btn {cls}" href="{L(href)}">{i}{label}</a>'


def hero_actions(secondary=("how-it-works.html", "See how it works"), interest=None):
    return btn_demo("Contact Us", "btn-primary btn-lg magnetic", interest) + btn_link(secondary[0], secondary[1], "btn-secondary btn-lg")


def feature_cards(items, cols=3, cls="card card-hover feature-card"):
    """items: list of dicts {icon, title, text, status?, href?}"""
    out = []
    for i, it in enumerate(items):
        st = badge(it.get("status")) if it.get("status") else ""
        head = f'<div class="card-head">{icon_tile(it["icon"])}{st}</div>' if st else icon_tile(it["icon"])
        link = f'<a class="link-arrow" href="{L(it["href"])}">{it.get("cta", "Explore")} {icon("arrow-right")}</a>' if it.get("href") else ""
        out.append(f'<article class="{cls} reveal" style="--d:{i % cols}">{head}<h3>{it["title"]}</h3><p>{it["text"]}</p>{link}</article>')
    return f'<div class="grid grid-{cols}">{"".join(out)}</div>'


def workflow(steps):
    """steps: list of (icon, title, text)"""
    lis = "".join(
        f'<li class="wf-step reveal" style="--d:{i}"><div class="wf-icon">{icon(ic)}</div><div><h4>{t}</h4><p>{d}</p></div></li>'
        for i, (ic, t, d) in enumerate(steps))
    return f'<ol class="workflow" style="--steps:{len(steps)}">{lis}</ol>'


def flow(items):
    lis = "".join(f'<li><span class="flow-pill">{icon(ic)}{t}</span>{icon("arrow-right", "flow-arrow")}</li>' for ic, t in items)
    return f'<ol class="flow">{lis}</ol>'


def benefits(items):
    """items: list of (icon, title, text)"""
    mod = " benefits-3" if len(items) == 3 else ""
    return f'<div class="benefits{mod} reveal">' + "".join(
        f'<div class="benefit">{icon(ic)}<h3>{t}</h3><p>{d}</p></div>' for ic, t, d in items) + '</div>'


def challenge_list(items):
    return '<ul class="challenge-list">' + "".join(
        f'<li class="reveal" style="--d:{i}"><span class="x">{icon("x")}</span><div><strong>{t}</strong><span>{d}</span></div></li>'
        for i, (t, d) in enumerate(items)) + '</ul>'


def check_list(items):
    return '<ul class="feature-list">' + "".join(f'<li>{icon("check-circle")}<span>{t}</span></li>' for t in items) + '</ul>'


def related(files, title="Related capabilities"):
    cards = []
    for f in files:
        if f in PLATFORM_BY_FILE:
            _, n, d, ic, st = PLATFORM_BY_FILE[f]
        else:
            lookup = {r[0]: (r[1], r[2], r[3]) for r in ROLES + SOFTWARE + SERVICES + COMPANY + KNOWLEDGE + TOOLS}
            lookup.update({x[0]: (x[1], "Industry solution", x[2]) for x in INDUSTRIES})
            extra = {
                "categories.html": ("Categories", "Every category in one catalogue", "grid"),
                "how-it-works.html": ("How It Works", "Live in three steps", "route"),
                "engagement-models.html": ("Procurement Services", "Platform SaaS or Managed Procurement", "briefcase"),
            }
            lookup.update(extra)
            n, d, ic = lookup[f]
            st = None
        cards.append(f'<a class="related-card reveal" href="{L(f)}">{icon_tile(ic)}<div><h3>{esc(n)} {badge(st)}</h3><p>{esc(d)}</p></div></a>')
    return (f'<section class="section section-light section-tight"><div class="container">'
            f'<div class="section-head-row"><div class="section-head reveal"><p class="eyebrow">Keep exploring</p><h2>{title}</h2></div>'
            f'<a class="link-arrow reveal" href="{L("platform.html")}">Platform overview {icon("arrow-right")}</a></div>'
            f'<div class="related-grid">{"".join(cards)}</div></div></section>')


def status_legend():
    return ('<ul class="status-legend">'
            f'<li>{badge("early")} Available to selected clients</li>'
            f'<li>{badge("roadmap")} Planned</li>'
            '<li>No badge = live today</li></ul>')


# ---------------------------------------------------------------------------
# Structured data (page shell lives in chrome.py)
# ---------------------------------------------------------------------------
ORG_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "ProcEaze",
    "url": BASE_URL + "/",
    "logo": BASE_URL + "/assets/logo/proceaze-logo-full.png",
    "slogan": "Procurement, under one view.",
    "description": "B2B procurement intelligence and e-procurement platform for industrial, MRO and indirect procurement in India.",
}

SOFTWARE_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "ProcEaze",
    "applicationCategory": "BusinessApplication",
    "applicationSubCategory": "E-procurement software",
    "operatingSystem": "Web",
    "url": BASE_URL + "/",
    "description": "Procurement, under one view: a B2B procurement workspace with 5,00,000+ products, ARC-locked pricing, configurable approvals, reverse auctions and AI price negotiation.",
    "publisher": {"@type": "Organization", "name": "ProcEaze"},
}
