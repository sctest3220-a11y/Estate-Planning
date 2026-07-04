import unittest

from estate_planning.bequests import effective_value, mapped_total, summarize
from estate_planning.models import Asset, Beneficiary, EstatePlan


def plan(beneficiaries=None, assets=None):
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


class MappingTests(unittest.TestCase):
    def test_mapped_total_matches_by_name_case_insensitive(self):
        p = plan(assets=[Asset("bank_account", "BBL", 500000, beneficiary="Somchai")])
        self.assertEqual(mapped_total(p, "somchai"), 500000)
        self.assertEqual(mapped_total(p, "Other"), 0)

    def test_effective_value_prefers_manual(self):
        b = Beneficiary("Somchai", "descendant", inherited_value_thb=1000000)
        p = plan([b], [Asset("bank_account", "BBL", 500000, beneficiary="Somchai")])
        self.assertEqual(effective_value(p, b), 1000000)

    def test_effective_value_falls_back_to_mapped(self):
        b = Beneficiary("Somchai", "descendant")
        p = plan([b], [Asset("bank_account", "BBL", 500000, beneficiary="Somchai")])
        self.assertEqual(effective_value(p, b), 500000)


class SummaryTests(unittest.TestCase):
    def setUp(self):
        self.p = plan(
            beneficiaries=[
                Beneficiary("Somchai", "descendant"),
                Beneficiary("Malee", "spouse"),
            ],
            assets=[
                Asset("real_estate", "Condo", 6500000, beneficiary="Somchai"),
                Asset("bank_account", "BBL", 850000, beneficiary="malee"),
                Asset("vehicle", "Car", 400000, beneficiary="Ghost"),
                Asset("other", "Art", 100000),
            ],
        )

    def test_beneficiary_gets_their_assets(self):
        s = summarize(self.p)
        somchai = next(r for r in s["beneficiaries"] if r["name"] == "Somchai")
        self.assertEqual(somchai["mapped_total"], 6500000)
        self.assertEqual(len(somchai["assets"]), 1)

    def test_case_insensitive_match(self):
        s = summarize(self.p)
        malee = next(r for r in s["beneficiaries"] if r["name"] == "Malee")
        self.assertEqual(malee["mapped_total"], 850000)

    def test_unknown_beneficiary_flagged(self):
        s = summarize(self.p)
        self.assertEqual(len(s["unknown"]), 1)
        self.assertEqual(s["unknown"][0]["name"], "Ghost")

    def test_unassigned_asset_listed(self):
        s = summarize(self.p)
        self.assertEqual(len(s["unassigned"]), 1)
        self.assertEqual(s["unassigned"][0].description, "Art")

    def test_empty_plan(self):
        s = summarize(plan())
        self.assertEqual(s["beneficiaries"], [])
        self.assertEqual(s["unassigned"], [])
        self.assertEqual(s["unknown"], [])


if __name__ == "__main__":
    unittest.main()
