'''
    Create 'Source' Tags that mimic the sources used on the GES DISC website that can be inputted into Zotero
    based on the mission/instrument pairs that were found
'''

import json
import re
from pyzotero import zotero
import time


def tag(current_item, tag_text, zot):
    print("Tag called with", tag_text)
    zot.add_tags(current_item, tag_text)

# Load the features. We will use the 'summary_stats' to get the pltaform/ins couples & models
with open('../CMR_Queries/cmr_results/forward_gesdisc/forward_gesdisc_features_rerun_all.json', encoding='utf-8') as f:
    features_data = json.load(f)

with open('../more_papers_data/forward_gesdisc_linkage/pubs_with_attchs_forward_ges.json', encoding='utf-8') as f:
    pubs_with_attachs = json.load(f)


library_id = '7185722'
library_id = '2395775'  # group
library_type = 'group'
# api_key = 'tJBEs3kpyfxotFPcqi7vO4tA'
api_key = 'IfniSMyDpw2y2TlSnHBWr852'
# edward_small_collection = 'HVBLJZ68'
group_forward_gesdisc = '8L3ZJKKV'


# Connect to the Zotero API
zot = zotero.Zotero(library_id, library_type, api_key)

pdf_key_to_zotero_key = {pwa['pdf_dir']: pwa['key'] for pwa in pubs_with_attachs}

unique_couples = set()
unique_models = set()

for pdf_key, feature in features_data.items():
    # print(pdf_key)
    summary_stats = feature['summary_stats']
    platform_ins_couples = summary_stats['valid_couples']
    for pic in platform_ins_couples:
        pic = re.sub(r'----level[\- ]\d', '', pic)
        unique_couples.add(pic)
    models = summary_stats['models']
    for mod in models:
        unique_models.add(mod)

# list of all valid sources from GES DISC website. Extracted from 'Refine By'
valid_sources = {
    'AC-690A CAR',
    'AEM-2 SAGE I',
    'Aqua AIRS',
    'Aqua AMSR-E',
    'Aqua AMSU-A',
    'Aqua HSB',
    'Aqua MODIS',
    'Aura HIRDLS',
    'Aura MLS',
    'Aura OMI',
    'C-131A CAR',
    'CORIOLIS WINDSAT',
    'COSMIC/FORMOSAT-3 RO',
    'CloudSat CloudSat-CPR',
    'Convair-580 CAR',
    'DMSP 5D-2/F10 SSM/I',
    'DMSP 5D-2/F11 SSM/I',
    'DMSP 5D-2/F13 SSM/I',
    'DMSP 5D-2/F14 SSM/I',
    'DMSP 5D-2/F15 SSM/I',
    'DMSP 5D-2/F8 SSM/I',
    'DMSP 5D-3/F15 SSM/I',
    'DMSP 5D-3/F16 SSM/I',
    'DMSP 5D-3/F16 SSMIS',
    'DMSP 5D-3/F17 SSM/I',
    'DMSP 5D-3/F17 SSMIS',
    'DMSP 5D-3/F18 SSM/I',
    'DMSP 5D-3/F18 SSMIS',
    'DMSP 5D-3/F19 SSM/I',
    'DMSP 5D-3/F19 SSMIS',
    'DMSP SSM/I',
    'DMSP SSMIS',
    'EP-TOMS SEAWIFS',
    'EP-TOMS TOMS',
    'ERBS SAGE II',
    'GCOM-W1 AMSR2',
    'GMS INFRARED RADIOMETERS',
    'GMS VISSR-GMS',
    'GMS WVSS',
    'GOES AVHRR',
    'GOES GOES I-M Imager',
    'GOES GOES I-M SOUNDER',
    'GOES GOES-15 Imager',
    'GOES GOES-16 Imager',
    'GOES INFRARED RADIOMETERS',
    'GOSAT TANSO-FTS',
    'GPM DPR',
    'GPM GMI',
    'Himawari-8 AHI',
    'ISS OCO-3',
    'J-31 CAR',
    'METEOROLOGICAL STATIONS RAIN GAUGES',
    'METEOSAT INFRARED RADIOMETERS',
    'METEOSAT SEVIRI',
    'METEOSAT VISSR-METEOSAT',
    'METOP-A MHS',
    'METOP-B MHS',
    'METOP-C MHS',
    'MT1 SAPHIR',
    'MTSAT MTSAT 1R Imager',
    'MTSAT MTSAT 2 Imager',
    'MTSAT-1R INFRARED RADIOMETERS',
    'MTSAT-2 INFRARED RADIOMETERS',
    'Meteor-3 TOMS',
    'Meteor-3M SAGE III',
    'Models/Analyses BLING',
    'Models/Analyses CASA-GFED3-V2',
    'Models/Analyses CASA-GFED3-V3',
    'Models/Analyses CLM-LSM',
    'Models/Analyses CMS-Flux-V1',
    'Models/Analyses Catchment-LSM',
    'Models/Analyses ECCO2_Darwin-V3',
    'Models/Analyses Environmental Modeling',
    'Models/Analyses FFDAS-V2',
    'Models/Analyses Forcing-LSM',
    'Models/Analyses GDAS',
    'Models/Analyses GEOS-5',
    'Models/Analyses GEOS-Chem',
    'Models/Analyses GLPM',
    'Models/Analyses IMERG',
    'Models/Analyses LANDMET',
    'Models/Analyses MERRA',
    'Models/Analyses MERRA-2',
    'Models/Analyses MITgcm',
    'Models/Analyses Merged IR',
    'Models/Analyses Mosaic-LSM',
    'Models/Analyses NCEP-CFSV2',
    'Models/Analyses NCEP-GFS',
    'Models/Analyses NOBM',
    'Models/Analyses Noah-LSM',
    'Models/Analyses OBSERVATION BASED',
    'Models/Analyses Penman-Monteith',
    'Models/Analyses RM-OBS/PU',
    'Models/Analyses TMPA',
    'Models/Analyses Unified Model UM',
    'Models/Analyses VIC-LSM',
    'NASA P-3 CAR',
    'NOAA POES HIRS',
    'NOAA POES TOVS',
    'NOAA-10 HIRS/2',
    'NOAA-10 MSU',
    'NOAA-10 TOVS',
    'NOAA-11 HIRS/2',
    'NOAA-11 MSU',
    'NOAA-11 SBUV/2',
    'NOAA-11 TOVS',
    'NOAA-12 HIRS/2',
    'NOAA-12 MSU',
    'NOAA-12 TOVS',
    'NOAA-14 HIRS/2',
    'NOAA-14 MSU',
    'NOAA-14 SBUV/2',
    'NOAA-14 TOVS',
    'NOAA-15 AMSU-B',
    'NOAA-16 AMSU-B',
    'NOAA-16 SBUV/2',
    'NOAA-17 AMSU-B',
    'NOAA-17 SBUV/2',
    'NOAA-18 MHS',
    'NOAA-18 SBUV/2',
    'NOAA-19 MHS',
    'NOAA-19 SBUV/2',
    'NOAA-19 TOMS',
    'NOAA-20 ATMS',
    'NOAA-20 CrIS',
    'NOAA-20 VIIRS',
    'NOAA-6 HIRS/2',
    'NOAA-6 MSU',
    'NOAA-6 TOVS',
    'NOAA-7 HIRS/2',
    'NOAA-7 MSU',
    'NOAA-7 TOVS',
    'NOAA-8 HIRS/2',
    'NOAA-8 MSU',
    'NOAA-8 TOVS',
    'NOAA-9 HIRS/2',
    'NOAA-9 MSU',
    'NOAA-9 SBUV/2',
    'NOAA-9 TOVS',
    'NPOESS (National Polar-orbiting Operational Environmental Satellite System ) WINDSAT',
    'NRL P-3 CAR',
    'Nimbus-1 HRIR',
    'Nimbus-2 HRIR',
    'Nimbus-2 MRIR',
    'Nimbus-3 HRIR',
    'Nimbus-3 MRIR',
    'Nimbus-3 SIRS',
    'Nimbus-4 BUV',
    'Nimbus-4 IRIS',
    'Nimbus-4 SCR',
    'Nimbus-4 SIRS',
    'Nimbus-4 THIR',
    'Nimbus-5 ESMR',
    'Nimbus-5 ITPR',
    'Nimbus-5 NEMS',
    'Nimbus-5 SCR',
    'Nimbus-5 THIR',
    'Nimbus-6 HIRS',
    'Nimbus-6 LRIR',
    'Nimbus-6 PMR',
    'Nimbus-6 SCAMS',
    'Nimbus-6 THIR',
    'Nimbus-7 LIMS',
    'Nimbus-7 SAMS',
    'Nimbus-7 SBUV',
    'Nimbus-7 SMMR',
    'Nimbus-7 THIR',
    'Nimbus-7 TOMS',
    'OCO-2 OCO SPECTROMETERS',
    'OCO-2 OCO-2',
    'OrbView-2 SEAWIFS',
    'PARASOL POLDER-1',
    'SCISAT-1/ACE ACE-FTS',
    'SHIPS RAIN GAUGES',
    'SMS-1 VISSR',
    'SMS-2 VISSR',
    'SORCE SIM',
    'SORCE SOLSTICE',
    'SORCE TIM',
    'SORCE XPS',
    'STPSat-3 TIM',
    'STS-34 SSBUV',
    'STS-41 SSBUV',
    'STS-43 SSBUV',
    'STS-45 SSBUV',
    'STS-56 SSBUV',
    'STS-62 SSBUV',
    'STS-66 SSBUV',
    'STS-72 SSBUV',
    'SUOMI-NPP ATMS',
    'SUOMI-NPP CrIS',
    'SUOMI-NPP OMPS',
    'SUOMI-NPP VIIRS',
    'Sentinel-5P TROPOMI',
    'TIROS-4 Medium-Resolution Scanning Radiometer',
    'TIROS-7 Medium-Resolution Scanning Radiometer',
    'TIROS-N HIRS/2',
    'TIROS-N MSU',
    'TIROS-N TOVS',
    'TRMM PR',
    'TRMM TMI',
    'TRMM VIRS',
    'TSIS-1 SIM',
    'TSIS-1 TIM',
    'TSX RO',
    'Terra MODIS',
    'UARS CLAES',
    'UARS HALOE',
    'UARS HRDI',
    'UARS ISAMS',
    'UARS MLS',
    'UARS PEM',
    'UARS SOLSTICE',
    'UARS SUSIM',
    'UARS WINDII',
    'WEATHER STATIONS NEXRAD',
    'WEATHER STATIONS RAIN GAUGES',
}

print(unique_couples)
print(unique_models)

# couples = "aura mls"
# words = couples.split(" ")
# for vs in valid_sources:
#     # if 'aura' in vs.lower() and 'mls' in vs.lower():
#     if all([w in vs.lower() for w in words]):
#         print(vs)

# Code to generate a reviewable baseline dictionary to use for plat/ins couples. Manually removed a few afterward
edward_couples_to_source_couples = {}
for couple in unique_couples:
    words = ' '.join(couple.split('/', maxsplit=1))
    match_found = False
    for vs in valid_sources:
        temp = [w for w in words.split()]
        word_occurrences = [w in vs.lower() for w in words.split()]
        if all(word_occurrences):
            print(couple, vs)
            match_found = True
            edward_couples_to_source_couples[couple] = vs
    if not match_found:
        print(couple, "no match found")

with open('temp_plat_ins_mapping.json', 'w', encoding='utf-8') as f:
    json.dump(edward_couples_to_source_couples, f, indent=4)
# This was generated by copying and pasting the temp_mapping json file and removing a few couples that could potentially
# map to multiple items and adding obvious ones where the mapping failed (dmsp/ssm/i and oco-2/oco-w)
couples_to_source_couples = {
    "aura/mls": "Aura MLS",
    "sentinel-5p/tropomi": "Sentinel-5P TROPOMI",
    "gpm/gmi": "GPM GMI",
    "meteosat/seviri": "METEOSAT SEVIRI",
    "nimbus-7/smmr": "Nimbus-7 SMMR",
    "trmm/pr": "TRMM PR",
    "suomi-npp/cris": "SUOMI-NPP CrIS",
    "aqua/amsr-e": "Aqua AMSR-E",
    "aura/omi": "Aura OMI",
    "iss/oco-3": "ISS OCO-3",
    "terra/modis": "Terra MODIS",
    "meteorological stations/rain gauges": "METEOROLOGICAL STATIONS RAIN GAUGES",
    "trmm/tmi": "TRMM TMI",
    "gosat/tanso-fts": "GOSAT TANSO-FTS",
    "aqua/amsu-a": "Aqua AMSU-A",
    "gcom-w1/amsr2": "GCOM-W1 AMSR2",
    "dmsp/ssm/i": "DMSP SSM/I",
    "dmsp/ssmis": "DMSP SSMIS",
    "himawari-8/ahi": "Himawari-8 AHI",
    "aqua/modis": "Aqua MODIS",
    "trmm/virs": "TRMM VIRS",
    "aqua/airs": "Aqua AIRS",
    "gpm/dpr": "GPM DPR",
    "suomi-npp/viirs": "SUOMI-NPP VIIRS",
    "scisat-1/ace/ace-fts": "SCISAT-1/ACE ACE-FTS",
    "oco-2/oco-2": "OCO-2 OCO-2"
}

print()
print()
print()
print("DICTIONARY CREATION FOR MODELS")


# Code to generate a reviewable baseline dictionary to use for Models. Manually removed a few afterward
edward_models_to_source_couples = {}
for model in unique_models:
    words = 'models/analyses ' + model
    match_found = False
    for vs in valid_sources:
        temp = [w for w in words.split()]
        word_occurrences = [w in vs.lower() for w in words.split()]
        if all(word_occurrences):
            print(model, vs)
            match_found = True
            edward_models_to_source_couples[model] = vs
    if not match_found:
        print(model, "no match found")

with open('temp_model_mapping.json', 'w', encoding='utf-8') as f:
    json.dump(edward_models_to_source_couples, f, indent=4)
# This was generated by copying and pasting the temp_mapping json file and removing a few couples that could potentially
# map to multiple items and adding obvious ones where the mapping failed
models_to_source_models = {
    "observation based": "Models/Analyses OBSERVATION BASED",
    "environmental modeling": "Models/Analyses Environmental Modeling",
    "penman-monteith": "Models/Analyses Penman-Monteith",
    "tmpa": "Models/Analyses TMPA",
    "nobm": "Models/Analyses NOBM",
    "merra-2": "Models/Analyses MERRA-2",
    "gdas": "Models/Analyses GDAS",
    "imerg": "Models/Analyses IMERG",
    "merra": "Models/Analyses MERRA",
    "geos-5": "Models/Analyses GEOS-5",
    "geos-chem": "Models/Analyses GEOS-Chem"
}




'''
Questions to ask: granuality of dsmp/ssims. I get that as an exact quote
oco-2/oco-2 OCO-2 OCO SPECTROMETERS
oco-2/oco-2 OCO-2 OCO-2
'''
print()
print()
print()

count = 0
source_plat_ins_added_count = 0
source_models_added_count = 0
papers_tagged_with_source = 0
# use the mapping to print out the pdf_key and the source_couples
for pdf_key, feature in features_data.items():
    count += 1
    # if count == 3:
    #     break
    # print(pdf_key)
    zotero_key = pdf_key_to_zotero_key[pdf_key]

    summary_stats = feature['summary_stats']
    platform_ins_couples_raw = summary_stats['valid_couples']
    platform_ins_couples = list(set([re.sub(r'----level[\- ]\d', '', pic) for pic in platform_ins_couples_raw]))  # remove the level from the couple
    source_plat_ins_couples = [couples_to_source_couples[pic] for pic in platform_ins_couples]

    models_raw = summary_stats['models']
    models_no_duplicates = list(set(models_raw))
    source_models = [models_to_source_models[mod] for mod in models_no_duplicates]

    print(pdf_key, zotero_key, source_plat_ins_couples)
    print(pdf_key, zotero_key, source_models)

    for spic in source_plat_ins_couples:
        current_item = None
        current_item = zot.item(zotero_key)
        source_plat_ins_added_count += 1
        # tag(current_item, f'source:{spic}', zot)
        # time.sleep(1)


    for sm in source_models:
        current_item = None
        # time.sleep(2)
        current_item = zot.item(zotero_key)
        source_models_added_count += 1
        tag(current_item, f'source:{sm}', zot)

    if len(source_plat_ins_couples) > 0 or len(source_models) > 0:
        papers_tagged_with_source += 1

print("added plat/ins", source_plat_ins_added_count)
print("added models counts", source_models_added_count)
print("papers tagged with at least one source", papers_tagged_with_source)