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

Then open http://127.0.0.1:5001. The flow is: register → log in → **acknowledge
the terms** (a required gate stating this is not legal advice and unreviewed) →
questionnaire → advice + draft documents → download all as a ZIP.

**Privacy by design:** estate-planning inputs (names, passport numbers,
beneficiaries, asset values) are processed in memory per request and are **never
written to disk or stored server-side**. The only persisted data is account
credentials (hashed) and a terms-acknowledgment timestamp, in a gitignored
`users.json`. The download re-posts your own form data rather than reading it from
the server.

Set these environment variables in any real deployment:

- `ESTATE_SECRET_KEY` — Flask session signing key (required; the default is for dev only).
- `ESTATE_USER_STORE` — path to the credentials file (point at a writable volume).

### CLI

The same logic is also available as an interactive command-line questionnaire:

```bash
python3 -m estate_planning.cli
```

It prints tailored advice (dual-will strategy, land/condo restrictions for foreign
heirs, unregistered marriage, overseas executor, inheritance-tax estimate) and
writes bilingual draft documents (Last Will, Living Will, Medical POA, Asset
Inventory) to `output/<name>_<timestamp>/`.

`output/` is gitignored since drafts contain personal information — nothing there
is committed.

## Project layout

- `estate-planning-thailand.md` — the source reference doc (law, forms, checklist).
- `estate_planning/models.py` — shared data model (`EstatePlan`, `Beneficiary`, `Witness`).
- `estate_planning/advice.py` — rules engine that turns a profile into warnings/recommendations/tax estimates.
- `estate_planning/documents.py` — bilingual document renderers.
- `estate_planning/cli.py` — interactive questionnaire entry point.
- `estate_planning/web/` — Flask web app (`app.py` routes, `forms.py` form→plan parsing, `store.py` credential store, `templates/`, `static/`).
- `tests/` — unit tests for the rules engine and web form parsing (`python3 -m unittest discover -s tests`).

## Sync

This folder is also linked as an Obsidian note folder at `AI Projects/Estate Planning`
(symlinked to this repo).
