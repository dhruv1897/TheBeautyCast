"""
Public pages.

Add a new page by copying one of these functions and creating a matching
template in app/templates/.
"""

from datetime import datetime

from flask import Blueprint, render_template

from app.services import load_content

main_bp = Blueprint("main", __name__)


@main_bp.app_context_processor
def inject_globals():
    """Make `site` and `current_year` available in every template."""
    return {
        "site": load_content(),
        "current_year": datetime.now().year,
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


@main_bp.route("/health")
def health():
    """Used by hosting platforms to check the site is alive."""
    return {"status": "ok"}, 200
