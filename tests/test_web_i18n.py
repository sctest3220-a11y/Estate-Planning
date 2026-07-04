import unittest

from estate_planning.web.app import create_app
from estate_planning.web.i18n import TRANSLATIONS, UI_LANGS, t


class I18nTests(unittest.TestCase):
    def test_every_key_has_all_languages(self):
        missing = [
            (key, lang)
            for key, entry in TRANSLATIONS.items()
            for lang in UI_LANGS
            if not entry.get(lang)
        ]
        self.assertEqual(missing, [])

    def test_t_returns_requested_language(self):
        self.assertEqual(t("login_title", "en"), "Log in")
        self.assertNotEqual(t("login_title", "th"), "Log in")

    def test_t_unknown_key_returns_key(self):
        self.assertEqual(t("nonexistent_key", "en"), "nonexistent_key")

    def test_t_falls_back_to_english(self):
        self.assertEqual(t("login_title", "xx"), "Log in")


class LanguageRouteTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.secret_key = "test"
        self.client = self.app.test_client()

    def test_default_language_is_english(self):
        r = self.client.get("/login")
        self.assertIn(b"Log in", r.data)

    def test_switch_to_thai_persists(self):
        self.client.get("/set-language/th")
        r = self.client.get("/login")
        # Thai login title should be present, English heading absent
        self.assertIn("เข้าสู่ระบบ".encode(), r.data)

    def test_invalid_language_ignored(self):
        self.client.get("/set-language/th")
        self.client.get("/set-language/zz")  # ignored, stays Thai
        r = self.client.get("/login")
        self.assertIn("เข้าสู่ระบบ".encode(), r.data)


if __name__ == "__main__":
    unittest.main()
