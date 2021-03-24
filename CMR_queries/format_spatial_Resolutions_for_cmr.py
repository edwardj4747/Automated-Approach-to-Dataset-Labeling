import json

with open('3-22-15-Aura_omi_features.json', encoding='utf-8') as f:
    features = json.load(f)

for key, value in features.items():
    for sentence in value['sentences']:
        resolutions = sentence['resolutions']
        if 0 < len(resolutions) < 6:  # tables create a lot of noise
            print(sentence['resolutions'])