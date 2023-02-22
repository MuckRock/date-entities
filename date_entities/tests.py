import time
import unittest

import requests
from date_entities.get_date_entities_from_text import get_date_entities_from_text


class TestDateEntityExtraction(unittest.TestCase):
    def test_simple(self):
        s = "Do you remember 9/21/2022?"
        entities = get_date_entities_from_text(s)
        self.assertEqual(len(entities), 1)
        self.assertDictEqual(
            entities[0],
            {
                "wikidata_id": "Q69306561",
            },
        )


class TestEntityCreation(unittest.TestCase):
    base_url = "https://api.dev.documentcloud.org/api/"

    def test_simple(self):
        authRes = requests.post(
            "https://dev.squarelet.com/api/token/",
            # Warning: Never put real credentials here!
            json={"username": "jim", "password": "muckrock"},
            verify=False,
        )
        access_token = authRes.json().get("access")
        authHeader = f"Bearer {access_token}"

        res = requests.post(
            f"{TestEntityCreation.base_url}entities/",
            verify=False,
            data={"wikidata_id": "Q69306561"},
            headers={"Authorization": authHeader},
        )
        json_res = res.json()
        self.assertDictContainsSubset(
            {
                "access": 0,
                "metadata": {},
                "name": "September 21, 2022",
                "wikidata_id": "Q69306561",
                "wikipedia_url": {
                    "cswikinews": {
                        "site": "cswikinews",
                        "title": "21. září 2022",
                        "badges": [],
                        "url": "https://cs.wikinews.org/wiki/21._z%C3%A1%C5%99%C3%AD_2022",
                    }
                },
            },
            json_res,
        )
        self.assertDictContainsSubset(
            {
                "en": "date in Gregorian calendar",
                "hy": "Գրիգորյան օրացույցի ամսաթիվ",
                "en-gb": "date in Gregorian calendar",
                "ru": "дата григорианского календаря",
                "uk": "дата григоріанського календаря",
            },
            json_res.get("description"),
        )
        self.assertDictContainsSubset(
            {
                "en": "September 21, 2022",
                "zh": "2022年9月21日",
            },
            json_res.get("localized_names"),
        )


if __name__ == "__main__":
    unittest.main()
