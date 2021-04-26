import json
import regex

param_dict = {
    "aura_mls": {
        "input_file_name": 'free_text/aura_mls_references'
    },
    "aura_omi": {
        "input_file_name": 'free_text/aura_omi_references'
    },
    "giovanni": {
        "input_file_name": 'free_text/giovanni_references'
    },
    "forward_gesdisc" :{
        "input_file_name": 'free_text/forward_ges_references_and_text'
    }
}

selection = param_dict['forward_gesdisc']
input_file_name = selection['input_file_name']

with open(input_file_name + '.json') as f:
    data = json.load(f)

doi_pattern = r'10\.\d{4,9}\/[-._;()\/:a-zA-Z0-9]+'

split_pattern = r'(?:\.\n)(?=(\d{1,2}\.? )?(?:\w+(\-\w+)?,? \w))'
split_pattern = rf'(?:((\.)|({doi_pattern}))\n)(?=(\d{1,2}\.? )?(?:\w+(\-\w+)?,? \w))'
split_pattern = rf'(\.|{doi_pattern})\n(?=(\d{1,2}\.? )?(\w+(\-\w+)?,? \w))'

doi_pattern = '10\.\d{4,9}\/[-._;()\/:a-zA-Z0-9]+'
doi_pattern = '1\n?0\n?\.\n?\d{4,9}(?:\n\d{4,9})?\/[-._;()\/:a-zA-Z0-9\n]+'  # include \n to account for cross line dois
look_behind_doi = f'(?<=\.|{doi_pattern})\n'
look_behind_doi = f'(?<=\.|{doi_pattern})\n(?=(?:\d{1,2}\.? )?(?:\w+(?:\-\w+)?[,:]? \w))'  # good for aura_omi
look_behind_doi = f'(?<=\.|{doi_pattern})\n(?=(?:\d{1,2}\.? )?(?:\w+(?:\-\w+)?[,:]? \w))'  # good for aura_omi
look_behind_doi = rf'(?<=\.|{doi_pattern})\n' + r'(?=(?:\d{1,2}\.? )?(?:[a-zA-Z]+(?:\-[a-zA-Z])?[,:]? [a-zA-Z]))'  # { inside of f'' messing up regex
look_behind_doi = rf'(?<=\.|{doi_pattern})\n' + r'(?=(?:\d{1,2}[a-zA-Z]?\.? )?(?:[a-zA-Z]+(?:\-[a-zA-Z])?[,:]? [a-zA-Z]))'  # account for no spaces between number and author name
look_behind_doi = rf'(?<=\.|{doi_pattern})\n' + r'(?=(?:(?:\d{1,2})|(?:\[\d{1,2}\])[a-zA-Z]?\.? )?(?:[a-zA-Z]+(?:\-[a-zA-Z])?[,:]? [a-zA-Z]))'  # bracketed numbers

'''
ends citation with '.' or a doi. Next line starts with one of
    LastName, First inital and 
    First Last
    ignore numbered references ie: 7.

todo: [pubmed omi 9ghy]
'''

keyword = r'(?:disc\.gsfc\.nasa\.gov)|(?:GES[ -]?DISC)'
for key, value in data.items():
    if 'free_text' in value and len(value['free_text']) >= 1:

        # Print values to console
        # print("------")
        # print(key)
        # print(value['free_text'][0])
        # # print("DOI: ", re.findall(rf'{doi_pattern}', value['free_text'][0]))
        # print()
        # splits = regex.split(look_behind_doi, value['free_text'][0])
        #
        # for s in splits:
        #     if s:
        #         print(s, '\n')
        # print("------")

        # assing new values
        print(key)
        new_free_text_citations = []
        splits = regex.split(look_behind_doi, value['free_text'][0])
        for s in splits:
            if s:
                keyword_occurrences = regex.findall(rf'{keyword}', s)
                print(s, '\n')
                if len(keyword_occurrences) >= 1:
                    new_free_text_citations.append(s.replace("\n", " "))


        data[key]['free_text'] = new_free_text_citations

with open(input_file_name + "_clean" + ".json", 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)
