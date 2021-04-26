import regex as re
import json

text = "Schwartz, M., Pumphrey, H., Livesey, N., and Read, W.: MLS/Aura Level 2 Carbon Monoxide (CO) Mixing Ratio V004, version 004, Greenbelt, MD, USA, Goddard Earth Sciences Data and Information Services Center (GES DISC), available at: doi:10.5067/AURA/MLS/DATA2005, last access: January 2016, 2015"


output_file_name = "free_text/forward_ges_references_and_text.json"
cermzones_directory = '../convert_using_cermzones/forward_gesdisc/successful_cermfiles/'
doi_to_dataset_mapping_location = '../data/json/doi_to_dataset_name.json'
dataset_long_to_short_mapping = '../data/json/dataset_long_to_short.json'

reference_label = "GEN_REFERENCES"
keyword = r'(?:disc\.gsfc\.nasa\.gov)|(?:GES[ -]?DISC)'
papers_with_explicit_mentions = 0
results = {}

with open(doi_to_dataset_mapping_location) as f:
    doi_to_dataset = json.load(f)

dataset_to_doi = {v: k for k, v in doi_to_dataset.items()}

with open(dataset_long_to_short_mapping) as f:
    dataset_long_to_short = json.load(f)

text = re.sub(r' \[CrossRef\] ?', '', text)

for doi in doi_to_dataset.keys():
    # print(doi)
    if '10.5067/Aura/MLS' in doi:
        print("YES", doi)
    if doi == "10.5067/AURA/MLS/DATA2005":
        print("DOI is 10.5067/AURA/MLS/DATA2005")
    matches = re.findall(rf'{doi}', text)
    # print(matches)
    if len(matches) >= 1:
        print(matches)

exit()
text = '''
Jahoda, E CHemical stuff https://doi.org/10.1029/2000gb001382
Kuehn, C Lawyer Stuff.
Maddalone, G. skating stuff https://doi.org/10.1126/science.1092779
'''

text = '''
Andreae, M. O., & Merlet, P. (2001). Emission of trace gases and aerosols from biomass burning. Global Biogeochemical Cycles, 15(4), 955-966.
https://doi.org/10.1029/2000gb001382
Andreae, M. O., Rosenfeld, D., Artaxo, P., Costa, A. A., Frank, G. P., Longo, K. M., & Silva-Dias, M. A. F. (2004). Smoking rain clouds over the
Amazon. Science, 303(5662), 1337-1342. https://doi.org/10.1126/s
cience.1092779
Bergeron, Y., & Gauthier, S. (Eds.) (2017). Fire regimes: Spatial and temporal variability and their effects on forests. St. Alban-anlage 66, 4052
Basel, Switzerland: Multidisciplinary Digital Publishing institute
'''


text = '''
Krotkov, N.A, Li, C. and Leonard, P. (2015). OMI/Aura
Sulfur Dioxide (SO2) Total Column L3 1 day Best Pixel
in 0.25 degree x 0.25 degree V3. Greenbelt, MD, USA,
Goddard Earth Sciences Data and Information Services
Center (GES DISC). https://doi.org/10.5067/Aura/OMI/
DATA3008
Krotkov, N.A., Lamsal, L.N., Celarier, E.A., Swartz, W.H.,
Marchenko, S.V., Bucsela, E.J., Chan, K.L., Wenig, M.
and Zara, M. (2017). The version 3 OMI NO2 standard
product. Atmos. Meas. Tech. 10: 3133-3149. https://doi.o
rg/10.5194/amt-10-3133-2017
Lee, C., Martin, R.V., van Donkelaar, A., Lee, H.,
Dickerson, R.R., Hains, J.C., Krotkov, N., Richter, A.,
Vinnikov, K. and Schwab, J.J. (2011). SO2 emissions and
lifetimes: Estimates from inverse modeling using in situ
and global, space-based (SCIAMACHY and OMI)
observations. J. Geophys. Res. 116: D06304. https://doi.
org/10.1029/2010JD014758
Lee, J.T., Son, J.Y. and Cho, Y.S. (2007). Benefits of
mitigated ambient air quality due to transportation control
on childhood asthma hospitalization during the 2002
summer Asian games in Busan, Korea. J. Air Waste
Manage. Assoc. 57: 968-973. https://doi.org/10.3155/104
7-3289.57.8.968
Lelieveld, J., Evans, J.S., Fnais, M., Giannadaki, D. and
Pozzer, A. (2015). The contribution of outdoor air
pollution sources to premature mortality on a global scale.
Nature 525: 367-371. https://doi.org/10.1038/nature15371
Li, C., Zhang, Q., Krotkov, N.A., Streets, D.G., He, K.,
Tsay, S.C. and Gleason, J.F. (2010). Recent large
reduction in sulfur dioxide emissions from Chinese power
plants observed by the Ozone Monitoring Instrument.
Geophys. Res. Lett. 37: L08807. https://doi.org/10.1029/
2010GL042594
Li, C., McLinden, C., Fioletov, V., Krotkov, N., Carn, S.,
Joiner, J., Streets, D., He, H., Ren, X., Li, Z. and
Dickerson, R.R. (2017). India is overtaking China as the
world's largest emitter of anthropogenic sulfur dioxide.
Sci. Rep. 7: 14304. https://doi.org/10.1038/s41598-01714639-8
Liu, F., Zhang, Q., van der A, R.J., Zheng, B., Tong, D.,
Yan, L., Zheng, Y. and He, K. (2016). Recent reduction
in NOx emissions over China: Synthesis of satellite
observations and emission inventories. Environ. Res.
Lett. 11: 114002. https://doi.org/10.1088/1748-9326/11/
11/114002
Lu, Z., Streets, D.G., de Foy, B. and Krotkov, N.A. (2013).
Ozone monitoring instrument observations of interannual
increases in SO2 emissions from Indian coal-fired power
plants during 2005-2012. Environ. Sci. Technol. 47:
13993-14000. https://doi.org/10.1021/es4039648
Maas, R., grennfelt, P., Amann, M., Harnett, B., Kerr, J.,
Berton, E., Pritula, D., Reiss, I., Almodovar, P., Héroux,
M.E., Fowler, D., Wright, D., de Wit, H.A., Tørseth, K.,
Mareckova, K., LeGall, A.C., Rabago, I., Hettelingh, J.P.,
Haeuber, R., … Reis, S. (2016). Towards cleaner air:
Scientific assessment report 2016 - Summary for
policymakers. United Nations Economic Commission for
Europe (UNECE). https://icpvegetation.ceh.ac.uk/sites/d
efault/files/Towards%20Cleaner%20Air%20-%20Summ
ary%20for%20Policymakers%202016%20%28English%
20Version%29.pdf
Monks, P.S., Granier, C., Fuzzi, S., Stohl, A., Williams, M.L.,
Akimoto, H., Amann, M., Baklanov, A., Baltensperger, U.,
Bey, I., Blake, N., Blake, R.S., Carslaw, K., Cooper, O.R.,
Dentener, F., Fowler, D., Fragkou, E., Frost, G.J.,
Generoso, S., … von Glasow, R. (2009). Atmospheric
composition change: Global and regional air quality.
Atmos. Environ. 43: 5268-5350. https://doi.org/10.1016/
j.atmosenv.2009.08.021
Myhre, G., Shindell, D. and Pongratz, J. (2014).
Anthropogenic and Natural Radiative Forcing, In Climate
Change 2013: The Physical Science Basis; Working
Group I Contribution to the Fifth Assessment Report of
the Intergovernmental Panel on Climate Change, Stocker,
T. (Ed.), Ludwig-Maximilians-Universität München,
Cambridge, pp. 659-740
'''

text = '''
13. Ojo J S & Ajewole M O, Dimensional statistics of rainfall
signature and fade duration for microwave propagation
in Nigeria, General Assembly and Scientific Symposium,
XXXth URSI, IEEE (Institute of Electrical and Electronics
Engineers, Istanbul, Turkey), 2011, 978-1-4244-6051-9/11.
14. Omotosho T V, Mandeep J S, Abdullah M & Adediji A T,
Distribution of one-minute rain rate in Malaysia derived from
TRMM satellite data, Ann Geophys (Germany), 31 (2013)
pp 2013-2022.
15. Mandeep J S & Hassan S I S, 60-to 1-min rainfall-rate
conversion: Comparison of existing prediction methods with
data obtained in the Southeast Asia region, J Appl Meteorol
Climatol - Notes Corres (USA), 47 (2008) pp 925-930.
'''

doi_pattern = '10\.\d{4,9}\/[-._;()\/:a-zA-Z0-9]+'
doi_pattern = '10\.\d{4,9}(?:\n\d{4,9})?\/[-._;()\/:a-zA-Z0-9\n]+'  # include \n to account for cross line dois
look_behind_doi = f'(?<=\.|{doi_pattern})\n(?=(?:\d{1,2}\.? )?(?:\w+(?:\-\w+)?,? \w))'
look_behind_doi = f'(?<=\.|{doi_pattern})\n(?=(?:\d{1,2}\.? )?(?:\w+(?:\-\w+)?[, :]? \w))'
look_behind_doi = rf'(?<=\.|{doi_pattern})\n' + r'(?=(?:\d{1,2}\.? )?(?:[a-zA-Z]+(?:\-[a-zA-Z])?[,:]? [a-zA-Z]))'

# look_ahead_doi = f'\n(?={doi_pattern})'


# print(re.findall(doi_pattern, text))
# print(re.split(doi_pattern, text))
splits = re.split(look_behind_doi, text)
# print(splits)
for s in splits:
    print(s, '\n')
    # if s:
    #     print(s, '\n')
        # print(re.sub(r'(?:\d{1,2}\.? )?(?:\w+(?:\-\w+)?[,:]? \w)', 'SUB', s, count=1), '\n')
# print("Rev")
# reverse = re.split(look_ahead_doi, text[::-1])
# print(reverse)
# print([r[::-1] for r in reverse])

text = '''
13. Ojo J S & Ajewole M O, Dimensional statistics of rainfall
signature and fade duration for microwave propagation
in Nigeria,
'''

# print(re.sub(r' ', ' SPACE ', text))
print(re.sub(r'(?:\d{1,2}\.? )?(?:\w+(?:\-\w+)?[,:]? \w)', 'AHHH', text))