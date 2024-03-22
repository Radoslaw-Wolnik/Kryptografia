import requests

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

#  badanie kasickieg
def substrings_with_indexes(s):
    substrings_with_indexes = {}
    n = len(s)
    for length in range(1, n):
        for start in range(n - length + 1):
            substring = s[start:start + length]
            if s.count(substring) > 1:
                if substring in substrings_with_indexes:
                    substrings_with_indexes[substring].append(start)
                else:
                    substrings_with_indexes[substring] = [start]
    return substrings_with_indexes


def distance(l):
    """substracts all elements of list with all lower elements of given list
    given list must be sorted lowest to highest"""
    res = []
    if len(l) == 2:
        return l[1] - l[0]
    for i in range(1, len(l)):
        for j in range(i):
            res.append(l[i] - l[j])
    return res

def break_down_to_divisiors(number):
    res = []
    for i in range(1, int(number/2) + 1):
        if number % i == 0:
            res.append(int(number/i))
    return res

def badanie_kasickiego(text):
    """returns list of posible lenghts of a key used to cipher the text"""
    alphabet_size = 20 # 26
    text = "".join([letter for letter in text if isAZaz(letter)])
    text = text.upper()
    substrings = substrings_with_indexes(text)
    # print(substrings)
    # orted_rozklad = {k: v for k, v in sorted(rozklad.items(), key=lambda item: item[1])}
    temp = [substring for substring in sorted(substrings, key=len, reverse=True)]

    # create a sorted list of lists : [[aaa, bbb, ccc], [aa, bb, cc], [a, b, c]]
    # sorted from longest substrings to shortest substrings
    longest = len(temp[0])
    res = [[] for _ in range(longest)]
    added = 0
    for i in range(longest):
        for el in temp[added:]:
            if len(el) < longest - i:
                break
            res[i].append(el)
            added += 1

    # print(res[0])
    key_len = set()
    # we take to concideration only the longest substrings
    # to stepik we can do len(res[0]) -1
    for i in range(len(res[0])):
        positions = substrings[res[0][i]]
        temp = distance(positions)
        if type(temp) == int:
            key_len.add(temp)
        else:
            for el in temp:
                key_len.add(el)

    # rozłożyć wynik na części złożone
    # eg 24 = 24, 12, 8, .. 3, 2
    key_rozklad = []
    for possible_key in key_len:
        key_rozklad += break_down_to_divisiors(possible_key)
    key_rozklad.sort()
    #print(key_rozklad)

    # change key_rozklad into list of unique key lenghts from most common to least common
    agregated = {key_rozklad[0] : 1}
    for i in range(1, len(key_rozklad)):
        if key_rozklad[i-1] != key_rozklad[i]:
            # there is no sense in having keys bigger then alphabet size
            if key_rozklad[i] >= alphabet_size:
                break
            agregated[key_rozklad[i]] = 1
        else:
            agregated[key_rozklad[i]] += 1

    # sort agregated through values
    agregated = dict(sorted(agregated.items(), key=lambda item: item[1], reverse =True))
    return list(agregated.keys())
# end badanie kasickiego

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



def atak_slownikowy(text):
    AZ = [chr(ord("A") + i) for i in range(26)]
    possible_key_lenghts = badanie_kasickiego(text)
    # possible_key_lenghts = possible_key_lenghts[:4] # im scared of big numbers
    letters = [letter.upper() for letter in text if isAZaz(letter)]
    result_key = ["None", 0]
    english_dictionary = set()
    dictionary_present = False
    r = requests.get("https://stepik.org/media/attachments/lesson/668860/dictionary.txt")
    if r.status_code == 200:
        dictionary_present = True
        # Read the content of the response
        dictionary_content = r.text
        # Convert the content into a set
        english_dictionary = set(dictionary_content.split('\r\n'))
    if dictionary_present == False:
        return "Dictionary not loaded correctly"
    
    # search in dictionary through all words that have the same lenght as possible_key_lenghts
    words = []
    for word in english_dictionary:
        if len(word) in possible_key_lenghts:
            words.append(word)
    # score text 
    for word_key in words:
        decipherd_text = decode_vigenere(text, word_key)
        decipherd_text = decipherd_text.upper()
        decipherd_text = "".join([letter for letter in decipherd_text if isAZaz(letter) or letter == " "])
        check = decipherd_text.split(" ")
        correct = 0
        for word in check:
            if word in english_dictionary:
                correct += 1
        # if percentage of text is higher then 69 % - correct
        performance = int(correct / (len(check)) * 100)
        # if performance > 5:
            # print(word_key, performance, "%")
        if correct > 0:
            if int(correct / (len(check)) * 100) >= 69:
                return word_key
        if performance > result_key[1]:
            result_key[0] = word_key
            result_key[1] = performance

    return result_key[0]
