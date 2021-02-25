import re
import xml.etree.ElementTree as ET
import glob
from tqdm import tqdm

'''
    Convert cermxml files to txt files.
    Advantages of cermine
        can basically remove or filter out a lot of things we don't want like footers, references, and title page
        information very easily
    
    A few things to note
        the spelling of words from cermine is not always perfect
        sometimes figure are extracted as text which forms nonsense sentences
'''


def remove_citations(txt):
    text = re.sub(r' *<xref ref-type.*?>.*?\[[0-9]{4}</xref>\n.*?\]', '', txt)  # in text citations
    text = re.sub(r'\n.*<xref ref-type.*\n?.*</xref>\n', '', text)  # step 1 remove all the <xref type ... </xref>
    text = re.sub(r' ?\[(.*?;){1,4}.*?\]', '', text)  # step 2 remove remaining tags of multiple occurrence form [  ;  ]
    text = re.sub(r' ?\[\s*\]', '', text)  # step 3 remove all the remaining tags of single occurrence form [        ]

    text = re.sub(r'(\s{4,};){1,4}\s{4,}\]', '', text)  # step 4 catch a few exceptions from step 2 [  ;  ]
    text = re.sub(r'\s{4,}\]', '', text)  # step 5 catch a few exceptions from step 3       ]

    return text


def recursive_extraction_of_title_and_paragraphs(item):
    # base case
    if all(children.tag == 'p' or children.tag == 'title' for children in item):
        # print("all children are p or title")
        return [children for children in item]
    else:
        for child in item:
            recursive_extraction_of_title_and_paragraphs(child)


def find_potential_page_numbers(text):
    num_with_commas = re.findall(r'[0-9]+,[0-9]{3}', text)
    min_pages = 5


def add_formatted_item_to_text(item, is_nested_section=False):
    if item.tag == 'title':
        # Remove numbers so that '1. Introduction' would just be 'Introduction'
        item_text = re.sub(r'[0-9]+\.? ?', '', item.text)
        return "\n" + item_text + "\n" if not is_nested_section else item_text + "\n"

    elif item.tag == 'p':
        # remove \n characters and strip out the white space
        item_text = re.sub(r'\n', ' ', item.text).strip()
        return item_text + "\n"


if __name__ == '__main__':
    location_of_cermxml = 'data/cermxml_full/'
    output_location = 'data/cermine_results/text_full/'

    for input_file in tqdm(glob.glob(location_of_cermxml + '*.cermxml')):
        # input_file = 'cermine_pdfs/Dolinar et al. - 2016 - A clear-sky radiation closure study using a one-di.cermxml'
        with open(input_file, encoding='utf-8') as f:
            clean_text = ""
            text = f.read()
            text = remove_citations(text)

            root = ET.fromstringlist(text)
            try:
                abstract = root.findall('./front/article-meta/abstract/p')[0].text
                if abstract is not None:
                    clean_text += "Abstract\n" + abstract + "\n"
            except:
                pass

            for item in root.findall("./body/sec/*"):  # * selects all the children
                if item.tag == 'p' or item.tag == 'title':
                    clean_text += add_formatted_item_to_text(item)
                elif item.tag == 'sec':
                    titles_and_paragraphs = recursive_extraction_of_title_and_paragraphs(item)
                    if titles_and_paragraphs is None:
                        continue
                    for tp in titles_and_paragraphs:
                        clean_text += add_formatted_item_to_text(tp, is_nested_section=True)

            output_file = input_file.replace('.cermxml', '.txt').split('\\')[-1]

            with open(output_location + output_file, 'w', encoding='utf-8') as file:
                file.write(clean_text)
