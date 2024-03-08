class CezarDecodeTwoStr:

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

    def diff(self, a, b):
        a = ord(a)
        b = ord(b)
        if a > ord("Z"):
            a -= 6
        if b > ord("Z"):
            b -= 6
        res = a - b
        while res < 0:
            res += 52
        if res > 52:
            res = res % 52
        return res

    def cezar_cipher_again(self, text, move):
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
            new_letter = self.mod(new_letter, base)
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

    def cezar_move(self, coded, decoded):
        x = []
        y = []
        for idx in range(len(decoded)):
            if decoded[idx].isalpha() == False:
                continue
            x.append(coded[idx])
            y.append(decoded[idx])
        same = True

        mod = self.diff(y[0], x[0])
        # mod = ord(y[0]) - ord(x[0])
        for i in range(len(x)):
            if self.diff(y[i], x[i]) != mod:
                same = False
            # if ord(y[i]) - ord(x[i]) != mod:
            # same = False
        if same == True:
            return self.cezar_cipher_again(coded, mod), mod
        return x, y