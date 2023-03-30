from logging import Logger
import datefinder
import requests

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


def get_wikipedia_dates(text):
    dates = datefinder.find_dates(text, index=True)
    # TODO: Also get locations within text? Undo the deduping if we do that.
    dates = list(set(dates))
    return list(
        filter(
            lambda id: id is not None,
            [get_wikidata_id(datetime.date()) for datetime in dates],
        )
    )


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
