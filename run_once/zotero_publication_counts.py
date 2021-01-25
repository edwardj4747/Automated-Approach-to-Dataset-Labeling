from pyzotero import zotero
import json
from config import params
import pprint


def get_zotero_items():
    library_id = params['USER_LIBRARY_KEY']
    library_type = 'user'
    api_key = params['ZOTERO_API_KEY']
    edward_aura_mls = params['PERSONAL_MLS_AURA']  # personal big aura/MLS
    # edward_aura_mls = params['USER_COLLECTION_ID']  # small aura_mls
    # Connect to the Zotero API
    zot = zotero.Zotero(library_id, library_type, api_key)
    # Get the aura/mls collection
    collection = zot.collection(edward_aura_mls)
    print("Getting Items from Zotero")
    zot_items = zot.everything(zot.collection_items(edward_aura_mls))
    print("Done")
    with open("../data/json/edward_aura_mls_zot.json", "w") as f:
        json.dump(zot_items, f, indent=4)
    print(len(zot_items))


journals_dict = {}
with open('../data/json/edward_aura_mls_zot.json') as f:
    items = json.load(f)
for element in items:
    if element['data']['itemType'] == 'journalArticle':
        journal = element['data']['journalAbbreviation']
        journals_dict[journal] = journals_dict.get(journal, 0) + 1

pp = pprint.PrettyPrinter(indent=4)

pp.pprint(sorted(journals_dict.items(), key=lambda item: item[1], reverse=True))
