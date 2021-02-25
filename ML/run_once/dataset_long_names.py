import json
import glob
import csv
import re
from collections import defaultdict

'''
    Create mappings for
        dataset short name -> dataset long name
        dataset long name -> dataset short name
'''

dataset_directory = 'C:/Users/edwar/Desktop/Publishing Internship/datasets'
output_file_name = 'long_dataset_names.json'
output_file_location = '../data/csv/' + output_file_name
long_name_list = defaultdict(list)  # series-name : long-name

for file in glob.glob(dataset_directory + "/*.json"):
    # print(file)
    with open(file, errors='ignore') as f:
        contents = json.load(f)

    collection_citations = contents['CollectionCitations']
    for list_item in collection_citations:
        series_name = list_item["SeriesName"]
        long_name = list_item['Title']
        # print(long_name)
        long_name = re.sub(r' ?[vV][0-9]+\.?([0-9]+)? ?', '', long_name)  # remove the dataset version
        long_name_list[series_name].append(long_name)

print(long_name_list)

for key, value in long_name_list.items():
    if len(value) > 1:
        long_name_list[key] = list(set(value))

print("*********")
for key, value in long_name_list.items():
    long_name_list[key] = value[0]

for key, value in long_name_list.items():
    print(key, value)

with open('../../data/json/dataset_long_names.json', 'w', encoding='utf-8') as f:
    json.dump(long_name_list, f, indent=4)

with open('../../data/json/dataset_long_to_short.json', 'w', encoding='utf-8') as f:
    long_to_short = {value:key for key, value in long_name_list.items()}
    json.dump(long_to_short, f, indent=4)