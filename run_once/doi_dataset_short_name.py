import json
import glob
from collections import defaultdict

'''
    create a dictionary mapping each dataset DOI to the short name of the dataset
'''

dataset_directory = 'C:/Users/edwar/Desktop/Publishing Internship/datasets/'
output_file_name = 'doi_to_dataset_name.json'
output_file_location = '../data/json/'

no_doi_count = 0
doi_to_shortname = {}

for file in glob.glob(dataset_directory + "*.json"):
    with open(file, encoding='utf-8') as f:
        contents = json.load(f)
    # print(file)
    try:
        doi = contents['DOI']['DOI'].replace("doi:", "")
    except KeyError as e:
        no_doi_count += 1
        print("no doi for ", file)
        continue

    if doi == "Change" or doi == "TBD":
        continue

    dataset_short_name = contents['ShortName']
    series_name = contents['CollectionCitations'][0]['SeriesName']

    doi_to_shortname[doi] = dataset_short_name

print("Number of collections without doi", no_doi_count)

with open(output_file_location + output_file_name, 'w') as f:
    json.dump(doi_to_shortname, f, indent=4)
