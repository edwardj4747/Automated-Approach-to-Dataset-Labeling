import json
import requests
import re


def convert_science_keyword(science_keyword):
    with open('../data/json/keywords.json', encoding='utf-8') as f:
        keywords = json.load(f)

    with open('../data/json/species_to_variable_level.json', encoding='utf-8') as f:
        cmr_keywords = json.load(f)

    if science_keyword in cmr_keywords.keys():
        return science_keyword

    if keywords['variables']['short_to_long'].get(science_keyword, "").upper() in cmr_keywords:
        return keywords['variables']['short_to_long'][science_keyword]

    # a few manual mappings
    manual_mappings = {
        "NO": "nitrous oxide",
        "n2o": "nitrous oxide",
        "hcl": "hydrogen chloride",
        "rhi": "relative humidity",
        "bro": "bromine monoxide"
    }
    if science_keyword in manual_mappings:
        science_keyword = manual_mappings[science_keyword]
        return science_keyword


    # print("unresolved keyword ", science_keyword)
    return science_keyword


def get_top_cmr_dataset(platform, instrument, science_keyword, science_keyword_search=True, num_results=1, level=None):

    if science_keyword == 't':
        science_keyword = 'temperature'
    elif science_keyword == "iwc":
        science_keyword = "ice water content"

    url = f'https://cmr.earthdata.nasa.gov/search/collections.json?pretty=true&page_size={num_results}&page_num=1&has_granules=True&data_center=*GESDISC*&options[data_center][pattern]=true'
    if level:
        level = re.sub(r'level ', '', level)
        url += f'&processing_level_id[]={level}'

    science_keywords_with_no_mapping = {'temperature', "ice water content", 'halons', 'ch3br', 'vocs'}

    if science_keyword_search:
        query_string = ""
        if platform:
            query_string += f'&platform={platform}&options[platform][ignore-case]=true'
        if instrument:
            query_string += f'&instrument={instrument}&options[instrument][ignore-case]=true'
        if science_keyword:
            science_keyword = convert_science_keyword(science_keyword)
            query_string += f'&science_keywords[0][variable-level-1]=*{science_keyword}*' \
                            f'&science_keywords[1][variable-level-2]=*{science_keyword}*' \
                            f'&science_keywords[2][variable-level-3]=*{science_keyword}*' \
                            f'&science_keywords[3][detailed-variable]=*{science_keyword}*' \
                            f'&options[science_keywords][pattern]=true&options[science_keywords][or]=true' \
                            f'&options[science_keywords][ignore-case]=true'

        url += query_string
    else:
        if science_keyword:
            science_keyword = convert_science_keyword(science_keyword)
        url += f'&keyword={platform if platform else ""}%20{instrument}%20{science_keyword}'

    response = requests.get(url)
    # print(url)
    if response.status_code == 200:
        data = response.json()
    else:
        print(url)
        print("response code", response.status_code)
        raise RuntimeWarning("Could not access CMR API")

    # print(data)
    top_datasets = []
    for element in data['feed']['entry']:
        top_datasets.append(element['short_name'])  # dataset_id and title

    query_description = f'{platform}/{instrument}_{science_keyword}'
    if level:
        query_description += f'-level {level}'

    return query_description, top_datasets, url


if __name__ == '__main__':
    print(get_top_cmr_dataset('uars', 'mls', 'ozone'))