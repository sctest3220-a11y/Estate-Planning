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

The Flask dev server is not for production. The repo ships deployment artifacts:

- **`Dockerfile`** — serves the app with gunicorn (binds `$PORT`, default 8000) and
  keeps credentials on a `/data` volume.
- **`render.yaml`** — Render Blueprint (Singapore region, persistent disk).
- **`fly.toml`** — Fly.io config (Singapore region, persistent volume).
- **`Procfile`** — for Heroku-style platforms.
- **`.env.example`** — copy to `.env` and fill in the variables above.

> **Why not Vercel/serverless?** This is a stateful app: it writes a small login
> store (`users.json`) to disk. Serverless filesystems are ephemeral, so accounts
> would reset on cold starts. A **container host with a persistent volume** is the
> right fit. All options below provide one.

### Persistence matters

The only thing persisted is the credential store. It must live on a **persistent
volume/disk** or accounts and terms-acknowledgments reset on redeploy. The configs
below mount one at `/data` (matching `ESTATE_USER_STORE=/data/users.json`).

### Option A — Render (blueprint)

1. Push this repo to GitHub (done).
2. In the Render dashboard: **New + → Blueprint**, connect the repo. Render reads
   `render.yaml`, provisions the web service + 1 GB disk, and generates
   `ESTATE_SECRET_KEY` automatically.
3. Deploy. Your URL is `https://<name>.onrender.com`.
4. (Optional) To enable Google sign-in, add `GOOGLE_CLIENT_ID` /
   `GOOGLE_CLIENT_SECRET` in the dashboard and the callback
   `https://<name>.onrender.com/auth/google/callback` in Google Cloud Console.

   *Note: the persistent disk requires the paid Starter plan. On the free plan
   there is no disk, so accounts reset on each redeploy — demo only.*

### Option B — Fly.io (CLI)

```bash
fly launch --copy-config --no-deploy      # pick an app name if "estate-planning" is taken
fly volumes create data --region sin --size 1
fly secrets set ESTATE_SECRET_KEY=$(openssl rand -hex 32)
fly deploy
# optional Google sign-in:
fly secrets set GOOGLE_CLIENT_ID=... GOOGLE_CLIENT_SECRET=...
# then add https://<app>.fly.dev/auth/google/callback in Google Cloud Console
```

### Option C — plain Docker (any VPS)

```bash
docker build -t estate-planning .
docker run -d -p 8000:8000 -e ESTATE_SECRET_KEY=$(openssl rand -hex 32) \
  -v estate-data:/data estate-planning
```

Put it behind HTTPS (platform TLS or a reverse proxy). See [[User Guide]] for the
user experience and [[Development]] for the test suite (run in CI via
`.github/workflows/tests.yml`).

## Privacy note

Only account credentials (hashed) and a terms-acknowledgment timestamp are
persisted. Estate data is processed in memory per request and never written to
disk. Keep it that way — do not add server-side storage of questionnaire input
without revisiting the [[Disclaimer]] and privacy commitments.

## Still open

Hosting choice, HTTPS/domain, and whether to require login for everyone are open
decisions — track them with the project's task list.
