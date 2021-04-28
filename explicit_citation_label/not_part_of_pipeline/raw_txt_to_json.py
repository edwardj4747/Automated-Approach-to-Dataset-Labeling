# This is NOT actually used in the process. I had the printed text output from one of the runs, but for some reason
# the file did not get saved. This just took the printed text output and put it into the format I wanted, so I didn't
# have to run the whole process again.


import json
import re


with open('C:\\Users\\edwar\\Documents\\giovanni include free text.txt', encoding='utf-8', errors='ignore') as f:
    text = f.read()

with open('giovanni_explicit_doi_dataset_map.json', encoding='utf-8') as f:
    base_data = json.load(f)

# print(text)
lines = text.split("\n")
print(len(lines))

index = 0
pdf_key = ''
citation_lines = []
cl_formatted = []
while index < len(lines):
    if not lines[index].startswith("../convert_using_cermzones") and "{" not in lines[index]:
        line_value = re.sub(r'[A-Z\d]{8}\.cermzones ', '', lines[index])
        citation_lines.append(line_value.replace(' -----', ''))
    else:
        if len(citation_lines) >= 1:
            # print(pdf_key, citation_lines)
            citation_value = ['\n'.join(citation_lines)]
            print(pdf_key, citation_value)
            # add to the base data
            if pdf_key in base_data:
                base_data[pdf_key]["free_text"] = citation_value
            else:
                base_data[pdf_key] = {
                    "explicit_dois": [],
                    "explicit_datasets": [],
                    "datasets_and_doi": [],
                    "free_text": citation_value
                }
            pass
        citation_lines = []
        pdf_key = lines[index].split("\\")[-1].replace(".cermzones", "")
    index += 1

with open('giovanni_references.json', 'w', encoding='utf-8') as f:
    json.dump(base_data, f, indent=4)