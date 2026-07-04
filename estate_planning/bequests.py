"""Map assets to beneficiaries and summarize who inherits what.

An asset is linked to a beneficiary by name (`Asset.beneficiary` matched to
`Beneficiary.name`, case-insensitively). This powers the will's bequest summary,
the results "who gets what" view, and the effective values used for tax.
"""

from .models import ASSET_CATEGORIES


def _norm(name):
    return (name or "").strip().lower()


def asset_label(asset):
    """A short human label for an asset, e.g. 'Bangkok Bank (Bank account)'."""
    name = asset.description or ASSET_CATEGORIES.get(asset.category, asset.category)
    category = ASSET_CATEGORIES.get(asset.category, asset.category)
    if asset.description and category and category.lower() not in name.lower():
        return f"{name} ({category})"
    return name


def mapped_total(plan, beneficiary_name):
    """Total value of assets assigned to a given beneficiary name."""
    key = _norm(beneficiary_name)
    return sum(
        (a.value_thb or 0.0)
        for a in plan.assets
        if _norm(a.beneficiary) == key and key
    )


def effective_value(plan, beneficiary):
    """A beneficiary's inheritance value: the manually entered amount if given,
    otherwise the sum of assets mapped to them."""
    if beneficiary.inherited_value_thb and beneficiary.inherited_value_thb > 0:
        return beneficiary.inherited_value_thb
    return mapped_total(plan, beneficiary.name)


def summarize(plan):
    """Return {beneficiaries, unassigned, unknown} describing who gets what."""
    named = {}  # normalized beneficiary name -> list of assets
    unassigned = []
    for a in plan.assets:
        if _norm(a.beneficiary):
            named.setdefault(_norm(a.beneficiary), []).append(a)
        else:
            unassigned.append(a)

    rows = []
    seen = set()
    for b in plan.beneficiaries:
        key = _norm(b.name)
        seen.add(key)
        assets = named.get(key, [])
        rows.append(
            {
                "name": b.name,
                "relationship": b.relationship,
                "bequest_text": b.asset_description,
                "assets": assets,
                "mapped_total": sum((a.value_thb or 0.0) for a in assets),
                "effective_value": effective_value(plan, b),
            }
        )

    # Assets assigned to a name that is not in the beneficiaries list.
    unknown = []
    for key, assets in named.items():
        if key in seen:
            continue
        unknown.append(
            {
                "name": assets[0].beneficiary,
                "assets": assets,
                "mapped_total": sum((a.value_thb or 0.0) for a in assets),
            }
        )

    return {"beneficiaries": rows, "unassigned": unassigned, "unknown": unknown}
