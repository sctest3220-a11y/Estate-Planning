# Asset Sheet

Itemizing assets three ways, and how they feed the documents and tax estimate.
Implemented in `assets_csv.py` and the questionnaire (see [[Architecture]]).
Related: [[Inheritance Tax]], [[Tips]], [[User Guide]].

## Three ways to use it

1. **Online** — add rows in the questionnaire (category, description, value,
   location, notes).
2. **Offline** — download the **Excel template** (`/asset-template.xlsx`): a
   multi-tab workbook with **one tab per asset category**, each with
   category-specific columns and **required fields marked `*`** (shaded), plus an
   Instructions tab. Fill in the tabs that apply in Excel / Google Sheets / Numbers.
3. **Upload** — submit the filled `.xlsx` (a plain `.csv` also works); rows are
   parsed across all tabs and merged.

Categories (one tab each): real estate, vehicle, bank account, investment,
insurance, business, digital asset, other. Each tab has extra optional fields — e.g.
a bank account captures bank name, account number, account type, branch, and
currency; insurance captures insurer, policy number, policy type, and beneficiary.
Field schemas live in `asset_schema.py`; the workbook is built and parsed in
`asset_workbook.py` (see [[Architecture]]).

## Mapping assets to beneficiaries

Every asset is linked to the person who inherits it:

- **Online rows** — a **dropdown** on each asset row lists the beneficiaries you've
  added (kept in sync as you add/rename/remove them), so there are no typos. If a
  selected name is later renamed, the old selection is preserved and marked
  "(not in list)" rather than silently dropped.
- **Excel sheet** — a free-text **Beneficiary** column on each category tab (the
  template is downloaded before you enter beneficiaries, so it can't be a live
  dropdown); type the name exactly as in the Beneficiaries section.

Matching is by name (case-insensitive). This drives the **who-gets-what** summary
in the results and the will, and the per-beneficiary totals used for tax. Assets
with a name not in your beneficiary list are flagged; assets left blank appear as
"unassigned". See [[Architecture]] (`bequests.py`).

## Where assets go

- Rendered as a **table with a total** in the Asset Inventory document.
- Grouped by beneficiary in the will's "Beneficiaries and Bequests" section.
- Included in the [[Inheritance Tax]] estimate — a beneficiary's value is taken
  from the assets mapped to them (or a manually entered amount).
- Round-trip safe: uploaded assets are re-emitted as hidden fields so the ZIP
  download regenerates identically — nothing is persisted server-side.

## Valuation tip (ราคาประเมิน)

For land and buildings, value by the **official government appraised value
(ราคาประเมินราชการ)**, usually lower than market price:
<https://assessprice.treasury.go.th>. This note also appears in the Asset Inventory
document's real-estate section and in [[Tips]].

## Details preservation

Each parsed asset keeps a `details` dict of its category-specific fields. On the
results page these are re-emitted as a JSON hidden field so the **download
regenerates the full detail** without re-uploading — still nothing is stored
server-side. See `tests/test_asset_workbook.py`.

## Legacy CSV

A flat CSV template/parser (`assets_csv.py`) still exists and `.csv` uploads are
still accepted — columns `category, description, value_thb, location, notes`. The
Excel workbook is the richer, recommended template.
