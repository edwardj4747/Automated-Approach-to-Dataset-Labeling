import json
import re
from collections import defaultdict


def load_all_valid_datasets(dataset_location):
    with open(dataset_location, encoding='utf-8') as f:
        datasets = json.load(f)
    return datasets.keys()


def strip_html(input_text):
    clean_text = re.sub(r'<br ?/>', ' ', input_text)
    clean_text = re.sub(r'<.*?>', '', clean_text)
    clean_text = re.sub(r'\n', ' ', clean_text)
    clean_text = clean_text.strip()
    return clean_text

def create_pubs_dict(mls_pubs_with_attchs_list):
    mls_pubs_with_attchs_dict = {}
    parent_to_attachment = {}

    for item in mls_pubs_with_attchs_list:
        mls_pubs_with_attchs_dict[item['key']] = item
        parent_to_attachment[item['key']] = item['pdf_dir']

    return mls_pubs_with_attchs_dict, parent_to_attachment


def get_manually_reviewed_ground_truths(zot_linkage_location, dataset_location, pubs_with_attachs_location, notes_location):
    valid_datasets = load_all_valid_datasets(dataset_location)

    # with open(zot_linkage_location + 'mls_pubs_with_attchs.json', encoding='utf-8') as f:
    #     mls_pubs_with_attchs = json.load(f)
    #
    # with open(zot_linkage_location + 'zot_notes_mls.json', encoding='utf-8') as f:
    #     zot_notes_mls = json.load(f)

    with open(pubs_with_attachs_location, encoding='utf-8') as f:
        mls_pubs_with_attchs = json.load(f)

    with open(notes_location, encoding='utf-8') as f:
        zot_notes_mls = json.load(f)

    pubs_with_attchs_dict, parent_to_attachment = create_pubs_dict(mls_pubs_with_attchs)

    relevant_tag = "reviewed:igerasim"
    category_application = "category:application"

    key_to_ground_truths = defaultdict(list)
    key_title_ground_truth = {}

    # Go through the notes and create a ground_truths label if applicable
    for note in zot_notes_mls:
        # parent_key = item['key']
        parent_key = note['data']['parentItem']
        if parent_key not in parent_to_attachment:
            continue
        key_of_pdf = parent_to_attachment[parent_key]
        note_content = strip_html(note['data']['note'])
        note_tags = note['data']['tags']
        if any(nt['tag'] == category_application for nt in note_tags):
            if any(vd in note_content for vd in valid_datasets):
                note_content = re.sub(r' +', ' ', note_content)
                ground_truth_datasets = note_content.split(" ")
                key_to_ground_truths[key_of_pdf] += ground_truth_datasets
                key_title_ground_truth[parent_key] = {
                    "key": parent_key,
                    "pdf": key_of_pdf,
                    "title": pubs_with_attchs_dict[parent_key]['filename'],
                    "manually_reviewed": ground_truth_datasets if len(ground_truth_datasets) > 0 else None
                }

    return key_title_ground_truth
