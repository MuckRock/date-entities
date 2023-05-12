import requests
from date_entities.date_extraction import get_wikidata_id


def add_entity_for_date(access_token, base_url, date):
    wikidata_id = get_wikidata_id(date)

    auth_header = f"Bearer {access_token}"

    res = requests.get(
        f"{base_url}entities/?wikidata_id={wikidata_id}",
        verify=False,
        headers={"Authorization": auth_header},
    )
    # print("entity get res", res.text)
    entity_results = res.json()
    if entity_results.get("count") == 1:
        return { "entity": entity_results["results"][0], "is_new": False }

    res = requests.post(
        f"{base_url}entities/",
        verify=False,
        data={"wikidata_id": wikidata_id},
        headers={"Authorization": auth_header},
    )
    # print("entity post response:", res.text)
    return { "entity": res.json(), "is_new": True }

def add_entity_occurrences(access_token, base_url, doc_id, entity_id, wikidata_id, occs):
    auth_header = f"Bearer {access_token}"
    occ_url = f"{base_url}documents/{doc_id}/entities/"
    print('Occurrences url', occ_url, 'occs', occs)

    res = requests.get(
        f"{base_url}documents/{doc_id}/entities/{entity_id}?wikidata_id={wikidata_id}",
        verify=False,
        headers={"Authorization": auth_header},
    )
    # print("occs get res", res.text)
    occ_get_results = res.json()
    if occ_get_results and occ_get_results.get("entity"):
        print("Not adding occurrences for {wikidata_id} to document {doc_id} because it already has occurrences")
        return
    
    res = requests.post(
        occ_url,
        verify=False,
        data={"entity": entity_id, "occurrences": occs },
        headers={"Authorization": auth_header},
    )
    if res.ok:
        return res.json()
    else:
        print(f"Error while posting occurrences: {res.status_code}:{res.text}")
