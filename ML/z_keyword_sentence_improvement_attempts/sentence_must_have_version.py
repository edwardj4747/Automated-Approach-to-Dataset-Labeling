import json
import re

'''
    Represent papers as series of only keywords. Sentences represent sections that potentially identify a dataset. 
        ie: a paper may look something like
        aura mls aura o3 o3 o3 o3 o3
        mls mls mls o3 o3 mls
        ....

    If a paper does not have sentences, do not add the paper. REQUIRE that all sentences that are added have mention
    a version as this is likely indicative of a dataset
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
        if word != 'no' and (
                word in missions_short or word in instruments_short or word in variables_short or re.fullmatch(r'v\d',
                                                                                                               word)):
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

    # see if levels are mentioned
    lowercase_sentence = re.sub(r'[lL]evel ([0-9])', 'L\\1', lowercase_sentence)

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

    with open(alt_path + '../more_papers_data/zot_linkage/new_papers_ground_truths.json') as f:
        ground_truths = json.load(f)

    all_paper_list = list(ground_truths.keys())
    print("Len all papers ", len(all_paper_list))

    papers_sentences_with_versions = {}
    for paper in all_paper_list:
        try:
            text = get_text(paper, alt_path=alt_path)
        except FileNotFoundError:
            continue
        text = basic_clean(text)
        keyword_sub_text = substitute_keywords(text, keywords)

        '''
            todo: this is not working how I expect/want it to currently
            
        '''

        keyword_sentences_with_version = []
        sentences_with_version = []
        for sent in keyword_sub_text.split('.'):
            if len(re.findall('[vV]ersion', sent)) > 0:
                keyword_sentences_with_version.append(substitute_keywords(sent, keywords))
                sentences_with_version.append(sent)

        papers_sentences_with_versions[paper] = {
            "original_sentences": sentences_with_version,
            "keyword_sentences": keyword_sentences_with_version
        }

    with open('data/paper_sentences_require_version.json', 'w', encoding='utf-8') as f:
        json.dump(papers_sentences_with_versions, f, indent=4)


if __name__ == '__main__':
    run_keyword_sentences()