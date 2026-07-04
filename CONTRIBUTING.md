# Contributing

Thanks for helping improve this Thailand estate-planning tool.

> **Reminder:** this project produces informational drafts, not legal advice. Any
> change to legal figures, document clauses, or advice text should be flagged for
> the pending lawyer review. See [docs/Disclaimer.md](docs/Disclaimer.md).

## Setup

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/python -m unittest discover -s tests
```

## Running

- Web app: `./.venv/bin/python -m flask --app estate_planning.web.app run --port 5001`
- CLI: `./.venv/bin/python -m estate_planning.cli`

## Guidelines

- **Tests required** — add or update tests under `tests/` for any behavior change.
  Run the full suite before opening a PR.
- **Legal accuracy** — when you touch a tax threshold, gift exemption, statutory
  reference, or document clause, update the relevant test and note the change in the
  PR so it can be verified by a lawyer.
- **Keep the disclaimer framing** on any user-facing legal text.
- **No secrets in git** — `users.json`, `.venv/`, and generated `output/` are
  gitignored; keep it that way.
- **Privacy** — do not add server-side persistence of questionnaire input. Estate
  data is processed in memory only.

## Docs

Deeper documentation lives in [`docs/`](docs/) and is written as an Obsidian vault
(cross-linked with `[[wikilinks]]`). Start at [docs/Home.md](docs/Home.md):

- [Architecture](docs/Architecture.md) — code map
- [Development](docs/Development.md) — setup, tests, conventions
- [Deployment](docs/Deployment.md) — hosting and Google sign-in
- [Thai Estate Law](docs/Thai%20Estate%20Law.md), [Inheritance Tax](docs/Inheritance%20Tax.md),
  [Living Will Directives](docs/Living%20Will%20Directives.md), [Asset Sheet](docs/Asset%20Sheet.md)

On GitHub the `[[wikilinks]]` inside those notes render as plain text; use the
standard links above (or open the folder in Obsidian) to navigate.
