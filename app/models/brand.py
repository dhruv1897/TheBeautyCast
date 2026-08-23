"""
Brand enquiry table.

Filled in when a brand requests a creator shortlist or a UGC package.
"""

from datetime import datetime, timezone

from app.extensions import db


class BrandEnquiry(db.Model):
    __tablename__ = "brand_enquiries"

    id = db.Column(db.Integer, primary_key=True)

    brand_name = db.Column(db.String(160), nullable=False)
    contact_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), nullable=False, index=True)
    website = db.Column(db.String(200))

    product = db.Column(db.Text)              # what they want promoted
    package = db.Column(db.String(60))        # which package they clicked
    budget = db.Column(db.String(60))
    timeline = db.Column(db.String(120))
    message = db.Column(db.Text)

    status = db.Column(db.String(40), default="New", nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self) -> str:
        return f"<BrandEnquiry {self.brand_name}>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "brand_name": self.brand_name,
            "contact_name": self.contact_name,
            "email": self.email,
            "website": self.website or "",
            "product": self.product or "",
            "package": self.package or "",
            "budget": self.budget or "",
            "timeline": self.timeline or "",
            "message": self.message or "",
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
        }
