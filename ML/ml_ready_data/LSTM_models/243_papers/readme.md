This was the first draft at creating data for LSTM models. Note this was done with my local keys. This data was entered in a model of architecture:   
Embedding -> Dropout -> LSTM -> Droupout -> Dense Output
* KEYWORD_sentences.json
    * A dictionary of paper: { "ground_truths":[], "keyword_sentences":[] }
* Feb24_int_encoded_miv_plus_version
    * Papers represented as integer encoded representation of their keywords (mission, instrument, science keyword, version)
    * ie: the paper started as o3 o3 o3 o3 aura mls o3...mls o3 h2o and is now represented as [1, 1, 1, 1, 2, 3, ...]
* Feb24_ML2xx_num_datasets_9_papers_243.npy
    * a (243, 9) numpy array with each row representing a paper (ignored papers with no keyword sentences)
* Feb24_9_dataset_mapping_threshold_10_243_papers.json
    * a dictionary mapping a dataset to a column number. ie, ML2H2O: 0