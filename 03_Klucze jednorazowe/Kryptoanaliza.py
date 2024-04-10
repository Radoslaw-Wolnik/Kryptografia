import requests
import random
import secrets
import time


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' took {end_time - start_time} seconds to execute.")
        return result

    return wrapper


class Kryptoanaliza:
    """Uses a fact that two ciphered texts by the same key resemble a vigenere ciphered text with two repeats of used key
    The correct way of solving it would be to use crib dragging or automation of crib dragging (via mapping all words in used language)"""

    def __init__(self):
        self.ciphered1 = None
        self.ciphered2 = None
        self.most_common_characters = ["E", "T", "A", "O", "I", "N"]
        self.least_common_characters = ["V", "K", "J", "X", "Q", "Z"]
        self.english_dictionary = set()
        r = requests.get("https://stepik.org/media/attachments/lesson/668860/dictionary.txt")
        if r.status_code == 200:
            # Read the content of the response
            dictionary_content = r.text
            # Convert the content into a set
            english_dictionary = set(dictionary_content.split('\r\n'))
        # else:
        # return "Dictionary not loaded correctly"

    def accuracy(self, text):
        """returns how many words in text were found in given english_dictionary"""
        if self.english_dictionary == set():
            return None
        check = text.split(" ")
        correct = 0
        for word in check:
            if word in self.english_dictionary:
                correct += 1
        performance = int(correct / (len(check)) * 100)
        return performance

    def compare(self, text1, text2):
        """returns the percentage of similarity between two texts - to the len of shorter one"""
        shorter = 0
        if len(text1) > len(text2):
            shorter = len(text2)
        else:
            shorter = len(text1)
        suma = 0
        for i in range(shorter):
            if text1[i] == text2[i]:
                suma += 1
        return int(suma / shorter * 100)

    def generate_rand_key(self, length, seedly=0):
        random.seed(seedly)
        temp = [random.randint(0, 255) for _ in range(length)]
        return self.decimal_to_str(temp)

    def generate_secret_key(self, length):
        temp = [secrets.randbelow(256) for _ in range(length)]
        return self.decimal_to_str(temp)

    def xor_two_str(self, text, key):
        text = self.text_to_deci(text)
        key = self.text_to_deci(key)
        res = []
        if len(text) != len(key):
            print("diff len")
            print(text)
            print(key)
            return ([-8])
        for i in range(len(text)):
            temp = text[i] ^ key[i]
            res.append(temp)
        return res

    def text_to_deci(self, text):
        # special = {"n" : "\n",
        #            "t" : "\t",
        #            "'" : "\'",
        #            '"' : "\"",
        #            "b" : "\b",
        #            "r" : "\r",
        #            "f" : "\f",
        #            "v" : "\v",
        #            "a" : "\x07",
        #           }
        i = 0
        result = []
        while i < len(text):
            if ord(text[i]) == 92:
                if ord(text[i + 1]) == ord("x"):
                    hexa = text[i + 2:i + 4]
                    deci = int(hexa, 16)
                    result.append(deci)
                    # print(f"hex: {hexa}; dec: {deci}")
                    i += 3
            #         else:
            #              # print("special: ", text[i+1])
            #              temp = text[i+1]
            #              if temp in special.keys():
            #                  deci = ord(special[temp])
            #              else:
            #                  # print(f"special character not in specials: {temp}")
            #                  deci = ord("\\") # tego brakuje
            #              result.append(deci)
            #              i+=1
            else:
                result.append(ord(text[i]))
                # print("normal: ", text[i])
            i += 1
            # print(ord(el))
        return result

    def dec_to_str(self, text):
        res = []
        special = {"\n": "\\n",
                   "'": "\\" + "'",
                   '\"': "\\\"",
                   "\t": "\\t",
                   "\r": "\\r",
                   "\a": "\\x07",
                   "\\": "\\\\"
                   }
        # "\f" : "\\f",
        # "\b" : "\\b",
        # "\v" : "\\v",

        special_numbers = [ord(key) for key in special.keys()]
        for number in text:
            if number < 32 or number == 127 or number == 160 or number == 173:
                if number in special_numbers:
                    res.append(special[chr(number)])
                else:
                    hexa = hex(number)
                    hexa = str(hexa)[2:]
                    if len(hexa) == 1:
                        hexa = "0" + hexa
                    res.append("\\x" + hexa)
            else:
                # if number == ord("'") or number == ord("\""):
                #     res.append("\\" + chr(number))
                # else:
                res.append(chr(number))
        return res

    def decimal_to_str(self, text):
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

    def isAZaz(self, letter):
        return (ord("A") <= ord(letter) <= ord("Z")) or (ord("a") <= ord(letter) <= ord("z"))

    def rozklad_czestotliwosci_liter(self, text):
        most = ["E", "T", "A", "O", "I", "N"]
        least = ["V", "K", "J", "X", "Q", "Z"]
        text = text.upper()
        rozklad = dict([(chr(ord("A") + i), 0) for i in range(26)])
        for letter in text:
            if self.isAZaz(letter):
                rozklad[letter] += 1
        # we dont remove 0 values idk why
        # rozklad = {k: v for k, v in rozklad.items() if v != 0}
        # sort ascending
        sorted_rozklad = {k: v for k, v in sorted(rozklad.items(), key=lambda item: item[1])}
        # sorted descending
        # sorted_dict = {k: v for k, v in sorted(rozklad.items(), key=lambda item: item[1], reverse=True)}
        result = -1
        if len(rozklad.keys()) >= 12:
            result += 1  # or result = 0
            keys = list(sorted_rozklad.keys())
            for key in keys[0:6]:
                if key in least:
                    result += 1
            for key in keys[-6::]:
                if key in most:
                    result += 1
        return result

    def decode_vigenere(self, text, K):
        base = 26  # how many letters A-Z
        # letters = [letter.isalpha() for letter in text] # map text : 1 - is letter; 0 - is not
        letters = [self.isAZaz(letter) for letter in text]
        upper = [letter.isupper() if letters[idx] else -1 for idx, letter in
                 enumerate(text)]  # map text: 1: isUpper; 0 isLower; -1 not isAlpha()
        # text = text.upper() insted line below
        text = "".join([letter.upper() if self.isAZaz(letter) else letter for letter in text])
        K = K.upper()
        res = []
        not_alpha = 0

        for i in range(len(text)):
            if not letters[i]:
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

    @timer
    def interface_veginere(self, text, length):
        AZ = [chr(ord("A") + i) for i in range(26)]
        letters = [letter.upper() for letter in text if self.isAZaz(letter)]
        result_key = ["None", 0]
        key_len = length
        # generate list of lists where every list corresponds to possible solution to number % key_len
        sample = [[] for _ in range(key_len)]
        possible_letters = []
        for i in range(len(letters)):
            sample[i % key_len].append(letters[i])
        for i in range(len(sample)):
            # score = {letter : score}
            score = {k: 0 for k in AZ}
            for letter in AZ:
                # for every sample we try every letter as a key
                # and we check what are the highest scoring letters
                # 1st step decipher sample through letter
                decoded_sample = self.decode_vigenere("".join(sample[i]), letter)
                # 2nd step - score
                scored_number = self.rozklad_czestotliwosci_liter(decoded_sample)
                score[letter] = scored_number
            # find max score
            max_score = max(score.values())
            # add to possible letters all that scored same as max
            temp = [k for k, v in score.items() if v == max_score]
            possible_letters.append(temp)
        # < print(possible_letters)
        # change possible_letters to words
        res = [[letter] for letter in possible_letters[0]]
        # < print(res)
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
        # < print(words)
        key_score = {k: 0 for k in words}
        for word_key in words:
            decipherd_text = self.decode_vigenere(text, word_key)
            decipherd_text = decipherd_text.upper()
            decipherd_text = "".join([letter for letter in decipherd_text if self.isAZaz(letter) or letter == " "])

            score_deciphered = self.rozklad_czestotliwosci_liter(decipherd_text)
            # score_deciphered max 12 min 0
            performance = int((score_deciphered / 12) * 100)

            if performance > result_key[1]:
                result_key[0] = word_key
                result_key[1] = performance

        return result_key

    def xor_two_decimal_lists(self, text, key):
        res = []
        if len(text) != len(key):
            print("diff len")
            print(text)
            print(key)
            return [-8]
        for i in range(len(text)):
            temp = text[i] ^ key[i]
            res.append(temp)
        return res

    @timer
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
                #< print(xored_sample)
                decoded_sample = self.decimal_to_str(xored_sample)
                #< print(decoded_sample)
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
                word1 = "".join([ chr(number) for number in deciphered_text[:length] ])
                word2 = "".join([ chr(number) for number in deciphered_text[length:] ])
                # both = "".join([ chr(number) for number in deciphered_text ])
                #< print(word1, word2, both)
                if word1 in self.english_dictionary or word2 in self.english_dictionary:
                    multiple.append(self.decimal_to_str(word_key))
                # or we can do analiza_czestotliwości and return highest scoring
                # but for that we would require longer texts

        if len(multiple) > 0:
            return multiple, 100
        return result_key
