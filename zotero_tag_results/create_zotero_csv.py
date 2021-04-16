# import json
#
# with open('../explicit_citation_label/') as f:
#     explicit = json.load(f)
#
# with open('../CMR_Queries/forward_gesdisc_features.json') as f:
#     features = json.load(f)
#
# # zotero key, pdf key, title, mission/instrument, models

import json
import re
from collections import defaultdict

output_filename = 'aura_mls'
with open('../CMR_Queries/cmr_results/aura_mls/_v1_features.json', encoding='utf-8') as f:
    features = json.load(f)

# with open('../CMR_Queries/forward_gesdisc_key_title_ground_truth.json', encoding='utf-8') as f:
#     key_title_ground_truth = json.load(f)

with open('../more_papers_data/zot_linkage/mls_pubs_with_attchs.json') as f:
    pubs_with_attachs = json.load(f)

key_title = {pwa['pdf_dir']: pwa for pwa in pubs_with_attachs}

with open('../explicit_citation_label/aura_mls_explicit_doi_dataset_map.json') as f:
    explicit_all_papers_results = json.load(f)

def get_explicit_datasets(pdf_key, doi_dataset_all=False):
    if not doi_dataset_all:
        if pdf_key in explicit_all_papers_results:
            explicit_datasets = explicit_all_papers_results[pdf_key]['datasets']
            return '; '.join(explicit_datasets)
        else:
            return ''
    else:
        if pdf_key in explicit_all_papers_results:
            # add columns for dois, datasets, mapped dois -> datasets
            explicit_dois = '; '.join(explicit_all_papers_results[pdf_key]['explicit_dois'])
            explicit_datasets = '; '.join(explicit_all_papers_results[pdf_key]['explicit_datasets'])
            mapped_datasets = '; '.join(explicit_all_papers_results[pdf_key]['datasets_and_doi'])
            return f'{explicit_dois}, {explicit_datasets}, {mapped_datasets}'
        else:
            return ''

def format_lot(lot):
    lot_str = str(lot)
    lot_str = re.sub(r'[\[\]\(\)]', '', lot_str)
    lot_str = re.sub(r', (\d+)', '(\\1)', lot_str)
    lot_str = re.sub(r',', ';', lot_str)
    return lot_str


def dump_data(zotero_key, pdf_key, features, csv, title='', sep_doi_and_dataset=True):

    summary_stats = features['summary_stats']
    couples = sorted(list(summary_stats['valid_couples'].items()), key=lambda x: x[1], reverse=True)
    models = sorted(list(summary_stats['models'].items()), key=lambda x: x[1], reverse=True)

    title = re.sub(',', '', title)

    csv += f'{zotero_key},{pdf_key},{title},{format_lot(couples)}, {format_lot(models)}, {get_explicit_datasets(pdf_key, doi_dataset_all=sep_doi_and_dataset)}'
    return csv + "\n"




added_pdfs = set()
show_separate_doi_and_dataset=True
if show_separate_doi_and_dataset:
    csv = "zotero key, pdf key, title, mission/instruments, models, dois, datasets, dois & datasets mapped\n"
else:
    csv = "zotero key, pdf key, title, mission/instruments, models, referenced datasets\n"
# iterate through the manually reviewed ones. Insert it into the paper applicable if possible
for parent_key, value in key_title.items():
    zotero_key = value['key']
    pdf_key = value['pdf_dir']
    added_pdfs.add(pdf_key)
    if pdf_key in features:
        csv = dump_data(zotero_key, pdf_key, features[pdf_key], csv, title=value['filename'], sep_doi_and_dataset=show_separate_doi_and_dataset)

for pdf_key, value in features.items():
    if pdf_key not in added_pdfs:
        zotero_key = key_title[pdf_key]
        csv = dump_data(zotero_key, pdf_key, value, csv, sep_doi_and_dataset=show_separate_doi_and_dataset)


with open(output_filename + '.csv', 'w', encoding='utf-8') as f:
    f.write(csv)