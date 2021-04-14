import xml.etree.ElementTree as ET
import re
import glob
import json

'''
1. Split citations. end in '.\n' and lookahead for Last, F.

NER model to pick up people/organizations? Probably overkill

    Look for http://disc.sci.gsfc.nasa Or Goddard Earth Sciences in addition to explicit mentions
'''


def search_occurrences(keyword):
    occurrences = re.findall(r'.{,130}\n?.{,130}' + keyword + '.{,70}\n?.{,70}', text)
    if occurrences:
        print(occurrences, file_name)


if __name__ == '__main__':
    # User parameters
    output_file_name = "giovanni_exp_2.json"
    cermzones_directory = '../convert_using_cermzones/giovanni/successful_cermfiles/'
    doi_to_dataset_mapping_location = '../data/json/doi_to_dataset_name.json'
    dataset_long_to_short_mapping = '../data/json/dataset_long_to_short.json'


    reference_label = "GEN_REFERENCES"
    keyword = r'disc\.gsfc\.nasa\.gov'
    papers_with_explicit_mentions = 0
    results = {}

    with open(doi_to_dataset_mapping_location) as f:
        doi_to_dataset = json.load(f)

    dataset_to_doi = {v: k for k, v in doi_to_dataset.items()}

    with open(dataset_long_to_short_mapping) as f:
        dataset_long_to_short = json.load(f)

    for file in glob.glob(cermzones_directory + "*.cermzones"):
        dois_founds = []
        datasets_found = []
        # print()
        # print()
        # print(file)
        file_name = file.split("\\")[-1]

        tree = ET.parse(file)
        root = tree.getroot()

        for child in root.findall('./zone'):
            if child.attrib['label'] == reference_label:
                text = child.text
                print(text)
                print("--------")
                # attempt to split between references
                splits = re.split(r'\.\n(?=(\d+\.? )?\w+, \w)', text)  # ends citation with '.' Next line starts with LastName, First inital and ignore starting numbers ie: 7.
                # is not perfect. Things like 8. World Meteorological Organization (WMO). S
                for s in splits:
                    print(s, '\n')
                print("--------")


                # search_occurrences()

                for doi in doi_to_dataset:
                    matches = re.findall(rf'{doi}', text)
                    # print(matches)
                    if len(matches) >= 1:
                        dois_founds.append(doi)
                        dataset_found = doi_to_dataset[doi]
                        datasets_found.append(dataset_found)

                for long_name, short_name in dataset_long_to_short.items():
                    long_matches = re.findall(rf'{long_name}', text)
                    short_matches = re.findall(rf'{short_name}', text)
                    if len(long_matches) >= 1:
                        dataset_found = [dataset_long_to_short[lm] for lm in long_matches]
                        datasets_found += dataset_found
                    elif len(short_matches) >= 1:
                        datasets_found += short_matches


        if len(dois_founds) >= 1 or len(datasets_found) >= 1:
            print(file_name, dois_founds, datasets_found)
            papers_with_explicit_mentions += 1
            modified_file_name = file_name.split('.')[0]
            results[modified_file_name] = dois_founds

    print("papers with explicit dataset citations", papers_with_explicit_mentions)
    with open(output_file_name, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)




