# Lawyer Review Checklist

This tool is **unreviewed by a lawyer** (see [[Disclaimer]]). Before anyone relies
on its output — and before opening it to more users — a licensed Thai
probate/estate lawyer should review the items below. This page is the review
packet: hand it to counsel so the engagement is efficient.

## Document templates (`documents.py`)

- [ ] **Last Will (Ordinary Written Will, Section 1656)** — form, execution clause,
      witness attestation wording, carve-out clause for the dual-will strategy.
- [ ] **Living Will (Section 12 advance directive)** — the base declaration and each
      selectable directive in [[Living Will Directives]] (DNR, ventilation, tube
      feeding, dialysis, comfort care, place of death, spiritual care) and the
      passive-only / terminal-stage framing.
- [ ] **Medical Power of Attorney** — validity and scope of the proxy appointment.
- [ ] **Asset Inventory** — confirm it reads as an administrative companion, not a
      will, and that the will↔inventory note is correct (see [[Asset Sheet]]).
- [ ] Thai-language wording throughout (translations were done carefully but are
      not certified).

## Encoded rules (`advice.py`)

- [ ] Intestacy classes and spouse share (Sections 1629, 1635).
- [ ] Foreigner land/condo inheritance restrictions (Land Code s.87; Condominium Act).
- [ ] Executor in-person requirement; witness/executor eligibility.
- [ ] Marriage-registration requirement (Section 1457).

## Tax figures (`tax.py`, [[Inheritance Tax]])

- [ ] Inheritance tax threshold (100M THB per beneficiary) and that only the excess
      is taxed; rates (5% lineal / 10% other); spouse exemption.
- [ ] Gift-tax annual exemptions (20M lineal/spouse, 10M others) and 5% rate.
- [ ] Land valuation basis (ราคาประเมิน) framing in [[Tips]].

## Legal-structure questions

- [ ] Whether the will's bequest summary sufficiently identifies gifts.
- [ ] Whether a binding "schedule of assets" is advisable and, if so, its execution
      formalities.
- [ ] Any content that should be added, removed, or reworded for enforceability.

## After review

Record the outcome here and in the source doc footer
([estate-planning-thailand.md](../estate-planning-thailand.md)): lawyer/firm name,
date, and any changes made. Update the affected tests (see [[Development]]) and, if
the review clears the templates, revise the "not yet reviewed" wording in the app.
