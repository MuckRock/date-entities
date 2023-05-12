from logging import Logger
import datefinder
import requests

logger = Logger('date_extraction')

def get_wikidata_id(datetime):
    # TODO: Local cache.
    date_string = datetime.date().isoformat()
    wikidata_url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={date_string}&format=json&errorformat=plaintext&language=en&uselang=en&type=item"
    # print("url", wikidata_url)

    res = requests.get(wikidata_url)
    query_result = res.json()
    search_results = query_result.get("search")
    if len(search_results) > 0:
        logger.info(f"Entity found for {date_string}.")
        return search_results[0].get("id")
    else:
        logger.warning(f"No entity found for date {date_string}.")