import json
from collections import defaultdict

'''
    For all extracted sentences in aura/mls corpus, create dictionary mapping from tag to all sentences with that tag
        ie:  { (aura/mls, o3): [sentence, sentence, .....], ... }
'''


with open('../ml_data/raw_data_aura_mls_ONLY_noNO.json') as f:
    raw_data = json.load(f)

tag_sentences = defaultdict(set)

for key, value in raw_data.items():
    for k, v in value['data'].items():
        for sentence in v['sentences']:
            tag_sentences[k].add(sentence)

tag_sentences_list = {}
for key, value in tag_sentences.items():
    tag_sentences_list[key] = list(value)

with open('../ml_data/sentences_by_tags.json', 'w', encoding='utf-8') as f:
    json.dump(tag_sentences_list, f, indent=4)