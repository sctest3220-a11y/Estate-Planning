# Thai Estate Law

Summary of the law this tool encodes. Source: [estate-planning-thailand.md](../estate-planning-thailand.md).
Not legal advice — see [[Disclaimer]]. Related: [[Inheritance Tax]],
[[Living Will Directives]], [[Asset Sheet]].

## Last will and testament

- **Governing law:** Civil and Commercial Code, Sections 1655–1672.
- **Recommended form:** Ordinary Written Will (พินัยกรรมแบบธรรมดา, **Section 1656**) —
  in writing, dated, signed by the testator before **≥2 witnesses** present together,
  who also sign. No notarization or registration required.
- **Witness eligibility:** ≥20 years old, sound mind, not a beneficiary or married
  to one.
- **Executor (ผู้จัดการมรดก):** ≥20, sound mind, not bankrupt, and must appear **in
  person** before the Thai probate court — so a Thai-based executor is preferred.

### Foreigners — the dual-will strategy

A Thai will typically covers only Thai-situated assets. Foreign assets are governed
by the law where they sit. Recommended: **two wills** (Thai + home-country), each
with a carve-out clause so neither revokes the other. Relying on one will forces
heirs into the "two-court problem" (6–12+ months of extra probate).

### Intestacy (no valid will) — Section 1629

Six classes of statutory heirs in priority: descendants; parents; full-blood
siblings; half-blood siblings; grandparents; uncles/aunts. A higher class excludes
lower ones (except parents inherit alongside descendants). The spouse inherits
alongside whichever class applies, after marital property (สินสมรส / Sin Somros) is
split. Thailand has **no forced heirship**.

## Living will / advance directive

Separate from the will — governs medical treatment, not property. Governed by
**Section 12, National Health Act B.E. 2550** and the 2010 Ministerial Regulation.
See [[Living Will Directives]] for the specific selectable options and their limits.

## Powers of attorney

- **Medical POA** — names a healthcare proxy for real-time decisions; pair with the
  living will.
- **Financial POA** — government offices/banks often require the standardized
  **Tor Dor 21 (ตด.21)** form, not a custom POA; POAs are usually transaction-specific.

## Marriage

Must be **registered at the Amphur** (Section 1457) to confer inheritance rights —
a religious/ceremonial marriage alone does not.

## What the tool checks

The rules engine (`advice.py`) flags: missing Thai/foreign wills, foreign land/condo
inheritance restrictions, unregistered marriage, overseas executor, and intestacy
exposure — see [[Architecture]].
