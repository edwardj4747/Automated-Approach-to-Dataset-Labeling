import json
from tqdm import tqdm
import sentences_broad
import pprint
from sentences_broad import SentenceMode
from enum import Enum

'''
    Extract Sentences from preprocessed text files. Result is dict of form
    
    "4MFNKR4V": {
        "ground_truth": ["ML2T", ...],
        "data": {
            "(aqua/modis,None)": {
                "mission": "aqua",
                "instrument": "modis",
                "variable": "None",
                "sentences": [
                    "the bottom plots of figure 1 are clear-sky aqua modis images for each site",
                    "the aqua modis images show examples of clear-sky cases at each site"
                ],
                "num_sentences": 2
            }, ...
        }
    }
'''


class RunningMode(Enum):
    SINGLE_FILE = 1,
    MULTIPLE_FILES = 2,
    ML_SPLITS = 3,


def read_json_file(file_name, alternate_path='ml_data/'):
    with open(alternate_path + file_name + ".json", encoding='utf-8') as f:
        return json.load(f)


def read_text_file(file_key):
    preprocessed_directory = '../convert_using_cermzones/preprocessed/'
    document = preprocessed_directory + file_key + '.txt'
    with open(document, encoding='utf-8') as f:
        txt = f.read()
    return txt


def display_heading(key, key_title_mapping):
    print("**********")
    print(key, ": ", key_title_mapping[key])


def process_paper(paper, key_to_title_mapping, input_features, ground_truths, paper_variable_counts=None,
                  sent_mode=SentenceMode.STRICT):
    display_heading(paper, key_to_title_mapping)

    # get the text for the document
    document_text = read_text_file(paper)

    data, reanalysis_data, var_stats = sentences_broad.create_sentences_for_ML(document_text, sent_mode)
    # print(data)
    # print(reanalysis_data)

    mission_statistics, instrument_statistics, variable_statistics, mission_instrument_statistics, complete_mis_ins_couples, mis_ins_var \
        = sentences_broad.compute_summary_statistics_basic(data)

    missions_list = list(mission_statistics.keys())
    instrument_list = list(instrument_statistics.keys())
    variable_list = list(variable_statistics.keys())
    reanalysis_list = list(reanalysis_data.keys())

    # convert data into an cleaner format
    clean_data = {}
    for key in data.keys():
        sentences = [data[key][i]['sentence'] for i in range(len(data[key]))]
        standardized_sentences = [sentences_broad.text_substitution(s, aliases, missions_list,
                                                                    instrument_list, variable_list, reanalysis_list) for
                                  s in sentences]
        clean_data[str(key)] = {
            'mission': data[key][0]['mission'],
            'instrument': data[key][0]['instrument'],
            'variable': data[key][0]['variable'],
            'sentences': standardized_sentences,
            'num_sentences': len(standardized_sentences)
        }

    paper_ground_truths = ground_truths.get(paper, 'Unknown')
    input_features[paper] = {
        'ground_truth': paper_ground_truths,
        'data': clean_data,
    }

    return input_features, var_stats


def display_results(input_features, display_input_dict=False):
    if display_input_dict:
        pp = pprint.PrettyPrinter(width=300)
        pp.pprint(input_features)

    all_sentences = []
    for paper_key, paper_value in input_features.items():
        for mis_ins_var_key, data_value in paper_value['data'].items():
            all_sentences += data_value['sentences']

    unique_sentences = list(set(all_sentences))
    print("all sentences ", len(all_sentences))
    print(all_sentences)
    print("unique sentences ", len(unique_sentences))
    print(unique_sentences)


if __name__ == '__main__':
    running_mode = RunningMode.MULTIPLE_FILES

    key_to_title_mapping = read_json_file('key_to_title')
    ground_truths = read_json_file('ground_truths')
    manually_reviewed_pdfs = ground_truths.keys()
    aliases = read_json_file('aliases', alternate_path='../data/json/')
    input_features = {}
    paper_var_counts = {}

    if running_mode == RunningMode.SINGLE_FILE:
        paper = list(manually_reviewed_pdfs)[0]  # 4MFNKR4V A clear-sky radiation closure study using a (Dolinar)
        paper = '2XYSGVI2'  # Assessment of upper tropospheric and stratospheric water vapor and ozone..as part of S-RIP
        input_features, paper_var_counts = process_paper(paper, key_to_title_mapping, input_features, ground_truths,
                                                         sent_mode=SentenceMode.BROAD)
        display_results(input_features, display_input_dict=True)
        print("var stats ", paper_var_counts)

    elif running_mode == RunningMode.MULTIPLE_FILES:
        papers = list(manually_reviewed_pdfs)

        for paper in tqdm(papers):
            try:
                input_features, _ = process_paper(paper, key_to_title_mapping, input_features,
                                                  ground_truths, sent_mode=SentenceMode.BROAD)
            except FileNotFoundError:
                continue
        display_results(input_features)
        # with open('ml_data/raw_data_all_papers_braod.json', 'w', encoding='utf-8') as f:
        #     json.dump(input_features, f, indent=4)

    elif running_mode == RunningMode.ML_SPLITS:
        splits = read_json_file('train_test_split')
        train_keys = splits['train']
        print(train_keys)
        # merge all the extracted sentences from a paper into one paragraph
        one_paragraph_per_paper = []
        one_paragraph_per_dict = {}
        papers_without_any_sentences = 0
        for paper in tqdm(train_keys):
            try:
                input_features, _ = process_paper(paper, key_to_title_mapping, input_features,
                                                                 ground_truths)
                if len(input_features[paper]['sentences']) == 0:
                    papers_without_any_sentences += 1
                para = '. '.join(input_features[paper]['sentences'])
                one_paragraph_per_paper.append(para)
                one_paragraph_per_dict[paper] = para
            except FileNotFoundError:
                continue
        print("papers without any sentences ", papers_without_any_sentences)
        display_results(input_features)
        print("len one_pg_per paper ", len(one_paragraph_per_paper))
        print(one_paragraph_per_paper)
        print(one_paragraph_per_dict)
