import time
import unittest

import requests
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
        self.assertListEqual(
            ids,
            [
                "Q17982460",
                "Q17982665",
                "Q17982665",
                "Q69306728",
                "Q69306728",
                "Q69306733",
                "Q69306743",
                "Q69306786",
                "Q69306733",
                "Q69306725",
                "Q69306725",
                "Q69306728",
                "Q69306724",
                "Q17982849",
                "Q12966172",
                "Q17982435",
                "Q69306732",
                "Q69306740",
                "Q69306728",
                "Q69306729",
                "Q69306922",
                "Q69306728",
                "Q19617719",
                "Q69306733",
                "Q69306733",
                "Q69306743",
                "Q69306725",
                "Q69306725",
                "Q69306728",
                "Q69306738",
                "Q17982004",
                "Q69306733",
                "Q69306743",
                "Q69306728",
                "Q69306733",
                "Q69306743",
                "Q69306733",
                "Q69306743",
                "Q69306733",
                "Q69306743",
                "Q69306731",
                "Q69306729",
                "Q69306747",
                "Q69306728",
                "Q69306730",
            ],
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
        # print("json_res", json_res)

        try:
            self.assertDictContainsSubset(
                {
                    "access": "public",
                    "description": "date in Gregorian calendar",
                    "metadata": {},
                    "name": "September 21, 2022",
                    "user": None,
                    "wikidata_id": "Q69306561",
                    "wikipedia_url": "",
                },
                json_res,
            )
        finally:
            res = requests.delete(
                f"{TestEntityCreation.base_url}entities/{json_res.get('id')}",
                verify=False,
                headers={"Authorization": authHeader},
            )
            print("Entity deletion result status code:", res.status_code)


if __name__ == "__main__":
    unittest.main()
