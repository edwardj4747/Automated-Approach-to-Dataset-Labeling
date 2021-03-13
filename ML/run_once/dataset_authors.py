from collections import defaultdict
import json
import glob
import re

'''
    Create a dictionary mapping of dataset: [author(s) of the dataset] as based on the metadata files
'''


def dictionary_to_list(dataset_author_mapping, save=False):
    seen = set()
    unique_authors = []
    for list_of_authors in dataset_author_mapping.values():
        for author in list_of_authors:
            author = re.sub(r'^Dr\. ', '', author)  # remove the Dr. in a Dr. so-and-so
            author = re.sub(r'(, PH\. ?D\.?)|(, PHD)', '', author)
            author = author.lower()
            if author not in seen:
                unique_authors.append(author)
                seen.add(author)

    if save:
        with open('../ml_data/author_keywords_list.json', 'w', encoding='utf-8') as f:
            json.dump(unique_authors, f, indent=4)


dataset_directory = 'C:/Users/edwar/Desktop/Publishing Internship/datasets'
output_file_name = 'dataset_to_miv.json'
output_file_location = '../ml_data/' + output_file_name

data = defaultdict(list)

for file in glob.glob(dataset_directory + "/*.json"):
    print(file)
    with open(file, errors='ignore') as f:
        contents = json.load(f)

    dataset_name = contents['CollectionCitations'][0]['SeriesName']
    contact_person = contents['ContactPersons']

    authors = []
    for index, element in enumerate(contact_person):  # will sometimes be a list
        if "Investigator" in element['Roles']:
            author_name = element['FirstName'] + " " + element['LastName']
            authors.append(author_name)

    data[dataset_name] += authors

# Remove duplicate entries
for key, all_authors in data.items():
    seen = set()
    unique = []
    for item in all_authors:
        if item not in seen:
            unique.append(item)
        seen.add(item)
    data[key] = unique

with open('../ml_data/dataset_authors.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

dictionary_to_list(data, save=True)
