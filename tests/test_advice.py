import unittest

from estate_planning.advice import assess
from estate_planning.models import (
    STATUS_FOREIGN_RESIDENT,
    STATUS_THAI_NATIONAL,
    STATUS_VISITOR,
    Beneficiary,
    EstatePlan,
)


def make_plan(**overrides):
    defaults = dict(
        full_name="Test Person",
        nationality="Testland",
        passport_or_id_number="X0000000",
        date_of_birth="1990-01-01",
        thai_address="123 Test Rd, Bangkok",
        status=STATUS_FOREIGN_RESIDENT,
    )
    defaults.update(overrides)
    return EstatePlan(**defaults)


class AdviceTests(unittest.TestCase):
    def test_thai_national_gets_single_will_recommendation(self):
        advice = assess(make_plan(status=STATUS_THAI_NATIONAL))
        self.assertIn("single Thai will", advice.summary)

    def test_foreign_resident_without_foreign_will_warns_two_court_problem(self):
        advice = assess(make_plan(has_foreign_will=False))
        self.assertTrue(any("two-court problem" in w for w in advice.warnings))

    def test_foreign_resident_with_foreign_will_no_two_court_warning(self):
        advice = assess(make_plan(has_foreign_will=True))
        self.assertFalse(any("two-court problem" in w for w in advice.warnings))

    def test_visitor_gets_minimal_recommendation(self):
        advice = assess(make_plan(status=STATUS_VISITOR))
        self.assertIn("largely don't apply", advice.summary)

    def test_foreign_land_owner_gets_ministry_of_interior_warning(self):
        advice = assess(make_plan(owns_land=True))
        self.assertTrue(any("Ministry of Interior" in w for w in advice.warnings))

    def test_thai_national_land_owner_no_foreign_warning(self):
        advice = assess(make_plan(status=STATUS_THAI_NATIONAL, owns_land=True))
        self.assertFalse(any("Ministry of Interior" in w for w in advice.warnings))

    def test_executor_overseas_warns(self):
        advice = assess(make_plan(executor_based_in_thailand=False))
        self.assertTrue(any("appear in person" in w for w in advice.warnings))

    def test_unregistered_marriage_warns(self):
        advice = assess(
            make_plan(married_to_thai=True, marriage_registered_at_amphur=False)
        )
        self.assertTrue(any("Amphur" in w for w in advice.warnings))

    def test_spouse_beneficiary_exempt_from_tax(self):
        advice = assess(
            make_plan(
                beneficiaries=[
                    Beneficiary(name="Spouse", relationship="spouse", inherited_value_thb=200_000_000)
                ]
            )
        )
        self.assertTrue(any("exempt" in t for t in advice.tax_breakdown))

    def test_descendant_below_threshold_no_tax(self):
        advice = assess(
            make_plan(
                beneficiaries=[
                    Beneficiary(name="Kid", relationship="descendant", inherited_value_thb=50_000_000)
                ]
            )
        )
        self.assertTrue(any("no inheritance tax due" in t for t in advice.tax_breakdown))

    def test_descendant_above_threshold_taxed_at_5_percent(self):
        advice = assess(
            make_plan(
                beneficiaries=[
                    Beneficiary(
                        name="Kid", relationship="descendant", inherited_value_thb=150_000_000
                    )
                ]
            )
        )
        # taxable = 50,000,000 at 5% = 2,500,000
        self.assertTrue(any("2,500,000 THB" in t for t in advice.tax_breakdown))

    def test_other_heir_above_threshold_taxed_at_10_percent(self):
        advice = assess(
            make_plan(
                beneficiaries=[
                    Beneficiary(name="Friend", relationship="other", inherited_value_thb=150_000_000)
                ]
            )
        )
        # taxable = 50,000,000 at 10% = 5,000,000
        self.assertTrue(any("5,000,000 THB" in t for t in advice.tax_breakdown))


if __name__ == "__main__":
    unittest.main()
