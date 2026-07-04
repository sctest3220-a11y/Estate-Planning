# Estate Planning — Thailand

Reference, rules-based advice engine, and document drafter for estate planning and
advance directives under Thai law: last will, living will, medical/financial power
of attorney, asset inventory, and inheritance tax.

> **Not legal advice.** This is an informational tool encoding publicly available
> statutory rules (Civil and Commercial Code, National Health Act B.E. 2550). It is
> not a substitute for a licensed Thai probate/estate lawyer. Every generated
> document is a **draft** — have it reviewed by a lawyer before signing or
> witnessing, and confirm the law hasn't changed since this was written.

See [estate-planning-thailand.md](estate-planning-thailand.md) for the full bilingual
(Thai/English) checklist and legal reference this tool is built from.

## Web app (multi-user)

A login-gated web front-end over the same advice/document logic.

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/python -m flask --app estate_planning.web.app run --port 5001
```

Then open http://127.0.0.1:5001. The flow is: log in (local account or Google) →
**acknowledge the terms** (a required gate stating this is not legal advice and
unreviewed) → questionnaire → advice + draft documents → download as a ZIP.

Features:

- **Choose documents** — generate any subset of Last Will, Living Will, Medical POA,
  and Asset Inventory, or all of them.
- **Context-aware questions** — the questionnaire only shows the questions relevant
  to the documents you selected (e.g. beneficiaries/executor appear only for a Will,
  the healthcare proxy only for a Medical POA). Hidden fields are disabled so stale
  answers are never submitted.
- **Choose document language** — English, Thai, or dual (English + Thai) output.
- **Interface language (TH / ENG)** — a separate toggle in the header translates the
  app UI itself into Thai or English.
- **Light / dark mode** — a header toggle; the choice is remembered (localStorage) and
  defaults to your system preference.
- **Preview blank templates** — see every document with `[placeholders]` at
  `/preview`, in any language, without entering any personal data.
- **Mandatory vs optional fields** — only full name and status are required; every
  other field is marked optional and can be left blank to fill in by hand.
- **Selectable living-will directives** — choose which specific instructions to
  include (DNR/no CPR, no mechanical ventilation, no tube feeding, no dialysis,
  palliative/comfort care, place-of-death preference, spiritual care) plus free-text
  wishes. Each is phrased within Thailand's Section 12 framework (terminal stage,
  passive refusal only — active euthanasia is illegal) and the UI + document carry a
  prominent note to confirm each directive with the hospital and a Thai lawyer.
- **Asset sheet** — itemize assets (category, description, value, location, notes)
  three ways: fill in online, or **download a CSV template** (`/asset-template.csv`)
  to complete offline in Excel/Sheets and **upload** it back. Assets flow into the
  Asset Inventory document (as a table with a total) and the tax estimate.
- **Inheritance tax planning** — estimates tax per beneficiary (only the excess over
  100M THB is taxed; 5% for descendants/ascendants, 10% for others; spouses exempt),
  shows total estate and total tax, and gives planning suggestions: inherited assets
  are exempt from personal income tax, distributing across beneficiaries (the 100M
  allowance is per person), routing through an exempt spouse, and lifetime gift-tax
  exemptions (20M/yr to lineal relatives or spouse, 10M/yr to others).
- **Works on web and mobile browsers** — fully responsive down to small phone widths.

**Privacy by design:** estate-planning inputs (names, passport numbers,
beneficiaries, asset values) are processed in memory per request and are **never
written to disk or stored server-side**. The only persisted data is account
credentials (hashed) and a terms-acknowledgment timestamp, in a gitignored
`users.json`. The download re-posts your own form data rather than reading it from
the server.

### Configuration (environment variables)

- `ESTATE_SECRET_KEY` — Flask session signing key (required in production; the default is dev-only).
- `ESTATE_USER_STORE` — path to the credentials file (point at a writable volume).
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` — enable "Sign in with Google". If unset,
  the Google button is hidden and local accounts still work.

**Setting up Google sign-in:** In [Google Cloud Console](https://console.cloud.google.com/)
→ APIs & Services → Credentials, create an **OAuth 2.0 Client ID** of type *Web
application*. Add your callback URL to *Authorized redirect URIs*
(`http://127.0.0.1:5001/auth/google/callback` for local dev, or
`https://your-domain/auth/google/callback` in production). Put the generated client ID
and secret in the two env vars above. Configure the OAuth consent screen as well.

### CLI

The same logic is also available as an interactive command-line questionnaire:

```bash
python3 -m estate_planning.cli
```

It prints tailored advice (dual-will strategy, land/condo restrictions for foreign
heirs, unregistered marriage, overseas executor, inheritance-tax estimate), lets you
choose which documents and which language (English / Thai / dual), and writes the
draft documents (Last Will, Living Will, Medical POA, Asset Inventory) to
`output/<name>_<timestamp>/`.

`output/` is gitignored since drafts contain personal information — nothing there
is committed.

## Project layout

- `estate-planning-thailand.md` — the source reference doc (law, forms, checklist).
- `estate_planning/models.py` — shared data model (`EstatePlan`, `Beneficiary`, `Witness`).
- `estate_planning/advice.py` — rules engine that turns a profile into warnings/recommendations/tax estimates.
- `estate_planning/documents.py` — bilingual document renderers.
- `estate_planning/documents.py` — language-aware (English/Thai/dual) document renderers + `generate()`.
- `estate_planning/tax.py` — inheritance & gift tax estimation and planning suggestions.
- `estate_planning/assets_csv.py` — asset-sheet CSV template generation and upload parsing.
- `estate_planning/sample.py` — placeholder plan used for the blank-template preview.
- `estate_planning/cli.py` — interactive questionnaire entry point.
- `estate_planning/web/` — Flask web app (`app.py` routes, `forms.py` form→plan parsing, `store.py` credential store, `google_auth.py` Google OAuth, `templates/`, `static/`).
- `tests/` — unit tests for the rules engine, document language modes, and web form parsing (`python3 -m unittest discover -s tests`).

## Sync

This folder is also linked as an Obsidian note folder at `AI Projects/Estate Planning`
(symlinked to this repo).
