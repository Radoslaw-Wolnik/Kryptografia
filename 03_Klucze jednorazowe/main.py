from Kryptoanaliza import Kryptoanaliza
def xor(a, b):
    return a ^ b


def isAZaz(letter):
    return (ord("A") <= ord(letter) <= ord("Z")) or (ord("a") <= ord(letter) <= ord("z"))


def text_to_deci(text):
    special = {"n": "\n",
               "t": "\t",
               "'": "\\'",
               '"': '\"',
               "b": "\b",
               "r": "\r",
               "f": "\f",
               "v": "\v",
               "a": "\x07",
               }
    i = 0
    result = []
    while i < len(text):
        if ord(text[i]) == 92:
            if ord(text[i + 1]) == 120:
                hexa = text[i + 2:i + 4]
                deci = int(hexa, 16)
                result.append(deci)
                # print(f"hex: {hexa}; dec: {deci}")
                i += 3
            else:
                # print("special: ", text[i+1])
                temp = text[i + 1]
                if temp in special.keys():
                    deci = ord(special[temp])
                else:
                    print(f"special character not in specials: {temp}")
                    deci = ord("\\")  # chyba tego brakuje
                result.append(deci)
                i += 1
        else:
            result.append(ord(text[i]))
            # print("normal: ", text[i])
        i += 1
        # print(ord(el))
    return result


def xor_two_str(text, key):
    text = text_to_deci(text)
    key = text_to_deci(key)
    res = []
    if len(text) != len(key):
        print("diff len")
        print(text)
        print(key)
        return ([-8])
    for i in range(len(text)):
        temp = xor(text[i], key[i])
        res.append(temp)
    return res


def dec_to_str(text):
    res = []
    for number in text:
        if number < 32 or number > 126:
            hexa = hex(number)
            hexa = str(hexa)[2:]
            if len(hexa) == 1:
                hexa = "0" + hexa
            res.append("\\x" + hexa)
        else:
            res.append(chr(number))
    return res


def decode_vigenere(text, K):
    base = 26  # how many letters A-Z
    # letters = [letter.isalpha() for letter in text] # map text : 1 - is letter; 0 - is not
    letters = [isAZaz(letter) for letter in text]
    upper = [letter.isupper() if letters[idx] else -1 for idx, letter in
             enumerate(text)]  # map text: 1: isUpper; 0 isLower; -1 not isAlpha()
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

        move = ord(K[(i - not_alpha) % len(K)]) - ord("A")
        # print(K[i%len(K)]) good
        temp = (ord(text[i]) - ord("A") - move)
        if temp < 0:
            temp += base
        temp = temp % base
        temp = chr(temp + ord("A"))

        if upper[i] == 0:
            temp = temp.lower()
        # print(i, temp)
        res.append(temp)

    return "".join(res)


if __name__ == '__main__':
    print("Kryptoanaliza")
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
    # print(analise.interface_vigenere(cod1spaceless[:10] + cod2spaceless[:10]))
    print(new_1)
    print(new_2)

    # it doesnt fully work but it works a little
    analise = Kryptoanaliza()
    possible_key = analise.interface_veginere(new_1 + new_2, 10)
    print(f'possible key: {possible_key[0]} scored: {possible_key[1]}')
    print(decode_vigenere(new_1, possible_key[0]))
    print(new_ans1)
    print(decode_vigenere(new_2, possible_key[0]))
    print(new_ans2)
    print()

    # kryptoanaliza xor TESTING DATA
    xor_ansv_11 = "dad"
    xor_eg_11 = "\x0f\x14\x0c"
    xor_ansv_12 = "mom"
    xor_eg_12 = "\x06\x1a\x05"
    xor_key_10 = "kuh"

    xor_ansv_31 = "esta"
    xor_eg_31 = "\ny\x1bf"
    xor_ansv_32 = "agni"
    xor_eg_32 = "\x0em\x01n"
    xor_key_30 = "o\no\x07"

    K = ['P', 'TA', 'POE', 'PERI', 'MARCI', 'VOTESB']
    A = ['E', 'IC', 'SUB', 'MERR', 'BAUXI', 'IMMERS']
    cipheredA = ['\\x15', '\\x1d\\x02', '\\x03\\x1a\\x07', '\\x1d\\x00\\x00\\x1b', '\\x0f\\x00\\x07\\x1b\\x00', '\\x1f\\x02\\x19\\x00\\x01\\x11']
    B = ['A', 'CO', 'CHA', 'ASYM', 'MACRO', 'BUSBOY']
    cipheredB = ['\\x11', '\\x17\\x0e', '\\x13\\x07\\x04', '\\x11\\x16\\x0b\\x04', '\\x00\\x00\\x11\\x11\\x06', '\\x14\\x1a\\x07\\x07\\x1c\\x1b']

    Krand = ['\\xe7', '\\xf2\\x89', '\\x84\\x94_', '6~\\x8a\\x82', 'j\\x05\\x12Pz', '\\xb9\\xf0\\xf6\\x91\\xd5t']
    Arand = ['S', 'CH', 'SWE', 'LATC', 'DISAG', 'MALLAR']
    Brand = ['T', 'RO', 'SPH', 'PARO', 'EXTIN', 'KNAPPA']
    ArandCiphered = ['\\xb4', '\\xb1\\xc1', '\\xd7\\xc3\\x1a', 'z?\\xde\\xc1', '.LA\\x11=', '\\xf4\\xb1\\xba\\xdd\\x94&']
    BrandCiphered = ['\\xb3', '\\xa0\\xc6', '\\xd7\\xc4\\x17', 'f?\\xd8\\xcd', '/]F\\x194', '\\xf2\\xbe\\xb7\\xc1\\x855']
    # xored = xor_two_str(xor_ansv_11, xor_key_10)
    # result = dec_to_str(xored)
    # print("".join(result))
    xor_possible_key = analise.interface_xor(xor_eg_11 + xor_eg_12, 3)
    print(f'possible key: {xor_possible_key[0]} scored: {xor_possible_key[1]}')
    # print(xor_two_str(xor_eg_11, possible_key[0]))
    # print(xor_ansv_11)
    # print(decode_vigenere(xor_eg_12, possible_key[0]))
    # print(xor_ansv_12)
    print()

    # TESTING
    #for i in range(len(A)):
    #    xor_possible_key = analise.interface_xor(cipheredA[i] + cipheredB[i], len(A[i]))
    #    print(f'possible key: {xor_possible_key[0]} scored: {xor_possible_key[1]} in time: {xor_possible_key[2]}')

    print("Plotting")
    temp = analise.mierzenie_czas_dlugosc_klucza("x", 1, 7, False)
    print("Kryptoanaliza Xor zakończona klucze z słow")
    print(temp)
    analise.make_plot(temp,
                      "Kryptoanaliza czasu w zaleznosci od dlugosci klucza dla\n XOR z kluczami z słów",
                      "XOR_1_7_WordsKey")

    temp = analise.mierzenie_czas_dlugosc_klucza("v", 1, 7, False)
    print("Kryptoanaliza veginere zakończona klucze z słow")
    print(temp)
    analise.make_plot(temp,
                      "Kryptoanaliza czasu w zaleznosci od dlugosci klucza dla\n VEGINERE z kluczami z słów",
                      "VEGINERE_1_7_WordsKey")

    temp = analise.mierzenie_czas_dlugosc_klucza("x", 1, 7, True)
    print("Kryptoanaliza xor random=True zakonczona")
    print(temp)
    analise.make_plot(temp, "Kryptoanaliza czasu w zaleznosci od dlugosci klucza dla\n XOR z randomowo wygenerowanymi kluczami", "XOR_1_7_RandKey")

    temp = analise.mierzenie_czas_dlugosc_klucza("v", 1, 7, True)
    print("kryptoanaliza Veginere random true zakończona")
    print(temp)
    analise.make_plot(temp,
                      "Kryptoanaliza czasu w zaleznosci od dlugosci klucza dla\n VEGINERE z randomowo wygenerowanymi kluczami",
                      "VEGINERE_1_7_RandKey")


    print("\nStepik zadanie: ")
    print(analise.interface_veginere("qwzv" + "ssui ", 4))
    print(analise.interface_veginere("rcgwpv" + "hibppp", 6))
    print(decode_vigenere("qwzv", "qogi"))
    print(decode_vigenere("ssui", "qogi"))
    print(decode_vigenere("rcgwpv", "DUNWBC"))
    print(decode_vigenere("hibppp", "DUNWBC"))
