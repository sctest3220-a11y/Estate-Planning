# Living Will Directives

The selectable advance-directive options and the Thai law behind them. Implemented
as `LIVING_WILL_OPTIONS` in `documents.py` (see [[Architecture]]). Not legal advice —
see [[Disclaimer]]. Related: [[Thai Estate Law]], [[User Guide]].

## Legal basis

- **Section 12, National Health Act B.E. 2550 (2007)** and the **2010 Ministerial
  Regulation** on advance directives.
- Applies only in a **terminal stage** where treatment merely prolongs dying.
- **Passive only** — you may refuse/withhold/withdraw life-prolonging treatment.
  **Active euthanasia / assisted dying is illegal** in Thailand.
- Requirements: age 18+, in writing, dated, signed, with witnesses.

## Selectable options

Each is phrased inside the passive terminal-stage framework:

- **DNR / no CPR** — do not attempt resuscitation.
- **No mechanical ventilation** to prolong dying.
- **No artificial nutrition/hydration by tube** to prolong dying.
- **No dialysis** to prolong dying.
- **Palliative / comfort care** and pain relief (an affirmative request).
- **Place of death** — prefer home / a peaceful setting.
- **Spiritual / religious care** per your beliefs.
- Plus a free-text **additional wishes** field.

## Important caveat (built into the tool)

Acceptance of specific directives can vary. Both the questionnaire and the generated
document carry a prominent note to **confirm each directive with your hospital and a
Thai lawyer** before relying on it. This matches the standing [[Disclaimer]].

## In the UI

The directives section is **context-aware** — it appears only when the Living Will
is selected (see [[Architecture]] → context-aware form). Sources verified via public
Thai legal summaries; exact clause wording still belongs in the lawyer review.
