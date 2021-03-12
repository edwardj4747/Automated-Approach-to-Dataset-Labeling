from ML.keyword_sentences import run_keyword_sentences
import json
import re

'''
    An attempt to find 'Gold' sentences. A gold sentences is something which is something that very likely references
    a dataset
'''


def get_sentences():
    keyword_sentences_dict, original_sentences_dict = run_keyword_sentences()
    print(keyword_sentences_dict)
    with open('data/359_keyword_sentences_max_sent_3.json', 'w', encoding='utf-8') as f:
        json.dump(keyword_sentences_dict, f, indent=4)

    with open('data/359_original_sentences_max_sent_3.json', 'w', encoding='utf-8') as f:
        json.dump(original_sentences_dict, f, indent=4)


def load_sentences():
    with open('data/359_keyword_sentences.json', encoding='utf-8') as f:
        keyword_sentences_dict = json.load(f)

    with open('data/359_original_sentences.json', encoding='utf-8') as f:
        original_sentences_dict = json.load(f)

    return keyword_sentences_dict, original_sentences_dict

get_sentences()
exit()
keyword_sentences_dict, original_sentences_dict = load_sentences()

version_sentences_keywords_and_original = {}
for key, value in keyword_sentences_dict.items():
    keyword_sentences = value['keyword_sentences']
    original_sentence = original_sentences_dict[key]['original_sentences']

    for i, ks in enumerate(keyword_sentences):
        paper_ks_with_v, papers_os_with_v = [], []  # paper keyword with sentence and paper original sentence w/ version
        if len(re.findall(r'v[0-9]', ks)) > 0:  # keyword sentences contains a version
            paper_ks_with_v.append(ks)
            papers_os_with_v.append(' '.join(original_sentence[i]))
        if len(paper_ks_with_v) > 0:  # There were some sentences with a version
            version_sentences_keywords_and_original[key] = {
                "keyword_sentences": paper_ks_with_v,
                "original_sentences": papers_os_with_v
            }

with open("data/gold_sentences_draft.json", 'w', encoding='utf-8') as f:
    json.dump(version_sentences_keywords_and_original, f, indent=4)

