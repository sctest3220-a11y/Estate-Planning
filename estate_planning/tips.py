"""General estate-planning tips and reminders, some tailored to the user's plan.

Informational only — not legal or tax advice. Kept as English strings (with Thai
terms inline) to match the advice/warnings style.
"""

ASSESS_PRICE_URL = "https://assessprice.treasury.go.th"


def _has_real_estate(plan):
    return (
        plan.owns_land
        or plan.owns_condo
        or any(a.category == "real_estate" for a in plan.assets)
    )


def planning_tips(plan):
    """Return a list of tip strings, some conditional on the plan."""
    tips = []

    # Land/condo valuation — the user-requested tip.
    if _has_real_estate(plan) or not plan.assets:
        tips.append(
            "Valuing land and buildings: for inheritance and tax purposes the value "
            "is generally based on the official government appraised value "
            "(ราคาประเมินราชการ), which is usually lower than the market price. Look up "
            f"the appraised value at the Treasury Department's site: {ASSESS_PRICE_URL}"
        )

    # Where the documents live.
    tips.append(
        "Tell your executor and family where the signed originals are kept, and give "
        "your hospital and healthcare proxy a copy of your living will and medical "
        "power of attorney."
    )

    # Keep documents current.
    tips.append(
        "Review your documents after major life events — marriage, divorce, a new "
        "child, buying or selling property, or moving country — and re-date them."
    )

    # Bank account freeze / liquidity.
    tips.append(
        "Thai bank accounts are generally frozen on death until the estate is "
        "administered. Make sure someone can access funds for immediate funeral and "
        "living costs (for example a separate emergency fund)."
    )

    # Beneficiary designations outside the will.
    tips.append(
        "Life insurance proceeds and some provident/retirement funds pass to the "
        "named beneficiary outside your will — check those designations are current, "
        "as your will does not override them."
    )

    # Foreign assets.
    if plan.status != "thai_national" or plan.has_foreign_will:
        tips.append(
            "Assets outside Thailand are governed by the law where they are located. "
            "Keep a matching home-country will with a carve-out clause so neither will "
            "revokes the other."
        )

    # Digital assets.
    if any(a.category == "digital" for a in plan.assets):
        tips.append(
            "For crypto and online accounts, securely record how to access them (seed "
            "phrases, passwords) and leave instructions for your executor — these are "
            "lost forever if no one can reach them. Consider a password manager whose "
            "master credentials your executor can obtain."
        )

    # Keep the inventory updated.
    tips.append(
        "Keep your asset inventory up to date — it is the single most useful thing you "
        "can leave your executor, and it speeds up probate."
    )

    return tips
