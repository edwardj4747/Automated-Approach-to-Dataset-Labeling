1. put all pdfs into z_pdfs_to_convert
2. run convert_all_possible_pdfs.py (create .cermzones files for all pdfs that can be converted -> successful_cermfiles)
3. run cermzone_to_txt.py to create the text files (will output .txt files to 'text' folder)
4. extract_relevant_sections.py to extract only the relevant sections (ie: get rid of the introduction)

failed_conversions -> pdfs that could not be converted for some reason
successful_cermfiles -> .cermzone files
successful_conversions -> pdf documents that were successfully converted
text -> resulting .txt files form the .cermzone files in successful_cermfiles
z_pdfs_to_convert -> all pdfs at the beginning