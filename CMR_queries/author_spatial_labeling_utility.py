import re
import json

"""
    This gets called from sentence_label utilities to identify spatial resolutions and authors
"""


# Search for an author name in the sentence passed in. May find extra authors if author has a last time that is sometimes
# used just like a common word
def label_author(lowercase_sentence, keywords):
    authors_list = keywords['author_last_names']
    authors = []

    for last_name in authors_list:
        author_matches = re.findall(rf'[^a-zA-Z]({last_name})[^a-zA-Z]', lowercase_sentence)
        if len(author_matches) > 0:
            authors += author_matches

    return authors


# Determine if the candidate lowercase sentence actually contains spatial resolutions
def get_resolution(lowercase_sentence):
    # regex patterns crafted to identify spatial resolutions. Note that the order matters. more specific -> less specific
    patterns = [r'(\d+(?:\.\d+)? ?(?:to|\-) ?\d+ k?m(?!hz))', # 2 - 4 km,
                r'\d+(?:\.\d+)? ?(?:k?m)? ?[\u00d7|x] ?\d+(?:\.\d+)? ?k?m',  #40km x 320km
                r'(\d+(?:\.\d+)?[ \-]k?m(?!hz))',  # 2.3km. For both not mhz
                r'\d+(?:\.\d+)?\u25e6? ?[\u00d7|x] ?\d+(?:\.\d+)?\u25e6',  # 5.6◦ × 5.6◦
                r'\d+(?:\.\d+)?◦']  # 5.6◦

    resolutions = []
    for pattern in patterns:
        if len(re.findall(pattern, lowercase_sentence)) > 0:
            res = re.findall(pattern, lowercase_sentence)
            # print(res)
            resolutions += res
            lowercase_sentence = re.sub(pattern, '', lowercase_sentence)
    return resolutions


# Find candidate phrases that may contain spatial resolutions. Pass them into get_resolution to determine if actually a
# spatial resolution of not
def identify_spatial_resolution(lowercase_sentence):
    key_phrases = ['vertical resolution', 'horizontal resolution']
    with_numbers, without_numbers, found_resolutions = [], [], []
    # remove years as this sometimes creates noise
    lowercase_sentence = re.sub(r'\d{4}(?! ?k?m)', '', lowercase_sentence)  # remove 4-digit (year) numbers unless is a distance in km or m

    for kp in key_phrases:  # candidate phrases that may contain spatial resolutions
        if len(re.findall(rf'{kp}', lowercase_sentence)) > 0:
            # has some digits that are denoting things other figures, tables, versions, or level
            if len(re.findall(r'\d', lowercase_sentence)) > 0 and len(re.findall(r' \d', lowercase_sentence)) > len(re.findall(r'(fig )|(table )|(version )|(level )\d', lowercase_sentence)):
                with_numbers.append(lowercase_sentence)  # just for debugging
                found_resolutions += get_resolution(lowercase_sentence)  # determine if the sentence actually has a spatial resolution mentioned
            else:
                without_numbers.append(lowercase_sentence)  # just for debugging

    return found_resolutions

# just experiments to text some of the functions.
if __name__ == '__main__':
    s = 'the results were horizontal resolution and vertical resolution 5 km observed by (livesey et al.) in 2012...'
    s = 'horizontal resolution (40 km x 320 km) than...'
    s = 'the nadir horizontal resolution of omi is 13 km2  24 km2...'
    keyword_file_location = '../data/json/keywords.json'
    with open(keyword_file_location) as f:
        keywords = json.load(f)

    results = label_author(s.lower(), keywords)
    print(results)

    spatial = identify_spatial_resolution(s.lower())
    print(spatial)