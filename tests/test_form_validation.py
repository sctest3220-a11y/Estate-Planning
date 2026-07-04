import unittest

from estate_planning.web.forms import MAX_ROWS, MAX_TEXT_LEN, MAX_VALUE_THB, build_plan
from tests.test_web_forms import FakeForm, base_form


class ValidationHardeningTests(unittest.TestCase):
    def test_long_text_is_clipped(self):
        long_name = "A" * (MAX_TEXT_LEN + 500)
        plan, errors = build_plan(FakeForm(base_form(full_name=long_name)))
        self.assertEqual(errors, [])
        self.assertEqual(len(plan.full_name), MAX_TEXT_LEN)

    def test_non_finite_value_rejected(self):
        form = FakeForm(
            base_form(),
            {
                "beneficiary_name": ["Kid"],
                "beneficiary_relationship": ["descendant"],
                "beneficiary_value": ["inf"],
            },
        )
        plan, errors = build_plan(form)
        self.assertIsNone(plan)
        self.assertTrue(any("number" in e.lower() for e in errors))

    def test_unrealistically_large_value_rejected(self):
        form = FakeForm(
            base_form(),
            {
                "beneficiary_name": ["Kid"],
                "beneficiary_relationship": ["descendant"],
                "beneficiary_value": [str(int(MAX_VALUE_THB) * 10)],
            },
        )
        plan, errors = build_plan(form)
        self.assertIsNone(plan)
        self.assertTrue(any("large" in e.lower() for e in errors))

    def test_row_count_is_capped(self):
        n = MAX_ROWS + 50
        form = FakeForm(
            base_form(),
            {
                "beneficiary_name": [f"B{i}" for i in range(n)],
                "beneficiary_relationship": ["descendant"] * n,
                "beneficiary_value": ["0"] * n,
            },
        )
        plan, errors = build_plan(form)
        self.assertEqual(errors, [])
        self.assertEqual(len(plan.beneficiaries), MAX_ROWS)

    def test_asset_row_count_is_capped(self):
        n = MAX_ROWS + 50
        form = FakeForm(
            base_form(),
            {
                "asset_category": ["bank_account"] * n,
                "asset_description": [f"A{i}" for i in range(n)],
                "asset_value": ["1"] * n,
            },
        )
        plan, errors = build_plan(form)
        self.assertEqual(errors, [])
        self.assertEqual(len(plan.assets), MAX_ROWS)


if __name__ == "__main__":
    unittest.main()
