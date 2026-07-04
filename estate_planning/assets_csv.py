"""Round-trip the asset sheet as CSV: a template to fill offline, and a parser
for the uploaded file. CSV is chosen so it opens in Excel/Google Sheets/Numbers.
"""

import csv
import io

from .models import ASSET_CATEGORIES, Asset

CSV_HEADERS = ["category", "description", "value_thb", "location", "notes"]

# Accept either the category key or its English label (case-insensitive).
_LABEL_TO_KEY = {label.lower(): key for key, label in ASSET_CATEGORIES.items()}


def template_csv():
    """A blank asset sheet with headers, a category reference row, and examples."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(CSV_HEADERS)
    # Reference comment rows the user can delete.
    writer.writerow(
        ["# categories:", " | ".join(ASSET_CATEGORIES.keys()), "", "", ""]
    )
    writer.writerow(
        ["real_estate", "Condo unit 5A, Sukhumvit", "6500000", "Chanote no. 1234", "example — replace"]
    )
    writer.writerow(
        ["bank_account", "Bangkok Bank savings", "850000", "Acct 123-4-56789", "example — replace"]
    )
    # A few blank rows to fill in.
    for _ in range(8):
        writer.writerow(["", "", "", "", ""])
    return buf.getvalue()


def _parse_value(raw):
    raw = (raw or "").replace(",", "").strip()
    if not raw:
        return 0.0
    try:
        return float(raw)
    except ValueError:
        return 0.0


def parse_csv(text):
    """Parse uploaded CSV text into a list of Asset. Skips headers, comment rows
    (first cell starts with '#'), and fully blank rows. Tolerant of the template's
    example rows only if the user keeps them."""
    assets = []
    reader = csv.reader(io.StringIO(text))
    for row in reader:
        if not row:
            continue
        cells = (row + ["", "", "", "", ""])[:5]
        category, description, value, location, notes = [c.strip() for c in cells]
        if not any([category, description, value, location, notes]):
            continue
        low = category.lower()
        if low in ("category", "#") or low.startswith("#"):
            continue
        # Normalize category to a known key.
        key = category if category in ASSET_CATEGORIES else _LABEL_TO_KEY.get(low, "other")
        assets.append(
            Asset(
                category=key,
                description=description,
                value_thb=_parse_value(value),
                location=location,
                notes=notes,
            )
        )
    return assets
