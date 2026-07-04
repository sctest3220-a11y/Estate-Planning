# User Guide

How to use the estate-planning tool. See [[Home]] for the overview and
[[Disclaimer]] for the important caveats.

## Web app

1. **Log in** — create a local account or use **Sign in with Google** (if the
   server has it configured; see [[Deployment]]).
2. **Acknowledge the terms** — a required gate stating this is not legal advice and
   has not been reviewed by a lawyer. You cannot proceed without it.
3. **Choose documents** — pick any of Last Will, Living Will, Medical POA, Asset
   Inventory. The questionnaire only shows the questions relevant to your
   selection (see [[Architecture]] → context-aware form).
4. **Choose the document language** — English, Thai, or dual.
5. **Fill in the questionnaire** — only *full name* and *status* are required;
   everything else is optional.
   - For the living will you can select specific directives — see [[Living Will Directives]].
   - For assets you can type rows, or use the [[Asset Sheet]] CSV template.
6. **Review results** — tailored advice, warnings, an [[Inheritance Tax]] estimate,
   and general [[Tips]] (like the ราคาประเมิน land-valuation tip).
7. **Download** — all selected documents as a ZIP of Markdown files.

### Interface options

- **TH / ENG toggle** (header) — switches the *app interface* language. This is
  separate from the *document* language chosen in the questionnaire.
- **Light / dark mode** (header) — remembered in your browser.

### Preview

Visit **Preview** to see every document with `[placeholders]`, in any language,
without entering any personal data.

## CLI

```bash
python3 -m estate_planning.cli
```

An interactive questionnaire that prints advice, the tax estimate, and tips, then
writes draft documents to `output/<name>_<timestamp>/`. See [[Development]] to run
it from a checkout.

## Privacy

Your estate data (names, passport numbers, beneficiaries, asset values) is
processed in memory per request and is **never stored on the server**. Only your
account credentials and a terms-acknowledgment timestamp are saved. See
[[Deployment]] for details.
