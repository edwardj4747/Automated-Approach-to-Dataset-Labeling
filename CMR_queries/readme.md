This contains the summary stats, the extracted sentences, and the results of querying CMR.

For each instrument/platform pair and each possible science keyword, I ran those parameters through
the CMR Earth Data Search API and took the first dataset.

To achieve this, run `automatically_label.py`

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
~~To remedy this, 'temperature' was treated just as a
keyword and not a science keyword. ie the query was similar to query1 but did not include a `science keyword` search
term. The other example of this was with 'ice water content' which was treated the same way as temperature.~~

Added. For all science keywords with count >1