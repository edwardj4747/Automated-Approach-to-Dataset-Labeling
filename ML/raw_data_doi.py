import json

'''
    convert a mapping of paper_key:value to paper_doi:value
'''

with open('ml_data/raw_data_all_papers_broad_aura_mls_ONLY.json') as f:
    raw_data = json.load(f)

with open('ml_data/children_to_top.json') as f:
    children_to_top = json.load(f)

with open('ml_data/top_to_doi.json') as f:
    top_to_doi = json.load(f)

doi_data = {}
for key, value in raw_data.items():
    paper_doi = top_to_doi[children_to_top[key]]
    # print(key, paper_doi)
    doi_data[paper_doi] = value

with open('ml_data/raw_data_all_papers_broad_aura_mls_ONLY_doi.json', 'w', encoding='utf-8') as f:
    json.dump(doi_data, f, indent=4)
