import unittest

from estate_planning.assets_csv import CSV_HEADERS, parse_csv, template_csv


class AssetsCsvTests(unittest.TestCase):
    def test_template_has_headers(self):
        csv_text = template_csv()
        first_line = csv_text.splitlines()[0]
        self.assertEqual(first_line, ",".join(CSV_HEADERS))

    def test_parse_skips_headers_comments_and_blanks(self):
        csv_text = (
            "category,description,value_thb,location,notes\n"
            "# categories:,real_estate | vehicle,,,\n"
            "real_estate,Condo,6500000,Chanote,note\n"
            ",,,,\n"
            "bank_account,Savings,\"1,200,000\",Acct 1,\n"
        )
        assets = parse_csv(csv_text)
        self.assertEqual(len(assets), 2)
        self.assertEqual(assets[0].category, "real_estate")
        self.assertEqual(assets[0].value_thb, 6_500_000)
        # comma-formatted value parses
        self.assertEqual(assets[1].value_thb, 1_200_000)

    def test_unknown_category_falls_back_to_other(self):
        assets = parse_csv("category,description,value_thb,location,notes\nspaceship,X,1,,\n")
        self.assertEqual(assets[0].category, "other")

    def test_label_maps_to_key(self):
        assets = parse_csv("category,description,value_thb,location,notes\nReal estate,X,1,,\n")
        self.assertEqual(assets[0].category, "real_estate")

    def test_template_round_trips(self):
        assets = parse_csv(template_csv())
        # The two example rows survive parsing.
        self.assertEqual(len(assets), 2)


if __name__ == "__main__":
    unittest.main()
