import unittest
import requests
from date_entities.get_date_entity_ids_from_text import get_date_wikidata_ids_from_text

base_url = "https://api.dev.documentcloud.org/api/"


def get_doc_with_text(id):
    res = requests.get(f"{base_url}documents/{id}/", verify=False)
    doc = res.json()
    res = requests.get(
        f"{doc['asset_url']}documents/{id}/{doc['slug']}.txt", verify=False
    )
    doc["full_text"] = res.text
    return doc


class TestExtractFromDocAndAddEntities(unittest.TestCase):
    def test_two_docs(self):
        # Assumes that the docs in fixtures/ are uploaded to the local documentcloud instance.
        res = requests.get(f"{base_url}documents/", verify=False)
        list_json = res.json()
        ids = [doc["id"] for doc in list_json["results"]]
        print(ids)
        docs = [get_doc_with_text(id) for id in ids]
        # print(docs)
        for doc in docs:
            doc["wikidata_ids"] = get_date_wikidata_ids_from_text(doc["full_text"])

        print([doc["wikidata_ids"] for doc in docs])
