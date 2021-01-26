# Extract a list of datasets like merra which have type Models/Analyses
import json
import glob
import csv

dataset_directory = 'C:/Users/edwar/Desktop/Publishing Internship/datasets'
output_file_name = 'models_and_analyses_LOWER.json'
output_file_location = '../data/json/' + output_file_name

model_datasets = []

for file in glob.glob(dataset_directory + "/*.json"):
    print(file)
    with open(file, errors='ignore') as f:
        contents = json.load(f)

    platforms = contents['Platforms']
    for index, elements in enumerate(platforms):  # will sometimes be a list
        platform_type = elements['Type']
        if platform_type == 'Models/Analyses':
            short_name = elements['ShortName']
            model_datasets.append(short_name.lower())
            try:
                long_name = elements['LongName']
                model_datasets.append(long_name.lower())
            except KeyError:
                pass


# add the science keywords to a set PRESERVING THEIR ORDER
seen = set()
seen_add = seen.add
model_datasets_unique = [x for x in model_datasets if not (x in seen or seen_add(x))]

print(model_datasets_unique)

with open(output_file_location, 'w') as f:
    json.dump(model_datasets_unique, f, indent=4)




