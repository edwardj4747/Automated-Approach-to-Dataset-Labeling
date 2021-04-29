'''
    Sometimes you may want to update just one paper at a time in the features file (ie: rerun the feature extraction
    code). This file allows you to do that.

    Reasons you might want to do this: you have added new keywords in the keywords file to better accommodate some papers
'''

from CMR_Queries.automatically_label import run_keyword_sentences
import json

if __name__ == '__main__':
    # User parameters
    pdf_to_update = '2AHP254C.txt'  # define which pdf we want to re-run the sentence labelling for
    update_CMR = False  # True means rer-run CMR queries. False means, say 'Not Run' for CMR queries
    save_backup = False  # Save a copy of the current features before modifying the pdf to update
    preprocessed_location = '../convert_using_cermzones/aura-omi/preprocessed/'
    features_dict_location = '../CMR_Queries/cmr_results/aura-omi/3-22-15-Aura_omi_features.json'

    dataset_couples_location = '../data/json/datasets_to_couples.json'
    keyword_file_location = '../data/json/keywords.json'
    mission_instrument_couples = '../data/json/mission_instrument_couples_LOWER.json'

    # re-extract the features for the specified pdf
    new_features = run_keyword_sentences(keyword_file_location, mission_instrument_couples, preprocessed_location,
                                         single_paper=pdf_to_update, update_CMR=False)

    print(new_features)

    # modify the features in the original features dict. Need to do this carefully to avoid deleting the whole file
    with open(features_dict_location, encoding='utf-8') as f:
        original_features = json.load(f)

    pdf_key = pdf_to_update.replace('.txt', '')
    if pdf_key not in original_features:
        print("\n\n\npdf_key", pdf_key, "is not in the original features dict. Exiting Program...")

    else:
        if save_backup:
            print("\n\n\nSaving a backup file")
            # save a copy of the original files just in case
            with open(features_dict_location.replace('.json', '_backup.json'), 'w', encoding='utf-8') as f:
                json.dump(original_features, f, indent=4)

        print('\n\nModifying the original...')
        original_features[pdf_key] = new_features[pdf_key]

        print('\n\nSaving the original')
        with open(features_dict_location, 'w', encoding='utf-8') as f:
            json.dump(original_features, f, indent=4)


    '''
        Code to update the feature extraction for all the papers in the directory
    '''
    # all_features = {}
    # for file in glob.glob(preprocessed_location + "*.txt"):
    #     pdf_to_update = file.split('\\')[-1].replace('.txt', '')
    #     new_features = run_keyword_sentences(keyword_file_location, mission_instrument_couples, preprocessed_location,
    #                                          single_paper=pdf_to_update, update_CMR=False)
    #     all_features[pdf_to_update] = new_features[pdf_to_update]  # just the value
    #
    # print(all_features)
    #
    # with open(features_dict_location.replace('.json', '_rerun_all.json'), 'w', encoding='utf-8') as f:
    #     json.dump(all_features, f, indent=4)`