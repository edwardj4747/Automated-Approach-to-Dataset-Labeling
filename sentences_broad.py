import csv
import re
import json
from collections import defaultdict
import itertools
import pprint
import glob
from tqdm import tqdm
from enum import Enum

from config import params


# This code will produce the notes that are entered into Zotero. Each note contains an exact text match with a
# mission/instrument and variable pair or with a match with one of the exceptions. The exceptions include all datasets
# labeled with the Microwave limb sounder and each of the data models.


# Extracts the variables from the mission, instrument, and variable csvs. This will extract both the short names and
# the long names. It will output a list of all missions, variables and instruments and all the potential pairs
# The aliases dictionaries contain mapping from short name to long name and the main dictionaries contain a mapping from
# long name to short name

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


def load_in_GES_parameters():
    # As created in produce_notes.py
    with open("data/json/aliases.json") as jsonfile:
        aliases = json.load(jsonfile)

    with open('data/json/GES_missions.json') as jsonfile:
        missions = json.load(jsonfile)

    with open('data/json/GES_instruments.json') as jsonfile:
        instruments = json.load(jsonfile)

    with open('data/json/variables.json') as jsonfile:
        variables = json.load(jsonfile)

    with open('data/json/mission_instrument_couples.json_LOWER') as f:
        valid_couples = json.load(f)

    with open('data/json/models_and_analyses_LOWER.json') as f:
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


def label_important_pieces(mission, instrument, variable, exception, sentence, data, tag=None):
    if tag is None:
        tag = "(" + mission + '/' + instrument + ',' + variable + ")"
    data[tag].append({
        "mission": mission,
        "instrument": instrument,
        "variable": variable,
        "exception": exception,
        "sentence": sentence
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

    data = defaultdict(list)

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
            if is_ordered_subset(v, s.lower()):
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

        # I think we only care about the mission name. @todo: check this with Irina
        # in couples the entries look like this, merra: ["not applicable"]
        for cd in complex_dataset:
            label_important_pieces(cd, 'n/a', 'n/a', False, s, data)
            if cd in mission:
                mission.remove(cd)

        # if complex_dataset:
        #     print("inside if complex condition")
        #     if instrument and var:
        #         for perm in itertools.product(*[complex_dataset, instrument, variable]):
        #             label_important_pieces(perm[0], perm[1], perm[2], False, s, data)
        #     elif instrument and not var:
        #         for perm in itertools.product(*[complex_dataset, instrument]):
        #             label_important_pieces(perm[0], perm[1], '-', False, s, data)
        #     elif var and not instrument:
        #         for perm in itertools.product(*[complex_dataset, var]):
        #             label_important_pieces(perm[0], '-', perm[1], False, s, data)
        #     else:
        #         for complex_data in complex_dataset:
        #             label_important_pieces(complex_data, '-', '-', False, s, data)

        if mission and instrument and var:
            for perm in itertools.product(*[mission, instrument, variable]):
                if check_if_valid_couple(perm[0], perm[1], valid_couples, debug_couples):
                    label_important_pieces(perm[0], perm[1], perm[2], False, s, data)

        elif sent_mode is SentenceMode.BROAD:
            if mission and instrument:
                for perm in itertools.product(*[mission, instrument]):
                    if check_if_valid_couple(perm[0], perm[1], valid_couples, debug_couples):
                        label_important_pieces(perm[0], perm[1], 'None', False, s, data)
            elif mission and var:
                for perm in itertools.product(*[mission, variable]):
                    label_important_pieces(perm[0], 'None', perm[1], False, s, data)
            elif instrument and var and len(complex_dataset) == 0:
                for perm in itertools.product(*[instrument, variable]):
                    label_important_pieces('None', perm[0], perm[1], False, s, data)

        # for e in exception:
        #     if e in aliases["exception_aliases"]:
        #         e = aliases["exception_aliases"][e]
        #     data[(e, "none")].append({
        #         "mission": False,
        #         "instrument": False,
        #         "variable": False,
        #         "exception": e,
        #         "sentence": s,
        #     })

    return data


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


'''
todo: Missions has MLS + Microwave Limb Sounder. Why?
'''


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
    values_to_avoid = {'n/a', 'None'}
    for key, value in data.items():
        for list_entry in value:
            mis = list_entry['mission']
            ins = list_entry['instrument']
            var = list_entry['variable']

            mission_statistics[mis] = mission_statistics.get(mis, 0) + 1
            instrument_statistics[ins] = instrument_statistics.get(ins, 0) + 1
            variable_statistics[var] = variable_statistics.get(var, 0) + 1
            mission_instrument_statistics[(mis, ins)] = mission_instrument_statistics.get((mis, ins), 0) + 1

    for key in values_to_avoid:
        mission_statistics.pop(key, None)
        instrument_statistics.pop(key, None)
        variable_statistics.pop(key, None)
    return mission_statistics, instrument_statistics, variable_statistics, mission_instrument_statistics


def write_to_csv(file_name, data_to_write):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(data_to_write)

'''
@todo: continue working on the summary statistics and add them into the csv files
'''

if __name__ == '__main__':

    running_mode = RunningMode.SINGLE_FILE
    sentence_mode = SentenceMode.BROAD

    file_directory_if_applicable = 'convert_using_cermzones/text/'
    file_if_applicable = '2GA7MN73.txt'  # Dolinar

    preprocessed_directory = 'z_active/preprocessed/'
    output_directory = 'z_active/sentences/'
    csv_results = ""

    aliases, missions, instruments, variables, valid_couples, complex_datasets = load_in_GES_parameters()
    # see if produce_notes_strict and produce_notes_broad(sent_mode = Strict) produce the same results

    if running_mode is RunningMode.SINGLE_SENTENCE:
        sentence = 'The Earth Observing System Microwave Limb Sounder (MLS) aboard the NASA Aura satellite provides a homogeneous, near-global (82°N to 82°S) observational data set of many important trace species, including water vapor in the UTLS'
        sentence = 'For the MLR analysis  we additionally consider equatorial ozone from the Global OZone Chemistry And Related trace gas Data records for the Stratosphere  Solar Backscatter Ultraviolet Instrument Merged Cohesive  SBUV Merged Ozone Dataset  composites and temperature from the Stratospheric Sounding Unit observations  and Japanese 55-year Reanalysis   and Modern-Era Retrospective analysis for Research and Applications   reanalyses'
        sentence = 'The ClO a priori profile was the same as that for Odin SMR which was based on the UARS MLS climatology'
        sentence = 'Between 10 and 87 km altitude the MLS temperature and pressure profiles collected during VESPA-22 observations in a radius of 300 km from the observation point of VESPA-22 are averaged together to produce a single set of daily meteorological vertical profiles'
        sentence = 'had also previously shown that the SBUV total ozone agrees to within 1 % with the ground-based Brewer-Dobson instrument network lidar and ozonesondes and was consistent with SAGE-II and Aura MLS satellite observations to within 5 %'
        sentence = 'modern-era retrospective analysis for research and applications version 2 was used with MLS data'
        data = produce_notes_broad(sentence, aliases, missions, instruments, variables, complex_datasets, debug=True,
                                   sent_mode=sentence_mode, couples=valid_couples)
        csv_results += add_to_csv(data, paper_name="Single Sentence")
        print(csv_results)
        with open("TEMPORARY_SENTENCE.csv", 'w', encoding='utf-8') as f:
            f.write(csv_results)

    elif running_mode is RunningMode.SINGLE_FILE:
        with open(file_directory_if_applicable + file_if_applicable, encoding='utf-8') as f:
            txt = f.read()
        data = produce_notes_broad(txt, aliases, missions, instruments, variables, complex_datasets,
                                   sent_mode=sentence_mode, couples=valid_couples)
        csv_results += add_to_csv(data, file_if_applicable)
        with open('sent_' + file_if_applicable.replace('.txt', '.csv'), 'w', encoding='utf-8') as f:
            f.write(csv_results)

        print(data)

    elif running_mode is RunningMode.ALL_FILES:
        with open('data/json/edward_aura_mls_zot_keyed.json') as f:
            keyed_items = json.load(f)
        for file in tqdm(glob.glob(preprocessed_directory + "*.txt")):
            file_name = file.split("\\")[-1]
            print(file_name)
            with open(file, encoding='utf-8') as f:
                txt = f.read()

            data = produce_notes_broad(txt, aliases, missions, instruments, variables, complex_datasets,
                                       sent_mode=sentence_mode, couples=valid_couples)
            csv_results += add_to_csv(data, get_paper_name(file_name, keyed_items))

            # with open(output_directory + file_name.replace('.txt', '.csv'), 'w', encoding='utf-8') as f:
            #     f.write(csv_results)
            write_to_csv(output_directory + file_name.replace('.txt', '.csv'), csv_results)
            csv_results = ""

            mission_stats, instrument_stats, variable_stats, mission_instrument_stats = compute_summary_statistics_basic(
                data)
            print(mission_stats)
            print(instrument_stats)
            print(variable_stats)
            print(mission_instrument_stats)
    '''
    sample results
    Data: 
    ('aura/mls', 'h2o') [{'sentence': ' in this study, we evaluate the modern-era retrospective analysis for research and applications version 2  reanalyzed clear-sky temperature and water vapor profiles with newly generated atmospheric profiles from department of energy atmospheric radiation measurement -merged soundings and aura microwave limb sounder retrievals at three arm sites', 'mission': 'aura', 'instrument': 'mls', 'variable': 'h2o', 'exception': False}, {'sentence': ' mls water vapor is retrieved at a frequency of 190 ghz with acceptable range of 316–0', 'mission': 'aura', 'instrument': 'mls', 'variable': 'h2o', 'exception': False}, {'sentence': ' the estimated uncertainty of mls water vapor in the stratosphere is ~10%', 'mission': 'aura', 'instrument': 'mls', 'variable': 'h2o', 'exception': False}, {'sentence': ' the black line represents the hybrid profiles from the arm-merged soundings  and the microwave limb sounder  for atmospheric temperature and water vapor', 'mission': 'aura', 'instrument': 'mls', 'variable': 'h2o', 'exception': False}]
    ('aura/mls', 't') [{'sentence': ' in this study, we evaluate the modern-era retrospective analysis for research and applications version 2  reanalyzed clear-sky temperature and water vapor profiles with newly generated atmospheric profiles from department of energy atmospheric radiation measurement -merged soundings and aura microwave limb sounder retrievals at three arm sites', 'mission': 'aura', 'instrument': 'mls', 'variable': 't', 'exception': False}, {'sentence': ' the black line represents the hybrid profiles from the arm-merged soundings  and the microwave limb sounder  for atmospheric temperature and water vapor', 'mission': 'aura', 'instrument': 'mls', 'variable': 't', 'exception': False}]
    ('merra/mls', 'h2o') [{'sentence': ' in this study, we evaluate the modern-era retrospective analysis for research and applications version 2  reanalyzed clear-sky temperature and water vapor profiles with newly generated atmospheric profiles from department of energy atmospheric radiation measurement -merged soundings and aura microwave limb sounder retrievals at three arm sites', 'mission': 'merra', 'instrument': 'mls', 'variable': 'h2o', 'exception': False}]
    ('merra/mls', 't') [{'sentence': ' in this study, we evaluate the modern-era retrospective analysis for research and applications version 2  reanalyzed clear-sky temperature and water vapor profiles with newly generated atmospheric profiles from department of energy atmospheric radiation measurement -merged soundings and aura microwave limb sounder retrievals at three arm sites', 'mission': 'merra', 'instrument': 'mls', 'variable': 't', 'exception': False}]
    ('merra', 'none') [{'sentence': ' in this study, we evaluate the modern-era retrospective analysis for research and applications version 2  reanalyzed clear-sky temperature and water vapor profiles with newly generated atmospheric profiles from department of energy atmospheric radiation measurement -merged soundings and aura microwave limb sounder retrievals at three arm sites', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra'}, {'sentence': ' in this study, temperature and water vapor profiles from modern-era retrospective analysis for research and applications version 2 , along with the climatic aerosol optical depths over the three arm sites, are used as input to the radiative transfer model to calculate the clear-sky surface and toa radiative fluxes', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra'}, {'sentence': ' a new version of merra has been released with several major improvements, making it the centerpiece of the evaluation performed in this study', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra'}, {'sentence': ' this is in contrast to the one and a half million observations assimilated in merra from 2002 to the present', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra'}]
    ('merra-2', 'none') [{'sentence': ' the temperature profiles are well replicated in merra-2 at all three sites, whereas tropospheric water vapor is slightly dry below ~700 hpa', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra-2'}, {'sentence': ' the first objective of this study is to evaluate the merra-2 clear-sky temperature and water vapor profiles using a newly generated atmospheric profile data set', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra-2'}, {'sentence': ' section 2 documents the groundand satellite-based data sets used in this study, as well as several of the notable updates in the recently released merra-2 reanalysis', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra-2'}, {'sentence': ' profiles of atmospheric temperature, water vapor mixing ratio, and ozone mixing ratio have been generated from arm-merged sounding and satellite  retrievals over three arm sites, which are used to evaluate the merra-2 profiles', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra-2'}, {'sentence': ' merra-2 is horizontally discretized on a cubed sphere grid, which is superior to the latitude-longitude methods used in earlier versions', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra-2'}, {'sentence': ' for merra-2 the number of assimilated observations per 6 h increment has increased from three million in 2010 to five million in 2015; however, capabilities of assimilating future satellite observations are also developed', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra-2'}, {'sentence': ' merra-2 is available on a 0', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra-2'}, {'sentence': ' differences in the vertical profiles are expected since the merra-2 profiles cannot be perfectly collocated with the satellite ground-based data', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra-2'}, {'sentence': ' the blue line is from the closest merra-2 grid point, and the red line is the midlatitude climatological mean', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra-2'}, {'sentence': ' the hybrid and merra-2 water vapor mixing ratios match very well above ~850 hpa', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra-2'}, {'sentence': ' however, below 850 hpa, the merra-2 water vapor profile diverges from the hybrid profile to the drier side \x002 g g', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra-2'}, {'sentence': ' on the global scale, a moist bias in merra-2 can be up to 75–150% in the upper tropoby <0', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra-2'}, {'sentence': ' the midlatitude climate mean water vapor mixing ratio is less than both the hybrid and merra-2 profiles in the lower troposphere ', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra-2'}, {'sentence': ' temperature  is well reproduced in merra-2 at the twpc3 site through the troposphere; however, a slight discrepancy is seen just above the tropopause and below the stratopause, which could be an artifact of the coarser vertical resolution of merra-2', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra-2'}, {'sentence': ' the tropical climate mean temperature agrees well with the hybrid and merra-2 profiles in the troposphere but is slightly warmer in the stratosphere and mesosphere', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra-2'}, {'sentence': ' the twpc3 ozone comparison is similar to the results at the arm sgp and nsa sites, where the ozone profiles from merra-2 and the hybrid data set are very close', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra-2'}, {'sentence': ' yet still, a noticeable discrepancy between the two data sets can be seen from ~10 to 20 hpa, where merra-2 is slightly smaller', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra-2'}, {'sentence': ' the merra-2 atmospheric temperature profiles are nearly identical to the hybrid ones, and the climate mean temperature profiles agree with the hybrid ones within several kelvin', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra-2'}, {'sentence': ' since mls ozone data are directly assimilated into merra-2, it is not surprising that the merra-2 and hybrid ozone profiles match extremely well at all three arm sites', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra-2'}, {'sentence': ' most of the merra-2 water vapor mixing ratios agree well with the hybrid ones over three sites except for in the boundary layer at the arm twpc3', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra-2'}, {'sentence': ' a bias of greater than \x0020 w m2 is found in the surface lw_dn flux using the hybrid and merra-2 profiles, a result that is inconsistent with long and turner  and is likely due to the skin temperature used in the rtm', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra-2'}, {'sentence': ' vertical profiles of temperature at the three sites are well replicated in merra-2 when compared to the newly generated satellite surface-based  data set', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra-2'}, {'sentence': ' finally, the merra-2 tropospheric water vapor mixing ratios are, on average, on the drier side of the combined satellite surfacebased data set at sgp and nsa for snow-free conditions', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra-2'}, {'sentence': ' however, the relatively small and constant tropospheric water vapor profile at nsa for the snow cases is well replicated in merra-2', 'mission': False, 'instrument': False, 'variable': False, 'exception': 'merra-2'}]
    ('aura/mls', 'o3') [{'sentence': ' stratospheric ozone from mls is retrieved at a frequency of 240 ghz, which offers the best precision for a wide vertical range', 'mission': 'aura', 'instrument': 'mls', 'variable': 'o3', 'exception': False}, {'sentence': ' the recommended range of the mls ozone product is from 261 to 0', 'mission': 'aura', 'instrument': 'mls', 'variable': 'o3', 'exception': False}, {'sentence': ' the mls ozone product used for this study is also from version 4', 'mission': 'aura', 'instrument': 'mls', 'variable': 'o3', 'exception': False}, {'sentence': ' the ozone profile  is from the atmospheric infrared sounder  and mls', 'mission': 'aura', 'instrument': 'mls', 'variable': 'o3', 'exception': False}, {'sentence': ' since mls ozone data are directly assimilated into merra-2, it is not surprising that the merra-2 and hybrid ozone profiles match extremely well at all three arm sites', 'mission': 'aura', 'instrument': 'mls', 'variable': 'o3', 'exception': False}, {'sentence': ' since mls ozone is directly assimilated, the merra2 ozone mixing ratios are very close to the hybrid profiles at all three arm sites', 'mission': 'aura', 'instrument': 'mls', 'variable': 'o3', 'exception': False}]
    ('aura/airs', 'o3') [{'sentence': ' the ozone profile  is from the atmospheric infrared sounder  and mls', 'mission': 'aura', 'instrument': 'airs', 'variable': 'o3', 'exception': False}]
    ('merra-2/an', 't') [{'sentence': ' temperature  is well reproduced in merra-2 at the twpc3 site through the troposphere; however, a slight discrepancy is seen just above the tropopause and below the stratopause, which could be an artifact of the coarser vertical resolution of merra-2', 'mission': 'merra-2', 'instrument': 'an', 'variable': 't', 'exception': False}]
    ('merra-2/mls', 'o3') [{'sentence': ' since mls ozone data are directly assimilated into merra-2, it is not surprising that the merra-2 and hybrid ozone profiles match extremely well at all three arm sites', 'mission': 'merra-2', 'instrument': 'mls', 'variable': 'o3', 'exception': False}]

    '''
