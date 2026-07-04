# Development

Running and extending the project. See [[Architecture]] for the code map and
[[Deployment]] for shipping it.

## Setup

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
```

## Run

- **Web app:** `./.venv/bin/python -m flask --app estate_planning.web.app run --port 5001`
  then open <http://127.0.0.1:5001>.
- **CLI:** `./.venv/bin/python -m estate_planning.cli`

## Tests

```bash
./.venv/bin/python -m unittest discover -s tests
```

Test modules:

- `test_advice.py` — rules engine (see [[Thai Estate Law]]).
- `test_tax.py` — inheritance/gift tax (see [[Inheritance Tax]]).
- `test_tips.py` — tips logic (see [[Tips]]).
- `test_documents.py` — language modes and document selection.
- `test_living_will_options.py` — directives (see [[Living Will Directives]]).
- `test_assets_csv.py` — CSV round-trip (see [[Asset Sheet]]).
- `test_web_forms.py`, `test_web_i18n.py` — form parsing and interface i18n.

## Conventions

- No secrets in git: `users.json`, `.venv/`, and `.claude/` are gitignored; drafts
  go to `output/` (also ignored).
- When you change a legal figure (tax threshold, gift exemption) or a document
  clause, update the matching test and note it for the lawyer review.
- Keep the [[Disclaimer]] framing on any user-facing legal text.

## Contributing

See `CONTRIBUTING.md` at the repo root for the GitHub-facing version of this.
