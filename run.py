"""
Development entry point.

Run the site locally with:
    python run.py

Then open http://127.0.0.1:5000 in your browser.

In production a WSGI server runs `app` from this file instead
(see Procfile).
"""

import os

from app import create_app

app = create_app(os.environ.get("FLASK_ENV", "development"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
