# Extract the lowest level science keywords from all of the dataset metadeta.
import json
import glob
import csv

dataset_directory = 'C:/Users/edwar/Desktop/Publishing Internship/datasets'
output_file_location = '../data/csv/'
mission_short_to_long = {}
instruments_short_to_long = {}

for file in glob.glob(dataset_directory + "/*.json"):
    print(file)
    with open(file, errors='ignore') as f:
        contents = json.load(f)

    platforms = contents['Platforms']
    for index, elements in enumerate(platforms):  # will sometimes be a list
        short_mission = elements.get('ShortName', '')
        long_mission = elements.get('LongName', '')
        mission_short_to_long[short_mission] = long_mission

        instruments = elements['Instruments']
        for instrument in instruments:
            short_instrument = instrument.get('ShortName', '')
            long_instrument = instrument.get('LongName', '')
            instruments_short_to_long[short_instrument] = long_instrument

print(mission_short_to_long)
print(instruments_short_to_long)

# with open('../data/json/GES_missions.json', 'w') as f:
#     m = []
#     for key, value in mission_short_to_long.items():
#         m.append(key.lower())
#         if value != '':
#             m.append(value.lower())
#     json.dump(m, f, indent=4)
#
# with open('../data/json/GES_instruments.json', 'w') as f:
#     i = []
#     for key, value in instruments_short_to_long.items():
#         i.append(key.lower())
#         if value != '':
#             i.append(value.lower())
#     json.dump(i, f, indent=4)

with open('../data/json/GES_missions_short_to_long.json', 'w') as f:
    # json.dump(mission_short_to_long, f, indent=4)
    json.dump({k.lower(): v.lower() for k, v in mission_short_to_long.items()}, f, indent=4)

with open('../data/json/GES_instruments_short_to_long.json', 'w') as f:
    # json.dump(instruments_short_to_long, f, indent=4)
    json.dump({k.lower(): v.lower() for k, v in instruments_short_to_long.items()}, f, indent=4)




save = False

if save:
    # Save the missions
    mission_columns = ['ShortName', 'LongName']
    mission_file = "GES_missions.csv"
    with open(output_file_location + mission_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(mission_columns)
        for key, value in mission_short_to_long.items():
            writer.writerow([key, value])

    # Save the instruments
    instrument_columns = ['ShortName', 'LongName']
    instrument_file = "GES_instruments.csv"
    with open(output_file_location + instrument_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(instrument_columns)
        for key, value in instruments_short_to_long.items():
            writer.writerow([key, value])


