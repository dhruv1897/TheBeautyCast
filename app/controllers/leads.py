"""
Form submissions and data export.

Creator applications and brand enquiries are saved to the database here.
There is also a CSV export so you can pull everything into Google Sheets
or Airtable without touching the database directly.
"""

import csv
import io
import os

from flask import (
    Blueprint,
    Response,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from app.extensions import db
from app.models import BrandEnquiry, Creator
from app.services import as_int, clean

leads_bp = Blueprint("leads", __name__)


# ---------------------------------------------------------------------
# Creator application
# ---------------------------------------------------------------------
@leads_bp.route("/apply", methods=["POST"])
def submit_creator():
    """Save a creator application."""
    name = clean(request.form.get("name"), 120)
    email = clean(request.form.get("email"), 200)
    instagram = clean(request.form.get("instagram"), 80)

    # Minimum viable validation. If these three are missing we cannot
    # do anything useful with the submission.
    if not name or not email or not instagram:
        flash("Please fill in your name, email and Instagram handle.", "error")
        return redirect(url_for("main.apply_page"))

    if "@" not in email or "." not in email.split("@")[-1]:
        flash("That email address does not look right.", "error")
        return redirect(url_for("main.apply_page"))

    creator = Creator(
        name=name,
        email=email.lower(),
        instagram=instagram.lstrip("@"),
        tiktok=clean(request.form.get("tiktok"), 80).lstrip("@"),
        location=clean(request.form.get("location"), 120),
        niche=clean(request.form.get("niche"), 40),
        followers=as_int(request.form.get("followers")),
        content_type=clean(request.form.get("content_type"), 120),
        typical_rate=clean(request.form.get("typical_rate"), 60),
        permission_to_feature=request.form.get("permission_to_feature") == "yes",
        open_to_paid_work=request.form.get("open_to_paid_work") == "yes",
        notes=clean(request.form.get("notes"), 2000),
    )

    db.session.add(creator)
    db.session.commit()

    return redirect(url_for("leads.thanks", who="creator"))


# ---------------------------------------------------------------------
# Brand enquiry
# ---------------------------------------------------------------------
@leads_bp.route("/brands", methods=["POST"])
def submit_brand():
    """Save a brand enquiry."""
    brand_name = clean(request.form.get("brand_name"), 160)
    contact_name = clean(request.form.get("contact_name"), 120)
    email = clean(request.form.get("email"), 200)

    if not brand_name or not contact_name or not email:
        flash("Please fill in your brand, your name and your email.", "error")
        return redirect(url_for("main.brands_page"))

    if "@" not in email or "." not in email.split("@")[-1]:
        flash("That email address does not look right.", "error")
        return redirect(url_for("main.brands_page"))

    enquiry = BrandEnquiry(
        brand_name=brand_name,
        contact_name=contact_name,
        email=email.lower(),
        website=clean(request.form.get("website"), 200),
        product=clean(request.form.get("product"), 2000),
        package=clean(request.form.get("package"), 60),
        budget=clean(request.form.get("budget"), 60),
        timeline=clean(request.form.get("timeline"), 120),
        message=clean(request.form.get("message"), 2000),
    )

    db.session.add(enquiry)
    db.session.commit()

    return redirect(url_for("leads.thanks", who="brand"))


# ---------------------------------------------------------------------
# Thank you page
# ---------------------------------------------------------------------
@leads_bp.route("/thanks/<who>")
def thanks(who: str):
    if who not in {"creator", "brand"}:
        abort(404)
    return render_template("thanks.html", who=who)


# ---------------------------------------------------------------------
# CSV export
# ---------------------------------------------------------------------
@leads_bp.route("/export/<table>")
def export(table: str):
    """Download creators or brand enquiries as a CSV file.

    Protected by a token so the URL is not public. Set EXPORT_TOKEN in
    your .env file, then visit:
        /export/creators?token=YOUR_TOKEN

    This is deliberately simple. When you have real volume, replace it
    with a proper admin login.
    """
    expected = os.environ.get("EXPORT_TOKEN")
    if not expected or request.args.get("token") != expected:
        abort(403)

    if table == "creators":
        rows = [c.to_dict() for c in Creator.query.order_by(Creator.created_at.desc())]
    elif table == "brands":
        rows = [
            b.to_dict()
            for b in BrandEnquiry.query.order_by(BrandEnquiry.created_at.desc())
        ]
    else:
        abort(404)

    if not rows:
        return Response("No records yet.", mimetype="text/plain")

    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

    return Response(
        buffer.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={table}.csv"},
    )
