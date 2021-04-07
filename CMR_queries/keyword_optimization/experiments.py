import re

key = 'aircraft operated by university of washington convair-580'

new_key = re.sub(r'-', '(?: |\\-)?', key)  # '-' to '-' or space
new_key = re.sub(r'/', '(?: |/)?', new_key)  # '/' to '/' or space

print(new_key)

