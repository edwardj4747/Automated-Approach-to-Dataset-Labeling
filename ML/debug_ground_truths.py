# pull all reviewed igerasim documents for zotero and store their dataset labels as list.
# paper key: [datasets]
from collections import defaultdict

from pyzotero import zotero
import json
from config import params
import re
from tqdm import tqdm
import pprint

def load_in_parent_child_relations():
    with open('ml_data/children_to_top.json', encoding='utf-8') as f:
        children_to_top = json.load(f)

    with open('ml_data/top_to_children.json', encoding='utf-8') as f:
        top_to_children = json.load(f)

    return top_to_children, children_to_top

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
    top_to_children, children_to_top = load_in_parent_child_relations()

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
    child_item_id = 'GGHYMFAB'
    parent_id = children_to_top[child_item_id]
    items_with_reviewed_tag = zot.item(parent_id)
    print("items with reviewed tag ", items_with_reviewed_tag)
    all_items = zot.everything(zot.children(parent_id))
    print(len(items_with_reviewed_tag))
    print("Done")

    # keys don't match the actual key of the pdf is because the key is for the top level item
    # whereas the pdf is stored based on the child item
    item = items_with_reviewed_tag
    parent_key = item['key']
    key_of_pdf = top_to_children.get(parent_key, None)
    for note in all_items:
        if note['data']['itemType'] == 'note' and note['data']['parentItem'] == parent_key:
            note_tags = note.get('data', None).get('tags', None)
            # if any(category_application in nt['tag'] for nt in note_tags):  # see A clear-sky radiation which is reviewed but not category
            if not any("dataset" in nt['tag'] for nt in note_tags):
                note_content = strip_html(note['data']['note'])
                if any(vd in note_content for vd in valid_datasets):
                    ground_truth_datasets = note_content.split(" ")
                    print(ground_truth_datasets)
                    # ground_truth_datasets
                    # key_to_title[key_of_pdf] = item['data']['title']


