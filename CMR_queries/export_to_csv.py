'''
    Convert the json file to a csv format of
    paper name, list of mission/instrument pairs and model names, manually added datasets and datasets returned by CMR
'''

import json
import re

with open('18-55-27features.json', encoding='utf-8') as f:
    features = json.load(f)

with open('18-55-27key_title_ground_truth.json', encoding='utf-8') as f:
    key_title_ground_truth = json.load(f)

# # CMR science keyword_datasets
# for key, value in features.items():
#     for inner_key, inner_value in value['cmr_results']['pairs'].items():
#         for dataset in inner_value['science_keyword_search']['dataset']:
#             print(dataset)
#
#
# exit()

def format_lot(lot):
    lot_str = str(lot)
    lot_str = re.sub(r'[\[\]\(\)]', '', lot_str)
    lot_str = re.sub(r', (\d+)', '(\\1)', lot_str)
    lot_str = re.sub(r',', ';', lot_str)
    return lot_str


def dump_data(key, features, csv, manually_reviewed=None, title=''):

    summary_stats = features['summary_stats']
    couples = sorted(list(summary_stats['valid_couples'].items()), key=lambda x: x[1], reverse=True)
    models = sorted(list(summary_stats['models'].items()), key=lambda x: x[1], reverse=True)

    title = re.sub(',', '', title)

    csv += f'{key},{title},{format_lot(couples)}, {format_lot(models)},'
    if manually_reviewed:
        manual_ground_truths = ';'.join(manually_reviewed['manually_reviewed'])
        csv += f'{manual_ground_truths}'

    # get SINGLE TOP CMR results
    cmr_results = set()
    for inner_key, inner_value in features['cmr_results']['pairs'].items():
        datasets = inner_value['science_keyword_search']['dataset']
        if len(datasets) >= 1:
            cmr_results.add(datasets[0])
    cmr_list = ';'.join(list(cmr_results))
    csv += f',{cmr_list}'

    return csv + "\n"

added_pdfs = set()

csv = "paper, title, mission/instruments, models, manually reviewed, CMR datasets\n"
# iterate through the manually reviewed ones. Insert it into the paper applicable if possible
for parent_key, value in key_title_ground_truth.items():
    pdf_key = value['pdf']
    added_pdfs.add(pdf_key)
    if pdf_key in features:
        csv = dump_data(pdf_key, features[pdf_key], csv, manually_reviewed=value, title=value['title'])

for key, value in features.items():
    if key not in added_pdfs:
        csv = dump_data(key, value, csv)

# csv = "paper, mission/instruments, models, manually reviewed, CMR datasets\n"
# for key, value in features.items():
#     summary_stats = value['summary_stats']
#     couples = sorted(list(summary_stats['valid_couples'].items()), key=lambda x: x[1], reverse=True)
#     models = sorted(list(summary_stats['models'].items()), key=lambda x: x[1], reverse=True)
#     # print(couples)
#     # print(format_lot(couples))
#     # print(models)
#     csv += f'{key},{format_lot(couples)}, {format_lot(models)}\n'



with open('Aura_mls.csv', 'w', encoding='utf-8') as f:
    f.write(csv)