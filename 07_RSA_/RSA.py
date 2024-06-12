import random
from math import ceil
from base64 import b64encode, b64decode


def xgcd(a, b):
    # rozszerzony algorytm euclidesa
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


def gcd(a, b):
    """Funkcja znajdująca greatest common divisor (GCD) wykożystując algorytm euklidesa"""
    while b != 0:
        a, b = b, a % b
    return a


def fast_modulo(base, power, mod):
    res = 1
    base = base % mod
    while power > 0:
        if power % 2 == 1:  # If power is odd
            res = (res * base) % mod
        base = (base * base) % mod  # Square the base
        power //= 2  # Divide the power by 2
    return res


def bytes2int(raw_bytes: bytes) -> int:
    return int.from_bytes(raw_bytes, "big", signed=False)


def int2bytes(number: int, fill_size: int = 0) -> bytes:
    if number < 0:
        raise ValueError("Number must be an unsigned integer: %d" % number)
    bytes_required = max(1, ceil(number.bit_length() / 8))
    if fill_size > 0:
        return number.to_bytes(fill_size, "big")
    return number.to_bytes(bytes_required, "big")


class RSA:
    def __init__(self, seed=1, n=10, test_times=5):
        random.seed(seed)
        self.n = n
        self.seed = seed
        self.test_times = test_times

        self.p = None
        self.q = None
        self.fi = None
        self.private_key = None
        self.public_key = None

        self.SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!?. "
        self.symbols_dict = {ord(key): idx for idx, key in enumerate(self.SYMBOLS)}
        self.generate()  # not sure about having this method here

    def generate(self):
        self.p = self.__get_prime()
        self.q = self.__get_prime()
        self.fi = (self.p - 1) * (self.q - 1)
        self.private_key = self.__random_relative_prime()
        inverse = xgcd(self.private_key, self.fi)[1]
        if inverse < 0:
            inverse += self.fi
        self.public_key = inverse

    def change_params(self, seed=None, n=None, test_times=None):
        self.seed = seed if seed is not None else self.seed
        random.seed(self.seed)
        self.n = n if n is not None else self.n
        self.test_times = test_times if test_times is not None else self.test_times
        self.generate()  # also not sure about having this method here

    def __str__(self):
        return (f'n : {self.n} seed : {self.seed} test_times : {self.test_times} ' +
                f'p : {self.p} q : {self.q} number : {self.p * self.q} fi : {self.fi} ' +
                f'private_key : {self.private_key} public_key : {self.public_key} ')

    def save(self, file_name=None):
        name = file_name if file_name is not None else 'out'
        with open(name + '.txt', 'w') as data:
            data.write(f'public_key : {self.public_key}\nprivate_key : {self.private_key}')

    def get_public_key(self):
        return (self.p * self.q, self.public_key)

    def get_private_key(self):
        return (self.private_key, self.p * self.q)

    def cipher(self, text=None, file=None, out_file=None, public_key=None):
        res, mod, key = None, None, None
        assert text is None or file is None, "Only one medium at a time, either text to function or file"

        if public_key is not None:
            assert type(public_key) == list or type(
                public_key) == tuple, "public key should be tuple or list of two int"
            assert len(public_key) == 2, "wrong number of elements in public key (should be n and public key)"
            assert type(public_key[0]) == int and type(
                public_key[1]) == int, "the arguments as public key should be integers"
            mod = public_key[0]
            key = public_key[1]
        else:
            mod = self.p * self.q
            assert self.public_key is not None, "No public key in the object somehow"
            key = self.public_key
        if text is not None:
            res = self.__cipher_blocks(text, mod, key)
        elif file is not None:
            with open(file, 'r') as file_text:
                res = self.__cipher_blocks(file_text, mod, key)
        # convert res - list of big numbers - into byte arrays of fixed size depending on p*q = number
        size_bit_array = (mod.bit_length() + 7) // 8
        byte_arrays = [int2bytes(num, size_bit_array) for num in res]
        # concatynate and change to utf-8
        byte_string = b''.join(byte_arrays)
        base64_string = b64encode(byte_string).decode('utf-8')
        # save to file
        out_name = out_file if out_file is not None else 'out.txt'
        with open(out_name, 'w') as out:
            out.write(base64_string)
        return base64_string

    def decipher(self, text=None, file=None, out_file=None):
        res = None
        assert self.private_key is not None, "no private key"
        assert text is None or file is None, "Only one medium at a time, either text to function or file"
        base64_string = None
        if text is not None:
            base64_string = text
        elif file is not None:  # could be just else but better check
            with open(file, 'r') as file_text:
                base64_string = file_text
        # change from base64 to bytearrays to list of numbers (int)
        byte_string = b64decode(base64_string)
        mod = self.q * self.p
        size_bit_array = (mod.bit_length() + 7) // 8
        byte_arrays = [byte_string[i:i + size_bit_array] for i in range(0, len(byte_string), size_bit_array)]
        reconstructed_numbers = [bytes2int(b) for b in byte_arrays]
        # decipher
        res = self.__decipher_blocks(reconstructed_numbers)

        out_name = out_file if out_file is not None else 'out.txt'
        with open(out_name, 'w') as out:
            out.write(res)
        return res

    def __cipher_blocks(self, text, mod, key):
        text = text.encode('utf-8')
        res = []
        for i in range(0, len(text), 1):
            # print(i)
            character = text[i]
            ciphered = fast_modulo(character, key, mod)  # (character ** public_key ) % mod ;; mod = n = p*q
            res.append(ciphered)
        return res

    def __decipher_blocks(self, ciphered_numbers):
        # gets a list of numbers returns text
        mod = self.p * self.q
        key = self.private_key
        res = []
        for i in range(0, len(ciphered_numbers)):
            # print(f'idx: {i} num: {ciphered_numbers[i]}')
            character = ciphered_numbers[i]
            # (character ** private_key ) % mod ;; mod = n = p*q
            deciphered = fast_modulo(character, key, mod)
            # print(deciphered, chr(deciphered))
            res.append(chr(deciphered))
        return "".join(res)

    def __test_millera_rabina(self, n, a):
        exp = n - 1
        while not exp & 1:
            exp //= 2
        x = fast_modulo(a, exp, n)
        if x == 1 or x == n - 1:
            return True
        while (exp << 1) != n - 1:
            x = fast_modulo(a, exp, n)
            if x == n - 1:
                return True
            exp <<= 1
        return False

    def __gen_prime(self):
        """tries to generate a prime number e < 2^(n-1), 2^n >
        if succesfull returns number (int)
        if not returns None"""
        losowa = random.randint(2 ** (self.n - 1), 2 ** self.n)
        if losowa % 2 == 0:
            losowa += 1
        for i in range(self.test_times):
            a = random.randint(2, losowa)
            if not self.__test_millera_rabina(losowa, a):
                return None
        return losowa

    def __get_prime(self):
        prime = None
        while prime is None:
            prime = self.__gen_prime()
        return prime

    def __random_relative_prime(self):
        """losowa liczba wzglednie pierwsza do {self.fi} z zakresu < 2**(n-1), 2**(n) >"""
        relative_prime = None
        while relative_prime is None:
            losowa = random.randint(2 ** (self.n - 1), 2 ** self.n)
            if losowa % 2 == 0:
                losowa = losowa - 1
                # continue
            if gcd(self.fi, losowa) == 1:
                relative_prime = losowa
        return relative_prime
