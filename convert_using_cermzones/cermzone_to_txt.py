import xml.etree.ElementTree as ET
import re
import glob

# {'GEN_REFERENCES', 'MET_CORRESPONDENCE', 'MET_ABSTRACT', 'GEN_OTHER' (like pg number), 'MET_DATES', 'MET_AFFILIATION', 'BODY_HEADING', 'BODY_CONTENT', 'MET_BIB_INFO', 'MET_TITLE', 'MET_AUTHOR'}
useful_zones = {'MET_ABSTRACT', 'BODY_HEADING', 'BODY_CONTENT'}

cermzones_directory = 'successful_cermfiles/'
output_directory = 'text/'
potential_missed_sections = ['acknowledgments', 'figure', 'table']

for file in glob.glob(cermzones_directory + "*.cermzones"):
    print(file)
    file_name = file.split("\\")[-1]

    tree = ET.parse(file)
    root = tree.getroot()

    text = ""
    # Bullet symbol has ordinal 8226
    for child in root.findall('./zone'):
        # print(child.tag, child.attrib)
        if child.attrib['label'] == 'BODY_HEADING':
            text += "\n\n" + child.text
        elif child.attrib['label'] == 'BODY_CONTENT':
            # remove citations and new lines
            new_text = re.sub('\n', ' ', child.text)
            new_text = re.sub(r'\[.*?\]', '', new_text)  # [] for citations

            first_word = new_text.split(" ", maxsplit=1)[0]
            if first_word.lower() in potential_missed_sections:
                text += "\n\n" + first_word
                text += "\n" + new_text[len(first_word):]
            else:
                text += "\n" + new_text

    with open(output_directory + file_name + ".txt", 'w', encoding='utf-8') as f:
        f.write(text)
