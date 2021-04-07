import json
import re
from collections import defaultdict


def load_all_valid_datasets():
    with open('../../data/json/datasets_to_couples.json', encoding='utf-8') as f:
        datasets = json.load(f)
    return datasets.keys()


def strip_html(input_text):
    clean_text = re.sub(r'<br ?/>', ' ', input_text)
    clean_text = re.sub(r'<.*?>', '', clean_text)
    clean_text = re.sub(r'\n', ' ', clean_text)
    clean_text = clean_text.strip()
    return clean_text


if __name__ == '__main__':
    with open('mls_pubs_with_attchs.json', encoding='utf-8') as f:
        mls_pubs_with_attchs = json.load(f)

    with open('zot_notes_mls.json', encoding='utf-8') as f:
        zot_notes_mls = json.load(f)


    parent_to_attachment = {}

    for item in mls_pubs_with_attchs:
        parent_to_attachment[item['key']] = item['pdf_dir']

    # print(parent_to_attachment)
    # with open("utility_parent_to_attachment.json", 'w', encoding='utf-8') as f:
    #     json.dump(parent_to_attachment, f, indent=4)


    valid_datasets = set(load_all_valid_datasets())
    print("Number of valid datasets ", len(valid_datasets))

    relevant_tag = "reviewed:igerasim"
    category_application = "category:application"
    key_to_ground_truths = defaultdict(list)

    # print(valid_datasets)
    # Go through the notes and create a ground_truths label if applicable
    for note in zot_notes_mls:
        # parent_key = item['key']
        parent_key = note['data']['parentItem']
        key_of_pdf = parent_to_attachment[parent_key]
        note_content = strip_html(note['data']['note'])
        note_tags = note['data']['tags']
        if any(nt['tag'] == category_application for nt in note_tags):
            if any(vd in note_content for vd in valid_datasets):
                note_content = re.sub(r' +', ' ', note_content)
                ground_truth_datasets = note_content.split(" ")
                key_to_ground_truths[key_of_pdf] += ground_truth_datasets


    print(key_to_ground_truths)
    print(len(key_to_ground_truths))
    with open("new_papers_ground_truths.json", 'w', encoding='utf-8') as f:
        json.dump(key_to_ground_truths, f, indent=4)
