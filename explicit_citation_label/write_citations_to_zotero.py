"""
    tag papers with 'reveiwer:autolabel'
    Add tags for the dois (ie 'doi:xxxxxxx') for papers with datasets
    Add in a note with tag 'category:unknown' containing short names of datasets found. DOIs are mapped to ShortNames
"""

import json
from pyzotero import zotero
import csv

def output_note(zot, note_text, tag_names, key, modify_text=True):
    note_item = zot.item_template('note')
    # note_item["note"] = '<p>' +  '</p><p>'.join(note_text) + '</p>'
    if modify_text:
        note_item["note"] = '<br />'.join(note_text)
    else:
        note_item['note'] = note_text

    for tag_name in tag_names:
        note_item["tags"].append({"tag": tag_name})

    print("note_item ", note_item)
    return zot.create_items([note_item], key)

def note_already_present(zot, zotero_key, tag_label):
    # check for previous duplications
    children = zot.children(zotero_key, itemType='note')
    note_already_added = False
    for child in children:
        child_tags = child['data']['tags']
        for ct in child_tags:
            if tag_label in ct['tag']:
                note_already_added = True

    return note_already_added


if __name__ == "__main__":

    file_name = 'zotero_tag_results/forward_gesdisc_doi_clean.csv'
    json_file = 'free_text/forward_ges_references_and_text_clean_doi_clean.json'

    library_id = '7185722'
    library_id = '2395775'  # group
    library_type = 'group'
    api_key = 'tJBEs3kpyfxotFPcqi7vO4tA'
    api_key = 'IfniSMyDpw2y2TlSnHBWr852'
    edward_small_collection = 'HVBLJZ68'
    group_forward_gesdisc = '8L3ZJKKV'

    # Declare all the tags that are going to be used
    reviewer_auto_label = 'reviewer:autolabel'
    reviewer_auto_label_free_text = 'reviewer:autolabel_free_text'
    category_unknown = 'category:unknown'

    # Connect to the Zotero API
    zot = zotero.Zotero(library_id, library_type, api_key)

    zotero_key_index = 0
    pdf_key_index = 1
    title_index = 2
    mission_ins_couples_index = 3
    single_ins_index = 4
    models_index = 5
    dois_index = 6
    datasets_index = 7
    dois_and_datasets_index = 8

    pdf_key_to_zotero_key = {}

    count = 0
    notes_added = 0

    with open(file_name, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # skip the heading row
        for row in reader:
            count += 1

            # noinspection PyRedeclaration
            print()
            print(row)
            zotero_key, pdf_key, title, mission_ins_couples, single_ins, models, dois, datasets, dois_and_datasets = '', '', '', '', '', '', '', '', ''
            try:
                zotero_key = row[zotero_key_index]
                pdf_key = row[pdf_key_index]
                pdf_key_to_zotero_key[pdf_key] = zotero_key
                title = row[title_index]
                mission_ins_couples = row[mission_ins_couples_index]
                single_ins = row[single_ins_index]
                models = row[models_index]
                dois = row[dois_index]
                datasets = row[datasets_index]
                dois_and_datasets = row[dois_and_datasets_index]


                # Get the current item
                current_item = zot.item(zotero_key)

                # check for previous duplications
                # children = zot.children(zotero_key, itemType='note')
                # note_already_added = False
                # for child in children:
                #     child_tags = child['data']['tags']
                #     for ct in child_tags:
                #         if reviewer_auto_label in ct['tag']:
                #             note_already_added = True

                note_already_added = note_already_present(zot, zotero_key, category_unknown)

                # Add in the short names if there is not already a note
                if not note_already_added:
                    short_names = dois_and_datasets.strip().split(';')
                    print(zotero_key, short_names)
                    if len(short_names) == 1 and short_names[0] == '':
                        print("No content to add")
                    else:
                        notes_added += 1
                        output_note(zot, short_names, [category_unknown], zotero_key)
                else:
                    print("Already a note with ", category_unknown)



                # add in new dois
                doi_tags = ["doi:" + d.strip() for d in dois.split(';') if d.strip() != '']
                print("doi tags", doi_tags)
                for doi_tag in doi_tags:
                    # re-get the item in case it has changed
                    current_item = zot.item(zotero_key)
                    zot.add_tags(current_item, doi_tag)

                # add a tag to the top-level item of 'reviewer:autolabel'
                current_item = zot.item(zotero_key)
                zot.add_tags(current_item, reviewer_auto_label)
            except IndexError:
                pass

    print("Notes added:", notes_added)

    # For the papers with free text, add that into
    with open(json_file, encoding='utf-8') as f:
        explicit_references = json.load(f)

    for pdf_key, value in explicit_references.items():
        print(pdf_key)
        free_text = value['free_text']
        if len(free_text) > 0:
            zotero_key = pdf_key_to_zotero_key[pdf_key]
            note_already_added = note_already_present(zot, zotero_key, reviewer_auto_label_free_text)
            if not note_already_added:
                free_text_string = ''
                for item in free_text:
                    free_text_string += item + "\n"
                output_note(zot, free_text_string, [reviewer_auto_label_free_text], zotero_key, modify_text=False)
            else:
                print("Note already added for free_text")
