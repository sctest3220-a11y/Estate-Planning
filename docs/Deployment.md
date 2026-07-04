# Deployment

Hosting the web app for multiple users. See [[Development]] for local runs and
[[Architecture]] for structure.

## Environment variables

- `ESTATE_SECRET_KEY` — Flask session signing key. **Required in production**; the
  default is for development only.
- `ESTATE_USER_STORE` — path to the credentials file; point at a writable volume.
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` — enable **Sign in with Google**. If
  unset, the Google button is hidden and local accounts still work.

## Google sign-in setup

In [Google Cloud Console](https://console.cloud.google.com/) → APIs & Services →
Credentials, create an **OAuth 2.0 Client ID** (type: Web application). Add your
callback to *Authorized redirect URIs*:

- Local: `http://127.0.0.1:5001/auth/google/callback`
- Production: `https://your-domain/auth/google/callback`

Configure the OAuth consent screen, then set `GOOGLE_CLIENT_ID` /
`GOOGLE_CLIENT_SECRET`.

## Production server

The Flask dev server is not for production. Run behind a WSGI server, e.g.:

```bash
./.venv/bin/pip install gunicorn
ESTATE_SECRET_KEY=... gunicorn "estate_planning.web.app:app" -b 0.0.0.0:8000
```

Put it behind HTTPS (a reverse proxy or platform TLS). See [[User Guide]] for what
users experience.

## Privacy note

Only account credentials (hashed) and a terms-acknowledgment timestamp are
persisted. Estate data is processed in memory per request and never written to
disk. Keep it that way — do not add server-side storage of questionnaire input
without revisiting the [[Disclaimer]] and privacy commitments.

## Still open

Hosting choice, HTTPS/domain, and whether to require login for everyone are open
decisions — track them with the project's task list.
