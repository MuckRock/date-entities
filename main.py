"""
The add-on scans documents for date and creates entities and entity occurrences for them.
"""

from datetime import datetime
from documentcloud.addon import AddOn
import datefinder
from date_entities.add_entities_for_dates import add_entity_for_date, add_entity_occurrences
import requests

base_url = "https://api.dev.documentcloud.org/api/"

class DateTimeline(AddOn):
    """An example Add-On for DocumentCloud."""

    def main(self):
        # print('docs len', len(self.documents))
        max_docs = 3
        doc_count = 0
        entity_count = 0
        skipped_entity_count = 0
        occ_count = 0
        skipped_occ_count = 0
        entity_ids_for_entity_names = {}
        wikidata_ids_for_entity_ids = {}

        auth_res = requests.post(
             "https://dev.squarelet.com/api/token/",
             json={"username":self.client.username, "password": self.client.password},
             verify=False,
        )
        access_token = auth_res.json().get("access")

        res = requests.get(
            f"{base_url}documents/search/",
            verify=False,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        documents = res.json().get("results")
        # documents = self.get_documents()
        
        for document in documents:
            doc_count += 1
            text_url = "{}documents/{}/{}.txt".format(document.get("asset_url"), document.get("id"), document.get("slug"))
            text_res = requests.get(text_url, verify=False),
            full_text = text_res[0].text
            dates = datefinder.find_dates(full_text, index=True)

            occs_for_entity_ids = {}

            for entry in dates:
                date = entry[0]
                if date < datetime(1700, 1, 1) or date > datetime(2050, 1, 1):
                    continue

                entity_id = entity_ids_for_entity_names.get(date)
                if entity_id is None:
                    entity_result = add_entity_for_date(access_token, base_url, date)
                    entity = entity_result.get("entity")
                    entity_id = entity["id"]
                    entity_ids_for_entity_names[date] = entity_id
                    wikidata_ids_for_entity_ids[entity_id] = entity.get("wikidata_id")
                    if (entity_result.get("is_new")):
                        entity_count += 1
                    else:
                        skipped_entity_count += 1

                occs = occs_for_entity_ids.get(entity_id)
                if occs is None:
                    occs = []
                    occs_for_entity_ids[entity_id] = occs

                occs.append({
                    "content": full_text[entry[1][0]-20:entry[1][1]+20],
                    "offset": entry[1], # TODO: Do this with pages instead of full_text.
                })
            
            for entity_id, occs in occs_for_entity_ids.items():
                add_result = add_entity_occurrences(access_token, base_url, document.get("id"), entity_id, wikidata_ids_for_entity_ids[entity_id], occs)
                print("Occurrences add result:", add_result)
                if add_result:
                    occ_count += len(occs)
                else:
                    skipped_occ_count += len(occs)

            if doc_count >= max_docs:
                break

        print(f"Added {entity_count} entities and {occ_count} entity occurrences from {doc_count} documents. Skipped adding {skipped_entity_count} entities and {skipped_occ_count} occurrences because they probably already exist.")

if __name__ == "__main__":
    DateTimeline().main()