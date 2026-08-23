"""
Controllers (Flask blueprints).

Each file here handles a group of URLs:
  main.py   - the public pages (landing page, usage rights, etc.)
  leads.py  - form submissions and the CSV export

Controllers should stay thin: read the request, talk to a model,
pick a template. Put reusable logic in app/services.py instead.
"""
