import re

# sentence = "(aura blah num) stuff/"
#
# new_sentence = ""
# for word in sentence.split(" "):
#     # strip the punctuation
#     word = re.sub(r'\(', '', word)
#     print(word)

s = "I ate v2.3 pieces of cake"
print(s.split(" "))

import re
word = 'v2/3'

word = re.sub(r'v(\d)/(\d)', '(v\\1 v\\2)', word)

print(word)

sentence = ' aura mls (v2 v2) o3'
new_sentence = ""
for word in sentence.split(" "):
    # strip the punctuation
    word = re.sub(r'[\(\)\-<>%=/]', '', word)
    # print(word)
    if word != 'no' and (
            re.fullmatch(r'v\d\.?\d?', word) or re.fullmatch(r'L\d', word)):
        new_sentence += word + " "

print(new_sentence)