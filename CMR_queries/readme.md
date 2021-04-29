This is where the **Feature Extraction** happens.

This is the directory which contains all the features for running CMR queries. In the process of running CMR queries,
sentences with keywords will also be extracted from the text.

The sub directories have the following uses
* `cmr_results`: store the results for labelled sentences and the actual datasets returned from CMR queries
* `experiments`:some things I was playing around with. You can feel free to
ignore these.
* `keyword_optimization`: some experiments to improve the keywords that are searched. Some experiments included using regex keywords. 
This did not seem to improve performance much. These files can mostly be ignored
* `stats_and_csv`: storing computed results (correct, missed, extraneous) for CMR queries as well as exported **csv** files
including the papers along with the found couples and models

How to use
1. In `automatically_label.py`, at the top of the main method, fill in the parameters for 
    * preprocessed_directory -> the location of the preprocessed text files
    * pubs_with_attchs_location -> Extracted info from Zotero (Created by Irina)
    * zot_notes_location -> Extracted info from Zotero (Created by Irina)
    * dataset_couples_location -> mapping from dataset_short_name: [platform/instrument couples]
    * keyword_file_location -> the keywords to look for
        * ```
          # Example from keywords.json
            "missions": {
                "short_to_long": {},
                "long_to_short": {},
            } ... (see data/json/keywords.json)
          ```
    * mission_instrument_couples -> mapping from platform: [instruments]
    * output_title -> the name of the file you want to output
2. Run `automatically_label.py`
    * This will output three files
        * HH-MM-SS_{output_title}_key_title_ground_truths.json
            * Result will be a dictionary of form 
            ```
          zotero_key: {
                "key": zotero_key,
                "pdf": the name of the pdf file key (ie: YCIZDRA2),
                "title": the title of the pdf (ie: 2020_Filonchyk_Impact Assessment of COVID-19 on Variations of SO2, NO2, CO and AOD over East.pdf),
                "manually_reviewed": [ list of manually_reviewed datasets ]
          }
            ```
          * Only papers for which there are manually reviewed datasets will be included in this file
        * HH-MM-SS_{output_title}_features.json
            * a dictionary of form
            ```
            pdf_key: {
                "summary_stats": {},  # includes valid couples, single missions, models, instruments, and species
                "cmr_results": {},  # results for CMR queries using CMR parameters (science_keyword_search) and just a free text search (keyword search)
                "sentences": []  # all the labelled sentences with keywords extracted and labeled
          }
          ```
          * Note: they key of this is based on the **PDF** key
        * HH-MM-SS_{output_title}_features_merged.json
            * Combines the results of key_title_ground_truths and features 
            for the papers which were manually reviewed
            * ```
              zotero_key: {
                    "key": zotero_key,
                    "pdf": the name of the pdf file key (ie: YCIZDRA2),
                    "title": the title of the pdf (ie: 2020_Filonchyk_Impact Assessment of COVID-19 on Variations of SO2, NO2, CO and AOD over East.pdf),
                    "man
                    "summary_stats": {},  # includes valid couples, single missions, models, instruments, and species
                    "cmr_results": {},  # results for CMR queries using CMR parameters (science_keyword_search) and just a free text search (keyword search)
                    "sentences": []  # all the labelled sentences with keywords extracted and labeled
                }
              ```

3. To create a CSV output file with papers, platform/instrument couples, models, and stats on dataset accuracy,
    * In `cme_stats.py` fill in the file locations for features, key_title_ground_truths you wnat to evaluate on
    * fill in the type of search. SCIENCE_KEYWORD is based on using the detailed CMR query parameters; 
    KEYWORD is based off the free text search; and BOTH merges the results from both together
    * fill in the initial and max value for `n`. This will look at the top-n datasets 
    returned from CMR. Ie: a range of n=1, max_n=3 would make three evaluations using the 
    top dataset, the top two datasets, and the top 3 datasets
    * run `cme_stats.py`
    

`automatically_label.py` also calls the methods in all the files that have '_utility(ies)' in their name (directly and indirectly)
    

-----------------------------------------------

        
    
This contains the summary stats, the extracted sentences, and the results of querying CMR.

For each instrument/platform pair and each possible science keyword, I ran those parameters through
the CMR Earth Data Search API and took the first dataset.

To achieve this, run `automatically_label.py`

`version1`: Aura MLS all possible combinations of platform/instrument couples and species + instrument/species   
`version2`: Aura MLS only platform/instrument couples + instrument/species in the same sentence

The following files are included
* `Aura_mls.csv` - csv with pdf name, title, mission/instrument pairs, models, manually reviewed datasets, Top CMR predictions
* `HH-MM-SSfeatures.json` - the extracted sentences, summary stats, and queries for each paper
* `HH-MM-SSfeatures_merged.json` - combined `HH-MM-SSfeatures.json` with metadata from zotero and manually reviewed datasets if applicable
* `HH-MM-SSkey_title_ground_truth.json` - information from zotero including zotero key, paper title, pdf name, and manually reviewed dataset if applicable

```buildoutcfg
For each sentence:
        Extract instruments, platforms or models (either GES DISC or not) record them as matching instrument/platform pair if possible, otherwise as single features.
        Extract science keywords, and record them.
    For each instrument/platform pair:
        For each science keyword:
            Query CMR and record first returned dataset
    For reminder of instruments
        For each science keyword:
            Query CMR and record first returned dataset
```

I made two queries to CMR for each possibility of platform/instrument and science keyword. The first query took
advantage of the `platform`, `instrument`, and `science_keyword` fields while the second query used only the `keyword`
field. The second query was analagous to typing into the search bar, while the first query corresponds to choosing a
platform and instrument from the list on the options on the Earth Datasearch Website.
```buildoutcfg
query1: base_cmr +  f'&platform={platform}&options[platform][ignore-case]=true'
            &instrument={instrument}&options[instrument][ignore-case]=true'
            science_keyword = convert_science_keyword(science_keyword)
            f'&science_keywords[0][variable-level-1]=*{science_keyword}*' \
                                f'&science_keywords[1][variable-level-2]=*{science_keyword}*' \
                                f'&science_keywords[2][variable-level-3]=*{science_keyword}*' \
                                f'&science_keywords[3][detailed-variable]=*{science_keyword}*' \
                                f'&options[science_keywords][pattern]=true&options[science_keywords][or]=true' \
                                f'&options[science_keywords][ignore-case]=true'

query2: base_cmr + f'&keyword={platform if platform else ""}%20{instrument}%20{science_keyword}'
```

Note: to use the CMR search api most effectively, some of the extracted science keywords had to be
converted back to their CMR form. For example, I extracted o3, but CMR only recognizes Ozone. For many of the extracted
science keywords this was easy, but there were a few exceptions.For example, 'temperature' is not a CMR keyword 
while 'atmospheric temperature', 'temperature trends', ...etc are. To remedy this, a wild card pattern was used in the CMR
science keyword search, so that anything could come before or after the science keyword. ie: for 'temperature' both 
'atmospheric temperature' and 'temperature trends' would be found using the wildcard.  

Added. For all science keywords with count >1