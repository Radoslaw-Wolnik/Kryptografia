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


def interface(text, lenght):
    AZ = [chr(ord("A") + i) for i in range(26)]
    letters = [letter.upper() for letter in text if isAZaz(letter)]
    result_key = ["None", 0]
    key_len = lenght
    # generate list of lists where every list coresponds to possible solution to number % key_len
    sample = [[] for _ in range(key_len)]
    possible_letters = []
    for i in range(len(letters)):
        sample[i%key_len].append(letters[i])
    for i in range(len(sample)):
        # score = {letter : score}
        score = {k : 0 for k in AZ}
        for letter in AZ:
            # for every samlpe we try every letter as a key
            # and we check what are the highest scorring letters
            # 1st step decipher sample through letter
            decoded_sample = decode_vigenere("".join(sample[i]), letter)
            # 2nd step - score
            scored_number = rozklad_czestotliwosci_liter(decoded_sample)
            score[letter] = scored_number
        # find max score
        max_score = max(score.values())
        # add to possible letters all that scored same as max
        temp = [k for k, v in score.items() if v == max_score]
        possible_letters.append(temp)
    #< print(possible_letters)
    # change possible_letters to words
    res= [[letter] for letter in possible_letters[0]]
    #< print(res)
    for i in range(1, len(possible_letters)):
        temp = []
        for j in range(len(possible_letters[i])):
            for r in range(len(res)):
                temp.append(res[r] + [possible_letters[i][j]])
        res = temp
    words = []
    for i in range(len(res)):
        words.append("".join(res[i]))
    # and testing
    #< print(words)
    key_score = {k : 0 for k in words}
    for word_key in words:
        decipherd_text = decode_vigenere(text, word_key)
        decipherd_text = decipherd_text.upper()
        decipherd_text = "".join([letter for letter in decipherd_text if isAZaz(letter) or letter == " "])

        score_deciphered = rozklad_czestotliwosci_liter(decipherd_text)
        # score_deciphered max 12 min 0
        performance = int((score_deciphered / 12) * 100)

        if performance > result_key[1]:
            result_key[0] = word_key
            result_key[1] = performance

    return result_key


def interface_xor(text, lenght):
    AZ = [chr(ord("A") + i) for i in range(26)]
    letters = [letter.upper() for letter in text if isAZaz(letter)]
    result_key = ["None", 0]
    key_len = lenght
    # generate list of lists where every list coresponds to possible solution to number % key_len
    sample = [[] for _ in range(key_len)]
    possible_letters = []
    for i in range(len(letters)):
        sample[i%key_len].append(letters[i])
    for i in range(len(sample)):
        # score = {letter : score}
        score = {k : 0 for k in AZ}
        for letter in AZ:
            # for every samlpe we try every letter as a key
            # and we check what are the highest scorring letters
            # 1st step decipher sample through letter
            decoded_sample = decode_vigenere("".join(sample[i]), letter) # change here for xor ------------------------------
            # 2nd step - score
            scored_number = rozklad_czestotliwosci_liter(decoded_sample)
            score[letter] = scored_number
        # find max score
        max_score = max(score.values())
        # add to possible letters all that scored same as max
        temp = [k for k, v in score.items() if v == max_score]
        possible_letters.append(temp)
    #< print(possible_letters)
    # change possible_letters to words
    res= [[letter] for letter in possible_letters[0]]
    #< print(res)
    for i in range(1, len(possible_letters)):
        temp = []
        for j in range(len(possible_letters[i])):
            for r in range(len(res)):
                temp.append(res[r] + [possible_letters[i][j]])
        res = temp
    words = []
    for i in range(len(res)):
        words.append("".join(res[i]))
    # and testing
    #< print(words)
    key_score = {k : 0 for k in words}
    for word_key in words:
        decipherd_text = decode_vigenere(text, word_key) # change here for xor ------------------------------
        decipherd_text = decipherd_text.upper()
        decipherd_text = "".join([letter for letter in decipherd_text if isAZaz(letter) or letter == " "])

        score_deciphered = rozklad_czestotliwosci_liter(decipherd_text)
        # score_deciphered max 12 min 0
        performance = int((score_deciphered / 12) * 100)

        if performance > result_key[1]:
            result_key[0] = word_key
            result_key[1] = performance

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