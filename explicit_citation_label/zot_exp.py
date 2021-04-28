import os
import random
from pyzotero import zotero


def output_note(zot, note_text, tag_names, key):
    note_item = zot.item_template('note')
    note_item["note"] = '<p>' +  '</p><p>'.join(note_text) + '</p>'

    for tag_name in tag_names:
        note_item["tags"].append({"tag": tag_name})

    print("note_item ", note_item)
    return zot.create_items([note_item], key)


if __name__ == "__main__":

    library_id = '7185722'
    library_type = 'user'
    api_key = 'tJBEs3kpyfxotFPcqi7vO4tA'
    edward_small_collection = 'HVBLJZ68'

    # Connect to the Zotero API
    zot = zotero.Zotero(library_id, library_type, api_key)

    # Get data from Zotero if needed
    # print("Getting Zotero data...")  # Gets everything including notes
    # zot_items = zot.everything(zot.top(edward_small_collection))
    # zot_items = zot.everything(zot.collection_items_top(edward_small_collection))
    #
    # print("Data loaded.")
    # print(zot_items)

    key = '36NAG66Q'
    output_note(zot, ['d1', 'd2', 'd3'], ['auto_label'], key)




