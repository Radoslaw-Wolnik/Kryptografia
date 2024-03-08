class SzyfrAfiniczny:
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

    def gcd(self, x, y):
        while y > 0:
            x, y = y, x % y
        return x

    def xgcd(self, a, b):
        a, b = max(a, b), min(a, b)

        q = [-1, -1]
        r = [a, b]
        s = [1, 0]
        t = [0, 1]

        while r[-1] > 0:
            q.append(r[-2] // r[-1])
            r.append(r[-2] % r[-1])
            s.append(s[-2] - q[-1] * s[-1])
            t.append(t[-2] - q[-1] * t[-1])

        return s[-2], t[-2]


    def szyfr_afiniczny(self, a, b, text):
        base = 26

        if self.gcd(26, a) != 1:
            return "BŁĄD"

        letters = [letter.isalpha() for letter in text]
        upper = [letter.isupper() if letters[idx] else -1 for idx, letter in enumerate(text)]
        text = text.lower()
        res = []
        for i in range(len(text)):
            if letters[i] is False:
                res.append(text[i])
                continue
            new_letter = ord(text[i]) - ord("a")
            new_letter = (new_letter * a + b)
            while new_letter < 0:
                new_letter += base
            new_letter = new_letter % base

            new_letter = chr(new_letter + ord("a"))
            if upper[i]:
                new_letter = new_letter.upper()
            res.append(new_letter)
        return "".join(res)

    # deszyfrowanie --------------------------------------

    def d_szyfr_afiniczny(self, a, b, text):
        base = 26

        if self.gcd(26, a) != 1:
            return "BŁĄD"

        letters = [letter.isalpha() for letter in text]
        upper = [letter.isupper() if letters[idx] else -1 for idx, letter in enumerate(text)]
        text = text.lower()
        res = []
        for i in range(len(text)):
            if letters[i] is False:
                res.append(text[i])
                continue
            new_letter = ord(text[i]) - ord("a")
            new_letter = (new_letter - b) * a  # to decipher ( new_letter -b ) * a^-1 ;; to cipher (new_letter * a) + b
            while new_letter < 0:
                new_letter += base
            new_letter = new_letter % base

            new_letter = chr(new_letter + ord("a"))
            if upper[i]:
                new_letter = new_letter.upper()
            res.append(new_letter)
        return "".join(res)

    def deszyfr_afiniczny(self, a, b, text):
        base = 26
        rev_a = self.xgcd(a, base)[-1]
        if rev_a < 0:
            rev_a += base
        if self.gcd(base, rev_a) != 1:
            return rev_a, b, "BŁĄD jest tu"
        return rev_a, b, self.d_szyfr_afiniczny(rev_a, b, text)

    def text_to_kongurency(self, coded, decoded):
        change = {}  # coded : decoded
        for idx in range(len(decoded)):
            if decoded[idx].isalpha() == False:
                continue
            if coded[idx] not in change:
                change[coded[idx]] = decoded[idx]
        return change

    def solve_kongurency(self, x, y, base):
        # x[0] * a + b = y[0] modulo base
        # x[1] * a + b = y[1] modulo base
        # add
        # x[0] - x[1] * a = y[0] - y[1]
        #
        # if x[0] > x[1]
        x_solv = self.mod(x[0] - x[1], base)
        y_solv = self.mod(y[0] - y[1], base)
        rev_x = 0
        if x_solv != 0:
            rev_x = self.xgcd(x_solv, base)[-1]
            if rev_x < 0:
                rev_x += base
        a = self.mod(y_solv * rev_x, base)
        # print(x[1], a, y[1])
        b = self.mod(y[1] - x[1] * a, base)
        return a, b

    def interface(self, coded, decoded):
        change = self.text_to_kongurency(coded, decoded)
        if not change:
            return 1, 0, coded
        y = [ord(key) - ord("a") for key in change.keys()]  # i couldnt get it to work becouse i switched x and y
        x = [ord(val) - ord("a") for val in change.values()]

        # for key, val in change.items():
        #     x.append(ord(key) - ord("a"))
        #     y.append(ord(val) - ord("a"))
        a, b = self.solve_kongurency(x, y, 26)
        # a = xgcd(a, 26)[-1]
        res = self.deszyfr_afiniczny(a, b, coded)
        return a, res[1], res[2]