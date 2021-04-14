import re

text = 'https://disc.gsfc.nasa.gov/'
file_name = 'temp'
keyword = r'disc.gsfc.nasa.gov'

occurrences = re.findall(r'.{,70}\n?.{,70}' + keyword + '.{,70}\n?.{,70}', text)
if occurrences:
    print(occurrences, file_name)