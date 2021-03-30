import re

s = "the nimbus-4 satellite using special sensor microwave imager ueah"
print(re.findall(r'nimbus(?: |\-)?4', s))
print(re.findall(r'special sensor microwave(?: |/)?imager', s))
