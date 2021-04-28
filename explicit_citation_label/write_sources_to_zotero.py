"""
    Create 'Source' Tags that mimic the sources used on the GES DISC website and input them into Zotero
    based on the mission/instrument pairs that were found.

    ie: in zotero tag an item as 'source:Aura MLS' with exact capitalization
"""

import json
import re
from pyzotero import zotero


# Push the tag into zotero
def tag(current_item, tag_text, zot):
    print("Tag called with", tag_text)
    zot.add_tags(current_item, tag_text)


if __name__ == '__main__':
    # Load the features. We will use the 'summary_stats' to get the pltaform/ins couples & models
    with open('../CMR_Queries/cmr_results/forward_gesdisc/forward_gesdisc_features_rerun_all.json', encoding='utf-8') as f:
        features_data = json.load(f)

    # Load the pubs_with_attachs_file to get both information to create a mapping from pdf_key to zotero_key
    with open('../more_papers_data/forward_gesdisc_linkage/pubs_with_attchs_forward_ges.json', encoding='utf-8') as f:
        pubs_with_attachs = json.load(f)

    # Decalre the Zotero Parameters
    library_id = '2395775'  # group GES DISC library
    library_type = 'group'
    api_key = 'IfniSMyDpw2y2TlSnHBWr852'  # on the Zotero API key generator, you have to specifically ALLOW write access

    # Connect to the Zotero API
    zot = zotero.Zotero(library_id, library_type, api_key)

    pdf_key_to_zotero_key = {pwa['pdf_dir']: pwa['key'] for pwa in pubs_with_attachs}

    with open('sources/couples_to_source_couples.json') as f:
        couples_to_source_couples = json.load(f)

    with open('sources/models_to_source_models.json') as f:
        models_to_source_models = json.load(f)

    count = 0
    source_plat_ins_added_count, source_models_added_count, papers_tagged_with_source = 0, 0, 0
    # loop through the papers in the features dict and add the appropriate zotero source tags
    for pdf_key, feature in features_data.items():
        count += 1
        zotero_key = pdf_key_to_zotero_key[pdf_key]  # zotero key used to reference item in zotero

        # get the couples from the features and convert them into source couples
        summary_stats = feature['summary_stats']
        platform_ins_couples_raw = summary_stats['valid_couples']
        platform_ins_couples = list(set([re.sub(r'----level[\- ]\d', '', pic) for pic in platform_ins_couples_raw]))  # remove the level from the couple
        source_plat_ins_couples = [couples_to_source_couples[pic] for pic in platform_ins_couples]

        # get the models from the features and convert them into source models
        models_raw = summary_stats['models']
        models_no_duplicates = list(set(models_raw))
        source_models = [models_to_source_models[mod] for mod in models_no_duplicates]

        print(pdf_key, zotero_key, source_plat_ins_couples)
        print(pdf_key, zotero_key, source_models)

        # add platform/ins source tags to the item in Zotero
        for spic in source_plat_ins_couples:
            current_item = None
            current_item = zot.item(zotero_key)
            source_plat_ins_added_count += 1
            tag(current_item, f'source:{spic}', zot)

        # add Models/Analyses tag to the item in Zotero
        for sm in source_models:
            current_item = None
            current_item = zot.item(zotero_key)
            source_models_added_count += 1
            tag(current_item, f'source:{sm}', zot)

        if len(source_plat_ins_couples) > 0 or len(source_models) > 0:
            papers_tagged_with_source += 1

    print("added plat/ins", source_plat_ins_added_count)
    print("added models counts", source_models_added_count)
    print("papers tagged with at least one source", papers_tagged_with_source)