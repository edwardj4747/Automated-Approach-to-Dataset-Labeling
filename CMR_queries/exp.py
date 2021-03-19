import re

# want to be able to keep the decimals but split the sentences based on '.' that are not included in decimals

sentences = [
    'mls satellite mipas satellite tes satellite omi satellite airs satellite gome-2 satellite limb limb nadir nadir nadir nadir absorption emission emission emission backscattered emission backscattered 3-4 3.5-5 6-96 mhz 0. cm1  80 000 cm1 ( 240 ghz) 685  cm1  6 0.1 cm1 250 cm1 3-5 0.420.63 nm 30 nm greater than  6 0.52 cm1 700 cm1 3-5  0.24 nm 35 nm instruments platform observation geometry observation mode vertical resolution (km) spectral resolution spectral domain ftir groundbased upward  9-15 0.009 cm1 400 cm1 and performance for the different channels are described by jarnot et al ()',
    'for example, the high horizontal resolution airs (airs) observations, with a 13.5-km nadir footprint and imaging capability, have deep vertical weighting functions that limit the detection of waves to those with vertical wavelengths longer than 12 km',
            'the uars mls vertical resolution is approximately 3-4 km throughout most of the stratosphere (pumphrey, )',
            'the sage ii data are retrieved on a 0.5 km grid from the surface to 50 km for wv and 0.5 to 70 km for o3. the sage sampling corresponds to a nyquist limited vertical resolution in transmission of 1 km ',
            'the haloe vertical resolution is 2.3 km for h2o and o3 (harries et al ; kley et al ) ',
             'the uars mls vertical resolution is approximately 3-4 km throughout most of the stratosphere (pumphrey, ) ']
for lowercase_sentence in sentences:
    print(lowercase_sentence)

    patterns = [r'(\d+(?:\.\d+)? ?(?:to|\-) ?\d+ k?m)', r'(\d+(?:\.\d)?[ \-]k?m)']  # 2 - 4 km, 2.3km
    patterns = [r'(\d+(?:\.\d+)? ?(?:to|\-) ?\d+ k?m(?!hz))', r'(\d+(?:\.\d)?[ \-]k?m(?!hz))']  # 2 - 4 km, 2.3km. For both not mhz
    for pattern in patterns:
        if len(re.findall(pattern, lowercase_sentence)) > 0:
            res = re.findall(pattern, lowercase_sentence)
            print(res)
            lowercase_sentence = re.sub(pattern, '', lowercase_sentence)
    # if len(re.findall(r'(\d+(?:\.\d+)? ?(?:to|\-) ?\d+ km)', lowercase_sentence)) > 0:  # 3 - 5 km
    #     res = re.findall(r'(\d+(?:\.\d+)? ?(?:to|\-) ?\d+ km)', lowercase_sentence)
    #
    #     print(res)
    # if len(re.findall(r'(\d\.?\d? km)', lowercase_sentence)) > 0:
    #     res = re.findall(r'(\d\.?\d? km)', lowercase_sentence)
    #     print(res)
    # print(res)

# print("****")
# lowercase_sentence = sentences[0]
# print(lowercase_sentence)
# res = re.findall(r'(\d+(?:\.\d+)? ?(?:to|\-) ?\d+ km)', lowercase_sentence)
# print(res)

