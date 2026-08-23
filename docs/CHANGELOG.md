# Changelog

Record every meaningful change here. Newest at the top.

## [0.1.0] — 2026-08-22

Initial build.

### Added
- Flask application factory with development / production / testing configs
- Landing page: hero, weekly cast rail, two doors, packages, submit section
- Creator application form saving to the `creators` table
- Brand enquiry form saving to the `brand_enquiries` table
- Token-protected CSV export at `/export/creators` and `/export/brands`
- Usage rights and privacy page
- 404 and 500 error pages
- All page copy externalised to `app/content/site.json`
- Design tokens at the top of `style.css` for one-line rebranding
- Test suite covering page loads, form saving, validation and export locking
