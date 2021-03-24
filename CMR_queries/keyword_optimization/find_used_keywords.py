import json
from collections import defaultdict


with open('../18-55-27features.json') as f:
    features = json.load(f)

with open('../../data/json/keywords.json') as f:
    keywords = json.load(f)

count_lists = defaultdict(list)

for key, value in features.items():
    # print(value['summary_stats']['species'])
    for species, count in value['summary_stats']['species'].items():
        count_lists[species].append(count)

# print(sorted(count_lists.items(), key=lambda x: x[1], reverse=True))

for species, species_count_list in sorted(count_lists.items(), key=lambda x: sum(x[1]), reverse=True):
    print(species)
    print(species_count_list)
    print()

# print all the keywords that are not found
variables_short_set = set(keywords['variables']['short_to_long'])
print(variables_short_set)
print()

count_lists_set = set(count_lists.keys())

print("Found keywords")
found = count_lists_set.intersection(variables_short_set)
print(found)


print()

print("Not Found")
not_found = variables_short_set - set(count_lists)
print(not_found)