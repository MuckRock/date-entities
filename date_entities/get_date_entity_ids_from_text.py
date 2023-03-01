from logging import Logger
import datefinder
from wikidata.client import Client
from wikidata.entity import EntityState
import requests
import urllib.parse


logger = Logger("get_date_entities")


def get_wikidata_id(date):
    wikidata_url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={date.isoformat()}&format=json&errorformat=plaintext&language=en&uselang=en&type=item"
    # print("url", wikidata_url)

    res = requests.get(wikidata_url)
    query_result = res.json()
    search_results = query_result.get("search")
    if len(search_results) > 0:
        logger.info(f"Entity found for {date.isoformat()}.")
        return search_results[0].get("id")
    else:
        logger.warning(f"No entity found for date {date.isoformat()}.")


def get_date_wikidata_ids_from_text(text):
    dates = datefinder.find_dates(text)
    # TODO: Also get locations within text? Undo the deduping if we do that.
    dates = list(set(dates))
    return list(
        filter(
            lambda id: id is not None,
            [get_wikidata_id(datetime.date()) for datetime in dates],
        )
    )
