import json
import glob
from collections import defaultdict

'''
    Create a mapping of dataset short name to the mission, instruments, and science keywords used by that dataset.
        ie: "GozMmlpHCl": ["uars/haloe,hcl", "aura/mls,hcl", "scisat-1/ace/ace-fts,hcl"],
'''


def standardize_and_tag(mission, instrument, variable, aliases):
    if mission in aliases["mission_aliases"]:
        mission = aliases["mission_aliases"][mission].lower()

    if instrument in aliases["instrument_aliases"]:
        instrument = aliases["instrument_aliases"][instrument]

    variable = variable.lower()
    if variable in aliases["var_aliases"]:
        variable = aliases["var_aliases"][variable]

    return mission if instrument == 'not applicable' else mission + "/" + instrument + "," + variable


def remove_duplicate_list_entries(input_list):
    # remove the duplicate entry (preserve order)
    seen = set()
    unique = []
    for item in input_list:
        if item not in seen:
            unique.append(item)
        seen.add(item)

    return unique


if __name__ == '__main__':
    dataset_directory = 'C:/Users/edwar/Desktop/Publishing Internship/datasets'
    output_file_name = 'dataset_to_miv.json'
    output_file_location = '../ml_data/' + output_file_name

    data = defaultdict(list)

    with open('../../data/json/aliases.json', encoding='utf-8') as f:
        aliases = json.load(f)

    for file in glob.glob(dataset_directory + "/*.json"):
        print(file)
        with open(file, errors='ignore') as f:
            contents = json.load(f)

        dataset_name = contents['CollectionCitations'][0]['SeriesName']
        dataset_name_based_on_file = file.split("\\")[-1].replace('.json', '')
        platforms = contents['Platforms']

        for index, elements in enumerate(platforms):  # will sometimes be a list
            short_mission = elements.get('ShortName', '').lower()
            # Science Keywords (variable)
            relevant_science_keywords = []
            science_keywords = contents['ScienceKeywords']
            for i, elem in enumerate(science_keywords):  # will sometimes be a list
                max_variable_level = max((key[-1] for key in elem.keys() if key.startswith("VariableLevel")),
                                         default=None)
                if max_variable_level is None:
                    continue
                highest_precision_key = "VariableLevel" + max_variable_level
                new_science_keyword = contents['ScienceKeywords'][i][highest_precision_key]
                relevant_science_keywords.append(new_science_keyword)

            instruments = elements['Instruments']
            for instrument in instruments:
                short_instrument = instrument.get('ShortName', '').lower()
                for science_keyw in relevant_science_keywords:
                    tag = standardize_and_tag(short_mission, short_instrument, science_keyw, aliases)
                    data[dataset_name].append(tag)
                    # datasets_to_couples[dataset_name].append(tag)

    for key, value in data.items():
        data[key] = remove_duplicate_list_entries(value)

    with open(output_file_location, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
