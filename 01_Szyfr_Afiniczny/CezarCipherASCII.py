class CezarCipherASCII:


    def __init__(self):
        pass

    def mod(self, num, base):
        if num > 0:
            return num % base
        if num < 0:
            while num < 0:
                num = num + base
            return num
        return 0


    def cezar_cipher(self, text, move):
        res = []
        base = 52
        for letter in text:
            if letter.isalpha() == False:
                res.append(letter)
                continue
            small = 0
            if ord(letter) >= ord("a"):
                small = 6
            new_letter = ord(letter) - ord("A") - small + move
            new_letter = mod(new_letter, base)
            # print(new_letter)
            # print(chr(new_letter + ord("A") + small))
            if move == 0:
                new_letter += small
            if move < 0:
                new_letter += 6

            if move > 0 and new_letter > 25 and new_letter < base:
                new_letter += 6
            if move < 0 and new_letter > 0 and new_letter < 32:
                new_letter -= 6
            # print(new_letter)

            res.append(chr(new_letter + ord("A")))

        return "".join(res)

    # Karolina Knopik, this code here is so much better
    def Caesar(self, txt, shift):
        encrypted = []
        for word_list in txt:
            encrypted_word = ""
            for word in word_list:
                for c in word:
                    if c.isalpha():
                        offset = ord('a') if c.islower() else ord('A')
                        res = chr((ord(c) - offset + shift) % 26 + offset)
                        # check how many times 26 is in number - if its odd times change letter size, if its even then nothing changes
                        # print(ord(c) - offset + shift)
                        if ((ord(c) - offset + shift) // 26) % 2 == 1:
                            # print(res)
                            res = res.swapcase()
                        encrypted_word += res

                    else:
                        encrypted_word += c
            encrypted.append([encrypted_word])
        return encrypted