This is a working test to try to add in author names into the keyword sentences for the 359 papers.
This will then be fed into decision trees and random forests to see the results

* Mar3
    * tf-idf representation of most common 30 (out of 192) words found in the keyword sentences
    * 11 datasets - ML2xx datasets with more than 10 occurrences
    
 * Dataset Mappings
    * 11 - all ML2xx datasets with more than 10 occurrences
    * 17 - all datasets with more than 10 occurrences (includes OMTO3, OMTO3d, UARHL3AT...)
    * 13 - combined OMTO3 and OMTO3d and all 4 UARH datasets into one, leaving 13 total
    
    
   344author_keywords_attempt_d1_mn4_tr6_MERGED.json  
   replaces all occurrences of OMTO3d with OMTO3 and all UARH... with UARH