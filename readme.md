This is my work for the Spring 2021 Internship at NASA Goddard Space 
Flight Center on the 'Automated Approach to Labelling Datasets in
Earth Science Publications' project. This readme serves as an overall guide to what 
is included in this repository. Each of the directories in this repository 
also contains a detailed readme with instructions on what the code files are present 
and how to use them.

I want to
* Convert PDFs into Text Files
    * This is done using the [Cermine package](https://github.com/CeON/CERMINE).
    You will need to download the [jar file](http://maven.ceon.pl/artifactory/webapp/#/artifacts/browse/simple/General/kdd-releases/pl/edu/icm/cermine/cermine-impl)
    to run the code.
    * Once you have the jar file downloaded the command to run cermine is. Note 
    that Cermine supports various output types (jats, text, zones, ...) 
    but for our use case for filtering out specific sections like the 
    introduction that are likely to contain a lot of noise, zones is the 
    most useful 
        ```
        java -cp cermine-impl-1.13-jar-with-dependencies.jar pl.edu.icm.cermine.ContentExtractor -path z_pdfs_to_convert -outputs zones
        ```

    * Cermine will be able to convert most 
    of the pdfs into .cermfiles with an xml like structure. Some of the tags 
    are  
        ```
        <zone label="BODY_HEADING">...</zone>
        <zone label="BODY_CONTENT">...</zone>
      ```
   * Using these tags, we can filter out sections like the introduction and 
  and references
  * However, not all the PDF files will be able to be converted because they
  may have characters that Cermine doesn't recognize. When this happens 
  Cermine will throw an error and stop processing other pdfs
    * The work around for this is to put the cermine command in a loop and 
    monitor write its output into text files. When it errors out, we can 
    simply read the output logs to see which files is successfully converted 
    (and move those into a directory) and which file it failed on (and 
    move that into a separate directory)
  * All of the code to do this is in the `convert_using_cermoznes` directory. 
  That folder also contains a detailed readme with how to use those code files

* Run Earth Datasearch CMR queries on the journal articles
    * The basic premise of this idea is as follows. Loop through the 
    sentences in the paper and extract the features from the sentence 
    (features may include some of: mission, instrument, models, 
    science keyword, author, level, version, spatial resolution, and temporal 
    resolution). For each valid platform/instrument couple (ie: Aura/MLS 
    is a valid couple but Aura/Buv is not) and science keyword that appears 
    in the paper, query [CMR API](https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html) 
    and get the datasets that are most returned, including additional 
    features when they are available. For all the papers that have been 
    manually reviewed, compare the results of CMR with those to see how 
    well it performs
    * All of the code to do this is in the `CMR_Queries` directory along
    with a readme file with detailed instructions on how to use the code 
    files
    
* Create some sort of dataset mapping (ie: dataset short name -> platform/
instrument couples)
    * The mapping you are looking for likely exists in `data/json/`
    * However, if the mapping does not exist and you would like to create 
    your own, the code in `run_once/create_mission_instrument_couples.py` 
    likely provides a good starting point for interacting with dataset metadata 
    that can quickly and easily be modified to meet a certain use case
    
* Interact with Zotero
    * All of the papers that were manually reviewed have a note in Zotero 
    with the tag: 'category: application' and 'reviewed: igerasim'.
    * Zotero can be accessed using [Pyzotero](https://pyzotero.readthedocs.io/en/latest/) 
    which is a python wrapper.
    * The code in `ML/generate_ground_truths.py` can be used to extract the 
    ground truth values from the notes in Zotero. Note: you will have to fill 
    in the library_id, library_type, and api_key

* Run supervised Machine Learning Algorithms
    * There are two main directories that deal with this `ML` and `ML_notebooks`.
    * Inside of `ML/ml_models`, `tree_based_models.py` can be used to run 
    either decision trees or random forest models on the data.
        * Both the `X` and `Y` values are numpy arrays. A detailed description
        of the specifics of the `X` and `Y`  values can be found in `ML/ml_ready_data/`
        * Both `X` and `Y` values were created using a Google Colab Notebook 
        which is in the `ML_notebooks/` directory
        
    * All neural network and sequence models were run inside of Google Colab 
    and can be found in the `ML_notebooks directory/`
    
* Create csv files that can be used to populate a knowledge graph in AWS Neptune
    * This was not the primary focus of my project, but I did spend some time 
    exploring how to create data files that could easily be added into Neptune. 
   * A few sample files along with the code used to create them is in the the 
   `neptune` directory.