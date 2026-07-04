"""Convert submitted web form data into a validated EstatePlan.

Mirrors the questionnaire flow in estate_planning/cli.py.
"""

import json

from ..documents import (
    DOCUMENT_SPECS,
    LANGUAGE_MODES,
    LIVING_WILL_OPTIONS,
    MODE_DUAL,
)
from ..models import (
    ASSET_CATEGORIES,
    STATUS_CHOICES,
    STATUS_VISITOR,
    RELATIONSHIP_CHOICES,
    Asset,
    Beneficiary,
    EstatePlan,
    Witness,
)


def parse_language(form):
    """Return a valid language mode, defaulting to dual."""
    mode = form.get("language")
    return mode if mode in LANGUAGE_MODES else MODE_DUAL


def parse_selected_docs(form):
    """Return the list of selected document keys (all if none selected)."""
    selected = [k for k in form.getlist("documents") if k in DOCUMENT_SPECS]
    return selected or list(DOCUMENT_SPECS.keys())


def _checkbox(form, name):
    return form.get(name) in ("on", "true", "1", "yes")


def _tristate(form, name):
    """Radio with values yes/no/unknown -> True/False/None."""
    value = form.get(name)
    if value == "yes":
        return True
    if value == "no":
        return False
    return None


def _parse_value(raw):
    if not raw:
        return 0.0
    return float(str(raw).replace(",", "").strip())


def build_plan(form):
    """Returns (plan, errors). plan is None if there are blocking errors."""
    errors = []

    full_name = (form.get("full_name") or "").strip()
    if not full_name:
        errors.append("Full legal name is required.")

    status = (form.get("status") or "").strip()
    if status not in STATUS_CHOICES:
        errors.append("Please choose a valid status.")

    # Witnesses (parallel lists from repeated fields).
    witnesses = []
    names = form.getlist("witness_name")
    ids = form.getlist("witness_id")
    for i, name in enumerate(names):
        name = (name or "").strip()
        if not name:
            continue
        id_no = (ids[i].strip() if i < len(ids) and ids[i] else "") or "TBD"
        witnesses.append(Witness(name=name, id_or_passport=id_no))

    # Beneficiaries.
    beneficiaries = []
    b_names = form.getlist("beneficiary_name")
    b_rels = form.getlist("beneficiary_relationship")
    b_assets = form.getlist("beneficiary_asset")
    b_values = form.getlist("beneficiary_value")
    for i, name in enumerate(b_names):
        name = (name or "").strip()
        if not name:
            continue
        rel = b_rels[i].strip() if i < len(b_rels) and b_rels[i] else "other"
        if rel not in RELATIONSHIP_CHOICES:
            rel = "other"
        # Free-text bequest note; empty is fine (assets are mapped separately).
        asset = b_assets[i].strip() if i < len(b_assets) and b_assets[i] else ""
        raw_value = b_values[i] if i < len(b_values) else "0"
        try:
            value = _parse_value(raw_value)
        except ValueError:
            errors.append(f"Inherited value for '{name}' must be a number.")
            value = 0.0
        if value < 0:
            errors.append(f"Inherited value for '{name}' cannot be negative.")
            value = 0.0
        beneficiaries.append(
            Beneficiary(
                name=name,
                relationship=rel,
                asset_description=asset,
                inherited_value_thb=value,
            )
        )

    # Itemized assets (online rows, or carried back from an uploaded sheet).
    assets = []
    a_cats = form.getlist("asset_category")
    a_descs = form.getlist("asset_description")
    a_values = form.getlist("asset_value")
    a_locs = form.getlist("asset_location")
    a_notes = form.getlist("asset_notes")
    a_bens = form.getlist("asset_beneficiary")
    a_details = form.getlist("asset_details")
    for i, cat in enumerate(a_cats):
        desc = a_descs[i].strip() if i < len(a_descs) and a_descs[i] else ""
        raw_value = a_values[i] if i < len(a_values) else "0"
        loc = a_locs[i].strip() if i < len(a_locs) and a_locs[i] else ""
        note = a_notes[i].strip() if i < len(a_notes) and a_notes[i] else ""
        ben = a_bens[i].strip() if i < len(a_bens) and a_bens[i] else ""
        # A row with only a default category and nothing else is empty.
        if not any([desc, (raw_value or "").strip(), loc, note, ben]):
            continue
        try:
            value = _parse_value(raw_value)
        except ValueError:
            errors.append(f"Asset value '{raw_value}' must be a number.")
            value = 0.0
        if value < 0:
            errors.append("Asset values cannot be negative.")
            value = 0.0
        category = cat.strip() if cat.strip() in ASSET_CATEGORIES else "other"
        details = {}
        if i < len(a_details) and a_details[i]:
            try:
                loaded = json.loads(a_details[i])
                if isinstance(loaded, dict):
                    details = {str(k): str(v) for k, v in loaded.items()}
            except (ValueError, TypeError):
                details = {}
        assets.append(
            Asset(
                category=category,
                description=desc,
                value_thb=value,
                location=loc,
                notes=note,
                beneficiary=ben,
                details=details,
            )
        )

    if errors:
        return None, errors

    is_visitor = status == STATUS_VISITOR

    plan = EstatePlan(
        full_name=full_name,
        nationality=(form.get("nationality") or "").strip(),
        passport_or_id_number=(form.get("passport_or_id_number") or "").strip(),
        date_of_birth=(form.get("date_of_birth") or "").strip(),
        thai_address=(form.get("thai_address") or "").strip(),
        status=status,
        has_thai_will=_checkbox(form, "has_thai_will"),
        has_foreign_will=_checkbox(form, "has_foreign_will"),
        owns_land=(not is_visitor) and _checkbox(form, "owns_land"),
        owns_condo=(not is_visitor) and _checkbox(form, "owns_condo"),
        has_lease=(not is_visitor) and _checkbox(form, "has_lease"),
        has_lease_with_succession_clause=_tristate(form, "lease_succession"),
        married_to_thai=(not is_visitor) and _checkbox(form, "married_to_thai"),
        spouse_name=(form.get("spouse_name") or "").strip(),
        marriage_registered_at_amphur=_tristate(form, "marriage_registered"),
        executor_name=(form.get("executor_name") or "").strip() or "TBD",
        executor_based_in_thailand=_tristate(form, "executor_in_thailand"),
        healthcare_proxy_name=(form.get("healthcare_proxy_name") or "").strip() or "TBD",
        living_will_options=[
            k for k in form.getlist("living_will_options") if k in LIVING_WILL_OPTIONS
        ],
        living_will_other=(form.get("living_will_other") or "").strip(),
        witnesses=witnesses,
        beneficiaries=beneficiaries,
        assets=assets,
    )
    return plan, []
