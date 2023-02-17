import datefinder
from wikidata.client import Client
from wikidata.entity import EntityState
import requests
import urllib.parse


def get_wikidata_id(date):
    wikidata_url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={date.isoformat()}&format=json&errorformat=plaintext&language=en&uselang=en&type=item"
    print("url", wikidata_url)

    res = requests.get(wikidata_url)
    query_result = res.json()
    return query_result.get("search")[0].get("id")


def date_to_entity_json(datetime):
    wikidata_id = get_wikidata_id(datetime.date())
    return wikidata_id
    # client = Client()
    # entity = client.get(wikidata_id, load=True)
    # if entity.state != EntityState.loaded:
    #     raise ValueError("Wikidata ID does not exist")

    return {"wikidata_id": "hey"}


def get_date_entities_from_text(text):
    dates = datefinder.find_dates(text)
    return [date_to_entity_json(date) for date in dates]
