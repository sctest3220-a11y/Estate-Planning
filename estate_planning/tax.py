"""Thai inheritance & gift tax estimation and planning suggestions.

Based on the Inheritance Tax Act B.E. 2558 (2015) and related Revenue Code
provisions as summarized in estate-planning-thailand.md. Not legal or tax advice;
figures and thresholds change — verify with a Thai tax lawyer or accountant.
"""

from .models import (
    RELATIONSHIP_ASCENDANT,
    RELATIONSHIP_DESCENDANT,
    RELATIONSHIP_SPOUSE,
)

# Inheritance tax: applies only to the portion each beneficiary receives ABOVE
# the threshold (not the whole inheritance).
TAX_THRESHOLD_THB = 100_000_000
TAX_RATE_DESCENDANT_ASCENDANT = 0.05  # lineal ascendants/descendants
TAX_RATE_OTHER = 0.10  # all other heirs
# Spouses are fully exempt.

# Lifetime gift tax (personal income tax treatment): annual exemptions, then a
# flat rate on the excess.
GIFT_EXEMPT_LINEAL_THB = 20_000_000  # per year to ascendants/descendants/spouse
GIFT_EXEMPT_OTHER_THB = 10_000_000  # per year to others
GIFT_TAX_RATE = 0.05

_LINEAL = (RELATIONSHIP_DESCENDANT, RELATIONSHIP_ASCENDANT)


def rate_for(relationship):
    if relationship in _LINEAL:
        return TAX_RATE_DESCENDANT_ASCENDANT
    return TAX_RATE_OTHER


def beneficiary_tax(beneficiary):
    """Return a structured inheritance-tax estimate for one beneficiary."""
    inherited = beneficiary.inherited_value_thb or 0.0
    if beneficiary.relationship == RELATIONSHIP_SPOUSE:
        return {
            "name": beneficiary.name,
            "relationship": beneficiary.relationship,
            "inherited": inherited,
            "exempt": True,
            "taxable": 0.0,
            "rate": 0.0,
            "tax": 0.0,
        }
    taxable = max(0.0, inherited - TAX_THRESHOLD_THB)
    rate = rate_for(beneficiary.relationship)
    return {
        "name": beneficiary.name,
        "relationship": beneficiary.relationship,
        "inherited": inherited,
        "exempt": False,
        "taxable": taxable,
        "rate": rate,
        "tax": taxable * rate,
    }


def _fmt(n):
    return f"{n:,.0f} THB"


def tax_breakdown_lines(plan):
    """Human-readable per-beneficiary lines (kept stable for the CLI/advice)."""
    lines = []
    for b in plan.beneficiaries:
        est = beneficiary_tax(b)
        if est["exempt"]:
            lines.append(f"{est['name']}: exempt (spouse).")
        elif est["taxable"] <= 0:
            lines.append(
                f"{est['name']}: below the {_fmt(TAX_THRESHOLD_THB)} threshold — "
                "no inheritance tax due."
            )
        else:
            lines.append(
                f"{est['name']} ({est['relationship']}): taxable amount "
                f"{_fmt(est['taxable'])} x {est['rate']:.0%} = {_fmt(est['tax'])} "
                "estimated inheritance tax."
            )
    return lines


def tax_plan(plan):
    """Return {estimates, total_tax, total_estate, tips} for tax planning."""
    estimates = [beneficiary_tax(b) for b in plan.beneficiaries]
    total_tax = sum(e["tax"] for e in estimates)
    total_estate = sum((a.value_thb or 0.0) for a in plan.assets)

    tips = []

    # Foundational, always-true framing.
    tips.append(
        "Assets you inherit are exempt from personal income tax. A separate "
        "inheritance tax applies only to the value each beneficiary receives above "
        f"{_fmt(TAX_THRESHOLD_THB)} — and only to the excess, not the whole amount."
    )
    tips.append(
        "Rates on the excess: 5% for descendants/ascendants (children, parents), "
        "10% for other heirs. Surviving spouses are fully exempt."
    )

    over = [e for e in estimates if e["taxable"] > 0]
    if over:
        names = ", ".join(e["name"] for e in over)
        tips.append(
            f"These beneficiaries are currently over the threshold: {names}. "
            "Because the 100M THB allowance is per beneficiary, distributing assets "
            "among more beneficiaries can reduce or eliminate the tax."
        )
        tips.append(
            "Assets left to a spouse are exempt, so routing part of the estate "
            "through a spouse (where appropriate) can defer or avoid tax."
        )
        tips.append(
            "Lifetime gifting can shrink the taxable estate: gifts to ascendants, "
            f"descendants, or a spouse are exempt up to {_fmt(GIFT_EXEMPT_LINEAL_THB)} "
            f"per year; gifts to others up to {_fmt(GIFT_EXEMPT_OTHER_THB)} per year. "
            "Amounts above the annual exemption are taxed at 5%."
        )
    elif estimates:
        tips.append(
            "Based on the values entered, no beneficiary exceeds the "
            f"{_fmt(TAX_THRESHOLD_THB)} threshold, so no inheritance tax is currently "
            "estimated. Re-check if asset values grow."
        )

    if total_estate and estimates:
        assigned = sum(e["inherited"] for e in estimates)
        if assigned + 1 < total_estate:  # tolerance for rounding
            tips.append(
                f"Your listed assets total {_fmt(total_estate)}, but only "
                f"{_fmt(assigned)} is assigned to beneficiaries above. Assign the "
                "remainder so the tax estimate reflects the full estate."
            )

    return {
        "estimates": estimates,
        "total_tax": total_tax,
        "total_estate": total_estate,
        "tips": tips,
    }
