# Extract the lowest level science keywords from all of the dataset metadeta.
import json
import glob
import csv

dataset_directory = 'C:/Users/edwar/Desktop/Publishing Internship/datasets'
output_file_name = 'science_keywords_E.csv'
output_file_location = '../data/csv/' + output_file_name
relevant_science_keywords = []

keyword_to_variable_level = {}

for file in glob.glob(dataset_directory + "/*.json"):
    print(file)
    with open(file, errors='ignore') as f:
        contents = json.load(f)

    science_keywords = contents['ScienceKeywords']
    for index, elements in enumerate(science_keywords):  # will sometimes be a list
        max_variable_level = max((key[-1] for key in elements.keys() if key.startswith("VariableLevel")), default=None)
        if max_variable_level is None:
            continue
        highest_precision_key = "VariableLevel" + max_variable_level
        new_science_keyword = contents['ScienceKeywords'][index][highest_precision_key]
        relevant_science_keywords.append(new_science_keyword)
        keyword_to_variable_level[new_science_keyword] = highest_precision_key

# save the keyword_to_variable_mapping
with open('../data/json/species_to_variable_level.json', 'w', encoding='utf-8') as f:
    json.dump(keyword_to_variable_level, f, indent=4)


# # add the science keywords to a set PRESERVING THEIR ORDER
# seen = set()
# seen_add = seen.add
# unique_order_preserved = [x for x in relevant_science_keywords if not (x in seen or seen_add(x))]
#
# with open(output_file_location, "w", newline='') as f:
#     writer = csv.writer(f, delimiter='\n')
#     writer.writerow(unique_order_preserved)

