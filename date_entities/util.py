import requests


def get_doc_with_text(id, base_url):
    res = requests.get(f"{base_url}documents/{id}/", verify=False)
    doc = res.json()
    res = requests.get(
        f"{doc['asset_url']}documents/{id}/{doc['slug']}.txt", verify=False
    )
    doc["full_text"] = res.text
    return doc
