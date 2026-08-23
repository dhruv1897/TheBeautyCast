"""
Creator table.

Every creator who applies through the site lands here. These columns
deliberately match the Airtable schema in the business plan, so the two
can be kept in sync or migrated later.
"""

from datetime import datetime, timezone

from app.extensions import db


class Creator(db.Model):
    __tablename__ = "creators"

    id = db.Column(db.Integer, primary_key=True)

    # Who they are
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), nullable=False, index=True)
    instagram = db.Column(db.String(80), nullable=False)
    tiktok = db.Column(db.String(80))
    location = db.Column(db.String(120))

    # What they make
    niche = db.Column(db.String(40))          # Nails / Makeup / Skincare / Hair / Hacks
    followers = db.Column(db.Integer)
    content_type = db.Column(db.String(120))  # e.g. "tutorials, GRWM"
    typical_rate = db.Column(db.String(60))   # kept as text: people type "$150-200"

    # The two answers that actually matter commercially
    permission_to_feature = db.Column(db.Boolean, default=False, nullable=False)
    open_to_paid_work = db.Column(db.Boolean, default=False, nullable=False)

    # Internal pipeline tracking
    status = db.Column(db.String(40), default="New", nullable=False)
    notes = db.Column(db.Text)
    source = db.Column(db.String(60), default="website")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self) -> str:
        return f"<Creator {self.instagram}>"

    def to_dict(self) -> dict:
        """Used by the CSV export in app/controllers/leads.py."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "instagram": self.instagram,
            "tiktok": self.tiktok or "",
            "location": self.location or "",
            "niche": self.niche or "",
            "followers": self.followers or "",
            "content_type": self.content_type or "",
            "typical_rate": self.typical_rate or "",
            "permission_to_feature": "yes" if self.permission_to_feature else "no",
            "open_to_paid_work": "yes" if self.open_to_paid_work else "no",
            "status": self.status,
            "source": self.source,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
        }
