import json
import re

with open('../ml_data/dataset_authors_v2.json', encoding='utf-8') as f:
    dataset_authors = json.load(f)

all_names = set()
last_names = set()

# extract last names
for key, value in dataset_authors.items():
    for item in value:
        item = re.sub(r' {2,}', ' ', item)
        item = re.sub(r', ,', ',', item)
        item = re.sub(r',$', '', item)

        split = item.split(',')
        fn = split[0]
        ln = fn.split(' ')[-1]
        if ln == 'iii' or ln.endswith('.'):
            ln = fn.split(' ')[-2]

        print(fn, ":", ln)
        if ln == "":
            print("************")
            print(item)
        last_names.add(ln)

        # # author substitutions
        #
        #
        #
        # if len(re.findall(r'\.', item)) == 0:
        #     # standard case 'first last, ...?'
        #     for name in split:
        #         split = item.split(',')
        #         last_names.add(name)
        # else:
        #     print(item)

        # if re.findall(r'\w{2,}, \w\.,', item):
        #     print("Matches")
    # one name: joel susskind
    # multiple name: eric fetzer, brian wilson,  gerald manipon
    # many order reversed: erson, j., l. froidevaux, r. a. fuller, p. f. bernath, n. j. livesey, h. c. pumphrey,

print(all_names)
print(len(all_names))
print(last_names)
print(len(last_names))

last_names_list = list(sorted(last_names))
print(last_names_list)

with open('../../data/json/author_last_names.json', 'w', encoding='utf-8') as f:
    json.dump(last_names_list, f, indent=4)