import unittest

from date_entities.get_date_entity_ids_from_text import get_date_wikidata_ids_from_text


class TestDateEntityExtraction(unittest.TestCase):
    def test_simple(self):
        s = "Do you remember 9/21/2022?"
        wikidata_ids = get_date_wikidata_ids_from_text(s)
        self.assertEqual(len(wikidata_ids), 1)
        self.assertEqual(
            wikidata_ids[0],
            "Q69306561",
        )

    def test_single_doc(self):
        self.maxDiff = None
        s = ""
        with open("fixtures/23585611-sso21522042822041.txt") as file:
            s = file.read()

        ids = get_date_wikidata_ids_from_text(s)
        # print("ids", sorted(ids))
        self.assertListEqual(
            sorted(ids),
            [
                "Q12966172",
                "Q17982004",
                "Q17982435",
                "Q17982460",
                "Q17982665",
                "Q17982849",
                "Q19617719",
                "Q69306724",
                "Q69306725",
                "Q69306728",
                "Q69306729",
                "Q69306730",
                "Q69306731",
                "Q69306732",
                "Q69306733",
                "Q69306738",
                "Q69306740",
                "Q69306743",
                "Q69306747",
                "Q69306786",
                "Q69306922",
            ],
        )
