import json
import re
import ast

# Want to replace ONLY long names with regex patterns

# make punctuation optional
# 1st -> first in both directions


def regex_substitutions(initial_value):
    final_value = re.sub(r'-', '(?: |\\-)?', initial_value)  # '-' to '-' or space
    final_value = re.sub(r'/', '(?: |/)?', final_value)  # '/' to '/' or space
    return final_value


with open('../../data/json/keywords.json', encoding='utf-8') as f:
    keywords = json.load(f)

str_keywords = str(keywords)
str_keywords = re.sub(r'-', '(?: |\\-)?', str_keywords)  # '-' to '-' or space
str_keywords = re.sub(r'/', '(?: |/)?', str_keywords)  # '/' to '/' or space

long_missions = keywords['missions']['long_to_short']
long_instruments = keywords['instruments']['long_to_short']
long_models = keywords['models']['long_to_short']
new_long_missions, new_long_instruments, new_long_models = {}, {}, {}

for key, value in long_missions.items():
    new_key = regex_substitutions(key)
    new_long_missions[new_key] = value

for key, value in long_instruments.items():
    new_key = regex_substitutions(key)
    new_long_instruments[new_key] = value

for key, value in long_models.items():
    new_key = regex_substitutions(key)
    new_long_models[new_key] = value

keywords['missions']['long_to_short'] = new_long_missions
keywords['instruments']['long_to_short'] = new_long_instruments
keywords['models']['long_to_short'] = new_long_models

with open('keywords_regex_revised.json', 'w', encoding='utf-8') as f:
    json.dump(keywords, f, indent=4)
exit()


print(str_keywords)
print(type(ast.literal_eval(str_keywords)))

with open('keywords_regex.json', 'w', encoding='utf-8') as f:
    json.dump(ast.literal_eval(str_keywords), f, indent=4)