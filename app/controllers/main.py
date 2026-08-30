"""
Public pages.

Add a new page by copying one of these functions and creating a matching
template in app/templates/.
"""

from datetime import datetime

from flask import Blueprint, Response, abort, render_template, url_for

from app.services import get_guide, load_content, load_guides, related_guides

main_bp = Blueprint("main", __name__)


@main_bp.app_context_processor
def inject_globals():
    """Make `site` and `current_year` available in every template."""
    return {
        "site": load_content(),
        "current_year": datetime.now().year,
        "guides": load_guides(),
    }


@main_bp.route("/")
def index():
    """The landing page."""
    return render_template("index.html")


@main_bp.route("/apply")
def apply_page():
    """Creator application form."""
    return render_template("apply.html")


@main_bp.route("/brands")
def brands_page():
    """Brand enquiry form."""
    return render_template("brands.html")


@main_bp.route("/usage-rights")
def usage_rights():
    """Plain-language content permission and privacy page."""
    return render_template("usage_rights.html")


# ---------------------------------------------------------------------
# The Beauty Room — public guides. This is the SEO engine: each guide is
# its own page with its own URL, title and structured data.
# ---------------------------------------------------------------------
@main_bp.route("/beauty-room")
def beauty_room():
    """Index of every guide."""
    return render_template("beauty_room.html", guides=load_guides())


@main_bp.route("/beauty-room/<slug>")
def guide(slug: str):
    """A single guide page."""
    item = get_guide(slug)
    if item is None:
        abort(404)
    return render_template("guide.html", guide=item, related=related_guides(item))


@main_bp.route("/sitemap.xml")
def sitemap():
    """Lists every page so search engines can find the guides."""
    pages = [
        (url_for("main.index", _external=True), "1.0"),
        (url_for("main.beauty_room", _external=True), "0.9"),
        (url_for("main.apply_page", _external=True), "0.8"),
        (url_for("main.brands_page", _external=True), "0.8"),
        (url_for("main.usage_rights", _external=True), "0.3"),
    ]
    entries = "".join(
        f"<url><loc>{loc}</loc><priority>{pri}</priority></url>" for loc, pri in pages
    )
    for item in load_guides():
        loc = url_for("main.guide", slug=item["slug"], _external=True)
        entries += (
            f"<url><loc>{loc}</loc>"
            f"<lastmod>{item.get('updated', '')}</lastmod>"
            f"<priority>0.7</priority></url>"
        )

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{entries}</urlset>"
    )
    return Response(xml, mimetype="application/xml")


@main_bp.route("/robots.txt")
def robots():
    """Tells search engines what to crawl and where the sitemap is."""
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /export/",
        f"Sitemap: {url_for('main.sitemap', _external=True)}",
    ]
    return Response("\n".join(lines), mimetype="text/plain")


@main_bp.route("/health")
def health():
    """Used by hosting platforms to check the site is alive."""
    return {"status": "ok"}, 200
