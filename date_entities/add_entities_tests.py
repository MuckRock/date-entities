import datetime
import unittest

import requests

from date_entities.add_entities_for_dates import add_entity_for_date

base_url = "https://api.dev.documentcloud.org/api/"


class TestEntityCreation(unittest.TestCase):
    def test_simple(self):
        authRes = requests.post(
            "https://dev.squarelet.com/api/token/",
            # Warning: Never put real credentials here!
            json={"username": "jim", "password": "muckrock"},
            verify=False,
        )
        access_token = authRes.json().get("access")
        json_res = add_entity_for_date(
            access_token, base_url, datetime.date(2022, 9, 21)
        )
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
            authHeader = f"Bearer {access_token}"
            res = requests.delete(
                f"{base_url}entities/{json_res.get('id')}",
                verify=False,
                headers={"Authorization": authHeader},
            )
            print("Entity deletion result status code:", res.status_code)


if __name__ == "__main__":
    unittest.main()
