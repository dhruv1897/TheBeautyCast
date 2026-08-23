"""
The Beauty Cast - Flask application factory.

This file builds the app. It does not contain page logic or HTML.
- Page logic lives in  app/controllers/
- HTML lives in        app/templates/
- Database tables in   app/models/
- Editable text in     app/content/site.json

To add a new page, create a route in app/controllers/main.py and a
template in app/templates/. You should not need to edit this file often.
"""

from flask import Flask, render_template

from app.config import get_config
from app.extensions import db, csrf


def create_app(config_name: str | None = None) -> Flask:
    """Build and return the Flask application.

    Args:
        config_name: "development", "production" or "testing".
                     Falls back to the FLASK_ENV environment variable.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(get_config(config_name))

    # Make sure the instance folder exists (SQLite lives there).
    import os
    os.makedirs(app.instance_path, exist_ok=True)

    # --- Extensions -------------------------------------------------
    db.init_app(app)
    csrf.init_app(app)

    # --- Controllers (blueprints) -----------------------------------
    from app.controllers.main import main_bp
    from app.controllers.leads import leads_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(leads_bp)

    # --- Error pages ------------------------------------------------
    @app.errorhandler(404)
    def not_found(_error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(_error):
        db.session.rollback()
        return render_template("500.html"), 500

    # --- Database ---------------------------------------------------
    with app.app_context():
        from app.models import creator, brand  # noqa: F401  (registers tables)
        db.create_all()

    return app
