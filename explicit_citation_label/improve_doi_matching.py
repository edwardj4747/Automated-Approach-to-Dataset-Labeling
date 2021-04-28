# Some citations with dois are getting sucked into free text because there are extra spaces of the capitalization
# was off or some small thing of that nature. Goal: Fix that

'''
    Common causes in forward gesdisc collection (these probably generalize/cannot hurt)
    10.5067/ restOfDoi (there is a space)

    https://doi.org/10.5067/GPM/IMERGDF/ DAY/05 ?? Is this the same as DAY/06 which is valid

     https://doi.org/10.5067/5NHC2 2T9375G  # missing a single char

     https://doi.org/10.5067/Aura/MLS/ DATA2 017  # a couple of extra spaces  # maybe use an is ordered subset type thing

     extra space https://doi.org/10.5067/VJAFPLI1 CSIV

     doi.org/10.5067/vjafpli1csiv  # perfect but was searched in case sensitive way

     https://doi.org/10.5067/GPM/ IMERGDF/DAY/06

     10.5067/ SXAVCZFAQLNO  # spaces after /
'''

import regex as re
import json
import copy
from nltk import edit_distance


with open('free_text/forward_ges_references_and_text_clean.json') as f:
    explicit = json.load(f)

explicit_modified = copy.deepcopy(explicit)

doi_to_dataset_mapping_location = '../data/json/doi_to_dataset_name.json'
doi_to_dataset_mapping_regex_location = '../data/json/doi_to_dataset_name_regex.json'

with open(doi_to_dataset_mapping_location) as f:
    doi_to_dataset = json.load(f)

with open(doi_to_dataset_mapping_regex_location) as f:
    doi_to_dataset_regex = json.load(f)

dataset_to_doi = {v: k for k, v in doi_to_dataset.items()}
regex_doi_to_doi = {k: dataset_to_doi[doi_to_dataset_regex[k]] for k in doi_to_dataset_regex}

# for key, value in explicit.items():
#     free_text = value['free_text']
#     if len(free_text) > 0:
#         for regex_doi in doi_to_dataset_regex:
#             matches = re.findall(rf'{regex_doi}', ' '.join(free_text))
#             if len(matches) >= 1:
#                 standard_doi = regex_doi_to_doi[regex_doi]
#                 print(free_text)
#                 print(standard_doi)
#                 print()
#                 # add in the doi and remove the free text
#                 explicit_modified[key]['explicit_dois'].append(standard_doi)
#                 explicit_modified[key]['free_text'] = []
#                 # add the dataset to the dois and dataset
#                 explicit_modified[key]['datasets_and_doi'].append(doi_to_dataset[standard_doi])

# with open('free_text/forward_ges_references_and_text_clean_doi_clean.json', 'w', encoding='utf-8') as f:
#     json.dump(explicit_modified, f, indent=4)

# Experiment with edit distance. In theory, edit distance is a good measurement to use for this in

for key, value in explicit.items():
    free_text = value['free_text']
    if len(free_text) > 0:
        # isolate the doi like thing
        after_doi = re.split(r'.*(?=10\.)', ' '.join(free_text))
        print(after_doi)
        continue

