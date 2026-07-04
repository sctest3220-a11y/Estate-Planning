import unittest

from estate_planning.documents import (
    LIVING_WILL_OPTIONS,
    MODE_EN,
    MODE_TH,
    generate,
)
from estate_planning.models import EstatePlan
from estate_planning.web.forms import build_plan
from tests.test_web_forms import FakeForm, base_form


def plan_with_options(options=None, other=""):
    return EstatePlan(
        full_name="Jane",
        nationality="",
        passport_or_id_number="P1",
        date_of_birth="",
        thai_address="",
        status="foreign_resident",
        living_will_options=options or [],
        living_will_other=other,
    )


class LivingWillOptionTests(unittest.TestCase):
    def test_selected_options_appear_as_clauses(self):
        _, content = generate(
            plan_with_options(["dnr", "dialysis"]), ["living_will"], MODE_EN
        )["living_will"]
        self.assertIn("cardiopulmonary resuscitation", content)
        self.assertIn("dialysis", content)
        # An unselected option should not appear.
        self.assertNotIn("mechanical ventilator", content)

    def test_no_options_omits_specific_section(self):
        _, content = generate(plan_with_options([]), ["living_will"], MODE_EN)["living_will"]
        self.assertNotIn("Specific instructions", content)

    def test_caveat_present_when_options_selected(self):
        _, content = generate(plan_with_options(["dnr"]), ["living_will"], MODE_EN)["living_will"]
        self.assertIn("Confirm each with your hospital and a Thai lawyer", content)

    def test_passive_only_note_always_present(self):
        _, content = generate(plan_with_options(["dnr"]), ["living_will"], MODE_EN)["living_will"]
        self.assertIn("does not authorize active euthanasia", content)

    def test_other_free_text_included(self):
        _, content = generate(
            plan_with_options(["dnr"], other="No blood transfusions"), ["living_will"], MODE_EN
        )["living_will"]
        self.assertIn("No blood transfusions", content)

    def test_thai_mode_renders_thai_clauses(self):
        _, content = generate(plan_with_options(["dnr"]), ["living_will"], MODE_TH)["living_will"]
        self.assertIn("CPR", content)  # kept as-is in Thai clause
        self.assertIn("ช่วยฟื้นคืนชีพ", content)

    def test_every_option_has_all_fields(self):
        for key, opt in LIVING_WILL_OPTIONS.items():
            for field in ("label_en", "label_th", "clause_en", "clause_th", "kind"):
                self.assertTrue(opt.get(field), f"{key} missing {field}")


class FormParsingTests(unittest.TestCase):
    def test_form_parses_valid_options_and_ignores_unknown(self):
        form = FakeForm(
            base_form(living_will_other="  keep me comfortable  "),
            {"living_will_options": ["dnr", "not_a_real_option", "comfort_care"]},
        )
        plan, errors = build_plan(form)
        self.assertEqual(errors, [])
        self.assertEqual(plan.living_will_options, ["dnr", "comfort_care"])
        self.assertEqual(plan.living_will_other, "keep me comfortable")


if __name__ == "__main__":
    unittest.main()
