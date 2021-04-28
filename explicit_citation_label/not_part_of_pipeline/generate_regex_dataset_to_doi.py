import regex as re
import json


doi_to_dataset_mapping_location = '../data/json/doi_to_dataset_name.json'

with open(doi_to_dataset_mapping_location) as f:
    doi_to_dataset = json.load(f)

dataset_to_doi = {v: k for k, v in doi_to_dataset.items()}

regex_doi_to_dataset = {}

for key, value in doi_to_dataset.items():
    regex_key = re.sub(r'/', '/ ?', key)
    regex_doi_to_dataset[regex_key] = value

with open('../../data/json/doi_to_dataset_name_regex.json', 'w', encoding='utf-8') as f:
    json.dump(regex_doi_to_dataset, f, indent=4)