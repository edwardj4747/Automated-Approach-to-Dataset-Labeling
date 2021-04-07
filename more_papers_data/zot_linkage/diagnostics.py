import json

with open('mls_pubs_with_attchs.json', encoding='utf-8') as f:
    mls_pubs_with_attchs = json.load(f)

with open('zot_atts_mls.json', encoding='utf-8') as f:
    zot_atts_mls = json.load(f)

with open('zot_notes_mls.json', encoding='utf-8') as f:
    zot_notes_mls = json.load(f)

with open('zot_pubs_mls.json', encoding='utf-8') as f:
    zot_pubs_mls = json.load(f)

print(len(mls_pubs_with_attchs))
print(len(zot_atts_mls))
print(len(zot_notes_mls))
print(len(zot_pubs_mls))
