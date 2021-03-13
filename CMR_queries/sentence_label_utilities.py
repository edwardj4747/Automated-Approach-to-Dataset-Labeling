import json
import re
import itertools
from collections import defaultdict
from CMR_Queries.cmr_query_utilities import get_top_cmr_dataset
import glob


def get_text(paper, preprocessed_location, alt_path=''):
    with open(preprocessed_location + paper + '.txt', encoding='utf-8') as f:
        text = f.read()
    return text


def basic_clean(text):
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # remove non unicode characters
    text = re.sub(r'et al.,?', 'et al', text)
    text = re.sub(r'e.g.,?', 'eg', text)
    text = re.sub(r'i.e.,?', 'ie', text)
    text = re.sub(r'\.[0-9]+', '', text)  # removing the decimals
    text = re.sub(r'\(\)', '', text)  # punctuation
    text = re.sub(r'(https?://)?([\da-z\.-]+)\.([a-z\.]{2,6})([/\w \.-]*)', '', text)  # removing the links

    text = re.sub('\n', ' ', text)
    return text


def is_valid_couple(mission, instrument, couples, debug=False):
    potential_instruments = couples.get(mission, [])
    result = instrument in potential_instruments
    if debug and result:
        print("Valid Couple ", mission, instrument)
    elif debug and not result:
        print("Invalid Couple ", mission, instrument)
    return result


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


def substitute_keywords(sentence, keywords):
    keyword_count = 0
    found_missions, found_instruments, found_species, found_models = set(), set(), set(), set()

    sentence = " " + sentence + " "  # to make regex work at begging/end of lines
    # Check for 'NO' before we lowercase the sentence

    if len(re.findall(rf'[^a-zA-Z]NO[^a-zA-Z]', sentence)) > 0:
        found_species.add('NO')

    lowercase_sentence = sentence.lower()
    missions_long = list(keywords['missions']['long_to_short'])
    # @TODO: add this in
    models_long = list(keywords['models']['long_to_short'])
    instruments_long = list(keywords['instruments']['long_to_short'])
    variables_long = list(keywords['variables']['long_to_short'])

    missions_short = list(keywords['missions']['short_to_long'])
    # @TODO: add this in
    models_short = list(keywords['models']['short_to_long'])
    instruments_short = list(keywords['instruments']['short_to_long'])
    variables_short = list(keywords['variables']['short_to_long'])


    for short_m in missions_short:
        if short_m == '':
            continue
        short_matches = re.findall(rf'[^a-zA-Z]{short_m}[^a-zA-Z]', lowercase_sentence)
        if len(short_matches) > 0:
            found_missions.add(short_m)
        keyword_count += len(short_matches)

    for short_i in instruments_short:
        if short_i == '' or short_i == 'not applicable':
            continue

        short_matches = re.findall(rf'[^a-zA-Z]{short_i}[^a-zA-Z]', lowercase_sentence)
        if len(short_matches) > 0:
            found_instruments.add(short_i)
        keyword_count += len(short_matches)

    for short_mod in models_short:
        if short_mod == '':
            continue

        short_matches = re.findall(rf'[^a-zA-Z]{short_mod}[^a-zA-Z]', lowercase_sentence)
        if len(short_matches) > 0:
            found_models.add(short_mod)
        keyword_count += len(short_matches)

    for short_v in variables_short:
        if short_v == '':
            continue

        short_matches = re.findall(rf'[^a-zA-Z]{short_v}[^a-zA-Z]', lowercase_sentence)
        if len(short_matches) > 0:
            found_species.add(short_v)

    for long_m in missions_long:
        if long_m in lowercase_sentence and long_m != '':
            short_m = keywords['missions']['long_to_short'][long_m]
            lowercase_sentence = re.sub(rf'{long_m}', f'{short_m}', lowercase_sentence)
            keyword_count += 1
            found_missions.add(short_m)

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

    versions = re.findall(r'[vV]ersion \d', lowercase_sentence)
    levels = re.findall(r'[lL]evel [0-4]', lowercase_sentence)

    # if len(re.findall(r'(resolution)|(km)', lowercase_sentence)) > 0:
    #     print(lowercase_sentence)

    return lowercase_sentence, keyword_count, found_missions, found_instruments, found_species if keyword_count >= 1 else [], versions, levels, found_models


def run_keyword_sentences(keyword_file_location, mission_instrument_couples, preprocessed_directory, alt_path=''):
    with open(keyword_file_location) as f:
        keywords = json.load(f)

    with open(mission_instrument_couples, encoding='utf-8') as f:
        all_couples = json.load(f)

    papers_not_found = []
    paper_to_results = {}
    count = 0

    for paper in glob.glob(preprocessed_directory + "*.txt"):
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
        # print(text)

        summary_stats = {
            "valid_couples": defaultdict(int),
            "single_mission": defaultdict(int),
            "models": defaultdict(int),
            "single_instrument": defaultdict(int),
            "species": defaultdict(int),
        }

        # text = "aura no microwave limb sounder eos mls level 2 water vapor data merra too. Other mls aura hcl and water vapor data was also used"
        sentences_list = []
        for original_sent in text.split("."):
            sent, keyword_count, found_missions, found_instruments, found_species, versions, levels, found_models = substitute_keywords(original_sent, keywords)
            valid_couples, single_mission, single_instrument = find_valid_couples(found_missions, found_instruments, all_couples, levels)

            # stats based on number of sentences it appeared in
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

            if keyword_count >= 1:
                s = {
                    "sentence": re.sub(r' {2,}', ' ', sent).strip(),
                    "couples": list(valid_couples),
                    "missions": list(single_mission),
                    "instruments": list(single_instrument),
                    "species": list(found_species),
                    "version": versions,
                    "levels": levels,
                }
                sentences_list.append(s)

        # compute the CMR Queries
        cmr_couples_results = {}
        cmr_singles_results = {}

        for vc in summary_stats['valid_couples']:
            platform_instrument = vc.split('----')
            if len(platform_instrument) > 1:
                level = platform_instrument[1]
                platform_instrument = platform_instrument[0]
            else:
                platform_instrument = platform_instrument[0]
                level = None

            for science_keyword in summary_stats['species']:
                if summary_stats['species'][science_keyword] <= 1:
                    continue
                # query_str, cmr_dataset, url = get_top_cmr_dataset(vc.split('/')[0], vc.split('/')[1], science_keyword, num_results=5)
                # _, cmr_dataset_false, url_false = get_top_cmr_dataset(vc.split('/')[0], vc.split('/')[1], science_keyword, science_keyword_search=False, num_results=5)
                query_str, cmr_dataset, url = get_top_cmr_dataset(platform_instrument.split('/')[0], platform_instrument.split('/')[1], science_keyword,
                                                                  num_results=5, level=level)
                _, cmr_dataset_false, url_false = get_top_cmr_dataset(platform_instrument.split('/')[0], platform_instrument.split('/')[1],
                                                                      science_keyword, science_keyword_search=False,
                                                                      num_results=5, level=level)
                # cmr_couples_results[query_str] = {
                #     "dataset": cmr_dataset,
                #     "query": url
                # }
                cmr_couples_results[query_str] = {
                    "science_keyword_search": {
                        "dataset": cmr_dataset,
                        "query": url
                    },
                    "keyword_search": {
                        "dataset": cmr_dataset_false,
                        "query": url_false
                    }
                }

        instruments_in_pairs = [vc.split('/')[1] for vc in summary_stats['valid_couples']]
        for instrument in summary_stats['single_instrument']:
            if instrument not in instruments_in_pairs:
                for science_keyword in summary_stats['species']:
                    query_str, cmr_dataset, url = get_top_cmr_dataset(None, instrument, science_keyword, num_results=5)
                    _, cmr_dataset_false, url_false = get_top_cmr_dataset(None, instrument, science_keyword, num_results=5)
                    # cmr_singles_results[query_str] = {
                    #     "dataset": cmr_dataset,
                    #     "query": url
                    # }
                    cmr_singles_results[query_str] = {
                        "science_keyword_search": {
                            "dataset": cmr_dataset,
                            "query": url
                        },
                        "keyword_search": {
                            "dataset": cmr_dataset_false,
                            "query": url_false
                        }
                    }


        # print("cmr_results", cmr_couples_results)
        paper_to_results[paper] = {
            "summary_stats": summary_stats,
            "cmr_results": {
                "pairs": cmr_couples_results,
                "singles": cmr_singles_results
            },
            "sentences": sentences_list
        }
        # print(paper, paper_to_results[paper])
        if count % 100 == 0:
            with open(f'partial_results_{count}.json', 'w', encoding='utf-8') as f:
                json.dump(paper_to_results, f, indent=4)

    return paper_to_results

if __name__ == '__main__':
    run_keyword_sentences()
