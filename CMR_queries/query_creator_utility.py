"""
Similar to code in sentence_label_utilities.py. This file is not part of the pipeline. This code allows you to rerun
the cmr queries if you have already extracted the sentence features.
"""

from enum import Enum
import json
from collections import defaultdict
from CMR_Queries.cmr_query_utilities import get_top_cmr_dataset


class QueryMode(Enum):
    ALL = 0,  # all combinations of missions/instruments and science keywords
    RESTRICTED = 1  # only mission/instruments in the same sentence


# split something like aura/mls----level 3 into platform/ins: aura/mls and level: level 3
def get_platform_instrument_level(vc):
    platform_instrument = vc.split('----')
    if len(platform_instrument) > 1:
        level = platform_instrument[1]
        platform_instrument = platform_instrument[0]
    else:
        platform_instrument = platform_instrument[0]
        level = None

    return platform_instrument, level


# build the cmr query and call get_top_cmr_dataset to actually run the query
def run_CMR_query(platform_instrument, species, level, cmr_results_dictionary, sort_by_usage=False):
    platform_instrument_split = platform_instrument.split('/')
    platform, instrument = platform_instrument_split[0], platform_instrument_split[1]

    if platform == 'None':
        platform = None

    query_str, cmr_dataset, url = get_top_cmr_dataset(platform, instrument, species,
                                                      num_results=20, level=level, sort_by_usage=sort_by_usage)
    _, cmr_dataset_false, url_false = get_top_cmr_dataset(platform, instrument,
                                                          species, science_keyword_search=False,
                                                          num_results=20, level=level, sort_by_usage=sort_by_usage)
    # cmr_couples_results[query_str] = {
    #     "dataset": cmr_dataset,
    #     "query": url
    # }
    cmr_results_dictionary[query_str] = {
        "science_keyword_search": {
            "dataset": cmr_dataset,
            "query": url
        },
        "keyword_search": {
            "dataset": cmr_dataset_false,
            "query": url_false
        }
    }


# Given an initial features dictionary, rerun the cmr queries without having to refind the features
def update_cmr_values(features, query_mode, sort_by_usage):
    paper_to_results = {}
    count = 0

    for paper, feature in features.items():
        count += 1
        print(paper)
        summary_stats = feature['summary_stats']

        couples_to_species = defaultdict(dict)
        instrument_to_species = defaultdict(dict)

        # go through the sentences
        sentences_list = []
        for sentence_labels in feature['sentences']:  # includes sentence, missions, instruments, ...
            sentences_list.append(sentence_labels)

            # **********************************
            if query_mode == QueryMode.RESTRICTED:  # only looking at keywords in the same sentence, so need to determine ones that re in same sentences
                # update the couples and species dict
                for vc in sentence_labels['couples']:
                    for species in sentence_labels['species']:
                        couples_to_species[vc][species] = couples_to_species[vc].get(species, 0) + 1

                for i in sentence_labels['instruments']:
                    for species in sentence_labels['species']:
                        instrument_to_species[i][species] = instrument_to_species[i].get(species, 0) + 1
            # ************************************

        # compute the CMR Queries
        cmr_couples_results = {}
        cmr_singles_results = {}

        # Restricted
        if query_mode == QueryMode.RESTRICTED:
            for couple, dict_counts in couples_to_species.items():
                platform_instrument, level = get_platform_instrument_level(couple)
                for species, species_count in dict_counts.items():
                    if species_count <= 1:
                        continue
                    run_CMR_query(platform_instrument, species, level, cmr_couples_results, sort_by_usage)

            instruments_in_pairs = [couple.split('/')[1] for couple in couples_to_species]
            for instrument, dict_counts in instrument_to_species.items():
                platform, level = None, None
                # if instrument not in instruments_in_pairs:
                for species, species_count in dict_counts.items():
                    if species_count <= 1:
                        continue
                    run_CMR_query(f'{platform}/{instrument}', species, level, cmr_singles_results, sort_by_usage)


        # Non-Restricted
        elif query_mode == QueryMode.ALL:
            for vc in summary_stats['valid_couples']:
                platform_instrument, level = get_platform_instrument_level(vc)
                for science_keyword in summary_stats['species']:
                    if summary_stats['species'][science_keyword] <= 1:
                        continue
                    run_CMR_query(platform_instrument, science_keyword, level, cmr_couples_results, sort_by_usage)

            instruments_in_pairs = [vc.split('/')[1] for vc in summary_stats['valid_couples']]
            platform, level = None, None
            for instrument in summary_stats['single_instrument']:
                if instrument not in instruments_in_pairs:
                    for science_keyword in summary_stats['species']:
                        if summary_stats['species'][science_keyword] <= 1:
                            continue
                        run_CMR_query(f'{platform}/{instrument}', science_keyword, level, cmr_singles_results, sort_by_usage)

        # store the results
        paper_to_results[paper] = {
            "summary_stats": summary_stats,
            "cmr_results": {
                "pairs": cmr_couples_results,
                "singles": cmr_singles_results
            },
            "sentences": sentences_list
        }
        # print(paper, paper_to_results[paper])
        if count % 50 == 0:
            with open(f'partial_results_{count}.json', 'w', encoding='utf-8') as f:
                json.dump(paper_to_results, f, indent=4)
        # print(couples_to_species)
        # print(instrument_to_species)

    return paper_to_results


if __name__ == '__main__':
    with open('cmr_results/aura-omi/11-14-46omi_rerun_features.json', encoding='utf-8') as f:
        features = json.load(f)

    sort_by_usages = True
    results = update_cmr_values(features, QueryMode.ALL, sort_by_usages)

    filename = "cmr_results/aura-omi/11-14-46omi_rerun_by_usage_features.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)