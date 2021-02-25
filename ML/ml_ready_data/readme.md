# ML Data Explanations

There are three main types of input (only one is used at a time)
* **One Hot Counts**
	* 'I like to eat cake and I like to eat cookies" 
	* {'i': 1, 'like': 2, 'to': 3, 'eat': 4, 'cake': 5, 'and': 6, 'cookies': 7}
	* [0. 2. 2. 2. 2. 1. 1. 1.]
* **TF-IDF**
* **Doc2Vec**

There are two types of sentences
* **Strict** (contains all of mission, instrument, and science keyword) - 160 papers with at least one strict sentence
* **Broad** (contains two of mission, instrument, and science keyword) - 234 papers with at least one broad sentence

There are two main types of outputs
* **Thresholded Dataset**s (all ML2xx datasets which occurred more than 10 times in the ground truths) - 9 Datasets
	* Nine dimensional vectors with a 1 representing a dataset that appears and a 0 representing those that do not
	* ie: [1, 1, 0, 0, 0, 0, 0, 0, 1] corresponds to a ground_truth of [ML2HCL, ML2H2O, ML2CO] as determine by looking at 9_dataset_mapping_threshold_10.json file
* **Non-thresholded Datasets** (all ML2xx datasets) - 23 datasets
	* 23 dimensional vectors 

There are two utility dataset mapping files
* **9_dataset_mapping_threshold_10.json** (used with Thresholded Datasets)
* **23_dataset_mapping.json** (used with Non-thresholded datasets)
