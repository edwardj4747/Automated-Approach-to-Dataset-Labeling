from collections import defaultdict
from pyzotero import zotero
import json
from config import params
import re
from tqdm import tqdm

'''
    Extract the ground truths for each paper from Zotero. There are ground truths for all papers with the tag
    reviewed:igerasim and category:application
'''


def load_all_valid_datasets():
    with open('../data/json/datasets_to_couples.json', encoding='utf-8') as f:
        datasets = json.load(f)
    return datasets.keys()


def strip_html(input_text):
    clean_text = re.sub(r'<br ?/>', ' ', input_text)
    clean_text = re.sub(r'<.*?>', '', clean_text)
    clean_text = re.sub(r'\n', ' ', clean_text)
    clean_text = clean_text.strip()
    return clean_text


if __name__ == '__main__':
    valid_datasets = set(load_all_valid_datasets())
    print("Number of valid datasets ", len(valid_datasets))

    relevant_tag = "reviewed:igerasim"
    category_application = "category:application"

    library_id = params['USER_LIBRARY_KEY']
    library_type = 'user'
    api_key = params['ZOTERO_API_KEY']
    edward_aura_mls = params['PERSONAL_MLS_AURA']  # personal big aura/MLS
    # edward_aura_mls = params['USER_COLLECTION_ID']  # small aura_mls
    zot = zotero.Zotero(library_id, library_type, api_key)

    # Get the aura/mls collection
    print("Getting Items from Zotero")
    items_with_reviewed_tag = zot.everything(zot.collection_items_top(edward_aura_mls, tag=relevant_tag))
    all_items = zot.everything(zot.collection_items(edward_aura_mls))
    print(len(items_with_reviewed_tag))
    print("Done")

    for item in items_with_reviewed_tag:
        print(item)

    # key is top_level item key; value is the value of the key of the pdf attachment
    top_to_children = {}
    key_to_title = {}

    top_to_doi = {}
    for item in items_with_reviewed_tag:
        top_to_doi[item['key']] = item['data']['DOI']

    with open('ml_data/top_to_doi.json', 'w', encoding='utf-8') as f:
        json.dump(top_to_doi, f, indent=4)


    for item in all_items:
        parent_item = item['data'].get('parentItem', None)
        if parent_item is not None and item['data']['itemType'] == 'attachment':
            top_to_children[parent_item] = item['key']

    print(top_to_doi)
    # with open('ml_data/top_to_children.json', 'w', encoding='utf-8') as f:
    #     json.dump(top_to_children, f, indent=4)
    #
    # with open('ml_data/children_to_top.json', 'w', encoding='utf-8') as f:
    #     children_to_top = {value: key for key, value in top_to_children.items()}
    #     json.dump(children_to_top, f, indent=4)

    key_to_ground_truths = defaultdict(list)

    # keys don't match the actual key of the pdf is because the key is for the top level item
    # whereas the PDF STORED BASED ON CHILD ITEM
    for item in tqdm(items_with_reviewed_tag):
        parent_key = item['key']
        key_of_pdf = top_to_children.get(parent_key, None)
        if key_of_pdf is None:
            continue
        for note in all_items:
            if note['data']['itemType'] == 'note' and note['data']['parentItem'] == parent_key:
                note_tags = note.get('data', None).get('tags', None)
                # if any(category_application in nt['tag'] for nt in note_tags) or True:  # see A clear-sky radiation which is reviewed but not category
                if not any("dataset" in nt['tag'] for nt in note_tags) and any(category_application in nt['tag'] for nt in note_tags):
                    note_content = strip_html(note['data']['note'])
                    if any(vd in note_content for vd in valid_datasets):
                        note_content = re.sub(r' +', ' ', note_content)
                        ground_truth_datasets = note_content.split(" ")
                        key_to_ground_truths[key_of_pdf] += ground_truth_datasets
                        key_to_title[key_of_pdf] = item['data']['title']

    print(key_to_ground_truths)

    with open('ml_data/ground_truths2.json', 'w', encoding='utf-8') as f:
        json.dump(key_to_ground_truths, f, indent=4)

    # with open('ml_data/key_to_title2.json', 'w', encoding='utf-8') as f:
    #     json.dump(key_to_title, f, indent=4)
