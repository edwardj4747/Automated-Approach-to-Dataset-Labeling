import json
import re

'''
    Represent papers as series of only keywords. Sentences represent sections that potentially identify a dataset. 
        ie: a paper may look something like
        aura mls aura o3 o3 o3 o3 o3
        mls mls mls o3 o3 mls
        ....
        
    If a paper does not have sentences, do not add the paper.
'''


def get_text(paper, alt_path=''):
    preprocessed_location = alt_path + '../convert_using_cermzones/preprocessed/'
    with open(preprocessed_location + paper + '.txt', encoding='utf-8') as f:
        text = f.read()
    return text


def basic_clean(text):
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # remove non unicode characters
    text = re.sub(r'et al.,?', 'et al', text)
    text = re.sub(r'e.g.,?', 'eg', text)
    text = re.sub(r'i.e.,?', 'ie', text)
    text = re.sub(r'\.[0-9]+', '', text)  # removing the decimals
    text = re.sub(r'\(\)', '', text)  # punctuation
    text = re.sub(r'(https?://)?([\da-z\.-]+)\.([a-z\.]{2,6})([/\w \.-]*)', '', text)  # removing the links

    text = re.sub('\n', ' ', text)
    return text


def remove_all_non_keywords(sentence, keywords):
    if type(sentence) is list:
        sentence = '.'.join(sentence)

    missions_short = list(keywords['missions']['short_to_long'])
    instruments_short = list(keywords['instruments']['short_to_long'])
    variables_short = list(keywords['variables']['short_to_long'])

    sentence = substitute_keywords(sentence, keywords)

    new_sentence = ""
    for word in sentence.split(" "):
        if word != 'no' and (word in missions_short or word in instruments_short or word in variables_short or re.fullmatch(r'v\d', word)):
            new_sentence += word + " "
        elif word.endswith("."):
            new_sentence += ". "

    new_sentence = re.sub(r' \.', '.', new_sentence)  # spaces before the period
    new_sentence = re.sub(r'\.+', '.', new_sentence)  # multiple periods

    return new_sentence, len(new_sentence.split())


def substitute_keywords(sentence, keywords):
    lowercase_sentence = sentence.lower()

    missions = list(keywords['missions']['long_to_short'])
    instruments = list(keywords['instruments']['long_to_short'])
    variables = list(keywords['variables']['long_to_short'])

    for long_m in missions:
        if long_m in lowercase_sentence and long_m != '':
            short_m = keywords['missions']['long_to_short'][long_m]
            lowercase_sentence = re.sub(rf'{long_m}', f'{short_m}', lowercase_sentence)

    for long_i in instruments:
        if long_i in lowercase_sentence and long_i != '':
            short_i = keywords['instruments']['long_to_short'][long_i]
            lowercase_sentence = re.sub(rf'{long_i}', f'{short_i}', lowercase_sentence)

    for long_v in variables:
        if long_v in lowercase_sentence and long_v != '':
            short_v = keywords['variables']['long_to_short'][long_v]
            lowercase_sentence = re.sub(rf'{long_v}', f'{short_v}', lowercase_sentence)

    # see if dataset versions are mentioned and replace 'version 4' with v4
    lowercase_sentence = re.sub(r'[vV]ersion ([0-9])', 'v\\1', lowercase_sentence)

    return lowercase_sentence


def is_good_possibility(possibility, total_required):
    return sum(possibility) > total_required


def get_last_zero_index(possibilities):
    # this is inefficient but should work ok
    last_zero_index = len(possibilities)
    for i in range(len(possibilities) - 1, -1, -1):
        if possibilities[i] == 0:
            last_zero_index = i
        else:
            break
    return last_zero_index


def sentences_from_index(index_list, values):
    base_sentence = ' '.join(values[index_list[0]:index_list[-1] + 1])
    final_sentence = re.sub(r' {2,}', ' ', base_sentence)  # remove extra space
    return final_sentence.strip()

def run_keyword_sentences(save=False, alt_path=''):
    with open(alt_path + '../data/json/keywords.json') as f:
        keywords = json.load(f)

    paper = '2AQ88HE3.txt'

    # with open('ml_data/raw_data_all_papers_broad_aura_mls_ONLY.json') as f:
    #     raw_data = json.load(f)

    with open(alt_path + '../more_papers_data/zot_linkage/new_papers_ground_truths.json') as f:
        ground_truths = json.load(f)

    all_paper_list = list(ground_truths.keys())
    print("Len all papers ", len(all_paper_list))

    keyword_sentences_dict = {}
    original_sentences_dict = {}

    # all_paper_list = ['ZFGFZZTV']
    papers_not_found = []
    papers_with_no_sentences = []

    for paper in all_paper_list:
        try:
            text = get_text(paper, alt_path=alt_path)
        except FileNotFoundError:
            papers_not_found.append(paper)
            continue
        text = basic_clean(text)

        freqs = []
        values = []
        original_sentences = text.split(".")
        keyword_sentence = ""
        for sent in text.split("."):
            just_keywords, number_keywords = remove_all_non_keywords(sent, keywords)
            # if paper == 'LNW9PJEF':
            #     print(just_keywords)
            freqs.append(number_keywords)
            values.append(just_keywords)

        # Declare useful parameters
        min_in_first_sentence = 1
        max_sent_distance = 3
        max_num_sentences = 3
        total_required = 4

        continue_count = 0

        in_potential_sequence = False
        good_possibilities_list = []
        good_possibilities_index_list = []
        possibilities = []
        possibilities_index = []
        results = []
        cps_length = 0  # current possible sequence
        cps_num_zeros = 0

        for index, value in enumerate(freqs):
            if value == 0 and not in_potential_sequence:
                continue_count += 1
                in_potential_sequence = False
                continue
            if value > 0 and not in_potential_sequence:
                in_potential_sequence = True
                cps_num_zeros = 0  # every time we see a non-zero number, reset the zero count
                possibilities.append(value)
                possibilities_index.append(index)
            elif value >= 0 and in_potential_sequence:  # can have zero values b/c now in sequence
                if value == 0:
                    cps_num_zeros += 1
                    if cps_num_zeros > max_sent_distance:
                        in_potential_sequence = False
                        cps_num_zeros = 0
                        cps_length = 0
                        # print("possibilities ", possibilities)
                        if is_good_possibility(possibilities, total_required):
                            last_zero_index = get_last_zero_index(possibilities)
                            good_possibilities_list.append(possibilities[:last_zero_index])
                            good_possibilities_index_list.append(possibilities_index[:last_zero_index])
                        possibilities = []
                        possibilities_index = []
                        continue
                elif value > 0:
                    cps_num_zeros = 0
                cps_length += 1
                possibilities.append(value)
                possibilities_index.append(index)
                if cps_length > max_num_sentences:
                    in_potential_sequence = False
                    cps_num_zeros = 0
                    cps_length = 0
                    # print("possibilities ", possibilities)
                    if is_good_possibility(possibilities, total_required):
                        last_zero_index = get_last_zero_index(possibilities)
                        good_possibilities_list.append(possibilities[:last_zero_index])
                        good_possibilities_index_list.append(possibilities_index[:last_zero_index])
                    possibilities = []
                    possibilities_index = []

        # print("at end possibilities ", possibilities)
        # print("good possibiliteis ", good_possibilities_list)
        # print("good possibilities index ", good_possibilities_index_list)
        paper_sentences = []
        original_sentences_list = []
        for index_list in good_possibilities_index_list:
            paper_sentence = sentences_from_index(index_list, values)
            # print(paper_sentence)
            # print(original_sentences[index_list[0]: index_list[-1] + 1])
            # print('. '.join(original_sentences[index_list[0]: index_list[-1] + 1]))
            original_sentences_list.append(original_sentences[index_list[0]: index_list[-1] + 1])
            paper_sentences.append(paper_sentence)

        if len(paper_sentences) == 0:
            print("CONTINUE")
            papers_with_no_sentences.append(paper)
            continue

        keyword_sentences_dict[paper] = {
            "ground_truths": ground_truths[paper],
            "keyword_sentences": paper_sentences
        }

        original_sentences_dict[paper] = {
            "original_sentences": original_sentences_list
        }

        # print(paper, ground_truths[paper])
        # print()

    print("Papers not found ", len(papers_not_found), papers_not_found)
    print("Papers with no sentences ", len(papers_with_no_sentences), papers_with_no_sentences)
    num_papers_in_dictionary = len(all_paper_list) - len(papers_not_found) - len(papers_with_no_sentences)

    if save:
        with open('../more_papers_data/keyword_sentences_' + str(num_papers_in_dictionary) + "_papers.json", 'w', encoding='utf-8') as f:
            json.dump(keyword_sentences_dict, f, indent=4)

    return keyword_sentences_dict, original_sentences_dict

    '''
    Todo: clean out reanalysis data??
    '''

if __name__ == '__main__':
    run_keyword_sentences()