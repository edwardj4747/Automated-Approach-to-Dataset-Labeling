import json

'''
    aliases.json is good but it has way more than what GES DISC serves
    create file keywords.json which has only the mission, instruments and variables that GES DISC serves
    keywords = {
        "missions": {
            "short_to_long": {...},
            "long_to_short": {...}
        }, ...
    }
'''

with open('../data/json/GES_instruments_short_to_long.json') as f:
    instruments_short_to_long = json.load(f)

with open('../data/json/GES_missions_short_to_long.json') as f:
    missions_short_to_long = json.load(f)


missions_long_to_short = {v: k for k,v in missions_short_to_long.items()}
instruments_long_to_short = {v:k for k, v in instruments_short_to_long.items()}

with open('../data/json/aliases.json') as f:
    aliases = json.load(f)

variable_short_to_long = aliases['var_main']
variable_long_to_short = aliases['var_aliases']


keywords = {
    "missions": {
        "short_to_long": missions_short_to_long,
        "long_to_short": missions_long_to_short
    },
    "instruments": {
        "short_to_long": instruments_short_to_long,
        "long_to_short": instruments_long_to_short
    },
    "variables": {
        "short_to_long": variable_short_to_long,
        "long_to_short": variable_long_to_short
    }
}

with open('../data/json/keywords.json', 'w', encoding='utf-8') as f:
    json.dump(keywords, f, indent=4)