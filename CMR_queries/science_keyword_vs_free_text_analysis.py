'''
    Go through the results and for each search, determine if it perform better as a science keyword search
     or as a free text (keyword) search
'''

import json
from enum import Enum


class ScienceKeywordIs(Enum):
    BETTER = 0,
    EQUAL = 1,
    WORSE = 2,
    DATASET_NOT_PRESENT = 3,
    NO_DATASETS = 4


# open a features_merged file because it has both cmr_results and the manually reviewed ground_truths
with open('cmr_results/aura_mls/_v1_features_merged.json') as f:
    features_merged = json.load(f)

# store the result. Each dataset will have one of the values of BETTER, EQUAL, WORSE, DATA_SET_NOT_PRESENT
search_query_results = {}

for paper, paper_values in features_merged.items():
    manually_reviewed = paper_values['manually_reviewed']

    if 'cmr_results' not in paper_values:
        continue

    for search_query, search_results in paper_values['cmr_results']['pairs'].items():
        science_keyword_results = search_results['science_keyword_search']['dataset']
        keyword_results = search_results['keyword_search']['dataset']

        # print(science_keyword_results)
        # print(keyword_results)

        # determine if a science_keyword search is better, equal, worse, or neither search gets dataset
        result = ScienceKeywordIs.DATASET_NOT_PRESENT.name
        found_result = False
        science_keyword_index, keyword_index = 0, 0
        # what if the datasets are not equal but they are both in manually reviewed
        while not found_result:
            if len(science_keyword_results) == 0 and len(keyword_results) == 0:
                result = ScienceKeywordIs.NO_DATASETS.name
                break

            science_keyword_dataset = science_keyword_results[science_keyword_index] if science_keyword_index < len(science_keyword_results) else None
            keyword_dataset = keyword_results[keyword_index] if keyword_index < len(keyword_results) else None

            if science_keyword_dataset is None and keyword_dataset is None:
                break

            if science_keyword_dataset == keyword_dataset and keyword_dataset in manually_reviewed:
                result = ScienceKeywordIs.EQUAL.name
                found_result = True
            elif science_keyword_dataset in manually_reviewed and keyword_dataset not in manually_reviewed:
                result = ScienceKeywordIs.BETTER.name
                found_result = True
            elif keyword_dataset in manually_reviewed and science_keyword_dataset not in manually_reviewed:
                result = ScienceKeywordIs.WORSE.name
                found_result = True
            elif science_keyword_dataset in manually_reviewed and keyword_dataset in manually_reviewed:
                print("EXCEPTION CASE", search_query)

            science_keyword_index += 1
            keyword_index += 1

        search_query_results[search_query] = result

sorted_results = sorted(search_query_results.items())

for key, value in sorted_results:
    print(key, value)

with open("science_keyword_vs_free_text_analysis_raw.json", 'w', encoding='utf-8') as f:
    json.dump(sorted_results, f, indent=4)

# extract EQUAL, WORSE, BETTER, ...
better = [x[0] for x in sorted_results if x[1] == ScienceKeywordIs.BETTER.name]
worse = [x[0] for x in sorted_results if x[1] == ScienceKeywordIs.WORSE.name]
equal = [x[0] for x in sorted_results if x[1] == ScienceKeywordIs.EQUAL.name]
no_datasets = [x[0] for x in sorted_results if x[1] == ScienceKeywordIs.NO_DATASETS.name]

print(sorted_results)

better_worse_equal_dict = {
    "better": better,
    "worse": worse,
    "equal": equal,
    "no_datasets": no_datasets,
}

with open("science_keyword_vs_free_text_analysis.json", 'w', encoding='utf-8') as f:
    json.dump(better_worse_equal_dict, f, indent=4)
