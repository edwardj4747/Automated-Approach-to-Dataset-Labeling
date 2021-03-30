from CMR_Queries.manually_reviewed_utilities import *
from CMR_Queries.sentence_label_utilities import *
from datetime import datetime

'''
key: {
    key
    article_name
    file_name
    manually_reviewed_datasets
    sentences with instrument, platform, model
        MORE STUFF HERE
    summary stats
    *******************************
    Per citation generate a json file containing:
    Article name, key, file name
    Manually identified datasets, if available
    
    The sentences that contain at least one of the GES DISC instruments, platforms or models
    Summary statistics:
        Instrument/platform pair counts
        Single instrument, platform, model counts
        Derived dataset (from CMR) counts
    
    For each sentence:
        Extract instruments, platforms or models (either GES DISC or not) record them as matching instrument/platform pair if possible, otherwise as single features.
        Extract science keywords, and record them.
    For each instrument/platform pair:
        For each science keyword:
            Query CMR and record first returned dataset
    For reminder of instruments
        For each science keyword:
            Query CMR and record first returned dataset
            
            
    I want to add spatial resolutions, level, versions, etc.. if possible
}

'''

if __name__ == '__main__':
    preprocessed_directory = '../convert_using_cermzones/aura-mls/preprocessed/'
    zot_linkage_location = '../more_papers_data/omi_zot_linkage/'
    pubs_with_attchs_location = '../more_papers_data/zot_linkage/mls_pubs_with_attchs.json'
    zot_notes_location = '../more_papers_data/zot_linkage/zot_notes_mls.json'
    dataset_couples_location = '../data/json/datasets_to_couples.json'
    keyword_file_location = '../data/json/keywords.json'
    mission_instrument_couples = '../data/json/mission_instrument_couples_LOWER.json'

    key_title_ground_truth = get_manually_reviewed_ground_truths(zot_linkage_location, dataset_couples_location, pubs_with_attchs_location, zot_notes_location)
    sentences_stats_queries = run_keyword_sentences(keyword_file_location, mission_instrument_couples, preprocessed_directory)

    now = datetime.now()
    current_time = now.strftime("%H-%M-%S") + "_aura_mls_no_cap_ALL_papers_"

    with open(current_time + 'key_title_ground_truth.json', 'w', encoding='utf-8') as f:
        json.dump(key_title_ground_truth, f, indent=4)

    with open(current_time + 'features.json', 'w', encoding='utf-8') as f:
        json.dump(sentences_stats_queries, f, indent=4)

    # Merge the features and zotero information
    for parent_key, value in key_title_ground_truth.items():
        pdf_key = value['pdf']
        if pdf_key in sentences_stats_queries:
            for inner_key, inner_value in sentences_stats_queries[pdf_key].items():
                value[inner_key] = inner_value

        key_title_ground_truth[parent_key] = value

    with open(current_time + 'features_merged.json', 'w', encoding='utf-8') as f:
        json.dump(key_title_ground_truth, f, indent=4)

