class CezarCipherDict:

    def __init__(self):
        big_letters = [chr(i) for i in range(ord("A"), ord("Z") + 1, 1)]
        small_letters = [chr(i) for i in range(ord("a"), ord("z") + 1, 1)]
        self.alfabet = {key : val for val, key in enumerate(big_letters + small_letters)}
        self.back = {val : key for val, key in enumerate(big_letters + small_letters)}
        self.mod = 52

    def cipher(self, text, move):
        res = []
        for letter in text:
            if letter.isalpha() == False:
                res.append(letter)
                continue
            new_letter = self.alfabet[letter] + move
            if new_letter < 0:
                new_letter += self.mod
            new_letter = new_letter % self.mod
            res.append(self.back[new_letter])

        return "".join(res)

    def decipher(self, text, move):
        return self.cipher(text, -1 * move)

    def cipher_sentence(self, sentence, move):
        words = sentence.split(" ")
        for idx, word in enumerate(words):
            words[idx] = self.cipher(word, move)
        return " ".join(words)

    def decipher_sentence(self, sentence, move):
        return self.cipher_sentence(sentence, -1 * move)