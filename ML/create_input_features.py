# generate a dictionary of form: 'pdf_key': detected_tags: [], sentences:[], counts:[], prior: []
# @todo: why are there only 260 items instead of all 287 reviewed by Irina
import json
import sentences_broad
import pprint
from sentences_broad import RunningMode, SentenceMode


def read_json_file(file_name):
    with open('ml_data/' + file_name + ".json", encoding='utf-8') as f:
        return json.load(f)


def read_text_file(file_key):
    preprocessed_directory = '../convert_using_cermzones/preprocessed/'
    document = preprocessed_directory + file_key + '.txt'
    with open(document, encoding='utf-8') as f:
        txt = f.read()
    return txt


def display_heading(key, key_title_mapping):
    print(key, ": ", key_title_mapping[key])


if __name__ == '__main__':
    key_to_title = read_json_file('key_to_title')

    manually_reviewed_pdfs = read_json_file('ground_truths').keys()
    paper = list(manually_reviewed_pdfs)[0]  # 4MFNKR4V A clear-sky radiation closure study using a one-dimens (Dolinar)
    display_heading(paper, key_to_title)

    # get the text for the document
    document_text = read_text_file(paper)

    # get the sentences
    input_features = {}

    data = sentences_broad.create_sentences_for_ML(document_text)
    mission_statistics, instrument_statistics, variable_statistics, mission_instrument_statistics, mis_ins_var \
        = sentences_broad.compute_summary_statistics_basic(data)

    print(mission_statistics)
    print(instrument_statistics)
    print(variable_statistics)
    print(mission_instrument_statistics)
    print(mis_ins_var)

    unique_mission_instrument_pairs = []
    for key in mission_instrument_statistics.keys():
        if key[0] == 'None' or key[0] == 'n/a' or key[1] == 'None' or key[1] == 'n/a':
            continue
        unique_mission_instrument_pairs.append(key)

    sentences = []
    for key, value in data.items():
        for item in value:
            sentences.append(item['sentence'])

    print(unique_mission_instrument_pairs)
    print(len(sentences))

    input_features[paper] = {
        'unique_mission_instrument': unique_mission_instrument_pairs,
        'mis_ins_stat': mission_instrument_statistics,
        'mis_ins_var_stat': mis_ins_var,
        'var_stats': variable_statistics,
        'sentences': sentences
    }


    print()
    print()
    print()
    print(input_features)

    '''
    {'4MFNKR4V': {'unique_mission_instrument': [('aqua', 'modis'), ('aura', 'mls'), ('aqua', 'airs')], 'mis_ins_stat': {('merra-2', 'n/a'): 44, ('aqua', 'modis'): 2, ('aura', 'mls'): 2, ('None', 'mls'): 12, ('None', 'sage ii'): 1, ('aqua', 'airs'): 1, ('None', 'airs'): 4, ('merra', 'n/a'): 2}, 'mis_ins_var_stat': {('merra-2', 'n/a', 'n/a'): 44, ('aqua', 'modis', 'None'): 2, ('aura', 'mls', 'None'): 2, ('None', 'mls', 't'): 2, ('None', 'mls', 'o3'): 6, ('None', 'sage ii', 'o3'): 1, ('None', 'mls', 'h2o'): 4, ('aqua', 'airs', 'None'): 1, ('None', 'airs', 'o3'): 2, ('None', 'airs', 'h2o'): 1, ('None', 'airs', 't'): 1, ('merra', 'n/a', 'n/a'): 2}, 'var_stats': {'t': 3, 'o3': 9, 'h2o': 5}, 'sentences': ['In this study, temperature and water vapor profiles from Modern-Era Retrospective Analysis for Research and Applications version 2 , along with the climatic aerosol optical depths over the three ARM sites, are used as input to the radiative transfer model to calculate the clear-sky surface and TOA radiative fluxes', 'The first objective of this study is to evaluate the MERRA-2 clear-sky temperature and water vapor profiles using a newly generated atmospheric profile data set', 'Section 2 documents the groundand satellite-based data sets used in this study, as well as several of the notable updates in the recently released MERRA-2 reanalysis', 'Profiles of atmospheric temperature, water vapor mixing ratio, and ozone mixing ratio have been generated from ARM-merged sounding and satellite  retrievals over three ARM sites, which are used to evaluate the MERRA-2 profiles', 'MERRA-2 is horizontally discretized on a cubed sphere grid, which is superior to the latitude-longitude methods used in earlier versions', 'For MERRA-2 the number of assimilated observations per 6 h increment has increased from three million in 2010 to five million in 2015; however, capabilities of assimilating future satellite observations are also developed', 'MERRA-2 is available on a 0', 'One of the major improvements in MERRA-2 includes the minimization of abrupt variations in global interannual states  due to changes in observing system', 'In terms of the zonal temperature, MERRA-2 is within 1 K of its previous version', '6 K are seen in the tropics with MERRA-2 being slightly warmer', 'Differences in the vertical profiles are expected since the MERRA-2 profiles cannot be perfectly collocated with the satellite ground-based data', 'The blue line is from the closest MERRA-2 grid point, and the red line is the midlatitude climatological mean', 'the MERRA-2 grid box  and the point of the hybrid profile, the temperature profiles match very well  through the atmospheric column and their differences are nearly indistinguishable', 'Since stratospheric ozone is directly assimilated into MERRA-2, it is not surprising that the hybrid and MERRA-2 ozone profiles in Figure 2b match very well', 'On the other hand, MERRA-2 does not assimilate tropospheric ozone, which allows for differences of up to 200-400% for some cases', 'The midlatitude climate mean ozone mixing ratio is less than the hybrid and MERRA-2 profiles in the middle to upper stratosphere but is slightly larger in the upper troposphere and lower stratosphere', 'The hybrid and MERRA-2 water vapor mixing ratios match very well above ~850 hPa', 'However, below 850 hPa, the MERRA-2 water vapor profile diverges from the hybrid profile to the drier side by <0', 'On the global scale, a moist bias in MERRA-2 can be up to 75-150% in the upper troposphere  when compared to AIRS and MLS', 'The midlatitude climate mean water vapor mixing ratio is less than both the hybrid and MERRA-2 profiles in the lower troposphere', 'The MERRA-2 temperature profiles  for both the snow and snow-free cases at the ARM NSA site show an excellent agreement with the hybrid profiles through most of the troposphere and stratosphere', 'For the snow-free cases, the MERRA-2 temperature is slightly colder just below the stratopause  and warmer above 0', 'Nevertheless, MERRA-2 is able to reproduce the low-level temperature 13,704  4', 'A typical decrease in temperature is observed through the shallow troposphere at the NSA site for a snowcovered surface, whereas in the stratosphere, a rather isothermal temperature structure is seen in both the hybrid and MERRA-2 profiles', 'Similar to the ozone comparison at the SGP site, the MERRA-2 and hybrid profiles match very well through the whole column', 'For the snow cases, the water vapor mixing ratios are almost constant  through the entire troposphere, which is well replicated in MERRA-2', 'The climate mean water vapor mixing ratio is much too moist and almost twice as large as the hybrid and MERRA-2 values through the troposphere', 'Temperature  is well reproduced in MERRA-2 at the TWPC3 site through the troposphere; however, a slight discrepancy is seen just above the tropopause and below the stratopause, which could be an artifact of the coarser vertical resolution of MERRA-2', 'The tropical climate mean temperature agrees well with the hybrid and MERRA-2 profiles in the troposphere but is slightly warmer in the stratosphere and mesosphere', 'The TWPC3 ozone comparison is similar to the results at the ARM SGP and NSA sites, where the ozone profiles from MERRA-2 and the hybrid data set 13,705  2', 'Yet still, a noticeable discrepancy between the two data sets can be seen from ~10 to 20 hPa, where MERRA-2 is slightly smaller', 'Both the hybrid and MERRA-2 water vapor mixing ratios are much drier than the tropical climatological mean through the troposphere by <0', 'It is expected that the unrepresentativeness between the MERRA-2 grid box and the ARM point location may lead to their relatively large difference , especially since the TWPC3 site is located directly on the coast', 'The MERRA-2 atmospheric temperature profiles are nearly identical to the hybrid ones, and the climate mean temperature profiles agree with the hybrid ones within several kelvin', 'Since MLS ozone data are directly assimilated into MERRA-2, it is not surprising that the MERRA-2 and hybrid ozone profiles match extremely well at all three ARM sites', 'Most of the MERRA-2 water vapor mixing ratios agree well with the hybrid ones over three sites except for in the boundary layer at the ARM TWPC3', 'The Averaged Surface and TOA Radiative Fluxes  From ARM CERES Observations and Untuned Tuned RTM Calculations With Inputs From the Three Profile Types TOA SW_up TOA LW_up Surface SW_dn Surface LW_dn SGP Hybrid MERRA-2 Climate Observations NSA snow  Hybrid MERRA-2 Climate Observations NSA snow-free  Hybrid MERRA-2 Climate Observations TWPC3 Hybrid MERRA-2 Climate Observations Untuned Tuned Untuned Tuned Untuned Tuned Untuned Tuned 176', 'The 90% Confidence Intervals for the Average Tuned RTM-Calculated Fluxes  a TOA SW_up TOA LW_up Surface SW_dn SGP Hybrid MERRA-2 Climate NSA snow  Hybrid MERRA-2 Climate NSA snow-free  Hybrid MERRA-2 Climate TWPC3 Hybrid MERRA-2 Climate Interval          % 10', 'A bias of greater than 20 W m2 is found in the surface LW_dn flux using the hybrid and MERRA-2 profiles, a result that is inconsistent with Long and Turner  and is likely due to the skin temperature used in the RTM', 'This study focuses on the evaluation of MERRA-2 clear-sky vertical profiles of temperature, ozone mixing ratio, and water vapor mixing ratio at three ARM sites  from August 2004 to December 2013', 'Vertical profiles of temperature at the three sites are well replicated in MERRA-2 when compared to the newly generated satellite surface-based  data set', 'Finally, the MERRA-2 tropospheric water vapor mixing ratios are, on average, on the drier side of the combined satellite surfacebased data set at SGP and NSA for snow-free conditions', 'However, the relatively small and constant tropospheric water vapor profile at NSA for the snow cases is well replicated in MERRA-2', 'The averaged flux differences  using the hybrid and MERRA-2 profiles at three ARM sites are generally below 5 W m2, while the calculated fluxes from climate mean profiles are typically higher biased', 'The bottom plots of Figure 1 are clear-sky Aqua MODIS images for each site', 'The Aqua MODIS images show examples of clear-sky cases at each site', 'Microwave Limb Sounder Launched in 2004, the Aura satellite became the second member of the A-Train  array of satellites that observes the Earth in a Sun-synchronous, polar orbit ~15 times a day', 'Aura is equipped with the Microwave Limb Sounder  instrument , which is designed to make high-quality measurements of upper atmospheric temperature, water vapor, ozone, and an assortment of other climate sensitive atmospheric constituents', 'The retrieved MLS temperature used for this study is from version 4', 'The black line represents the hybrid profiles from the ARM-merged soundings  and the Microwave Limb Sounder  for atmospheric temperature and water vapor', 'Stratospheric ozone from MLS is retrieved at a frequency of 240 GHz, which offers the best precision for a wide vertical range', 'Intercomparison studies suggest that the ozone values from MLS match fairly well with multiinstrument means and Stratospheric Aerosol and Gas Experiment II values', 'The recommended range of the MLS ozone product is from 261 to 0', 'The MLS ozone product used for this study is also from version 4', 'The ozone profile  is from the Atmospheric Infrared Sounder  and MLS', 'Since MLS ozone is directly assimilated, the MERRA2 ozone mixing ratios are very close to the hybrid profiles at all three ARM sites', 'Intercomparison studies suggest that the ozone values from MLS match fairly well with multiinstrument means and Stratospheric Aerosol and Gas Experiment II values', 'MLS water vapor is retrieved at a frequency of 190 GHz with acceptable range of 316-0', 'The estimated uncertainty of MLS water vapor in the stratosphere is ~10%', 'In the upper troposphere the estimated MLS water vapor uncertainty is 20% in the tropics and midlatitudes and ~50% at high latitudes', 'The black line represents the hybrid profiles from the ARM-merged soundings  and the Microwave Limb Sounder  for atmospheric temperature and water vapor', 'AIRS is aboard on the Aqua satellite, which was launched in 2002 for the advancement and support of knowledge related to climate research and weather forecasting', 'Tropospheric profiles of temperature and water vapor are from the ARM-merged soundings , while ozone is from AIRS', 'The ozone profile  is from the Atmospheric Infrared Sounder  and MLS', 'Tropospheric profiles of temperature and water vapor are from the ARM-merged soundings , while ozone is from AIRS', 'Tropospheric profiles of temperature and water vapor are from the ARM-merged soundings , while ozone is from AIRS', 'A new version of MERRA has been released with several major improvements, making it the centerpiece of the evaluation performed in this study', 'This is in contrast to the one and a half million observations assimilated in MERRA from 2002 to the present']}}
    
    {'merra-2': 44, 'aqua': 3, 'aura': 2, 'merra': 2}
    {'modis': 2, 'mls': 14, 'sage ii': 1, 'airs': 5}
    {'t': 3, 'o3': 9, 'h2o': 5}
    {('merra-2', 'n/a'): 44, ('aqua', 'modis'): 2, ('aura', 'mls'): 2, ('None', 'mls'): 12, ('None', 'sage ii'): 1, ('aqua', 'airs'): 1, ('None', 'airs'): 4, ('merra', 'n/a'): 2}
    {('merra-2', 'n/a', 'n/a'): 44, ('aqua', 'modis', 'None'): 2, ('aura', 'mls', 'None'): 2, ('None', 'mls', 't'): 2, ('None', 'mls', 'o3'): 6, ('None', 'sage ii', 'o3'): 1, ('None', 'mls', 'h2o'): 4, ('aqua', 'airs', 'None'): 1, ('None', 'airs', 'o3'): 2, ('None', 'airs', 'h2o'): 1, ('None', 'airs', 't'): 1, ('merra', 'n/a', 'n/a'): 2}
    [('aqua', 'modis'), ('aura', 'mls'), ('aqua', 'airs')]
    68
    
    '''
'''
    ('aura/mls', 'h2o')[{
                            'sentence': ' in this study, we evaluate the modern-era retrospective analysis for research and applications version 2  reanalyzed clear-sky temperature and water vapor profiles with newly generated atmospheric profiles from department of energy atmospheric radiation measurement -merged soundings and aura microwave limb sounder retrievals at three arm sites',
                            'mission': 'aura', 'instrument': 'mls', 'variable': 'h2o', 'exception': False}, {
                            'sentence': ' mls water vapor is retrieved at a frequency of 190 ghz with acceptable range of 316–0',
                            'mission': 'aura', 'instrument': 'mls', 'variable': 'h2o', 'exception': False}, {
                            'sentence': ' the estimated uncertainty of mls water vapor in the stratosphere is ~10%',
                            'mission': 'aura', 'instrument': 'mls', 'variable': 'h2o', 'exception': False}, {
                            'sentence': ' the black line represents the hybrid profiles from the arm-merged soundings  and the microwave limb sounder  for atmospheric temperature and water vapor',
                            'mission': 'aura', 'instrument': 'mls', 'variable': 'h2o', 'exception': False}]
    ('aura/mls', 't')[{
                          'sentence': ' in this study, we evaluate the modern-era retrospective analysis for research and applications version 2  reanalyzed clear-sky temperature and water vapor profiles with newly generated atmospheric profiles from department of energy atmospheric radiation measurement -merged soundings and aura microwave limb sounder retrievals at three arm sites',
                          'mission': 'aura', 'instrument': 'mls', 'variable': 't', 'exception': False}, {
                          'sentence': ' the black line represents the hybrid profiles from the arm-merged soundings  and the microwave limb sounder  for atmospheric temperature and water vapor',
                          'mission': 'aura', 'instrument': 'mls', 'variable': 't', 'exception': False}]
    ('merra/mls', 'h2o')[{'sentence': ' in this study, we evaluate t
'''
