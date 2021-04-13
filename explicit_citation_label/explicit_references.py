import xml.etree.ElementTree as ET
import re
import glob
import json


# {'GEN_REFERENCES', 'MET_CORRESPONDENCE', 'MET_ABSTRACT', 'GEN_OTHER' (like pg number), 'MET_DATES', 'MET_AFFILIATION', 'BODY_HEADING', 'BODY_CONTENT', 'MET_BIB_INFO', 'MET_TITLE', 'MET_AUTHOR'}
reference_label = "GEN_REFERENCES"
cermzones_directory = '../convert_using_cermzones/giovanni/successful_cermfiles/'

results = {}

'''
    Look for , http://disc.sci.gsfc.nasa.
gov/Aura/data-holdings/OMI/omso2_v003.shtml. ?
Or Foddard Earth Sciences
'''

with open('../data/json/doi_to_dataset_name.json') as f:
    doi_to_dataset = json.load(f)

dataset_to_doi = {v: k for k, v in doi_to_dataset.items()}

with open('../data/json/dataset_long_to_short.json') as f:
    dataset_long_to_short = json.load(f)

keyword = r'disc\.gsfc\.nasa\.gov'

papers_count = 0
for file in glob.glob(cermzones_directory + "*.cermzones"):
    dois_founds = []
    # print(file)
    file_name = file.split("\\")[-1]

    tree = ET.parse(file)
    root = tree.getroot()

    text = ""
    # Bullet symbol has ordinal 8226
    for child in root.findall('./zone'):
        # print(child.tag, child.attrib)
        if child.attrib['label'] == reference_label:
            # print(child.text)
            text = child.text

            occurrences = re.findall(r'.{,70}' + keyword + '.{,70}', text)
            if occurrences:
                print(occurrences, file_name)


            # for doi in doi_to_dataset:
            #     matches = re.findall(rf'{doi}', text)
            #     # print(matches)
            #     if len(matches) >= 1:
            #         dois_founds.append(doi)
            #
            # for long_name, short_name in dataset_long_to_short.items():
            #     matches = re.findall(rf'{long_name}', text) + re.findall(rf'{short_name}', text)
            #     if len(matches) >= 1:
            #         dois_founds.append(short_name)

    if len(dois_founds) >= 1:
        print(file_name, dois_founds)
        papers_count += 1
        modified_file_name = file_name.split('.')[0]
        results[modified_file_name] = dois_founds

# print("papers count", papers_count)
# with open('Giovanni_explicit.json', 'w', encoding='utf-8') as f:
#     json.dump(results, f, indent=4)




