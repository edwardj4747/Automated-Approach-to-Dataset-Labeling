import json

with open('data/344author_keywords_attempt_d1_mn4_tr6.json') as f:
    raw_data = json.load(f)


threshold = 10
all_datasets = {}
for key, value in raw_data.items():
    for ground_truth in value['ground_truths']:
        all_datasets[ground_truth] = all_datasets.get(ground_truth, 0) + 1

print(len(all_datasets))
sorted_by_freqs = sorted(all_datasets.items(), key=lambda x: x[1], reverse=True)
print(sorted_by_freqs)

new_datasets_to_inlude = [s[0] for s in sorted_by_freqs if not s[0].startswith('M2') and s[1] > threshold]
print("Datasets with more than 10 and Non merra: num datasets", len(new_datasets_to_inlude))
print(new_datasets_to_inlude)