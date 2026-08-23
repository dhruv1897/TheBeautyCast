# Deployment checklist

Work through this before pointing the domain at the site.

## Before you deploy

- [ ] `pytest` passes
- [ ] `SECRET_KEY` in the host's environment variables is a long random string,
      NOT the default from `.env.example`
- [ ] `FLASK_ENV=production` is set
- [ ] `EXPORT_TOKEN` is set to something nobody could guess
- [ ] `.env` is not in the repository (check: `git ls-files | grep .env`
      should show only `.env.example`)
- [ ] Real contact email is set in `app/content/site.json`
- [ ] Stats in `site.json` show your true numbers, not the placeholders

## After you deploy

- [ ] Landing page loads over HTTPS
- [ ] Submit a test creator application, confirm it saves
- [ ] Submit a test brand enquiry, confirm it saves
- [ ] Download both CSV exports
- [ ] Open the site on a real phone and tap every button
- [ ] Delete the test records before launch

## Domain

Point these DNS records at your host:

```
A     @      <IP your host gives you>
CNAME www    <hostname your host gives you>
```

DNS can take up to 24 hours. Usually it is under an hour.
