import json
import glob
from collections import defaultdict

dataset_directory = 'C:/Users/edwar/Desktop/Publishing Internship/datasets/'
output_file_name = 'mission_instrument_couples.json'
output_file_location = '../data/json/'

couples = defaultdict(set)  # short mission name : [ short instrument names ]

for file in glob.glob(dataset_directory + "*.json"):
    with open(file, encoding='utf-8') as f:
        contents = json.load(f)

    platforms = contents['Platforms']
    for index, elements in enumerate(platforms):  # will sometimes be a list
        short_mission = elements.get('ShortName', '')
        long_mission = elements.get('LongName', '')

        instruments = elements['Instruments']
        for instrument in instruments:
            short_instrument = instrument.get('ShortName', '')
            long_instrument = instrument.get('LongName', '')
            couples[short_mission].add(short_instrument)


couples_list = {}
for key, value in couples.items():
    couples_list[key] = list(value)

print(couples_list)

with open(output_file_location + output_file_name, 'w') as f:
    json.dump(couples_list, f, indent=4)
