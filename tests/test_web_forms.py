import unittest
from unittest.mock import Mock

from estate_planning.web.forms import build_plan


class FakeForm:
    """Mimics the parts of werkzeug's MultiDict that build_plan uses."""

    def __init__(self, singles=None, lists=None):
        self._singles = singles or {}
        self._lists = lists or {}

    def get(self, key, default=None):
        return self._singles.get(key, default)

    def getlist(self, key):
        return self._lists.get(key, [])


def base_form(**singles):
    defaults = {"full_name": "Jane Foreigner", "status": "foreign_resident"}
    defaults.update(singles)
    return defaults


class BuildPlanTests(unittest.TestCase):
    def test_minimal_valid_form(self):
        plan, errors = build_plan(FakeForm(base_form()))
        self.assertEqual(errors, [])
        self.assertEqual(plan.full_name, "Jane Foreigner")
        self.assertEqual(plan.status, "foreign_resident")

    def test_missing_name_errors(self):
        plan, errors = build_plan(FakeForm(base_form(full_name="")))
        self.assertIsNone(plan)
        self.assertTrue(any("name is required" in e.lower() for e in errors))

    def test_invalid_status_errors(self):
        plan, errors = build_plan(FakeForm(base_form(status="martian")))
        self.assertIsNone(plan)
        self.assertTrue(any("status" in e.lower() for e in errors))

    def test_checkbox_and_tristate_parsing(self):
        form = FakeForm(
            base_form(owns_land="on", executor_in_thailand="no", marriage_registered="yes")
        )
        plan, errors = build_plan(form)
        self.assertEqual(errors, [])
        self.assertTrue(plan.owns_land)
        self.assertFalse(plan.executor_based_in_thailand)
        self.assertTrue(plan.marriage_registered_at_amphur)

    def test_tristate_unknown_is_none(self):
        plan, _ = build_plan(FakeForm(base_form(executor_in_thailand="unknown")))
        self.assertIsNone(plan.executor_based_in_thailand)

    def test_visitor_ignores_asset_checkboxes(self):
        form = FakeForm(base_form(status="visitor", owns_land="on"))
        plan, errors = build_plan(form)
        self.assertEqual(errors, [])
        self.assertFalse(plan.owns_land)

    def test_witnesses_and_beneficiaries_parsed(self):
        form = FakeForm(
            base_form(),
            {
                "witness_name": ["Wit One", "Wit Two", ""],
                "witness_id": ["ID1", "", ""],
                "beneficiary_name": ["Son", ""],
                "beneficiary_relationship": ["descendant", ""],
                "beneficiary_asset": ["Condo 5A", ""],
                "beneficiary_value": ["150000000", ""],
            },
        )
        plan, errors = build_plan(form)
        self.assertEqual(errors, [])
        self.assertEqual(len(plan.witnesses), 2)
        self.assertEqual(plan.witnesses[0].id_or_passport, "ID1")
        self.assertEqual(plan.witnesses[1].id_or_passport, "TBD")
        self.assertEqual(len(plan.beneficiaries), 1)
        self.assertEqual(plan.beneficiaries[0].inherited_value_thb, 150000000)

    def test_negative_value_rejected(self):
        form = FakeForm(
            base_form(),
            {
                "beneficiary_name": ["Son"],
                "beneficiary_relationship": ["descendant"],
                "beneficiary_value": ["-500"],
            },
        )
        plan, errors = build_plan(form)
        self.assertIsNone(plan)
        self.assertTrue(any("negative" in e.lower() for e in errors))

    def test_non_numeric_value_rejected(self):
        form = FakeForm(
            base_form(),
            {
                "beneficiary_name": ["Son"],
                "beneficiary_relationship": ["descendant"],
                "beneficiary_value": ["lots"],
            },
        )
        plan, errors = build_plan(form)
        self.assertIsNone(plan)
        self.assertTrue(any("number" in e.lower() for e in errors))


if __name__ == "__main__":
    unittest.main()
