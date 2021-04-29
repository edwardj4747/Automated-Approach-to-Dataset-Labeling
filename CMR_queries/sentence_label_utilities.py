"""
This is the CORE of the feature labelling. It calls some helper methods in other files but this is the main one
"""

import json
import re
import itertools
from collections import defaultdict
from CMR_Queries.cmr_query_utilities import get_top_cmr_dataset
from CMR_Queries.author_spatial_labeling_utility import label_author, identify_spatial_resolution
import glob
from enum import Enum


class QueryMode(Enum):
    ALL = 0,  # all combinations of missions/instruments and science keywords
    RESTRICTED = 1  # only mission/instruments in the same sentence


def get_text(paper, preprocessed_location, alt_path=''):
    with open(preprocessed_location + paper + '.txt', encoding='utf-8') as f:
        text = f.read()
    return text


# Clean the text up a little
def basic_clean(text):
    text = re.sub(r'[^(?:\x00-\x7F)|\u25e6|\u00d7]+', '', text)  # remove non unicode characters but keep ◦ and ×
    text = re.sub(r'et al\.,?', 'et al', text)
    text = re.sub(r'e\.g\.,?', 'eg', text)
    text = re.sub(r'i\.e\.,?', 'ie', text)
    text = re.sub(r'\(\)', '', text)  # punctuation
    text = re.sub(r'(https?://)?([\da-z\.-]+)\.([a-z\.]{2,6})([/\w \.-]*)', '', text)  # removing the links

    text = re.sub('\n', ' ', text)
    return text


# Given a mission and instrument, determine if that mission/ins couple is possible (ie: Aura/MLS) or not possible
def is_valid_couple(mission, instrument, couples, debug=False):
    potential_instruments = couples.get(mission, [])
    result = instrument in potential_instruments
    if debug and result:
        print("Valid Couple ", mission, instrument)
    elif debug and not result:
        print("Invalid Couple ", mission, instrument)
    return result


# Create a list of all the valid couples
def find_valid_couples(missions, instruments, all_possible_couples, levels=[]):
    valid_couples = set()
    single_mission, single_instrument = set(missions), set(instruments)

    level_modifier = ''
    if len(levels) == 1:
        level_modifier = f'----{levels[0]}'

    for perm in itertools.product(*[missions, instruments]):
        if is_valid_couple(perm[0], perm[1], couples=all_possible_couples):
            valid_couples.add(f'{perm[0]}/{perm[1]}{level_modifier}')

    return valid_couples, single_mission, single_instrument


# in the text, convert all long long names to short names (ie 'microwave limb sounder' -> 'mls')
def substitute_keywords(sentence, keywords):
    keyword_count = 0  # count for how many keywords we find in total
    # keep track of the missions, instrument, species, and models that we find
    found_missions, found_instruments, found_species, found_models = set(), set(), set(), set()

    sentence = " " + sentence + " "  # to make regex work at begging/end of lines

    # Check for 'NO' (as in Nitrogen Oxide) before we lowercase the sentence which is different than the english word no
    if len(re.findall(rf'[^a-zA-Z]NO[^a-zA-Z]', sentence)) > 0:
        found_species.add('NO')

    lowercase_sentence = sentence.lower()

    # Declare the short and long names we are looking for
    missions_long = list(keywords['missions']['long_to_short'])
    models_long = list(keywords['models']['long_to_short'])
    instruments_long = list(keywords['instruments']['long_to_short'])
    variables_long = list(keywords['variables']['long_to_short'])

    missions_short = list(keywords['missions']['short_to_long'])
    models_short = list(keywords['models']['short_to_long'])
    instruments_short = list(keywords['instruments']['short_to_long'])
    variables_short = list(keywords['variables']['short_to_long'])

    for short_m in missions_short:
        if short_m == '':
            continue
        short_matches = re.findall(rf'[^a-zA-Z]{short_m}[^a-zA-Z\-]', lowercase_sentence)  # look for occurrences of the mission
        if len(short_matches) > 0:
            found_missions.add(short_m)  # keep track of the mission we find
        keyword_count += len(short_matches)

    for short_i in instruments_short:
        if short_i == '' or short_i == 'not applicable':
            continue
        short_matches = re.findall(rf'[^a-zA-Z]{short_i}[^a-zA-Z\-]', lowercase_sentence)
        if len(short_matches) > 0:
            found_instruments.add(short_i)
        keyword_count += len(short_matches)

    for short_mod in models_short:
        if short_mod == '':
            continue
        short_matches = re.findall(rf'[^a-zA-Z]{short_mod}[^a-zA-Z\-]', lowercase_sentence)
        if len(short_matches) > 0:
            found_models.add(short_mod)
        keyword_count += len(short_matches)

    for short_v in variables_short:
        if short_v == '':
            continue
        short_matches = re.findall(rf'[^a-zA-Z]{short_v}[^a-zA-Z\-]', lowercase_sentence)
        if len(short_matches) > 0:
            found_species.add(short_v)

    # Look for long names
    for long_m in missions_long:
        if long_m in lowercase_sentence and long_m != '':
            short_m = keywords['missions']['long_to_short'][long_m]
            lowercase_sentence = re.sub(rf'{long_m}', f'{short_m}', lowercase_sentence)  # replace long name with short name
            keyword_count += 1
            found_missions.add(short_m)  # keep track of the missions that were found

    for long_i in instruments_long:
        if long_i in lowercase_sentence and long_i != '':
            short_i = keywords['instruments']['long_to_short'][long_i]
            lowercase_sentence = re.sub(rf'{long_i}', f'{short_i}', lowercase_sentence)
            keyword_count += 1
            found_instruments.add(short_i)

    for long_mod in models_long:
        if long_mod in lowercase_sentence and long_mod != '':
            short_mod = keywords['models']['long_to_short'][long_mod]
            lowercase_sentence = re.sub(rf'{long_mod}', f'{short_mod}', lowercase_sentence)
            keyword_count += 1
            found_instruments.add(short_mod)

    for long_v in variables_long:
        if long_v in lowercase_sentence and long_v != '':
            short_v = keywords['variables']['long_to_short'][long_v]
            lowercase_sentence = re.sub(rf'{long_v}', f'{short_v}', lowercase_sentence)
            found_species.add(short_v)

    # simple regex pattern to look for version and levels
    versions = re.findall(r'[vV]ersion \d', lowercase_sentence)
    levels = re.findall(r'[lL]evel[- ][0-4][a-z]?', lowercase_sentence)

    authors = label_author(lowercase_sentence, keywords)
    resolutions = []
    if keyword_count >= 1:
        resolutions = identify_spatial_resolution(lowercase_sentence)

    return lowercase_sentence, keyword_count, found_missions, found_instruments, found_species if keyword_count >= 1 else [], versions, levels, found_models, authors, resolutions


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


# code to launch a CMR query
def run_CMR_query(platform_instrument, species, level, cmr_results_dictionary, sort_by_usage=False):
    platform_instrument_split = platform_instrument.split('/')
    platform, instrument = platform_instrument_split[0], platform_instrument_split[1]

    if platform == 'None':
        platform = None

    query_str, cmr_dataset, url = get_top_cmr_dataset(platform, instrument, species,
                                                      num_results=20, level=level, sort_by_usage=False)
    _, cmr_dataset_false, url_false = get_top_cmr_dataset(platform, instrument,
                                                          species, science_keyword_search=False,
                                                          num_results=20, level=level, sort_by_usage=False)
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


# Main function. Loop through all the papers finding the keywords, querying CMR, and storing the results
def run_keyword_sentences(keyword_file_location, mission_instrument_couples, preprocessed_directory, alt_path='',
                          query_mode=QueryMode.ALL, sort_by_usage=False, single_paper=None, update_CMR=True):
    # single paper will be the pdf key of a specific paper if we just want to run the labelling on that specific paper

    with open(keyword_file_location) as f:
        keywords = json.load(f)

    with open(mission_instrument_couples, encoding='utf-8') as f:
        all_couples = json.load(f)

    papers_not_found = []
    paper_to_results = {}
    count = 0

    # we may be calling this from spot_update_features and just want to run this code for one single pdf
    if single_paper:
        pdf_dirs = [single_paper]
    else:
        pdf_dirs = glob.glob(preprocessed_directory + "*.txt")  # otherwise run for all files

    for paper in pdf_dirs:
        count += 1
        paper = paper.split('\\')[-1].split('.')[0]  # just the pdf_key (ie: AI5SBBh6)
        print(paper)

        try:
            text = get_text(paper, preprocessed_directory, alt_path=alt_path)
        except FileNotFoundError:
            papers_not_found.append(paper)
            print("NOT FOUND")
            continue
        text = basic_clean(text)

        # dictionary to store how many times we observed each valid couple, or how many we observed each model, ..etc
        summary_stats = {
            "valid_couples": defaultdict(int),
            "single_mission": defaultdict(int),
            "models": defaultdict(int),
            "single_instrument": defaultdict(int),
            "species": defaultdict(int),
        }
        couples_to_species = defaultdict(dict)
        instrument_to_species = defaultdict(dict)

        sentences_list = []
        for original_sent in re.split(r'(?<!\d)\.(?!\d)', text):  # split on '.' if '.' is not in a decimal. Basically for each sentence
            sent, keyword_count, found_missions, found_instruments, found_species, versions, levels, found_models, authors, resolutions = substitute_keywords(original_sent, keywords)
            valid_couples, single_mission, single_instrument = find_valid_couples(found_missions, found_instruments, all_couples, levels)

            # **********************************
            # update the couples and species dict
            if query_mode == QueryMode.RESTRICTED:  # remember restricted requires the
                for vc in valid_couples:
                    for species in found_species:
                        couples_to_species[vc][species] = couples_to_species[vc].get(species, 0) + 1

                for i in single_instrument:
                    for species in found_species:
                        instrument_to_species[i][species] = instrument_to_species[i].get(species, 0) + 1
            # ************************************

            # Building up the summary stats based on number of sentences a couple/model/mission...etc appeared in
            for vc in valid_couples:
                summary_stats["valid_couples"][vc] += 1

            for mod in found_models:
                summary_stats['models'][mod] += 1

            for m in single_mission:
                summary_stats["single_mission"][m] += 1

            for i in single_instrument:
                summary_stats['single_instrument'][i] += 1

            for s in found_species:
                summary_stats['species'][s] += 1

            # if the sentence contained at least once keyword, store the sentence and the labels for that sentence
            if keyword_count >= 1:
                s = {
                    "sentence": re.sub(r' {2,}', ' ', sent).strip(),
                    "couples": list(valid_couples),
                    "missions": list(single_mission),
                    "instruments": list(single_instrument),
                    "models": list(found_models),
                    "species": list(found_species),
                    "version": versions,
                    "levels": levels,
                    "authors": authors,
                    "resolutions": resolutions,
                }
                sentences_list.append(s)

        if update_CMR:
            # store the CMR Queries here
            cmr_couples_results = {}
            cmr_singles_results = {}
        else:
            cmr_couples_results = 'Not Run'
            cmr_singles_results = 'Not Run'

        # Launching CMR queries
        if update_CMR:
            # Restricted - keywords must be in the same sentence
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

            # Non-Restricted - any combinations of keywords accross the whole paper
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

        paper_to_results[paper] = {
            "summary_stats": summary_stats,
            "cmr_results": {
                "pairs": cmr_couples_results,
                "singles": cmr_singles_results
            },
            "sentences": sentences_list
        }
        # Because this is a time consuming process, save a copy of the results every so often
        if count % 100 == 0:
            with open(f'partial_results_{count}.json', 'w', encoding='utf-8') as f:
                json.dump(paper_to_results, f, indent=4)

    return paper_to_results

