import re
import json
from collections import defaultdict
import itertools
from enum import Enum


class RunningMode(Enum):
    ALL_FILES = 1,
    SINGLE_FILE = 2,
    SINGLE_SENTENCE = 3


class SentenceMode(Enum):
    BROAD = 1,
    STRICT = 2


# convert everything to short names. ie: water vapor -> h2o
def standardize(mission, instrument, variable, complex_dataset, aliases):
    for index, m in enumerate(mission):
        if m in aliases["mission_aliases"]:
            mis = aliases["mission_aliases"][m].lower()
            mission[index] = mis

    for index, ins in enumerate(instrument):
        if ins in aliases["instrument_aliases"]:
            ins = aliases["instrument_aliases"][ins]
            instrument[index] = ins

    for index, v in enumerate(variable):
        if v in aliases["var_aliases"]:
            var = aliases["var_aliases"][v]
            variable[index] = var

    for index, cd in enumerate(complex_dataset):
        if cd in aliases['exception_aliases']:
            temp_dataset = aliases["exception_aliases"][cd].lower()
            complex_dataset[index] = temp_dataset

    return mission, instrument, variable, complex_dataset


def check_if_valid_couple(mission, instrument, couples, debug=False):
    # only works for all lowercase
    potential_instruments = couples.get(mission, [])
    result = instrument in potential_instruments
    if debug and result:
        print("Valid Couple ", mission, instrument)
    elif debug and not result:
        print("Invalid Couple ", mission, instrument)
    return result


# This will output the potential tags. It simply takes the possible permutations of the missions, instruments and variables
# and outputs all the possible permutations of each that occur. Note again that MLS implies the aura satellite
def get_tags(mission_input, instrument_input, variable_input, aliases):
    tags = []
    mission, instrument, variable, complex_dataset = standardize(mission_input, instrument_input, variable_input,
                                                                 aliases)
    for perm in itertools.product(*[mission, instrument, variable]):
        mis, ins, var = perm
        # if mis == "mls" or mis == "microwave limb sounder":
        #     mis = "aura"
        if (mis + "/" + ins, var) not in tags:
            tags.append((mis + "/" + ins, var))
    return tags


def load_in_GES_parameters(outside=False):
    path_modifier = ""
    if outside:
        path_modifier = "../"
    with open(path_modifier + "data/json/aliases.json") as jsonfile:
        aliases = json.load(jsonfile)

    with open(path_modifier + 'data/json/GES_missions.json') as jsonfile:
        missions = json.load(jsonfile)

    with open(path_modifier + 'data/json/GES_instruments.json') as jsonfile:
        instruments = json.load(jsonfile)

    with open(path_modifier + 'data/json/variables.json') as jsonfile:
        variables = json.load(jsonfile)

    with open(path_modifier + 'data/json/mission_instrument_couples_LOWER.json') as f:
        valid_couples = json.load(f)

    with open(path_modifier + 'data/json/models_and_analyses_LOWER.json') as f:
        complex_datasets = json.load(f)

    return aliases, missions, instruments, variables, valid_couples, complex_datasets


def is_ordered_subset(subset, sentence):
    sub = subset.split(" ")
    lst = sentence.split(" ")
    ln = len(sub)
    for i in range(len(lst) - ln + 1):
        if all(sub[j] == lst[i + j] for j in range(ln)):
            return True
    return False


def label_important_pieces(mission, instrument, variable, exception, sentence, data, tag=None, reanalysis=False, aliases=None):
    if reanalysis:
        tag = mission
        data[tag].append(sentence)
    else:
        # if mission is not None and instrument == 'n/a' and variable == 'n/a':  # complex datasets
        #     tag = mission
        if tag is None:
            tag = "(" + mission + '/' + instrument + ',' + variable + ")"
        data[tag].append({
            "mission": mission,
            "instrument": instrument,
            "variable": variable,
            "sentence": sentence
            # "sentence": text_substitution(sentence, aliases, mission, instrument, variable, None)
        })


# This function takes the text of a preprocessed txt document and outputs the notes. Each note contains all
# the notes for each (mission/instrument, variable) tuple. It also passes through the aliases used in this file
# The output format is a dictionary with key = (mission/instrument, variable) and value = list of sentences with matches
def produce_notes_broad(text, aliases, missions, instruments, variables, complex_datasets, debug=False,
                        sent_mode=SentenceMode.BROAD, couples=None, debug_couples=False):
    text = re.sub("[\(\[].*?[\)\]]", "",
                  text)  # I think this is to remove the citations. Does this also not remove like Global Position System (GPS)
    text = re.sub("\n", " ", text)
    text = re.sub("- ", "", text)
    text = re.sub("/", " ", text)
    text = re.sub(r',', '', text)  # commas. Otherwise things like ozone, temperature, don't get found
    text = re.sub(r' +', ' ', text)

    data = defaultdict(list)
    reanalysis_data = defaultdict(list)

    var_stats_total = {}
    for s in text.split("."):
        s = s.strip()
        mission = []
        instrument = []
        var = []
        complex_dataset = []

        for c in complex_datasets:
            if is_ordered_subset(c.lower(), s.lower()):
                complex_dataset.append(c)

        for m in missions:
            if is_ordered_subset(m, s.lower()):
                mission.append(m)

        for i in instruments:
            if is_ordered_subset(i, s.lower()):
                instrument.append(i)

        for v in variables:
            # shortcut around 'NO'
            if v == 'no':
                if is_ordered_subset('NO', s):
                    var.append(v)
            elif is_ordered_subset(v, s.lower()):
                var.append(v)
        if mission is None and instrument is None and var is None and complex_dataset is None:  # None of them found
            continue

        mission, instrument, variable, complex_dataset = standardize(mission, instrument, var, complex_dataset, aliases)

        # @todo: generalize this solution
        if 'merra' in complex_dataset and 'merra-2' in complex_dataset:
            complex_dataset.remove('merra')
        if 'merra' in mission and 'merra-2' in mission:
            mission.remove('merra')

        # sometimes get instrument = ['buv', 'sbuv', 'sbuv']. ALSO needs to be more Restrive for sbuv and buv
        instrument = list(set(instrument))

        if debug:
            print(s)
            print(complex_dataset)
            print(mission)
            print(instrument)
            print(var)

        # I think we only care about the mission name. @todo: check this with CMR_Queries
        # in couples the entries look like this, merra: ["not applicable"]
        for cd in complex_dataset:
            label_important_pieces(cd, 'n/a', 'n/a', False, s, reanalysis_data, reanalysis=True, aliases=aliases)
            if cd in mission:
                mission.remove(cd)

        # keep track of the variables that appear in the paper
        for v in var:
            var_stats_total[v] = var_stats_total.get(v, 0) + 1

        if mission and instrument and var:
            for perm in itertools.product(*[mission, instrument, variable]):
                if check_if_valid_couple(perm[0], perm[1], couples, debug_couples):
                    label_important_pieces(perm[0], perm[1], perm[2], False, s, data, aliases=aliases)
        # elif mission and instrument:
        #     for perm in itertools.product(*[mission, instrument]):
        #         if check_if_valid_couple(perm[0], perm[1], couples, debug_couples):
        #             label_important_pieces(perm[0], perm[1], 'None', False, s, data, aliases=aliases)

        elif sent_mode is SentenceMode.BROAD:
            if mission and var:
                for perm in itertools.product(*[mission, variable]):
                    label_important_pieces(perm[0], 'None', perm[1], False, s, data, aliases=aliases)
            elif instrument and var and len(complex_dataset) == 0:
                for perm in itertools.product(*[instrument, variable]):
                    label_important_pieces('None', perm[0], perm[1], False, s, data, aliases=aliases)
            elif mission and instrument:
                for perm in itertools.product(*[mission, instrument]):
                    if check_if_valid_couple(perm[0], perm[1], couples, debug_couples):
                        label_important_pieces(perm[0], perm[1], 'None', False, s, data, aliases=aliases)
    # print("var_stats_total ", var_stats_total)
    return data, reanalysis_data, var_stats_total


def add_to_csv(d, paper_name):
    csv_columns = ['paper', 'mission', 'instrument', 'variable', 'exception', 'sentence']
    csv_text = ""
    csv_text += "\n\n" + ",".join(csv_columns) + "\n"
    csv_text += paper_name
    for key in d.keys():
        # csv_text += str(key) + ',\n'
        for value in d[key]:
            csv_text += ","  # b/c we are leaving the paper column blank
            csv_text += str(value['mission']) + ","
            csv_text += str(value['instrument']) + ","
            csv_text += str(value['variable']) + ","
            csv_text += str(value['exception']) + ","
            sentence = value['sentence'] + "\n"
            sentence = re.sub(r',', '', sentence)
            csv_text += sentence + "\n"

    return csv_text


def get_paper_name(file_name, keyed_items):
    base_file_name = file_name.split(".")[0]
    try:
        title = keyed_items[base_file_name]['data']['filename']
        return base_file_name + " (" + title + ")"
    except KeyError:
        return base_file_name


def compute_summary_statistics_basic(data):
    mission_statistics = {}
    instrument_statistics = {}
    variable_statistics = {}
    mission_instrument_statistics = {}
    mis_ins_couples = {}
    mis_ins_var = {}
    values_to_avoid = {'n/a', 'None'}
    for key, value in data.items():
        for list_entry in value:
            mis = list_entry['mission']
            ins = list_entry['instrument']
            var = list_entry['variable']

            mission_statistics[mis] = mission_statistics.get(mis, 0) + 1
            instrument_statistics[ins] = instrument_statistics.get(ins, 0) + 1
            variable_statistics[var] = variable_statistics.get(var, 0) + 1
            if not any(mis == word for word in values_to_avoid) and not any (ins == word for word in values_to_avoid):
                mis_ins_couples[(mis, ins)] = mis_ins_couples.get((mis, ins), 0) + 1
            mission_instrument_statistics[(mis, ins)] = mission_instrument_statistics.get((mis, ins), 0) + 1
            mis_ins_var[(mis, ins, var)] = mis_ins_var.get((mis, ins, var), 0) + 1

    for key in values_to_avoid:
        mission_statistics.pop(key, None)
        instrument_statistics.pop(key, None)
        variable_statistics.pop(key, None)
    return mission_statistics, instrument_statistics, variable_statistics, mission_instrument_statistics, mis_ins_couples, mis_ins_var


def dict_to_csv_string(dict_to_convert):
    res = "\n"
    if dict_to_convert:
        for key, value in dict_to_convert.items():
            res += key + "," + str(value) + "\n"
    return res


def write_to_csv(file_name, data_to_write, mission_s=None, instrument_s=None, variable_s=None, mission_ins_s=None):
    mission_ins_summary = ""

    if mission_ins_s:  # include counts of valid mission/instrument couples
        for key, value in mission_ins_s.items():
            if key[0] is not 'None':
                joined_key = "(" + key[0] + ":" + key[1] + ")"
                mission_ins_summary += joined_key + "," + str(value) + "\n"

    # other counts
    # mission_summary = dict_to_csv_string(mission_s)
    instrument_summary = dict_to_csv_string(instrument_s)
    variable_summary = dict_to_csv_string(variable_s)

    data_to_write = mission_ins_summary + instrument_summary + variable_summary + data_to_write

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(data_to_write)



def text_substitution(sentence, aliases, mission, instrument, variable, complex_datasets):
    # main is short-> to long.
    # parameters are short name
    sentence = sentence.lower()

    if mission and mission != 'None':
        for m in mission:
            # candidates = [aliases['mission_main'][mission], mission]
            if m in aliases['mission_main']:
                long_mission = aliases['mission_main'][m]
                if long_mission != '':
                    sentence = re.sub(rf'{long_mission}', m, sentence)
    if instrument and instrument != 'None':
        for i in instrument:
            if i in aliases['instrument_main']:
                long_instrument = aliases['instrument_main'][i]
                if long_instrument != '':
                    sentence = re.sub(rf'{long_instrument}', i, sentence)

    if variable and variable != 'None':
        # main is short to long
        for v in variable:
            if v in aliases['var_main']:  # var main has 'h20' -> water vapor
                long_variable = aliases['var_main'][v]
                if long_variable != '':
                    sentence = re.sub(rf'{long_variable}', v, sentence)

    if complex_datasets:
        for cd in complex_datasets:
            if cd in aliases["exception_main"]:
                comp_data = aliases["exception_main"][cd].lower()
                if comp_data != '':
                    sentence = re.sub(rf'{comp_data}', cd, sentence)

    return sentence



def create_sentences_for_ML(text, sentence_mode):
    # sentence_mode = SentenceMode.STRICT
    aliases, missions, instruments, variables, valid_couples, complex_datasets = load_in_GES_parameters(outside=True)
    data, reanalysis_data, var_stats = produce_notes_broad(text, aliases, missions, instruments, variables, complex_datasets,
                               sent_mode=sentence_mode, couples=valid_couples)
    return data, reanalysis_data, var_stats


if __name__ == '__main__':
    print("These functions are usually called from other files such as aura_input_features.py")
    # running_mode = RunningMode.SINGLE_SENTENCE
    # sentence_mode = SentenceMode.STRICT
    #
    # file_directory_if_applicable = 'convert_using_cermzones/text/'
    # file_if_applicable = '2GA7MN73.txt'  # Dolinar
    #
    # preprocessed_directory = 'z_active/preprocessed/'
    # output_directory = 'z_active/sentences/'
    # csv_results = ""
    #
    # aliases, missions, instruments, variables, valid_couples, complex_datasets = load_in_GES_parameters()
    # # see if produce_notes_strict and produce_notes_broad(sent_mode = Strict) produce the same results
    #
    # if running_mode is RunningMode.SINGLE_SENTENCE:
    #     sentence = 'The Earth Observing System Microwave Limb Sounder (MLS) aboard the NASA Aura satellite provides a homogeneous, near-global (82°N to 82°S) observational data set of many important trace species, including water vapor in the UTLS'
    #     sentence = 'For the MLR analysis  we additionally consider equatorial ozone from the Global OZone Chemistry And Related trace gas Data records for the Stratosphere  Solar Backscatter Ultraviolet Instrument Merged Cohesive  SBUV Merged Ozone Dataset  composites and temperature from the Stratospheric Sounding Unit observations  and Japanese 55-year Reanalysis   and Modern-Era Retrospective analysis for Research and Applications   reanalyses'
    #     sentence = 'The ClO a priori profile was the same as that for Odin SMR which was based on the UARS MLS climatology'
    #     sentence = 'Between 10 and 87 km altitude the MLS temperature and pressure profiles collected during VESPA-22 observations in a radius of 300 km from the observation point of VESPA-22 are averaged together to produce a single set of daily meteorological vertical profiles'
    #     sentence = 'had also previously shown that the SBUV total ozone agrees to within 1 % with the ground-based Brewer-Dobson instrument network lidar and ozonesondes and was consistent with SAGE-II and Aura MLS satellite observations to within 5 %'
    #     sentence = 'modern-era retrospective analysis for research and applications version 2 was used with MLS data'
    #     sentence = 'aura is equipped with the mls  instrument , which is designed to make high-quality measurements of upper atmospheric temperature water vapor ozone a'
    #     data = produce_notes_broad(sentence, aliases, missions, instruments, variables, complex_datasets, debug=True,
    #                                sent_mode=sentence_mode, couples=valid_couples)
    #     print("Data ", data)
    #     csv_results += add_to_csv(data, paper_name="Single Sentence")
    #     print(csv_results)
    #     with open("TEMPORARY_SENTENCE.csv", 'w', encoding='utf-8') as f:
    #         f.write(csv_results)
    #
    # elif running_mode is RunningMode.SINGLE_FILE:
    #     with open(file_directory_if_applicable + file_if_applicable, encoding='utf-8') as f:
    #         txt = f.read()
    #     data = produce_notes_broad(txt, aliases, missions, instruments, variables, complex_datasets,
    #                                sent_mode=sentence_mode, couples=valid_couples)
    #     csv_results += add_to_csv(data, file_if_applicable)
    #     with open('sent_' + file_if_applicable.replace('.txt', '.csv'), 'w', encoding='utf-8') as f:
    #         f.write(csv_results)
    #
    #     print(data)
    #
    # elif running_mode is RunningMode.ALL_FILES:
    #     with open('data/json/edward_aura_mls_zot_keyed.json') as f:
    #         keyed_items = json.load(f)
    #     for file in tqdm(glob.glob(preprocessed_directory + "*.txt")):
    #         file_name = file.split("\\")[-1]
    #         print(file_name)
    #         with open(file, encoding='utf-8') as f:
    #             txt = f.read()
    #
    #         data = produce_notes_broad(txt, aliases, missions, instruments, variables, complex_datasets,
    #                                    sent_mode=sentence_mode, couples=valid_couples)
    #         csv_results += add_to_csv(data, get_paper_name(file_name, keyed_items))
    #
    #         # with open(output_directory + file_name.replace('.txt', '.csv'), 'w', encoding='utf-8') as f:
    #         #     f.write(csv_results)
    #
    #         mission_stats, instrument_stats, variable_stats, mission_instrument_stats = compute_summary_statistics_basic(
    #             data)
    #         print(mission_stats)
    #         print(instrument_stats)
    #         print(variable_stats)
    #         print(mission_instrument_stats)
    #
    #         write_to_csv(output_directory + file_name.replace('.txt', '.csv'), csv_results, mission_s=mission_stats, instrument_s=instrument_stats,
    #                      variable_s=variable_stats, mission_ins_s=mission_instrument_stats)
    #         csv_results = ""
