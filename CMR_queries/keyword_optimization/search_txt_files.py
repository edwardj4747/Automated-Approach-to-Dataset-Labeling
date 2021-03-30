import glob
import re

txt_location = '../../convert_using_cermzones/aura-mls/preprocessed/'

keyword = '◦'

for file in glob.glob(txt_location + "*.txt"):

    with open(file, encoding='utf-8') as f:
        text = f.read().lower()

    occurrences = re.findall('.{,70}' + keyword + '.{,70}', text)
    if occurrences:
        file_key = file.split('\\')[-1]
        print(occurrences, file_key)