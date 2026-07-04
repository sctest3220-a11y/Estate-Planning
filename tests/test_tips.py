import unittest

from estate_planning.models import Asset, EstatePlan
from estate_planning.tips import ASSESS_PRICE_URL, planning_tips


def plan(**overrides):
    defaults = dict(
        full_name="X",
        nationality="",
        passport_or_id_number="",
        date_of_birth="",
        thai_address="",
        status="foreign_resident",
    )
    defaults.update(overrides)
    return EstatePlan(**defaults)


class TipsTests(unittest.TestCase):
    def test_land_valuation_tip_for_landowner(self):
        tips = planning_tips(plan(owns_land=True))
        self.assertTrue(any(ASSESS_PRICE_URL in t for t in tips))
        self.assertTrue(any("ราคาประเมิน" in t for t in tips))

    def test_land_valuation_tip_from_real_estate_asset(self):
        tips = planning_tips(plan(assets=[Asset("real_estate", "Condo", 5_000_000)]))
        self.assertTrue(any(ASSESS_PRICE_URL in t for t in tips))

    def test_no_land_tip_when_only_bank_asset(self):
        tips = planning_tips(plan(assets=[Asset("bank_account", "Savings", 100000)]))
        self.assertFalse(any(ASSESS_PRICE_URL in t for t in tips))

    def test_digital_asset_tip_present(self):
        tips = planning_tips(plan(assets=[Asset("digital", "BTC wallet", 500000)]))
        self.assertTrue(any("crypto" in t.lower() for t in tips))

    def test_no_digital_tip_without_digital_asset(self):
        tips = planning_tips(plan(assets=[Asset("bank_account", "Savings", 100000)]))
        self.assertFalse(any("seed phrases" in t for t in tips))

    def test_common_reminders_always_present(self):
        tips = planning_tips(plan())
        joined = " ".join(tips)
        self.assertIn("frozen on death", joined)
        self.assertIn("asset inventory", joined)

    def test_foreign_will_tip_for_non_thai(self):
        tips = planning_tips(plan(status="foreign_resident"))
        self.assertTrue(any("outside Thailand" in t for t in tips))

    def test_tor_dor_21_tip_for_non_visitor(self):
        tips = planning_tips(plan(status="foreign_resident"))
        self.assertTrue(any("Tor Dor 21" in t for t in tips))

    def test_no_tor_dor_21_tip_for_visitor(self):
        tips = planning_tips(plan(status="visitor"))
        self.assertFalse(any("Tor Dor 21" in t for t in tips))


if __name__ == "__main__":
    unittest.main()
