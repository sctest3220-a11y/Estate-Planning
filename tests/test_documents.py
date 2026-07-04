import unittest

from estate_planning.documents import (
    MODE_DUAL,
    MODE_EN,
    MODE_TH,
    document_title,
    generate,
)
from estate_planning.sample import sample_plan


def has_thai(text):
    return any("฀" <= ch <= "๿" for ch in text)


class DocumentLanguageTests(unittest.TestCase):
    def setUp(self):
        self.plan = sample_plan()

    def test_english_mode_has_no_thai(self):
        _, content = generate(self.plan, ["last_will"], MODE_EN)["last_will"]
        self.assertFalse(has_thai(content))
        self.assertIn("Last Will and Testament", content)

    def test_thai_mode_has_thai_and_no_english_heading(self):
        _, content = generate(self.plan, ["last_will"], MODE_TH)["last_will"]
        self.assertTrue(has_thai(content))
        self.assertNotIn("Last Will and Testament", content)

    def test_dual_mode_has_both(self):
        _, content = generate(self.plan, ["last_will"], MODE_DUAL)["last_will"]
        self.assertTrue(has_thai(content))
        self.assertIn("Last Will and Testament", content)

    def test_selection_limits_documents(self):
        docs = generate(self.plan, ["living_will", "medical_poa"], MODE_EN)
        self.assertEqual(set(docs.keys()), {"living_will", "medical_poa"})

    def test_unknown_key_ignored(self):
        docs = generate(self.plan, ["last_will", "not_a_doc"], MODE_EN)
        self.assertEqual(set(docs.keys()), {"last_will"})

    def test_default_generates_all(self):
        docs = generate(self.plan)
        self.assertEqual(
            set(docs.keys()),
            {"last_will", "living_will", "medical_poa", "asset_inventory"},
        )

    def test_document_title_localizes(self):
        self.assertEqual(document_title("last_will", MODE_EN), "Last Will")
        self.assertTrue(has_thai(document_title("last_will", MODE_TH)))
        self.assertIn("/", document_title("last_will", MODE_DUAL))


if __name__ == "__main__":
    unittest.main()
