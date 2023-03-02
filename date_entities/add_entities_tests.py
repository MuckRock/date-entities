import unittest

import requests


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
