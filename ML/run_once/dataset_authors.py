from collections import defaultdict
import json
import glob
import re

'''
    Create a dictionary mapping of dataset: [author(s) of the dataset] as based on the metadata files
'''


def dictionary_to_list(dataset_author_mapping, save=False):
    seen = set()
    unique_authors = []
    for list_of_authors in dataset_author_mapping.values():
        for author in list_of_authors:
            author = re.sub(r'^Dr\. ', '', author)  # remove the Dr. in a Dr. so-and-so
            author = re.sub(r'(, PH\. ?D\.?)|(, PHD)', '', author)
            author = author.lower()
            if author not in seen:
                unique_authors.append(author)
                seen.add(author)

    if save:
        with open('../ml_data/author_keywords_list.json', 'w', encoding='utf-8') as f:
            json.dump(unique_authors, f, indent=4)


def remove_known_non_authors(author_string):
        not_useful = [
            '(goddard )?laboratory for atmospheres at( +gsfc)?',
            'copernicus sentinel data processed by esa, koninklijk nederls meteorologisch instituut \(knmi\)',
            'copernicus sentinel data processed by esa, german aerospace center \(dlr\)',
            'koninklijk nederls meteorologisch instituut \(knmi\)',
            'koninklijk nederl,s meteorologisch instituut \(knmi\)',
            'netherlands institute for space research \(sron\)',
            'copernicus sentinel data processed by esa, rutherford appleton laboratory \(ral\)',
            'copernicus sentinel data processed by esa, german aerospace center-institute for environmental research,university of bremen \(dlr_iup\)',
            'copernicus sentinel data processed by esa',
            'koninklijk nederlands meteorologisch instituut \(knmi\)',
            'oco-2 science team',
            'oco(-3)? science team',
            'airs project',
            'airs science team',
            'university of michigan',
            'global hydrology resource center',
            'neespi data center project',
            'goddard space flight center \(gsfc\)',
            'gpm science team',
            'tropical rainfall measuring mission \(trmm\)',
            'tropical rainfall measuring mission \(trmm\)',
            'global modeling',
            'polder science team,cnes',
            ', assimilation office \(gmao\)',
            'goddard space flight center',
            'modis science team',
            'oxford university( aopp)?',
            'trmm science team',
            'eos mls science team',
            'goddard earth sciences data',
            ', information services center',
            'ges disc northern eurasian earth science partnership initiative project',
            'ncep,emc',
            'omi science team',
            'oxford university aopp',
            'jet propulsion laboratory: ',
            'goddard laboratory for atmospheres at  gsfc',
            'toms science team',
            'goddard laboratory for atmospheres at nasa,gsfc',
            'nasa,gsfc',
            'msfc,nasa',
            'ges_disc',
            'at princeton university,',
            'gsfc',
            'nasa'
        ]
        for nu in not_useful:
            author_string = re.sub(rf'{nu},?', '', author_string)

        return author_string

dataset_directory = 'C:/Users/edwar/Desktop/Publishing Internship/datasets'
output_file_name = 'dataset_to_miv.json'
output_file_location = '../ml_data/' + output_file_name

data = defaultdict(set)

for file in glob.glob(dataset_directory + "/*.json"):
    print(file)
    with open(file, errors='ignore') as f:
        contents = json.load(f)

    collection_citations = contents['CollectionCitations']
    short_name = contents['CollectionCitations'][0]['SeriesName']
    for cc in collection_citations:
        creator = cc.get('Creator', '').lower()
        nasa_string = 'NASA/GSFC/HSL'.lower()
        creator = re.sub(rf'{nasa_string}', ',', creator)

        creator = re.sub(r'vrije universiteit amsterdam \(richard de jeu\) and nasa gsfc \(manfred owe\)\.?',
                         'richard de jeu, manfred owe', creator)
        creator = re.sub(r'usda agricultural research service \(wade crow\)', 'wade crow', creator)
        creator = re.sub(
            r'uw-madison space science and engineering center: hank revercomb; umbc atmospheric spectroscopy laboratory: larrabee strow',
            'hank revercomb, larrabee strow', creator)
        creator = re.sub(r'princeton university \(eric wood\)', 'eric wood', creator)
        creator = re.sub(r'colorado state university \(christian kummerow\)', 'christian kummerow', creator)
        creator = re.sub(r'airs science team \(joel susskind, nasa/gsfc\)', 'joel susskind', creator)
        creator = re.sub(r'crow, wade \(usda ars\)  k. tobin \(texas a,m iu\)', 'wade crow, k. tobin', creator)
        creator = re.sub(r'/|;', ',', creator)
        creator = re.sub(r'and ', ', ', creator)
        creator = re.sub(r'&', ',', creator)
        creator = re.sub(r'e\. ?g\. ?', '', creator)
        creator = re.sub(r', et al\.', '', creator)
        creator = re.sub(r'et al\.(, )?', ',', creator)
        creator = re.sub(r',?dr\. ', '', creator)
        creator = re.sub(r'\(\d{4}\)', '', creator)
        creator = re.sub(r', phd', '', creator)
        creator = re.sub(r'(\w) [a-z]\. (\w)', '\\1 \\2', creator)  # middle initials
        creator = remove_known_non_authors(creator)
        # formatting the commas
        creator = re.sub(r' {2,}', ' ', creator)
        creator = re.sub(r' ,', ',', creator)
        creator = re.sub(r', ?,', ',', creator)
        creator = creator.strip()
        if creator != '':
            data[short_name].add(creator)
#     dataset_name = contents['CollectionCitations'][0]['SeriesName']
#     contact_person = contents['ContactPersons']
#
#     authors = []
#     for index, element in enumerate(contact_person):  # will sometimes be a list
#         if "Investigator" in element['Roles']:
#             author_name = element['FirstName'] + " " + element['LastName']
#             authors.append(author_name)
#
#     data[dataset_name] += authors
#
# Remove duplicate entries
for key, all_authors in data.items():
    seen = set()
    unique = []
    for item in all_authors:
        if item not in seen:
            unique.append(item)
        seen.add(item)
    data[key] = unique

with open('../ml_data/dataset_authors_v2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

dictionary_to_list(data, save=True)
