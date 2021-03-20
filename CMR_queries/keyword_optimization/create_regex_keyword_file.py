import json
import re
import ast

with open('../../data/json/keywords.json', encoding='utf-8') as f:
    keywords = json.load(f)

str_keywords = str(keywords)
str_keywords = re.sub(r'-', '(?: |\\-)?', str_keywords)  # '-' to '-' or space
str_keywords = re.sub(r'/', '(?: |/)?', str_keywords)  # '/' to '/' or space


print(str_keywords)
print(type(ast.literal_eval(str_keywords)))

with open('keywords_regex.json', 'w', encoding='utf-8') as f:
    json.dump(ast.literal_eval(str_keywords), f, indent=4)