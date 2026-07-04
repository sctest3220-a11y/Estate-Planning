# Architecture

How the code is organized. See [[Development]] for running it and [[Home]] for the
overview.

## Core library (`estate_planning/`)

- `models.py` — dataclasses: `EstatePlan`, `Beneficiary`, `Witness`, `Asset`, plus
  status/relationship/asset-category constants.
- `advice.py` — the rules engine. `assess(plan)` → `Advice` (summary, warnings,
  recommendations, tax breakdown). Encodes the guidance in [[Thai Estate Law]].
- `tax.py` — inheritance & gift tax math and planning suggestions. See [[Inheritance Tax]].
- `tips.py` — general tips/reminders, some conditional on the plan. See [[Tips]].
- `bequests.py` — maps assets to beneficiaries by name and summarizes who gets what;
  supplies the effective per-beneficiary values used by `tax.py`.
- `documents.py` — language-aware document renderers (English / Thai / dual) via
  `_t()` / `_lbl()` helpers, `generate(plan, keys, mode)`, `DOCUMENT_SPECS`, and
  `LIVING_WILL_OPTIONS` (see [[Living Will Directives]]).
- `asset_schema.py` — per-category field definitions (labels + required flags).
- `asset_workbook.py` — multi-tab Excel template + upload parser for the [[Asset Sheet]].
- `assets_csv.py` — legacy flat-CSV template + parser (still accepted on upload).
- `sample.py` — a placeholder plan used for the blank-template preview.
- `cli.py` — interactive command-line questionnaire.

## Web app (`estate_planning/web/`)

- `app.py` — Flask routes, the login/terms gates, and the `urlize_links` filter.
- `forms.py` — turns submitted form data into a validated `EstatePlan`.
- `store.py` — file-backed user store (hashed passwords + acknowledgment only).
- `google_auth.py` — Google OAuth, gated on env vars (see [[Deployment]]).
- `i18n.py` — interface translations (English/Thai) for the app chrome.
- `templates/`, `static/` — Jinja templates and the stylesheet.

## Two cross-cutting ideas

**Context-aware form.** Each questionnaire section carries a `data-docs` attribute
listing the documents it applies to. Client-side JS hides sections whose documents
are unselected and disables their inputs so stale values are never submitted. A
CSS rule `[hidden] { display: none !important }` guarantees hidden sections truly
disappear (author styles would otherwise override the `hidden` attribute).

**Two "languages".** The *interface* language (`i18n.py`, header toggle) is
separate from the *document output* language (`documents.py`, questionnaire choice).

## Data flow

`questionnaire form → forms.build_plan() → EstatePlan → advice.assess() +
tax.tax_plan() + tips.planning_tips() + documents.generate() → results page →
download (ZIP)`. Nothing is persisted between requests.
