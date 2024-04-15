# good site http://www.crypto-it.net/pl/teoria/tryby-szyfrow-blokowych.html
def iKey(key, position):
    if position >= len(key):
        position = position % len(key)
    return key[position:] + key[:position]


def bit_expansion(text, pattern):
    res = []
    for i in range(len(pattern)):
        assert pattern[i] < len(
            text), f'Not possible to retrive idx: {pattern[i]} in text: {text} of lenght: {len(text)}'
        res.append(text[pattern[i]])
    return "".join(res)


def bit_block_size_12(text, key, permutation_pattern, sbox1, sbox2, rounds):
    # < print -u sed to test
    # eg input
    # text = "011100010110"
    # key = "10101010"
    # permutation_pattern = (0, 1, 3, 2, 3, 2, 4, 5)
    # sbox1 = "101 010 001 110 011 100 111 000 001 100 110 010 000 111 101 011"
    # sbox2 = "100 000 110 101 111 001 011 010 101 011 000 111 110 010 001 100"
    # rounds = 8
    # ----------------- then
    # solutions = ["101000", "100111", "110001", "011000", "011001", "000100", "011011"]
    assert len(text) == 12, f'Lenght of the given block {text} is different then 12 ({len(text)})'
    sbox1 = sbox1.split(" ")
    sbox2 = sbox2.split(" ")
    L = [text[:6]]
    R = [text[6:]]
    L.append(R[0])  # mby
    for i in range(1, rounds):  # (1, rounds)
        expanded = bit_expansion(R[i - 1], permutation_pattern)
        key_i = iKey(key, i)
        # < print(f'expanded: {expanded} \nkey_i   : {key_i}')
        xored = [1 if key_i[i] != expanded[i] else 0
                 for i in range(len(key_i))]
        # xored = int(expanded, 2) ^ int(key_i, 2)
        # xored = bin(xored)[2:] # or change to str but of binary representation
        # divide to 2 blocks of len 3
        S1 = "".join(str(num) for num in xored[:4])
        S2 = "".join(str(num) for num in xored[4:])
        s1idx = int(S1, 2)
        s2idx = int(S2, 2)
        # < print(f"S_box idx 1: {s1idx}, 2: {s2idx}")
        # get the corresponding values from s boxes
        sboxs = sbox1[s1idx] + sbox2[s2idx]
        # < print(f"from s_boxes: {sboxs}")
        xored = int(L[i - 1], 2) ^ int(sboxs,
                                       2)  # instead L[i-2] or R[i-1] if L will be appended // not sure what happened
        xored = format(xored, '06b')
        # < print(f"last step - xored: {xored}")
        # < print(f"correct solution : {solutions[i-1]} for step: {i}")
        # < print()
        R.append(xored)
        L.append(xored)  # not sure

    L.pop()
    final_result = R[-1] + L[-1]
    # < print(f'final result: {final_result}')
    return final_result


def mini_des_ECB(text, key, permutation_pattern, sbox1, sbox2, rounds):
    # slice text to blocks of 12 bits
    # if the lenght of text is eg 15 then we have on block of 12 and we don't care
    # about the 3 bits that were left (obcinamy)
    twelve_bits_blocks = []
    for i in range(0, len(text) - 11, 12):
        twelve_bits_blocks.append(text[i:i + 12])
    # feed them to bit_block_size_12()
    res = []
    for block in twelve_bits_blocks:
        res.append(bit_block_size_12(block, key, permutation_pattern, sbox1, sbox2, rounds))
    # put together
    return "".join(res)


def mini_des_CBC(text, key, permutation_pattern, sbox1, sbox2, rounds, IV):
    # text jawny xor wektor początkowy (IV)
    # wynik szyfrujemy z kluczem
    # zaszyfrowany blok jest wynikiem i przekzujemy go do następnego kroku jako wektor początkowy
    twelve_bits_blocks = []
    for i in range(0, len(text) - 11, 12):
        twelve_bits_blocks.append(text[i:i + 12])
    # feed them to bit_block_size_12()
    res = []
    assert len(
        IV) == 12, f'Lenght of initial IV must correspond to lenght of block: 12\nGiven IV:{IV} of lenght:{len(IV)}'
    vector = IV
    for block in twelve_bits_blocks:
        # in this shema block = m1, res[-1] = c1 .. c[i], IV is the first c0
        # < print(current block: {block}, current pre_xor: {pre_xor}')
        xored = ['1' if block[i] != vector[i] else '0'
                 for i in range(len(block))]
        xored = "".join(xored)
        # < print(result of xor: {xored}')
        ciphered_block = bit_block_size_12(xored, key, permutation_pattern, sbox1, sbox2, rounds)
        res.append(ciphered_block)
        vector = ciphered_block
    # put together
    return "".join(res)

def mini_des_OFB(text, key, permutation_pattern, sbox1, sbox2, rounds, IV):
    # wektor inicjujący (IV) + klucz zostaje zaszyfrowany
    # wynik przekazujemy jako wektor do kolejnego kroku
    # wynik xor text jawny jako resulting block
    twelve_bits_blocks = []
    for i in range(0, len(text) - 11, 12):
        twelve_bits_blocks.append(text[i:i + 12])
    # feed them to bit_block_size_12()
    res = []
    assert len(
        IV) == 12, f'Lenght of initial IV must correspond to lenght of block: 12\nGiven IV:{IV} of lenght:{len(IV)}'
    vector = IV
    for block in twelve_bits_blocks:
        # < print(current block: {block}, current pre_xor: {pre_xor}')
        ciphered_vector = bit_block_size_12(vector, key, permutation_pattern, sbox1, sbox2, rounds)
        xored = ['1' if block[i] != ciphered_vector[i] else '0'
                 for i in range(len(block))]
        xored = "".join(xored)

        vector = ciphered_vector
        res.append(xored)
    # put together
    return "".join(res)


def mini_des_CTR(text, key, permutation_pattern, sbox1, sbox2, rounds, nonce):
    # nonce (nonce oznacza unikalny numer: number used once)
    # nonce + licznik szyfrowanie z kluczem
    # wynik xorujemy z tekstem jawnym
    # zwiększamy licznik o 1

    twelve_bits_blocks = []
    for i in range(0, len(text) - 11, 12):
        twelve_bits_blocks.append(text[i:i + 12])
    # feed them to bit_block_size_12()
    res = []
    assert type(nonce) == int, f'The nonce parameter must be an integer; given type:{type(nonce)}'
    for idx, block in enumerate(twelve_bits_blocks):
        # < print(current block: {block}, current pre_xor: {pre_xor}')
        vector = bin(nonce + idx)[2:]
        if len(vector) > 12:
            vector = vector[-12:]
        elif len(vector) < 12:
            vector = format((nonce + idx), '012b')

        ciphered_vector = bit_block_size_12(vector, key, permutation_pattern, sbox1, sbox2, rounds)
        xored = ['1' if block[i] != ciphered_vector[i] else '0'
                 for i in range(len(block))]
        xored = "".join(xored)

        vector = ciphered_vector
        res.append(xored)
    # put together
    return "".join(res)