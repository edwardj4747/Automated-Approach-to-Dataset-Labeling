'''
    add models: {
        "short_to_long": {},
        "long_to_short": {}
    }

    to keywords.

    If a keyword is in both models and missions, remove it from missions and only keep it in models
'''

import json

with open('../data/json/keywords.json', encoding='utf-8') as f:
    keywords = json.load(f)

with open('../data/json/models_and_analyses_dict.json', encoding='utf-8') as f:
    models_dict = json.load(f)


# keywords['models'] = {
#     "short_to_long": models_dict,
#     "long_to_short": {v: k for k, v in models_dict.items() if v != ''}
# }

missions_short_to_long = keywords['missions']['short_to_long']
missions_long_to_short = keywords['missions']['long_to_short']


remove_list = []
for short_mission in missions_short_to_long:
    if short_mission in keywords['models']['short_to_long']:
        remove_list.append(short_mission)


for item in remove_list:
    missions_long_to_short.pop(missions_short_to_long[item])
    long_mission = missions_short_to_long.pop(item)
    print("removed ", item, long_mission)




with open('../data/json/keywords.json', 'w', encoding='utf-8') as f:
    keywords = json.dump(keywords, f, indent=4)