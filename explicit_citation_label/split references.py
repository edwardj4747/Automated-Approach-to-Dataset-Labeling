import json
import regex

with open('aura_omi_doi_dataset_map_gd_link_false.json') as f:
    data = json.load(f)

doi_pattern = r'10\.\d{4,9}\/[-._;()\/:a-zA-Z0-9]+'

split_pattern = r'(?:\.\n)(?=(\d{1,2}\.? )?(?:\w+(\-\w+)?,? \w))'
split_pattern = rf'(?:((\.)|({doi_pattern}))\n)(?=(\d{1,2}\.? )?(?:\w+(\-\w+)?,? \w))'
split_pattern = rf'(\.|{doi_pattern})\n(?=(\d{1,2}\.? )?(\w+(\-\w+)?,? \w))'

doi_pattern = '10\.\d{4,9}\/[-._;()\/:a-zA-Z0-9]+'
look_behind_doi = f'(?<=\.|{doi_pattern})\n'
look_behind_doi = f'(?<=\.|{doi_pattern})\n(?=(?:\d{1,2}\.? )?(?:\w+(?:\-\w+)?,? \w))'

'''
ends citation with '.' Next line starts with one of
    LastName, First inital and 
    First Last
    DOI ending without '.'
ignore starting numbers ie: 7.

Still to do: split line dois

is not perfect. Things like 8. World Meteorological Organization (WMO). S
'''


for key, value in data.items():
    if len(value['free_text']) >= 1:
        print("------")
        print(key)
        print(value['free_text'][0])
        # print("DOI: ", re.findall(rf'{doi_pattern}', value['free_text'][0]))
        print()
        splits = regex.split(look_behind_doi, value['free_text'][0])

        for s in splits:
            print(s, '\n')

        print("------")
