import random

def xor(a, b):
    return a ^ b

def text_to_deci(text):
#    special = {"n" : "\n",
#               "t" : "\t",
#               "'" : "\'",
#               '"' : "\"",
#               "b" : "\b",
#               "r" : "\r",
#               "f" : "\f",
#               "v" : "\v",
#               "a" : "\x07",
#              }
    i = 0
    result = []
    while i < len(text):
        if ord(text[i]) == 92:
            if ord(text[i + 1]) == ord("x"):
                hexa = text[i+2:i+4]
                deci = int(hexa, 16)
                result.append(deci)
                # print(f"hex: {hexa}; dec: {deci}")
                i+=3
#            else:
#                # print("special: ", text[i+1])
#                temp = text[i+1]
#                if temp in special.keys():
#                    deci = ord(special[temp])
#                else:
#                    # print(f"special character not in specials: {temp}")
#                    deci = ord("\\") # tego brakuje
#                result.append(deci)
#                i+=1
        else:
            result.append(ord(text[i]))
            # print("normal: ", text[i])
        i+=1
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
    special = {"\n" : "\\n",
               "'" : "\\" + "'",
               '\"' : "\\\"",
               "\t" : "\\t",
               "\r" : "\\r",
               "\a" : "\\x07",
               "\\" : "\\\\"
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

# text1 = input()
# text2 = input()
answ1 = "esta"
text1 = "\ny\x1bf"
answ2 = "agni"
text2 = "\x0em\x01n"

keyOne = "o\no\x07"
A = text_to_deci(text1)
B = text_to_deci(text2)
# len(A) == len(B) == len(used_key)

xored = xor_two_str(answ1, keyOne)
result = dec_to_str(xored)
print("".join(result))