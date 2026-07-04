"""Rules engine encoding the Thai estate-planning guidance in estate-planning-thailand.md.

Not legal advice. Output must be verified with a Thai probate/estate lawyer.
"""

from .models import (
    STATUS_FOREIGN_RESIDENT,
    STATUS_THAI_NATIONAL,
    STATUS_VISITOR,
    Advice,
    EstatePlan,
)
from .tax import (
    TAX_RATE_DESCENDANT_ASCENDANT,
    TAX_RATE_OTHER,
    TAX_THRESHOLD_THB,
    tax_breakdown_lines,
)


def assess(plan: EstatePlan) -> Advice:
    warnings = []
    recommendations = []

    if plan.status == STATUS_THAI_NATIONAL:
        summary = (
            "Thai national: a single Thai will plus standard estate documents "
            "should cover your estate."
        )
        recommendations.append(
            "Prepare an Ordinary Written Will (Civil and Commercial Code Section 1656) "
            "covering all assets."
        )
    elif plan.status == STATUS_FOREIGN_RESIDENT:
        summary = (
            "Foreign resident / property owner / married to a Thai national: "
            "a dual-will strategy is recommended."
        )
        recommendations.append(
            "Prepare a Thai will (Section 1656 Ordinary Written Will) for Thai-situated "
            "assets, and a separate home-country will for foreign assets. Add a carve-out "
            "clause to each so neither revokes the other."
        )
        if not plan.has_foreign_will:
            warnings.append(
                "No foreign will on file: relying on only one jurisdiction's will risks "
                "the 'two-court problem' for assets in the other jurisdiction — expect "
                "6-12+ months of added probate delay without a matching will in each place."
            )
    else:
        summary = (
            "Occasional visitor with no Thai assets: Thailand-specific documents largely "
            "don't apply; rely on home-country will and directives."
        )
        recommendations.append(
            "Confirm you hold no Thai-situated assets; if that changes, revisit the "
            "dual-will strategy."
        )

    if plan.owns_land and plan.status != STATUS_THAI_NATIONAL:
        warnings.append(
            "Land inherited by a foreign statutory heir requires Ministry of Interior "
            "permission to retain it; area is capped under Land Code Section 87. Confirm "
            "eligibility before relying on inheriting land directly."
        )
    if plan.owns_condo and plan.status != STATUS_THAI_NATIONAL:
        warnings.append(
            "Condo units inherited by a foreigner must qualify under the Condominium Act's "
            "foreign-quota rules or be disposed of within approximately 1 year."
        )
    if plan.has_lease and plan.has_lease_with_succession_clause is False:
        warnings.append(
            "Lease(s) on file will terminate on the lessee's death — the contract does not "
            "include a succession clause. Beneficiaries will not inherit the leasehold "
            "unless this is renegotiated."
        )
    if plan.executor_based_in_thailand is False:
        warnings.append(
            "Named executor is based overseas. The executor must appear in person before "
            "the Thai probate court — this can add significant delay. Consider naming a "
            "Thai-based executor."
        )
    if plan.married_to_thai and plan.marriage_registered_at_amphur is False:
        warnings.append(
            "Marriage is not registered at the Amphur (Section 1457). A religious/ceremonial "
            "marriage alone confers no statutory inheritance rights for the spouse in Thailand."
        )
    if not plan.has_thai_will and plan.status != STATUS_VISITOR:
        warnings.append(
            "No Thai will on file: Thai-situated assets would pass under intestacy "
            "(Section 1629) to the statutory heir classes, with the surviving spouse "
            "inheriting alongside whichever class applies, after marital property "
            "(Sin Somros) is split first."
        )

    tax_breakdown = tax_breakdown_lines(plan)

    return Advice(
        summary=summary,
        warnings=warnings,
        recommendations=recommendations,
        tax_breakdown=tax_breakdown,
    )
