'''
    stats for correct, missed, extraneous using the top-n datasets returned
'''

import json
import re
from collections import defaultdict

with open('3-22-15-Aura_omi_features.json', encoding='utf-8') as f:
    features = json.load(f)

with open('20-20-16_omi_papers_key_title_ground_truth.json', encoding='utf-8') as f:
    key_title_ground_truth = json.load(f)



def format_lot(lot):
    lot_str = str(lot)
    lot_str = re.sub(r'[\[\]\(\)]', '', lot_str)
    lot_str = re.sub(r', (\d+)', '(\\1)', lot_str)
    lot_str = re.sub(r',', ';', lot_str)
    return lot_str


def correct_missed_extraneous(ground_truths, predictions):
    ground_truths = set(ground_truths)
    correct = predictions & ground_truths
    missed = ground_truths - predictions
    extraneous = predictions - ground_truths
    return correct, missed, extraneous


def dump_data(key, features, csv, manually_reviewed=None, title='', running_cme_stats=None, n=1):
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
        # datasets = inner_value['keyword_search']['dataset']
        if len(datasets) >= 1:
            for predic in datasets[:n]:
                cmr_results.add(predic)

    cmr_list = ';'.join(list(cmr_results))
    csv += f',{cmr_list}'

    if manually_reviewed:
        correct, missed, extraneous = correct_missed_extraneous(manually_reviewed['manually_reviewed'], cmr_results)
        running_cme_stats['correct_count'] += len(correct)
        running_cme_stats['missed_count'] += len(missed)
        running_cme_stats['extraneous_count'] += len(extraneous)
        for corr in correct:
            running_cme_stats['correct_dict'][corr] += 1
        for miss in missed:
            running_cme_stats['missed_dict'][miss] += 1
        for extra in extraneous:
            running_cme_stats['extraneous_dict'][extra] += 1
        csv += f',,,{len(correct)}, {len(missed)}, {len(extraneous)}'
    return csv + "\n"


if __name__ == '__main__':
    n = 1

    while n <= 20:
        filename = f'Aura_omi_cme_top_{n}'
        added_pdfs = set()
        running_cme_stats = {
            "correct_count": 0,
            "missed_count": 0,
            "extraneous_count": 0,
            "correct_dict": defaultdict(int),
            "missed_dict": defaultdict(int),
            "extraneous_dict": defaultdict(int)
        }
        csv = "paper, title, mission/instruments, models, manually reviewed, CMR datasets,,,correct, missed, extraneous\n"
        # iterate through the manually reviewed ones. Insert it into the paper applicable if possible
        for parent_key, value in key_title_ground_truth.items():
            pdf_key = value['pdf']
            added_pdfs.add(pdf_key)
            if pdf_key in features:
                csv = dump_data(pdf_key, features[pdf_key], csv, manually_reviewed=value, title=value['title'], running_cme_stats=running_cme_stats,
                                n=n)

        for key, value in features.items():
            if key not in added_pdfs:
                csv = dump_data(key, value, csv)

        running_cme_stats['correct_dict'] = dict(sorted(running_cme_stats['correct_dict'].items(), key=lambda x: x[1], reverse=True))
        running_cme_stats['missed_dict'] = dict(sorted(running_cme_stats['missed_dict'].items(), key=lambda x: x[1], reverse=True))
        running_cme_stats['extraneous_dict'] = dict(sorted(running_cme_stats['extraneous_dict'].items(), key=lambda x: x[1], reverse=True))

        with open(filename + '.json', 'w', encoding='utf-8') as f:
            json.dump(running_cme_stats, f, indent=4)

        with open(filename + '.csv', 'w', encoding='utf-8') as f:
            f.write(csv)

        n += 1