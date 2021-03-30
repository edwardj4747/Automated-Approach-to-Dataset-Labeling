# Calculate some features based on the top-n stats calculated
# total number of distinct datasets
# total number of distinct datasets correct

import json
from collections import defaultdict

with open('Aura_mls_cme_top_1.json', encoding='utf-8') as f:
    stats = json.load(f)



unique_datasets = set()
unique_datasets = unique_datasets.union(stats['correct_dict']).union(stats['missed_dict']).union(['extraneous_dict'])

thresh = 1
unique_datasets_thresh = set()
correct_thresh = [k for k, v in stats['correct_dict'].items() if v > thresh]
missed_thresh = [k for k, v in stats['missed_dict'].items() if v > thresh]
extraneous_thresh = [k for k, v in stats['extraneous_dict'].items() if v > thresh]

unique_datasets_thresh = unique_datasets_thresh.union(correct_thresh)\
                                                .union(missed_thresh)\
                                                # .union(extraneous_thresh)


print("total number of datasets ", len(unique_datasets))

print("total number of datasets threshold ", len(unique_datasets_thresh))
print("correct thresh ", len(correct_thresh))
print("missed thresh ", len(missed_thresh))
# print("extraneous thresh ", len(extraneous_thresh))

total_counts = defaultdict(int)

for k, v in stats['correct_dict'].items():
    total_counts[k] += v
for k, v in stats['missed_dict'].items():
    total_counts[k] += v

print(sorted(total_counts.items(), key=lambda x: x[1], reverse=True))
tc_one = [x for x in total_counts if total_counts[x] == 1]
print(len(tc_one))