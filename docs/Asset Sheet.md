# Asset Sheet

Itemizing assets three ways, and how they feed the documents and tax estimate.
Implemented in `assets_csv.py` and the questionnaire (see [[Architecture]]).
Related: [[Inheritance Tax]], [[Tips]], [[User Guide]].

## Three ways to use it

1. **Online** — add rows in the questionnaire (category, description, value,
   location, notes).
2. **Offline** — download the CSV template (`/asset-template.csv`), fill it in
   Excel / Google Sheets / Numbers.
3. **Upload** — submit the filled CSV; rows are parsed and merged.

Categories: real estate, vehicle, bank account, investment/retirement, insurance,
business, digital asset, other.

## Where assets go

- Rendered as a **table with a total** in the Asset Inventory document.
- Included in the [[Inheritance Tax]] estimate (total estate).
- Round-trip safe: uploaded assets are re-emitted as hidden fields so the ZIP
  download regenerates identically — nothing is persisted server-side.

## Valuation tip (ราคาประเมิน)

For land and buildings, value by the **official government appraised value
(ราคาประเมินราชการ)**, usually lower than market price:
<https://assessprice.treasury.go.th>. This note also appears in the Asset Inventory
document's real-estate section and in [[Tips]].

## CSV format

Columns: `category, description, value_thb, location, notes`. The parser skips the
header, comment rows starting with `#`, and blank rows, and maps either the category
key or its English label. See `tests/test_assets_csv.py`.
