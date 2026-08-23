"""
Basic tests. Run them with:  pytest

These check the site loads and the forms save data. Add a test whenever
you add a page — it takes two minutes and saves hours later.
"""

import pytest

from app import create_app
from app.extensions import db
from app.models import BrandEnquiry, Creator


@pytest.fixture
def client():
    app = create_app("testing")
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


def test_landing_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"The Beauty Cast" in response.data


def test_all_public_pages_load(client):
    for path in ["/", "/apply", "/brands", "/usage-rights", "/health"]:
        assert client.get(path).status_code == 200


def test_unknown_page_returns_404(client):
    assert client.get("/no-such-page").status_code == 404


def test_creator_application_is_saved(client):
    response = client.post("/apply", data={
        "name": "Maya R",
        "email": "maya@example.com",
        "instagram": "@mayadoesnails",
        "niche": "Nails",
        "followers": "8400",
        "permission_to_feature": "yes",
        "open_to_paid_work": "yes",
    }, follow_redirects=True)

    assert response.status_code == 200
    creator = Creator.query.filter_by(email="maya@example.com").first()
    assert creator is not None
    assert creator.instagram == "mayadoesnails"   # the @ is stripped
    assert creator.open_to_paid_work is True


def test_creator_application_needs_an_email(client):
    client.post("/apply", data={"name": "No Email", "instagram": "@x"})
    assert Creator.query.count() == 0


def test_brand_enquiry_is_saved(client):
    client.post("/brands", data={
        "brand_name": "Glow Co",
        "contact_name": "Sam",
        "email": "sam@glow.example",
        "product": "Vitamin C serum",
        "package": "Test Pack",
    }, follow_redirects=True)

    enquiry = BrandEnquiry.query.filter_by(email="sam@glow.example").first()
    assert enquiry is not None
    assert enquiry.package == "Test Pack"


def test_export_is_locked_without_token(client):
    assert client.get("/export/creators").status_code == 403
