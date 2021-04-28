import json
import re
from collections import defaultdict

param_dict = {
    "aura_omi": {
        "output_filename": "aura_omi",
        "features_loc": '../CMR_Queries/cmr_results/aura-omi/11-14-46omi_rerun_features.json',
        "pubs_with_attachs_loc": '../more_papers_data/omi_zot_linkage/omi_pubs_with_attchs.json',
        "explicit_mentions": '../explicit_citation_label/aura_omi_explicit_doi_dataset_map.json'
    },
    "aura_mls": {
            "output_filename": "aura_mls",
            "features_loc": '../CMR_Queries/cmr_results/aura_mls/_v1_features.json',
            "pubs_with_attachs_loc": '../more_papers_data/zot_linkage/mls_pubs_with_attchs.json',
            "explicit_mentions": '../explicit_citation_label/aura_mls_explicit_doi_dataset_map.json'
        },
    "giovanni": {
            "output_filename": "giovanni",
            "features_loc": '../CMR_Queries/cmr_results/giovanni/giovanni_papers_features.json',
            "pubs_with_attachs_loc": '../more_papers_data/giovanni_linkage/gior_pubs_with_attchs.json',
            "explicit_mentions": '../explicit_citation_label/giovanni_explicit_doi_dataset_map.json'
        },
    "forward_gesdisc": {
            "output_filename": "forward_gesdisc_doi_clean",
            # "features_loc": '../CMR_Queries/forward_gesdisc_features.json',
            "features_loc": '../CMR_Queries/cmr_results/forward_gesdisc/forward_gesdisc_features_rerun_all.json',
            "pubs_with_attachs_loc": '../more_papers_data/forward_gesdisc_linkage/pubs_with_attchs_forward_ges.json',
            # "explicit_mentions": '../explicit_citation_label/free_text/forward_ges_references_and_text.json',
            "explicit_mentions": '../explicit_citation_label/free_text/forward_ges_references_and_text_clean_doi_clean.json'
        },

}


selection = param_dict['forward_gesdisc']

with open('../data/json/keywords.json') as f:
    model_keywords = json.load(f)['models']['short_to_long']

output_filename = selection['output_filename']
with open(selection['features_loc'], encoding='utf-8') as f:
    features = json.load(f)


with open(selection['pubs_with_attachs_loc']) as f:
    pubs_with_attachs = json.load(f)

with open(selection['explicit_mentions']) as f:
    explicit_all_papers_results = json.load(f)

key_title = {pwa['pdf_dir']: pwa for pwa in pubs_with_attachs}


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
    single_instruments = sorted(list(summary_stats['single_instrument'].items()), key=lambda x:x[1], reverse=True)

    single_instruments = [si for si in single_instruments if si[0] not in model_keywords]

    title = re.sub(',', '', title)

    csv += f'{zotero_key},{pdf_key},{title},{format_lot(couples)}, {format_lot(single_instruments)}, {format_lot(models)}, {get_explicit_datasets(pdf_key, doi_dataset_all=sep_doi_and_dataset)}'
    return csv + "\n"




added_pdfs = set()
show_separate_doi_and_dataset=True
if show_separate_doi_and_dataset:
    csv = "zotero key, pdf key, title, mission/instruments couples, single instruments, models, dois, datasets, dois & datasets mapped\n"
else:
    csv = "zotero key, pdf key, title, mission/instruments couples, single instruments, models, referenced datasets\n"
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