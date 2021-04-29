"""
 Generate stats for correct (true pos), missed (false neg), extraneous (false pos) using the top-n datasets returned

 Creates a json/csv files. Look in stats_and_csv folder to see what the output look like
"""

import json
import re
from collections import defaultdict
from enum import Enum
import os


# When I ran CMR queries, I used two methods. Method 1: Use the parameters the CMR api exposes. Method 2: Just enter
# my terms as a free text search into CMR
class CMRSearchType(Enum):
    SCIENCE_KEYWORD = 0,  # used the CMR parameters
    KEYWORD = 1,  # used a free text search inside CMR
    BOTH = 2  # Merge the results from science keyword and plain text search


# format a comma separated list into a semi-colon separated list
def format_lot(lot):
    lot_str = str(lot)
    lot_str = re.sub(r'[\[\]\(\)]', '', lot_str)
    lot_str = re.sub(r', (\d+)', '(\\1)', lot_str)
    lot_str = re.sub(r',', ';', lot_str)
    return lot_str


# Given the true datasets and the predicted datasets, determine the true positives (correct), false negatives (missed),
# and false positivies (extraneous)
def correct_missed_extraneous(ground_truths, predictions):
    ground_truths = set(ground_truths)
    correct = predictions & ground_truths
    missed = ground_truths - predictions
    extraneous = predictions - ground_truths
    return correct, missed, extraneous


# csv is a string which will be written to a csv file at the end
# running_cme_stats is a dictionary which gets modified in place and will be written to a json file at the end
def dump_data(key, features, csv, manually_reviewed=None, title='', running_cme_stats=None, n=1, dataset_search_type=None, include_singles=False):
    # extract the platform/ins couples and models from the features
    summary_stats = features['summary_stats']
    couples = sorted(list(summary_stats['valid_couples'].items()), key=lambda x: x[1], reverse=True)
    models = sorted(list(summary_stats['models'].items()), key=lambda x: x[1], reverse=True)

    title = re.sub(',', '', title)
    # write key, title, platform/ins couples, and models to csv string
    csv += f'{key},{title},{format_lot(couples)}, {format_lot(models)},'
    # add a column with the manually reviewed datasets if the paper was manually reviewed
    if manually_reviewed:
        manual_ground_truths = ';'.join(manually_reviewed['manually_reviewed'])
        csv += f'{manual_ground_truths}'

    # get TOP-N CMR results from pairs
    cmr_results = set()
    for inner_key, inner_value in features['cmr_results']['pairs'].items():
        # the features dict contains both science keyword (using cmr parameters) and keyword (free text) searches.
        # get the predicted datasets from the appropriate search
        if dataset_search_type == CMRSearchType.SCIENCE_KEYWORD:
            datasets = inner_value['science_keyword_search']['dataset']
        elif dataset_search_type == CMRSearchType.KEYWORD:
            datasets = inner_value['keyword_search']['dataset']
        elif dataset_search_type == CMRSearchType.BOTH:
            # merge the two lists together, alternating order
            l1 = inner_value['science_keyword_search']['dataset']
            l2 = inner_value['keyword_search']['dataset']

            i, j, datasets_temp = 0, 0, []
            while i < len(l1) and j < len(l2):
                datasets_temp.append(l1[i])
                datasets_temp.append(l2[j])
                i += 1
                j += 1
            if i < len(l1):
                datasets_temp += l1[i:]
            elif j < len(l2):
                datasets_temp += l2[j:]

            # remove duplicates
            seen = set()
            datasets = []
            for i in range(len(datasets_temp)):
                if datasets_temp[i] in seen:
                    continue
                seen.add(datasets_temp[i])
                datasets.append(datasets_temp[i])

        if len(datasets) >= 1:
            for predic in datasets[:n]:
                cmr_results.add(predic)

    # cmr queries based on the single instruments and not just the couples
    if include_singles:
        for inner_key, inner_value in features['cmr_results']['singles'].items():
            if dataset_search_type == CMRSearchType.SCIENCE_KEYWORD:
                single_datasets = inner_value['science_keyword_search']['dataset']
            elif dataset_search_type == CMRSearchType.KEYWORD:
                single_datasets = inner_value['keyword_search']['dataset']
            else:
                single_datasets = None

            if single_datasets:
                for predic in single_datasets[:n]:
                    if predic not in cmr_results:
                        cmr_results.add(predic)

    # create semi-colon delineated string with the predicted datasets from CMR and add to csv string
    cmr_list = ';'.join(list(cmr_results))
    csv += f',{cmr_list}'

    # If the paper was manually reviewed update the dictionary containing overall stats about how many datasets were
    # correct, missed, and extraneous.
    if manually_reviewed:
        correct, missed, extraneous = correct_missed_extraneous(manually_reviewed['manually_reviewed'], cmr_results)
        running_cme_stats['correct_count'] += len(correct)
        running_cme_stats['missed_count'] += len(missed)
        running_cme_stats['extraneous_count'] += len(extraneous)
        # keep counts of how often each dataset was correct. (ie: at the end we'll have something like, we predicted
        # ML2O3 correctly 54 times)
        for corr in correct:
            running_cme_stats['correct_dict'][corr] += 1
        for miss in missed:
            running_cme_stats['missed_dict'][miss] += 1
        for extra in extraneous:
            running_cme_stats['extraneous_dict'][extra] += 1
        csv += f',,,{len(correct)}, {len(missed)}, {len(extraneous)}'
    return csv + "\n"


if __name__ == '__main__':
    # User Parameters
    features_location = 'cmr_results/giovanni/giovanni_papers_features.json'  # the extracted features
    key_title_ground_truth_location = 'cmr_results/giovanni/giovanni_papers_key_title_ground_truth.json'  # includes the ground truth if applicables
    n = 1  # range of Top-n results to search. Ie n=1, max_n=9 means analyze results for top-1, top-2, top-3, ..., top-9
    max_n = 9
    cmr_search_type = CMRSearchType.SCIENCE_KEYWORD  # use cmr parameters in search of use free text. See enum definition
    include_singles = False  # include results from NoPlatform/Instrument science keyword CMR searches
    # Declare the name of the output file
    output_title = 'giovanni_'  # change this
    include_singles_string = 'with_singles_' if include_singles else ''
    sub_folder = f'{output_title}{include_singles_string}{cmr_search_type.name.lower()}/'
    base_location = 'stats_and_csv/giovanni/' + sub_folder  # change this

    with open(features_location, encoding='utf-8') as f:
        features = json.load(f)

    with open(key_title_ground_truth_location, encoding='utf-8') as f:
        key_title_ground_truth = json.load(f)

    correct, missed, extraneous = [], [], []

    # make a folder if one doesn't exist
    if not os.path.exists(base_location):
        os.makedirs(base_location)

    # run the top-n results for all values of n
    while n <= max_n:
        filename = base_location + f'{output_title}top_{n}_{cmr_search_type.name.lower()}'
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
        # iterate through the manually reviewed papers. Add data into csv and json files via dump_data method
        for parent_key, value in key_title_ground_truth.items():
            pdf_key = value['pdf']
            added_pdfs.add(pdf_key)
            if pdf_key in features:
                # update both csv file and json file
                csv = dump_data(pdf_key, features[pdf_key], csv, manually_reviewed=value, title=value['title'], running_cme_stats=running_cme_stats,
                                n=n, dataset_search_type=cmr_search_type)

        # loop through the papers that were not manually reviewed
        for key, value in features.items():
            if key not in added_pdfs:
                # update only csv file
                csv = dump_data(key, value, csv, dataset_search_type=cmr_search_type)

        # sort the individual counts of number of times that a dataset was correct, missed, or extraneous
        running_cme_stats['correct_dict'] = dict(sorted(running_cme_stats['correct_dict'].items(), key=lambda x: x[1], reverse=True))
        running_cme_stats['missed_dict'] = dict(sorted(running_cme_stats['missed_dict'].items(), key=lambda x: x[1], reverse=True))
        running_cme_stats['extraneous_dict'] = dict(sorted(running_cme_stats['extraneous_dict'].items(), key=lambda x: x[1], reverse=True))

        # DON'T overwrite an existing file. Exit out in this case
        if os.path.exists(filename + '.json'):
            print("\n\nFile with name already exists\n\n")
            exit()

        # save the json and csv files for the top-n
        with open(filename + '.json', 'w', encoding='utf-8') as f:
            json.dump(running_cme_stats, f, indent=4)

        with open(filename + '.csv', 'w', encoding='utf-8') as f:
            f.write(csv)

        # save the counts for correct, missed, extraneous into the local arrays
        correct.append(running_cme_stats['correct_count'])
        missed.append(running_cme_stats['missed_count'])
        extraneous.append(running_cme_stats['extraneous_count'])
        # run the loop again with a larger value of n
        n += 1

    # save a file with the three lists for correct missed and extraneous and how the values change as a function of n
    summary_dict = {
        "cmr_mode": cmr_search_type.name.lower(),
        "correct_counts": correct,
        "missed_counts": missed,
        "extraneous_counts": extraneous,
    }
    # save the summary stats
    with open(base_location + f'{cmr_search_type.name.lower()}_summary_counts.json', 'w', encoding='utf-8') as f:
        json.dump(summary_dict, f)