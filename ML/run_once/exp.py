import re

creator = "an goddard earth sciences data, information services center".lower()
creator = re.sub(r'airs science team \(joel susskind, nasa/gsfc\)', 'joel susskind', creator)

nu = "goddard earth sciences data, information services center"

creator = re.sub(rf'{nu},?', '', creator)
print(creator)

s= "UW-Madison Space Science and Engineering Center: Hank Revercomb; UMBC Atmospheric Spectroscopy Laboratory: Larrabee Strow"
print(s.lower())