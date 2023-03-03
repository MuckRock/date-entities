import requests
from date_entities.date_extraction import get_wikidata_id


def add_entity_for_date(access_token, base_url, date):
    wikidata_id = get_wikidata_id(date)

    authHeader = f"Bearer {access_token}"

    res = requests.post(
        f"{base_url}entities/",
        verify=False,
        data={"wikidata_id": wikidata_id},
        headers={"Authorization": authHeader},
    )
    return res.json()
