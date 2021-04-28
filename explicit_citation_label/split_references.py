'''
    explicit_references.py only very coarsely splits the references before looking for free text mentions of 'GES DISC'
    or the GES DISC website. This means lots of citations that are near GES DISC citations will be included in the free
    text. The goal of this file is to split blob of free text references even more finely, so that only the citations
    that we care about are actually included. This is not perfect but represents a massive improvement.

    This will output a new file with the same name as the input with a '_clean' suffix to signify that the text has been
    further processed.
'''


import json
import regex  # NOTE: the import is regex and not re. regex allows backwards look behinds of variable length while re does not

# a dictionary with the files created from running explicit_references.py. Just a convenience thing to make switching easy
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

# choose which input file we want to use from the dictionary we just defined
selection = param_dict['forward_gesdisc']
input_file_name = selection['input_file_name']

with open(input_file_name + '.json') as f:
    data = json.load(f)

# # previous split pattern attempts. Not currently used
# split_pattern = r'(?:\.\n)(?=(\d{1,2}\.? )?(?:\w+(\-\w+)?,? \w))'
# split_pattern = rf'(?:((\.)|({doi_pattern}))\n)(?=(\d{1,2}\.? )?(?:\w+(\-\w+)?,? \w))'
# split_pattern = rf'(\.|{doi_pattern})\n(?=(\d{1,2}\.? )?(\w+(\-\w+)?,? \w))'

# I've left the evolution of my regex patterns here in case seeing the process and understanding what each statement does
# is useful. Like I said, these are not perfect, but they do filter the references a significant amount for most papers

doi_pattern = '10\.\d{4,9}\/[-._;()\/:a-zA-Z0-9]+'  # basic regex pattern to find dois
doi_pattern = '1\n?0\n?\.\n?\d{4,9}(?:\n\d{4,9})?\/[-._;()\/:a-zA-Z0-9\n]+'  # include \n to account for cross line dois

look_behind_doi = f'(?<=\.|{doi_pattern})\n'  # lookbehind. see if the last line ended with a '.' or a doi. Lets denote this (1)

look_behind_doi = f'(?<=\.|{doi_pattern})\n(?=(?:\d{1,2}\.? )?(?:\w+(?:\-\w+)?[,:]? \w))'
# (?=(?:\d{1,2}\.? )? current line MAY start with a number followed by an optional period ie '15.'
# (?:\w+(?:\-\w+)?[,:]? \w) Current line has things like 'Name Name' or 'Name, Name' or Name-LastName Name'
# whole expression: (1) && previous two lines

look_behind_doi = rf'(?<=\.|{doi_pattern})\n' + r'(?=(?:\d{1,2}[a-zA-Z]?\.? )?(?:[a-zA-Z]+(?:\-[a-zA-Z])?[,:]? [a-zA-Z]))'
# increase the specificity of the previous statement. instead of \w with matches lowercase letters, uppercase letter,
# AND numbers, just match letters of either case


look_behind_doi = rf'(?<=\.|{doi_pattern})\n' + r'(?=(?:(?:\d{1,2})|(?:\[\d{1,2}\])[a-zA-Z]?\.? )?(?:[a-zA-Z]+(?:\-[a-zA-Z])?[,:]? [a-zA-Z]))'
# allow for the option of bracketed numbers, so '15.' and [15.] are both okay


keyword = r'(?:disc\.gsfc\.nasa\.gov)|(?:GES[ -]?DISC)'  # ges disc website or words 'GES DISC'

# iterate through all the items that were found to have explicit references. If the references found free text in
# filter the text by splitting it into distinct references and keeping only the ones with 'GES DISC' or the website
for key, value in data.items():
    if 'free_text' in value and len(value['free_text']) >= 1:

        # assing new values
        print(key)
        new_free_text_citations = []
        splits = regex.split(look_behind_doi, value['free_text'][0])  # actually split up the big blob of references
        for s in splits:
            if s:
                keyword_occurrences = regex.findall(rf'{keyword}', s)
                print(s, '\n')
                # if the split up references still has the keywords, we care about then add it to the list
                if len(keyword_occurrences) >= 1:
                    new_free_text_citations.append(s.replace("\n", " "))

        # update the original references with the split references we found. This will always be <= to the length of the
        # original free text and hopefully less
        data[key]['free_text'] = new_free_text_citations

# save the new cleaned file
with open(input_file_name + "_clean" + ".json", 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)
