import json
import glob
import re
from tqdm import tqdm

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sentences_broad import load_in_GES_parameters, standardize, text_substitution
import nltk
# nltk.download('punkt')
# nltk.download('stopwords')


'''
    Create a corpus including all the sentences from any aura/mls papers
        Get the text from each paper
        Clean the text
        Keyword standardization ('microwave limb sounder' -> 'mls' etc)
        Add the sentence to the list of sentences if the ratio of characters to words is greater than a threshold
            this ignores some clearly wrong cermine sentences like 'n a s a a u t h o r...'
'''


def clean_text_function(sentence):
    sentence = re.sub(r'\(\w+ et al., [0-9]{2,4}\)''', '', sentence)  # (Author et al., 2015)
    sentence = re.sub(r'et al.', 'et al', sentence)  # remove periods from 'et al' for better sentence spliting
    sentence = re.sub(r'e.g.', 'eg', sentence)
    sentence = re.sub(r'i.e.', 'ie', sentence)

    sentence = re.sub(r'[^\x00-\x7F]+', '', sentence)  # non ascii characters
    sentence = re.sub(r'https?://.*?((.com)|(.org)|(.gov))', '', sentence)  # links http://disc.sci.gsfc.nasa.gov

    sentence = re.sub(r'[=~,:%;<>/\[\]\(\)\']', '', sentence)
    sentence = re.sub(r'--', ' ', sentence)
    sentence = re.sub(r'[^\-a-zA-Z][0-9]+', '', sentence)  # numbers
    sentence = re.sub(r'^[0-9]+ ', '', sentence)  # numbers at beginning
    sentence = re.sub(r'^([a-z] ){2,}', '', sentence)  # n a s a a u t h o ...

    sentence = re.sub(r' {2,}', ' ', sentence)  # extra spaces

    stop_words = set(stopwords.words('english'))
    stop_words.remove('t')
    word_tokens = word_tokenize(sentence)  # look at tokenization of things like 'sage ii' vs 'sage-ii'
    filtered_sentence = [w for w in word_tokens if not w in stop_words]

    sentence = ' '.join(filtered_sentence)
    sentence = re.sub(r' \.', '.', sentence)
    return sentence


def len_to_words_ratio(sen):
    ratio_threshold = 4
    word_threshold = 5
    length = len(sen)
    words = len(sen.split(' '))
    return length / words > ratio_threshold and words > word_threshold


if __name__ == '__main__':
    all_papers_text = []

    for file_path in tqdm(glob.glob('../convert_using_cermzones/preprocessed/*.txt')):
        with open(file_path, encoding='utf-8') as file:
            text = file.read()
            clean_text = clean_text_function(text)
            print(text.replace("\n", ''))
            print(clean_text)

        aliases, missions, instruments, variables, valid_couples, complex_datasets = load_in_GES_parameters(outside=True)
        sub_text = text_substitution(clean_text.lower(), aliases, missions, instruments, variables, complex_datasets)

        print(sub_text)
        all_papers_text += sub_text.split(".")
        all_papers_text = [apt for apt in all_papers_text if len_to_words_ratio(apt)]

    with open('ml_data/all_sentences_for_doc2vec.json', 'w', encoding='utf-8') as f:
        json.dump(all_papers_text, f, indent=4)
