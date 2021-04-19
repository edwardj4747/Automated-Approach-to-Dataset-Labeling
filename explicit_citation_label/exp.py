import regex as re

text = '''
Jahoda, E CHemical stuff https://doi.org/10.1029/2000gb001382
Kuehn, C Lawyer Stuff.
Maddalone, G. skating stuff https://doi.org/10.1126/science.1092779
'''

text = '''
AIRS Science Team/Joao Texeira (2013). AIRS/Aqua L2 standard physical retrieval (AIRS+AMSU) V006, Greenbelt, MD, USA, Goddard Earth
Sciences Data and Information Services Center (GES DISC), accessed on May 2017. https://doi.org/10.5067/AQUA/AIRS/DATA 201
Akagi, S. K., Yokelson, R. J., Wiedinmyer, C., Alvarado, M. J., Reid, J. S., Karl, T., et al. (2011). Emission factors for open and domestic biomass
burning for use in atmospheric models. Atmospheric Chemistry and Physics, 11(9), 4039-4072. https://doi.org/10.5194/acp-11-4039-2011
Andreae, M. O., & Merlet, P. (2001). Emission of trace gases and aerosols from biomass burning. Global Biogeochemical Cycles, 15(4), 955-966.
https://doi.org/10.1029/2000gb001382
Andreae, M. O., Rosenfeld, D., Artaxo, P., Costa, A. A., Frank, G. P., Longo, K. M., & Silva-Dias, M. A. F. (2004). Smoking rain clouds over the
Amazon. Science, 303(5662), 1337-1342. https://doi.org/10.1126/science.1092779
Bergeron, Y., & Gauthier, S. (Eds.) (2017). Fire regimes: Spatial and temporal variability and their effects on forests. St. Alban-anlage 66, 4052
Basel, Switzerland: Multidisciplinary Digital Publishing institute
'''

doi_pattern = '10\.\d{4,9}\/[-._;()\/:a-zA-Z0-9]+'
look_behind_doi = f'(?<=\.|{doi_pattern})\n(?=(?:\d{1,2}\.? )?(?:\w+(?:\-\w+)?,? \w))'
# look_ahead_doi = f'\n(?={doi_pattern})'


# print(re.findall(doi_pattern, text))
# print(re.split(doi_pattern, text))
splits = re.split(look_behind_doi, text)
print(splits)
for s in splits:
    print(s, '\n')
# print("Rev")
# reverse = re.split(look_ahead_doi, text[::-1])
# print(reverse)
# print([r[::-1] for r in reverse])