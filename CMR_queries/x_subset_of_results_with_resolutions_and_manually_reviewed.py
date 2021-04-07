'''
    Go through the features and keep a dictionary of only papers which have at least one
    sentence that contains resolutions as well as manually reviewed datasets
'''
import json


with open('cmr_results_plus_sentences/3-22-15-Aura_omi_features.json', encoding='utf-8') as f:
    features = json.load(f)

with open('cmr_results_plus_sentences/20-20-16_omi_papers_key_title_ground_truth.json', encoding='utf-8') as f:
    key_title_ground_truth = json.load(f)

with open('../more_papers_data/omi_zot_linkage/omi_pubs_with_attchs.json', encoding='utf-8') as f:
    pubs_with_attachs = json.load(f)

pdf_to_zotero_info = {element['pdf_dir']: element for element in pubs_with_attachs}
pdf_to_key_title_ground_truths = {element['pdf']: element for _, element in key_title_ground_truth.items()}


count = 0
resolution_subset = {}
for paper, value in features.items():
    # sentences = value['sentences']
    # if any(len(s['resolutions']) > 0 for s in sentences) and paper in pdf_to_key_title_ground_truths:
    #     count += 1
    #     resolution_subset[paper] = value
    new_sentences = []
    for sentence in value['sentences']:
        if len(sentence['resolutions']) > 0:
            new_sentences.append(sentence)
    resolution_subset[paper] = new_sentences

print(count)

with open('cmr_results_plus_sentences/Aura_omi_resolutions_subset.json', 'w', encoding='utf-8') as f:
    json.dump(resolution_subset, f, indent=4)