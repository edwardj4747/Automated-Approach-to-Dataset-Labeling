import json

with open('partial_res_version_1/features.json') as f:
    features = json.load(f)

with open('partial_res_version_1/features_merged.json') as f:
    features_merged = json.load(f)

with open('partial_res_version_1/key_title_ground_truth.json') as f:
    key_title_ground_truth = json.load(f)

print(len(features))
print(len(features_merged))
print(len(key_title_ground_truth))