# The Beauty Cast

Beauty creator discovery and content production. This repository holds the
public website: a landing page, a creator application form, and a brand
enquiry form.

Built with Flask (Python), plain HTML and CSS. No build step, no npm, no
JavaScript framework. Clone it, install five packages, and it runs.

---

## Quick start

```bash
# 1. Clone
git clone https://github.com/dhruv1897/thebeautycast.git
cd thebeautycast

# 2. Create a virtual environment
python -m venv .venv

#    Windows
.venv\Scripts\activate
#    Mac / Linux
source .venv/bin/activate

# 3. Install
pip install -r requirements.txt

# 4. Set up your environment file
copy .env.example .env        # Windows
cp .env.example .env          # Mac / Linux
#    Open .env and set SECRET_KEY to a long random string.
#    Generate one: python -c "import secrets; print(secrets.token_hex(32))"

# 5. Run
python run.py
```

Open <http://127.0.0.1:5000>.

The database creates itself on first run at `instance/thebeautycast.db`.

---

## Project structure

```
thebeautycast/
│
├── run.py                  Start the site locally
├── requirements.txt        Python packages (pinned versions)
├── Procfile                Tells a host how to run the site
├── .env.example            Template for your secrets file
├── .gitignore              What git should never upload
│
├── app/
│   ├── __init__.py         Application factory — wires everything together
│   ├── config.py           Settings for development / production / testing
│   ├── extensions.py       Shared database and CSRF objects
│   ├── services.py         Shared helper functions
│   │
│   ├── content/
│   │   └── site.json       *** ALL WEBSITE TEXT LIVES HERE ***
│   │
│   ├── models/             DATA  — database tables
│   │   ├── creator.py      Creator applications
│   │   └── brand.py        Brand enquiries
│   │
│   ├── controllers/        LOGIC — what happens at each URL
│   │   ├── main.py         Public pages
│   │   └── leads.py        Form handling and CSV export
│   │
│   ├── templates/          VIEW  — the HTML
│   │   ├── base.html       Shared layout every page extends
│   │   ├── index.html      The landing page
│   │   ├── apply.html      Creator form
│   │   ├── brands.html     Brand form
│   │   ├── thanks.html     Confirmation page
│   │   ├── usage_rights.html
│   │   ├── 404.html / 500.html
│   │   └── partials/       Reusable chunks (header, footer, creator card)
│   │
│   └── static/
│       ├── css/style.css   All styling. Design tokens at the top.
│       ├── js/main.js      Small conveniences only
│       └── img/            Put creator photos here
│
├── tests/
│   └── test_pages.py       Run with: pytest
│
└── docs/
    └── CHANGELOG.md        Record of what changed and when
```

**Model–View–Controller, in this project:**

| Layer | Where | What it does |
|---|---|---|
| Model | `app/models/` | Defines the database tables |
| View | `app/templates/` | The HTML the visitor sees |
| Controller | `app/controllers/` | Decides what happens at each URL |

Keep controllers thin. If a function grows past about 30 lines, move the
logic into `app/services.py`.

---

## Everyday jobs

### Change the words on the site

Edit **`app/content/site.json`**. Save, refresh the browser. No HTML needed.
Keep the quotes and commas exactly as they are — if the site errors after an
edit, you have almost certainly dropped a comma.

### Change the colours

Edit the `:root` block at the top of **`app/static/css/style.css`**:

```css
--ink:    #1A1720;   /* dark sections and text */
--paper:  #FAF8F6;   /* page background */
--accent: #8C2F4A;   /* buttons and highlights */
```

Change `--accent` and every button on the site changes with it.

### Add a real creator photo

1. Save the image into `app/static/img/` (for example `maya.jpg`)
2. Add `"photo": "maya.jpg"` to that creator in `site.json`
3. In `app/templates/partials/creator_card.html`, swap the placeholder
   `<svg>` for the `<img>` tag shown in the comment at the top of that file

Crop images to 4:5 and keep them under 200 KB.

### Add a new page

1. Create `app/templates/about.html` starting with `{% extends "base.html" %}`
2. Add a route in `app/controllers/main.py`:

```python
@main_bp.route("/about")
def about():
    return render_template("about.html")
```

3. Add a test in `tests/test_pages.py`

### Download your leads

Set `EXPORT_TOKEN` in `.env`, then visit:

```
/export/creators?token=YOUR_TOKEN
/export/brands?token=YOUR_TOKEN
```

You get a CSV you can open in Google Sheets or import into Airtable.

---

## Testing

```bash
pytest          # run everything
pytest -v       # show each test name
```

Run the tests before every push. They take under a second.

---

## Git workflow

Work on a branch, never straight on `main`:

```bash
git checkout -b feature/creator-photos
# ... make changes ...
pytest
git add .
git commit -m "Add real creator photos to the cast rail"
git push origin feature/creator-photos
```

Then open a pull request on GitHub and merge it.

**Commit message style:** start with a verb, say what changed and why.
Good: `Add CSV export for brand enquiries`.
Bad: `update`, `fix stuff`, `changes`.

---

## Deploying

The site is ready for any Python host. Render is the simplest free option.

1. Push this repository to GitHub
2. On Render, create a **New Web Service** and connect the repo
3. Settings:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn "run:app"`
4. Add environment variables: `SECRET_KEY`, `FLASK_ENV=production`,
   `EXPORT_TOKEN`
5. Point your domain at the URL Render gives you

**Important for production:** SQLite is fine for the first few months, but
it resets on some hosts when they restart. Once you have real leads coming
in, add a free Postgres database and paste its URL into `DATABASE_URL`.
The code already handles the switch — you do not need to change anything.

---

## Roadmap

Built:

- [x] Landing page
- [x] Creator application form saving to a database
- [x] Brand enquiry form
- [x] CSV export
- [x] Usage rights page
- [x] Tests

Next, roughly in order of business value:

- [ ] Email notification when a form is submitted
- [ ] Public creator roster page, filterable by niche
- [ ] Case study page (build it the day the first campaign finishes)
- [ ] Admin login to replace the token-protected CSV export
- [ ] Analytics

Do not build the admin panel before you have your first paying brand.

---

## Conventions

- Python formatted with `black`, 4-space indent
- Templates use 2-space indent
- CSS class names follow `block__element--modifier`
- Never commit `.env` or anything in `instance/`
- One change per commit
