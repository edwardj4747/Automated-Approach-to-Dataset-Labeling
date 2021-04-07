import json
from collections import defaultdict
import glob

dataset_directory = 'C:/Users/edwar/Desktop/Publishing Internship/datasets'
output_file_name = 'couples_to_datasets.json'
output_file_location = '../data/json/' + output_file_name


platform_csv = "~id, name, ~label, long_name \n"
instrument_csv = "~id, name, ~label, long_name \n"

platform_instrument_edges_csv = "~from, ~to, ~id, ~label\n"

platform_count, instrument_count = 0, 0
platform_to_idx, instrument_to_idx = {}, {}

platform_instrument_edges = set()

for file in glob.glob(dataset_directory + "/*.json"):

    with open(file, errors='ignore') as f:
        contents = json.load(f)

    dataset_name = contents['CollectionCitations'][0]['SeriesName']
    platforms = contents['Platforms']
    for index, elements in enumerate(platforms):  # will sometimes be a list
        short_platform = elements.get('ShortName', '').lower()
        long_platform = elements.get('LongName', '').lower()
        if short_platform not in platform_to_idx:
            platform_count += 1
            platform_to_idx[short_platform] = platform_count
            platform_csv += f'platform_{platform_count}, {short_platform}, platform, {long_platform} \n'

        instruments = elements['Instruments']
        for instrument in instruments:
            short_instrument = instrument.get('ShortName', '').lower()
            long_instrument = instrument.get('LongName', '').lower()

            if short_instrument not in instrument_to_idx:
                instrument_count += 1
                instrument_to_idx[short_instrument] = instrument_count
                instrument_csv += f'instrument_{instrument_count}, {short_instrument}, instrument, {long_instrument} \n'

            # create an edge relating the platform and the instrument
            platform_num = platform_to_idx[short_platform]
            instrument_num = instrument_to_idx[short_instrument]
            if (platform_num, instrument_num) not in platform_instrument_edges:
                platform_instrument_edges.add((platform_num, instrument_num))
                platform_instrument_edges_csv += f'platform_{platform_num}, instrument_{instrument_num}, edge_{short_platform}->{short_instrument}, contains\n'

with open('platform_vertices.csv', 'w', encoding='utf-8') as f:
    f.write(platform_csv)

with open('instrument_vertices.csv', 'w', encoding='utf-8') as f:
    f.write(instrument_csv)

with open('platform_instrument_edges.csv', 'w', encoding='utf-8') as f:
    f.write(platform_instrument_edges_csv)