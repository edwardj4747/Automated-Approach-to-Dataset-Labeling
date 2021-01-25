import json

with open('../data/json/edward_aura_mls_zot.json') as f:
    items = json.load(f)

item_dict = {}
for item in items:
    item_dict[item['key']] = item

print(item_dict)
with open('../data/json/edward_aura_mls_zot_keyed.json', 'w') as f:
    json.dump(item_dict, f, indent=4)