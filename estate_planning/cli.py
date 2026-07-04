"""Interactive questionnaire: collects a profile, prints Thai-law advice, and
drafts requested documents to an output directory.

Not legal advice. Review all output with a licensed Thai probate/estate lawyer.
"""

import os
from datetime import datetime

from .documents import (
    DISCLAIMER_EN,
    DISCLAIMER_TH,
    DOCUMENT_SPECS,
    LANGUAGE_LABELS,
    LANGUAGE_MODES,
    MODE_DUAL,
    generate,
)
from .models import (
    STATUS_CHOICES,
    STATUS_FOREIGN_RESIDENT,
    STATUS_THAI_NATIONAL,
    STATUS_VISITOR,
    RELATIONSHIP_CHOICES,
    Beneficiary,
    EstatePlan,
    Witness,
)
from .advice import assess
from .tax import tax_plan
from .tips import planning_tips


def ask(prompt, default=None):
    suffix = f" [{default}]" if default is not None else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value or (default if default is not None else "")


def ask_yes_no(prompt, default=None):
    default_str = "y" if default is True else "n" if default is False else None
    suffix = f" (y/n)" + (f" [{default_str}]" if default_str else "")
    while True:
        value = input(f"{prompt}{suffix}: ").strip().lower()
        if not value and default is not None:
            return default
        if value in ("y", "yes"):
            return True
        if value in ("n", "no"):
            return False
        print("Please answer y or n.")


def ask_float(prompt, default=0.0):
    while True:
        value = input(f"{prompt} [{default}]: ").strip()
        if not value:
            return default
        try:
            return float(value.replace(",", ""))
        except ValueError:
            print("Please enter a number.")


def ask_choice(prompt, choices, default=None):
    choices_str = "/".join(choices)
    while True:
        value = ask(f"{prompt} ({choices_str})", default)
        if value in choices:
            return value
        print(f"Please choose one of: {choices_str}")


def collect_witnesses():
    witnesses = []
    print("\nWitnesses (at least 2 recommended; press Enter with a blank name to stop):")
    while True:
        name = ask(f"  Witness {len(witnesses) + 1} name (blank to stop)")
        if not name:
            break
        id_no = ask("    ID/Passport number", "TBD")
        witnesses.append(Witness(name=name, id_or_passport=id_no))
    return witnesses


def collect_beneficiaries():
    beneficiaries = []
    print("\nBeneficiaries (press Enter with a blank name to stop):")
    while True:
        name = ask(f"  Beneficiary {len(beneficiaries) + 1} name (blank to stop)")
        if not name:
            break
        relationship = ask_choice("    Relationship to you", RELATIONSHIP_CHOICES, "other")
        asset_description = ask("    Asset(s) bequeathed to them", "TBD")
        value = ask_float("    Estimated inherited value (THB)", 0.0)
        beneficiaries.append(
            Beneficiary(
                name=name,
                relationship=relationship,
                asset_description=asset_description,
                inherited_value_thb=value,
            )
        )
    return beneficiaries


def collect_plan() -> EstatePlan:
    print("=" * 70)
    print("Thailand Estate Planning — Advice & Document Drafting")
    print(DISCLAIMER_EN)
    print(DISCLAIMER_TH)
    print("=" * 70)

    full_name = ask("\nFull legal name")
    nationality = ask("Nationality")
    passport_or_id_number = ask("Passport/ID number")
    date_of_birth = ask("Date of birth (YYYY-MM-DD)")
    thai_address = ask("Address in Thailand")

    print(
        "\nStatus categories:\n"
        f"  {STATUS_THAI_NATIONAL} — Thai national\n"
        f"  {STATUS_FOREIGN_RESIDENT} — foreign resident / property owner / married to a Thai national\n"
        f"  {STATUS_VISITOR} — occasional visitor, no Thai assets\n"
    )
    status = ask_choice("Which status applies to you?", STATUS_CHOICES, STATUS_FOREIGN_RESIDENT)

    has_thai_will = ask_yes_no("Do you already have a Thai will?", False)
    has_foreign_will = ask_yes_no("Do you already have a foreign (home-country) will?", False)

    owns_land = False
    owns_condo = False
    has_lease = False
    has_lease_with_succession_clause = None
    married_to_thai = False
    spouse_name = ""
    marriage_registered_at_amphur = None

    if status != STATUS_VISITOR:
        owns_land = ask_yes_no("Do you own land in Thailand?", False)
        owns_condo = ask_yes_no("Do you own a condominium unit in Thailand?", False)
        has_lease = ask_yes_no("Do you hold a lease in Thailand?", False)
        if has_lease:
            has_lease_with_succession_clause = ask_yes_no(
                "Does the lease include a succession clause?", False
            )
        married_to_thai = ask_yes_no("Are you married to a Thai national?", False)
        if married_to_thai:
            spouse_name = ask("Spouse's full name")
            marriage_registered_at_amphur = ask_yes_no(
                "Is the marriage registered at the Amphur (Section 1457)?", True
            )

    executor_name = ask("Executor's full name", "TBD")
    executor_based_in_thailand = ask_yes_no("Is the executor based in Thailand?", True)
    healthcare_proxy_name = ask("Healthcare proxy's full name", "TBD")

    witnesses = collect_witnesses()
    beneficiaries = collect_beneficiaries()

    return EstatePlan(
        full_name=full_name,
        nationality=nationality,
        passport_or_id_number=passport_or_id_number,
        date_of_birth=date_of_birth,
        thai_address=thai_address,
        status=status,
        has_thai_will=has_thai_will,
        has_foreign_will=has_foreign_will,
        owns_land=owns_land,
        owns_condo=owns_condo,
        has_lease=has_lease,
        has_lease_with_succession_clause=has_lease_with_succession_clause,
        married_to_thai=married_to_thai,
        spouse_name=spouse_name,
        marriage_registered_at_amphur=marriage_registered_at_amphur,
        executor_name=executor_name,
        executor_based_in_thailand=executor_based_in_thailand,
        healthcare_proxy_name=healthcare_proxy_name,
        witnesses=witnesses,
        beneficiaries=beneficiaries,
    )


def print_advice(advice):
    print("\n" + "=" * 70)
    print("ADVICE SUMMARY")
    print("=" * 70)
    print(advice.summary)

    if advice.recommendations:
        print("\nRecommendations:")
        for r in advice.recommendations:
            print(f"  - {r}")

    if advice.warnings:
        print("\nWarnings:")
        for w in advice.warnings:
            print(f"  ⚠️  {w}")

    if advice.tax_breakdown:
        print("\nEstimated inheritance tax by beneficiary:")
        for t in advice.tax_breakdown:
            print(f"  - {t}")


def choose_documents():
    print("\nAvailable documents:")
    keys = list(DOCUMENT_SPECS.keys())
    for i, key in enumerate(keys, 1):
        print(f"  {i}. {DOCUMENT_SPECS[key][0]} ({key})")
    raw = ask(
        "Which documents to generate? Comma-separated numbers or names, blank for all",
        "all",
    )
    if not raw or raw.strip().lower() == "all":
        return keys
    selected = []
    for token in raw.split(","):
        token = token.strip()
        if not token:
            continue
        if token.isdigit() and 1 <= int(token) <= len(keys):
            selected.append(keys[int(token) - 1])
        elif token in keys:
            selected.append(token)
    return selected or keys


def choose_language():
    print("\nLanguage for the documents:")
    for i, mode in enumerate(LANGUAGE_MODES, 1):
        print(f"  {i}. {LANGUAGE_LABELS[mode]} ({mode})")
    raw = ask("Choose a language", MODE_DUAL)
    token = raw.strip().lower()
    if token.isdigit() and 1 <= int(token) <= len(LANGUAGE_MODES):
        return LANGUAGE_MODES[int(token) - 1]
    return token if token in LANGUAGE_MODES else MODE_DUAL


def write_documents(plan: EstatePlan, selected_keys, mode, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    written = []
    for key, (_title, content) in generate(plan, selected_keys, mode).items():
        path = os.path.join(output_dir, f"{key}_{mode}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        written.append(path)
    return written


def print_tax_plan(plan):
    tplan = tax_plan(plan)
    print("\n" + "=" * 70)
    print("INHERITANCE TAX PLANNING")
    print("=" * 70)
    if tplan["total_estate"]:
        print(f"Total listed estate: {tplan['total_estate']:,.0f} THB")
    print(f"Estimated inheritance tax: {tplan['total_tax']:,.0f} THB")
    if tplan["tips"]:
        print("\nPlanning suggestions:")
        for tip in tplan["tips"]:
            print(f"  - {tip}")


def print_tips(plan):
    tips = planning_tips(plan)
    if not tips:
        return
    print("\n" + "=" * 70)
    print("TIPS & REMINDERS")
    print("=" * 70)
    for tip in tips:
        print(f"  - {tip}")


def main():
    plan = collect_plan()
    advice = assess(plan)
    print_advice(advice)
    print_tax_plan(plan)
    print_tips(plan)

    selected_keys = choose_documents()
    mode = choose_language()
    safe_name = "".join(c if c.isalnum() else "_" for c in plan.full_name).strip("_") or "draft"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join("output", f"{safe_name}_{timestamp}")
    written = write_documents(plan, selected_keys, mode, output_dir)

    print("\n" + "=" * 70)
    print(f"Draft documents written to {output_dir}/:")
    for path in written:
        print(f"  - {path}")
    print("\n" + DISCLAIMER_EN)
    print(DISCLAIMER_TH)


if __name__ == "__main__":
    main()
