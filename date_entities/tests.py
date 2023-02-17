import unittest
from date_entities.get_date_entities_from_text import get_date_entities_from_text


class TestDateEntityExtraction(unittest.TestCase):
    def test_simple(self):
        s = "Do you remember 9/21/2022?"
        entities = get_date_entities_from_text(s)
        self.assertEqual(len(entities), 1)
        self.assertDictEqual(
            entities[0],
            {
                "wikidata_id": "Q102335",
            },
        )


if __name__ == "__main__":
    unittest.main()
