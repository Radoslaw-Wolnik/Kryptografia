def isAZaz(letter):
    return (ord("A") <= ord(letter) <= ord("Z")) or (ord("a") <= ord(letter) <= ord("z"))

def rozklad_czestotliwosci_liter(text):
    most = ["E", "T", "A", "O", "I", "N"]
    least = ["V", "K", "J", "X", "Q", "Z"]
    text = text.upper()
    rozklad = dict([(chr(ord("A") + i), 0) for i in range (26)])
    for letter in text:
        if isAZaz(letter):
            rozklad[letter] += 1
    # we dont remove 0 values idk why
    # rozklad = {k: v for k, v in rozklad.items() if v != 0}
    # sort ascending
    sorted_rozklad = {k: v for k, v in sorted(rozklad.items(), key=lambda item: item[1])}
    # sorted descending
    # sorted_dict = {k: v for k, v in sorted(rozklad.items(), key=lambda item: item[1], reverse=True)}
    result = -1
    if len(rozklad.keys()) >= 12:
        result += 1 # or result = 0
        keys = list(sorted_rozklad.keys())
        for key in keys[0:6]:
            if key in least:
                result += 1
        for key in keys[-6::]:
            if key in most:
                result += 1
    return result


def decode_vigenere(text, K):
    base = 26  # how many letters A-Z
    # letters = [letter.isalpha() for letter in text] # map text : 1 - is letter; 0 - is not
    letters = [isAZaz(letter) for letter in text]
    upper = [letter.isupper() if letters[idx] else -1 for idx, letter in enumerate(text)] # map text: 1: isUpper; 0 isLower; -1 not isAlpha()
    # text = text.upper() insted line below
    text = "".join([letter.upper() if isAZaz(letter) else letter for letter in text])
    K = K.upper()
    res = []
    not_alpha = 0

    for i in range(len(text)):
        if letters[i] == False:
            # print(letters[i], text[i])
            res.append(text[i])
            not_alpha += 1
            continue

        move = ord(K[(i - not_alpha)%len(K)]) - ord("A")
        # print(K[i%len(K)]) good
        temp = (ord(text[i]) - ord("A") - move )
        if temp < 0:
            temp+=base
        temp = temp % base
        temp = chr(temp + ord("A"))

        if upper[i] == 0:
            temp = temp.lower()
        # print(i, temp)
        res.append(temp)

    return "".join(res)


def interface_xor(self, text, length):
    # important!
    # in this case we change text to decimal and instead text we always use a list of decimal numbers
    # remember tihis is chnaged version of interface_veginere to accomodate xor
    all = [i for i in range(256)]  # here we can change all characters that we consider that can be used as a key
    # letters = [letter.upper() for letter in text if self.isAZaz(letter)]
    characters = self.text_to_deci(text)
    result_key = ["None", 0]
    multiple = []  # in case multiple word_key have a score of 100
    key_len = length
    # generate list of lists where every list corresponds to possible solution to number % key_len
    sample = [[] for _ in range(key_len)]
    possible_letters = []
    for i in range(len(characters)):
        sample[i % key_len].append(characters[i])
    for i in range(len(sample)):
        # score = {letter : score}
        score = {k: 0 for k in all}
        for character in all:
            # for every sample we try every character as a key
            # and we check what are the highest scoring chcaracters
            # 1st step decipher sample through letter
            xored_sample = self.xor_two_decimal_lists(sample[i], [character for _ in range(len(sample[i]))])
            # 2nd step - score
            # < print(xored_sample)
            decoded_sample = self.decimal_to_str(xored_sample)
            # < print(decoded_sample)
            scored_number = -1
            # check if all characters are actually readable (not hexadecimal eg. "/xd5")
            if sum([1 if len(letter) == 1 else 0 for letter in decoded_sample]) == len(sample[i]):
                scored_number = self.rozklad_czestotliwosci_liter("".join(decoded_sample))
            score[character] = scored_number
        # find max score
        max_score = max(score.values())
        # add to possible letters all that scored same as max
        temp = [k for k, v in score.items() if v == max_score]
        possible_letters.append(temp)
    # < print(possible_letters)
    # change possible_letters to words
    res = [[number] for number in possible_letters[0]]
    # < print(res)
    for i in range(1, len(possible_letters)):
        temp = []
        for j in range(len(possible_letters[i])):
            for r in range(len(res)):
                temp.append(res[r] + [possible_letters[i][j]])
        res = temp
    words = []  # that will be a list of lists of decimal numbers
    # containing all possible combinations that scored best
    for i in range(len(res)):
        # words.append("".join(res[i]))
        words.append(res[i])
    # and testing to find the best one
    # < print(words)
    key_score = {"".join(self.decimal_to_str(k)): 0 for k in words}
    for word_key in words:
        deciphered_text = self.xor_two_decimal_lists(characters, word_key + word_key)
        score_deciphered = sum([self.isAZaz(chr(number)) for number in deciphered_text])
        performance = int((score_deciphered / len(characters)) * 100)

        if performance > result_key[1]:
            result_key[0] = "".join(self.decimal_to_str(word_key))
            result_key[1] = performance

        if performance == 100:
            # we could check if both of them are words using the dictionary
            word1 = "".join([chr(number) for number in deciphered_text[:length]])
            word2 = "".join([chr(number) for number in deciphered_text[length:]])
            # both = "".join([ chr(number) for number in deciphered_text ])
            # < print(word1, word2, both)
            if word1 in self.english_dictionary or word2 in self.english_dictionary:
                multiple.append(self.decimal_to_str(word_key))
            # or we can do analiza_czestotliwości and return highest scoring
            # but for that we would require longer texts

    if len(multiple) > 0:
        return multiple, 100
    return result_key

# interface("")
ans1 = "Im trying to guess the secret key to decrypt a message using Python I know the messages is going toy being something"
cod1 = "Bt teigba ac cwefa twt dcvyii kvr ps nrqnrdw i rjwjetx jszgy Ddmosp G zusn bze btjgaila af uhnbu edp psnry hsomtstlo"
cod1spaceless = "BtteigbaaccwefatwtdcvyiikvrpsnrqnrdwirjwjetxjszgyDdmospGzusnbzebtjgailaafuhnbuedppsnryhsomtstlo"
ans2 = "and parts of the messages There are few ways from here the most simple is because we know  generic case when the plain"
cod2 = "tud ckphm vt pje zmshprcl Altrv tni prk stmv nwtq yiex ihv fggy lpqrjt pw smuajhv ke muwo  tsgjfwn rrgs blwc xjm pwlgv"
cod2spaceless = "tudckphmvtpjezmshprclAltrvtniprkstmvnwtqyiexihvfggylpqrjtpwsmuajhvkemuwotsgjfwnrrgsblwcxjmpwlgv"
keyy = "ThankyouhowcanIapplythepartweknowtodifferentpartsofthecypherisapproachisnotfoolproofespeciallyi"

# print(len([letter for letter in ans1 if letter != " "]))
# print(len(keyy))

new_1 = "Btteigbaac"
new_2 = "tudckphmvt"
new_ans1 = "Imtryingto"
new_ans2 = "andpartsof"
possible_key, rozklad = interface(new_1 + new_2, 10)
# print(interface(cod1spaceless[:10] + cod2spaceless[:10]))
print(new_1)
print(new_2)

print(decode_vigenere(new_1, possible_key))
print(new_ans1)
print(decode_vigenere(new_2, possible_key))
print(new_ans2)
### It's stupid, it doesnt work and it should never work there is no logic behind this and why the hell are we doing it in such incorrect way
print(interface("qwzv" + "ssui ", 4))
print(interface("rcgwpv" + "hibppp ", 6))
print(decode_vigenere("qwzv", "qogi"))
print(decode_vigenere("ssui", "qogi"))