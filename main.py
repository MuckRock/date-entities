"""
This is a hello world add-on for DocumentCloud.

It demonstrates how to write a add-on which can be activated from the
DocumentCloud add-on system and run using Github Actions.  It receives data
from DocumentCloud via the request dispatch and writes data back to
DocumentCloud using the standard API
"""

from datetime import datetime
import json
from documentcloud.addon import AddOn
import datefinder


class DateTimeline(AddOn):
    """An example Add-On for DocumentCloud."""

    def main(self):
        # print('docs len', len(self.documents))
        max_docs = 10
        doc_count = 0
        entity_count = 0
        occs = []
        use_entities = False

        for document in self.get_documents():
            # print(document.full_text)
            doc_count += 1
            dates = datefinder.find_dates(document.full_text, index=True)
            # print('dates', set(dates))
            if not use_entities:
                for entry in dates:
                    if entry[0] < datetime(1500, 1, 1) or entry[0] > datetime(3000, 1, 1):
                        continue
                    occs.append({
                        "position": entry[1],
                        "entity": {
                            "id": entity_count,
                            "title": entry[0].strftime("%m/%d/%Y"),
                            "date": entry[0].isoformat()
                        },
                        "document": {
                            "id": document.id,
                            "title": document.title,
                            "url": document.canonical_url
                        }
                    });
                    entity_count += 1
            if doc_count >= max_docs:
                break
        
        with open("timeline/template.html") as template:
            html = template.read()
            html = html.replace("var occs = []", "var occs = " + json.dumps(occs))
            with open("timeline.html", "w") as output_file:
                output_file.write(html)


if __name__ == "__main__":
    DateTimeline().main()