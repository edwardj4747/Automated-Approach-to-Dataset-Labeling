import json
from collections import Counter

'''
    Create a list of the keys of the papers that do not have sentences containing all of mission, instrument, and 
    science keyword
'''

with open('../ml_data/raw_data_aura_mls_ONLY_noNO.json') as f:
    raw_data = json.load(f)

print(len(raw_data))
papers_with_no_sentences_list = []
missed_len_0_datasets = {}

unique_datasets = set()
papers_with_no_sentences = 0
papers_with_no_sentences_datasets_missed = 0
for key, value in raw_data.items():
    ground_truths = value['ground_truths']
    if len(value['data']) == 0:
        papers_with_no_sentences_list.append(key)
        print(key)
        papers_with_no_sentences += 1
        papers_with_no_sentences_datasets_missed += len(ground_truths)
        for gt in ground_truths:
            missed_len_0_datasets[gt] = missed_len_0_datasets.get(gt, 0 ) + 1

print("papers with no sentences ", papers_with_no_sentences)
print("datasets missed bc of no sentences ", papers_with_no_sentences_datasets_missed)

counter = Counter(missed_len_0_datasets)
print(counter.most_common())

# with open('../ml_data/papers_with_no_miv_sentences.json', 'w', encoding='utf-8') as f:
#     json.dump(papers_with_no_sentences_list, f)




