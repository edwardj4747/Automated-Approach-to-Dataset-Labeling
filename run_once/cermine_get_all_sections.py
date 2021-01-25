# java -cp cermine-impl-1.13-jar-with-dependencies.jar pl.edu.icm.cermine.ContentExtractor -path ../pdfs -outputs jats

import os
import glob
import xml.etree.ElementTree as ET
import re
import pprint


def cermine_files_to_directory():
    # copy all .cermxml to their own directory
    output_directory = "../data/cermxml_full/"
    for file in glob.glob("../pdfs_full/*.cermxml"):
        file_name = file.split("\\")[-1]
        os.replace(file, output_directory + file_name)

cermine_files_to_directory()

import sys
sys.exit()


sections = {}

# Go through all of the sections of the cermine files and keep a list of what they are
file = '../a_experiments/cermine_pdfs/Dolinar et al. - 2016 - A clear-sky radiation closure study using a one-di.cermxml'

for file in glob.glob('../a_experiments/cermine_pdfs/*.cermxml'):
    tree = ET.parse(file)
    root = tree.getroot()

    for item in root.findall('.//title'):
        name_of_section = item.text
        name_of_section = re.sub(r'[0-9]+.? ?', '', name_of_section).strip()  # remove numbers like '1. Introduction' and whitespace
        sections[name_of_section] = sections.get(name_of_section, 0) + 1

    # also make a pass through looking for paragraph labels that may not have been caugt

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(sorted(sections.items(), key=lambda x: x[1], reverse=True))