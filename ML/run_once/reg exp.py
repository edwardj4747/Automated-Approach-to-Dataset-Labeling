import re

my_list = ['I at version ', 'I like cat', 'version version', 'dog']
new_list = []

for s in my_list:
    if len(re.findall('[vV]ersion', s)) > 0:
        new_list.append(s)

print(new_list)