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

## Get advice and generate documents

Requires Python 3.9+, no third-party dependencies.

```bash
python3 -m estate_planning.cli
```

The questionnaire asks about your status (Thai national / foreign resident /
occasional visitor), assets, marriage, executor, witnesses, and beneficiaries, then:

1. Prints tailored advice — warnings (e.g. dual-will strategy, land/condo
   restrictions for foreign heirs, unregistered marriage, overseas executor) and
   an estimated inheritance tax breakdown per beneficiary.
2. Drafts the documents you select (Last Will, Living Will / Advance Directive,
   Medical Power of Attorney, Asset Inventory) as bilingual Markdown files under
   `output/<name>_<timestamp>/`.

`output/` is gitignored since drafts contain personal information — nothing there
is committed.

## Project layout

- `estate-planning-thailand.md` — the source reference doc (law, forms, checklist).
- `estate_planning/models.py` — shared data model (`EstatePlan`, `Beneficiary`, `Witness`).
- `estate_planning/advice.py` — rules engine that turns a profile into warnings/recommendations/tax estimates.
- `estate_planning/documents.py` — bilingual document renderers.
- `estate_planning/cli.py` — interactive questionnaire entry point.
- `tests/test_advice.py` — unit tests for the rules engine (`python3 -m unittest discover -s tests`).

## Sync

This folder is also linked as an Obsidian note folder at `AI Projects/Estate Planning`
(symlinked to this repo).
