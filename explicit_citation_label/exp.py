import re

# text = 'https://disc.gsfc.nasa.gov/'
# file_name = 'temp'
# keyword = r'disc.gsfc.nasa.gov'
#
# occurrences = re.findall(r'.{,70}\n?.{,70}' + keyword + '.{,70}\n?.{,70}', text)
# if occurrences:
#     print(occurrences, file_name)

text = '''
9. Hu man, G.J.; Adler, R.F.; Bolvin, D.T.; Nelkin, E.J. The TRMM Multi-satellite Precipitation Analysis (TMPA).
Chapter 1. In Satellite Rainfall Applications for Surface Hydrology; Springer: Dordrecht, The Netherlands, 2010;
pp. 3-22. [CrossRef]
10. Horishima, K. Rainfall observation from Tropical Rainfall Measuring Mission (TRMM) satellite. J. Vis. 1999,
2, 93-98.
'''
temp = re.split(r'\.( \[CrossRef\])', text)
print(temp)
splits = re.split(r'\. \[CrossRef\]\n(?=(\d{1,2}\.? )?\w+, \w)', text)  # ends citation with '.' Next line starts with LastName, First inital and ignore starting numbers ie: 7.
                # is not perfect.

for s in splits:
    print(s, '\n')

sent = 'I ate some food'
print(re.split(r'a(te)?', sent))

keyword = r'(?:disc\.gsfc\.nasa\.gov)|(?:GES[ -]?DISC)'
s = '''18. Amy McNally NASA; GSFC; HSL. FLDAS Noah Land Surface Model L4 Global Monthly 0.1 0.1 Degree (MERRA-2 and CHIRPS);
Goddard Earth Sciences Data and Information Services Center (GESDISC): Greenbelt, MD, USA, 2018. [CrossRef]'''

print(re.findall(keyword, s))