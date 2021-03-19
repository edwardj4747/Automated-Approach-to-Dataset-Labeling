import re
import json


def label_author(lowercase_sentence, keywords):
    authors_list = keywords['author_last_names']
    authors = []

    for last_name in authors_list:
        author_matches = re.findall(rf'[^a-zA-Z]({last_name})[^a-zA-Z]', lowercase_sentence)
        if len(author_matches) > 0:
            authors += author_matches

    return authors


def get_resolution(lowercase_sentence):
    # patterns = [r'(\d+(?:\.\d+)? ?(?:to|\-) ?\d+ k?m(?!hz))', r'(\d+(?:\.\d)?[ \-]k?m(?!hz)']  # 2 - 4 km, 2.3km
    patterns = [r'(\d+(?:\.\d+)? ?(?:to|\-) ?\d+ k?m(?!hz))',
                r'(\d+(?:\.\d+)?[ \-]k?m(?!hz))']  # 2 - 4 km, 2.3km. For both not mhz
    for pattern in patterns:
        if len(re.findall(pattern, lowercase_sentence)) > 0:
            res = re.findall(pattern, lowercase_sentence)
            print(res)
            lowercase_sentence = re.sub(pattern, '', lowercase_sentence)

    '''
        @todo: the nadir horizontal resolution of omi is 13 km2  24 km2. mls is a limbviewing instrument, and a single profile in standard products of mls o3 measurements has a spatial resolution of 6 km crosstrack and approximately 200 km along track
        high horizontal resolution (38 km by 38 km)
    '''

def identify_spatial_resolution(lowercase_sentence):
    # Look for degree symbols, word degree (actually not useful--false positive occurrences), km/m, horizontal/vertical resolution the 'x' char
    # avoid words fig, table, level, version

    key_phrases = ['vertical resolution', 'horizontal resolution']
    with_numbers = []
    without_numbers = []
    # temporarily remove years
    lowercase_sentence = re.sub(r'\d{4}(?! ?k?m)', '', lowercase_sentence)  # remove 4-digit (year) numbers unless is a distance in km or m

    for kp in key_phrases:
        if len(re.findall(rf'{kp}', lowercase_sentence)) > 0:
            if len(re.findall(r'\d', lowercase_sentence)) > 0 and len(re.findall(r' \d', lowercase_sentence)) > len(re.findall(r'(fig )|(table )|(version )|(level )\d', lowercase_sentence)):
                with_numbers.append(lowercase_sentence)
                get_resolution(lowercase_sentence)
            else:
                without_numbers.append(lowercase_sentence)
        elif len(re.findall(r'\u25e6', lowercase_sentence)) > 0:
            # For this to be useful need to keep the degree symbol in from the preprocessing step
            if len(re.findall(r'\d', lowercase_sentence)) > 0:
                with_numbers.append(lowercase_sentence)
            else:
                without_numbers.append(lowercase_sentence)
    if len(with_numbers) + len(without_numbers) >= 1:
        print(with_numbers)
        # print(without_numbers)
        print("----")
    return []

if __name__ == '__main__':

    s = "the results were observed by (livesey et al.) in 2012 and manney et al and lim"
    keyword_file_location = '../data/json/keywords.json'
    with open(keyword_file_location) as f:
        keywords = json.load(f)

    results = label_author(s.lower(), keywords)
    print(results)
