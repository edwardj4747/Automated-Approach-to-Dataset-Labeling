# create a dict of (mis/ins): dataset_file names
import json
import glob
from collections import defaultdict


def standardize_and_tag(mission, instrument, aliases):
    if mission in aliases["mission_aliases"]:
        mission = aliases["mission_aliases"][mission].lower()

    if instrument in aliases["instrument_aliases"]:
        instrument = aliases["instrument_aliases"][instrument]

    return mission if instrument == 'not applicable' else mission + ":" + instrument


def remove_duplicate_list_entries(input_list):
    # remove the duplicate entry (preserve order)
    seen = set()
    unique = []
    for item in input_list:
        if item not in seen:
            unique.append(item)
        seen.add(item)

    return unique


dataset_directory = 'C:/Users/edwar/Desktop/Publishing Internship/datasets'
output_file_name = 'couples_to_datasets.json'
output_file_location = '../data/json/' + output_file_name

data = defaultdict(list)
datasets_to_couples = defaultdict(list)

with open('../data/json/aliases.json', encoding='utf-8') as f:
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

        instruments = elements['Instruments']
        for instrument in instruments:
            short_instrument = instrument.get('ShortName', '').lower()
            tag = standardize_and_tag(short_mission, short_instrument, aliases)
            data[tag].append(dataset_name_based_on_file)
            datasets_to_couples[dataset_name_based_on_file].append(tag)

for key, value in data.items():
    data[key] = remove_duplicate_list_entries(value)

with open(output_file_location, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

with open('../data/json/datasets_to_couples.json', 'w', encoding='utf-8') as f:
    json.dump(datasets_to_couples, f, indent=4)
