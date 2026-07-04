import unittest

from estate_planning.models import Asset, Beneficiary, EstatePlan
from estate_planning.tax import beneficiary_tax, tax_plan


def plan_with(beneficiaries=None, assets=None):
    return EstatePlan(
        full_name="X",
        nationality="",
        passport_or_id_number="",
        date_of_birth="",
        thai_address="",
        status="foreign_resident",
        beneficiaries=beneficiaries or [],
        assets=assets or [],
    )


class BeneficiaryTaxTests(unittest.TestCase):
    def test_spouse_exempt(self):
        est = beneficiary_tax(Beneficiary("W", "spouse", inherited_value_thb=200_000_000))
        self.assertTrue(est["exempt"])
        self.assertEqual(est["tax"], 0.0)

    def test_descendant_only_excess_taxed_at_5pct(self):
        est = beneficiary_tax(Beneficiary("K", "descendant", inherited_value_thb=150_000_000))
        self.assertEqual(est["taxable"], 50_000_000)
        self.assertEqual(est["rate"], 0.05)
        self.assertEqual(est["tax"], 2_500_000)

    def test_other_heir_taxed_at_10pct(self):
        est = beneficiary_tax(Beneficiary("F", "other", inherited_value_thb=150_000_000))
        self.assertEqual(est["tax"], 5_000_000)

    def test_below_threshold_no_tax(self):
        est = beneficiary_tax(Beneficiary("K", "descendant", inherited_value_thb=80_000_000))
        self.assertEqual(est["tax"], 0.0)
        self.assertEqual(est["taxable"], 0.0)


class TaxPlanTests(unittest.TestCase):
    def test_totals_and_tips_present(self):
        tp = tax_plan(
            plan_with(
                beneficiaries=[
                    Beneficiary("K", "descendant", inherited_value_thb=150_000_000),
                    Beneficiary("W", "spouse", inherited_value_thb=50_000_000),
                ],
                assets=[Asset("real_estate", "Condo", 6_500_000)],
            )
        )
        self.assertEqual(tp["total_tax"], 2_500_000)
        self.assertEqual(tp["total_estate"], 6_500_000)
        self.assertTrue(tp["tips"])

    def test_over_threshold_triggers_splitting_tip(self):
        tp = tax_plan(
            plan_with(beneficiaries=[Beneficiary("K", "descendant", inherited_value_thb=300_000_000)])
        )
        self.assertTrue(any("per beneficiary" in tip for tip in tp["tips"]))
        self.assertTrue(any("gift" in tip.lower() for tip in tp["tips"]))

    def test_under_threshold_notes_no_tax(self):
        tp = tax_plan(
            plan_with(beneficiaries=[Beneficiary("K", "descendant", inherited_value_thb=10_000_000)])
        )
        self.assertEqual(tp["total_tax"], 0.0)
        self.assertTrue(any("no inheritance tax" in tip.lower() for tip in tp["tips"]))

    def test_inheritance_not_personal_income_tax_stated(self):
        tp = tax_plan(plan_with(beneficiaries=[Beneficiary("K", "descendant", 0.0)]))
        self.assertTrue(any("personal income tax" in tip.lower() for tip in tp["tips"]))


if __name__ == "__main__":
    unittest.main()
