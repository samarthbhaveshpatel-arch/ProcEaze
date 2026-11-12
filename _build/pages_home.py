"""Home page — a short story: control plane → numbers → categories → offer → people.
Each deep-dive section (lifecycle, ARC, approvals, dashboards, auctions, AI, trust…) lives on its own page only.
"""
from lib import SOFTWARE_SCHEMA, SOFTWARE, SERVICES, L, esc, icon_tile, section_head
import signature as S


def offer_section(cls="section section-light"):
    """Entry points into the Software Solutions and Procurement Services pages."""
    def cards(items):
        return "".join(f'<a class="related-card reveal" href="{L(f)}">{icon_tile(ic)}<div><h3>{esc(n)}</h3><p>{esc(d)}</p></div></a>'
                       for f, n, d, ic in items)
    return (f'<section class="{cls}"><div class="container">'
            + section_head("Procurement software", "Procurement software and services, on one platform.",
                           "Run procurement on ProcEaze with your own vendors, or let ProcEaze supply for you.")
            + f'<div class="related-grid">{cards(SOFTWARE)}</div>'
            + f'<div class="mt-48">{section_head("Procurement services", "Prefer us to run it with you?", None)}</div>'
            + f'<div class="related-grid">{cards(SERVICES)}</div></div></section>')


def body():
    return (
        S.hero()                                          # THE CONTROL PLANE
        + S.chaos_section()                               # ONE CONNECTED PLATFORM
        + S.photo_band()                                  # SCALE, IN NUMBERS
        + S.categories_section("section section-light")   # WHAT YOU CAN BUY
        + offer_section("section")                        # SOFTWARE + SERVICES
        + S.kam_section("section section-light")          # PEOPLE
    )


PAGES = [dict(
    path="index.html",
    title="Procurement Software for Enterprises in India | ProcEaze",
    desc="ProcEaze is procurement software for Indian enterprises: one catalogue at ARC prices, 1–5 level approvals, purchase orders and live spend analytics.",
    section="home",
    crumbs=None,
    schemas=[SOFTWARE_SCHEMA],
    body=body,
)]
