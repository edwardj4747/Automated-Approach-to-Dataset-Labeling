import json
from collections import Counter

with open('../ml_data/raw_data_aura_mls_ONLY_noNO.json') as f:
    raw_data = json.load(f)

counts = {}
for key, value in raw_data.items():
    ground_truth = value['ground_truths']
    for dataset in ground_truth:
        counts[dataset] = counts.get(dataset, 0) + 1


counter = Counter(counts)
print(counter.most_common(len(counts)))
print("Alphabetically ", sorted(counts))
print("Number of unique datasets ", len(counts))