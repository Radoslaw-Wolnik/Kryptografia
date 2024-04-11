import matplotlib.pyplot as plt
import subprocess
from pathlib import Path


def print_pbm(filePath):
    root_folder = Path(__file__).parents[1]
    file_path = root_folder / filePath

    # Define the PowerShell command to run the script with the file name as an argument
    ps_command = "powershell -ExecutionPolicy Unrestricted -File print.ps1 " + str(file_path)
    # Execute the PowerShell command using subprocess.run
    # subprocess.run(ps_command)
    result = subprocess.run(ps_command, capture_output=True, text=True)
    # Check if the command was successful
    if result.returncode == 0:
        # Print the output with proper formatting
        print(result.stdout)
    else:
        # Print any errors
        print("Error:", result.stderr)


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
    L.append(R[0])  # chyba
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
        # get the coresponding values from s boxes
        sboxs = sbox1[s1idx] + sbox2[s2idx]
        # < print(f"from s_boxes: {sboxs}")
        xored = int(L[i - 1], 2) ^ int(sboxs,
                                       2)  # insted L[i-2] or R[i-1] if L will be appended // not sure what happened
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
    # if the lenght of text is eg 15 then we have on block of 12 and we dont care about the 3 bits that were left (obcinamy)
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
    # slice text to blocks of 12 bits
    # if the lenght of text is eg 15 then we have on block of 12 and we dont care about the 3 bits that were left (obcinamy)
    twelve_bits_blocks = []
    for i in range(0, len(text) - 11, 12):
        twelve_bits_blocks.append(text[i:i + 12])
    # feed them to bit_block_size_12()
    res = []
    assert len(
        IV) == 12, f'Lenght of initial IV must correspond to lenght of block: 12\nGiven IV:{IV} of lenght:{len(IV)}'
    pre_xor = IV
    for block in twelve_bits_blocks:
        # in this shema block = m1, res[-1] = c1 .. c[i], IV is the first c0
        # < print(f'current block: {block}, current pre_xor: {pre_xor}')
        xored = ['1' if block[i] != pre_xor[i] else '0'
                 for i in range(len(block))]
        xored = "".join(xored)
        # < print(f'result of xor: {xored}')
        res.append(bit_block_size_12(xored, key, permutation_pattern, sbox1, sbox2, rounds))
        pre_xor = res[-1]
    # put together
    return "".join(res)


if __name__ == '__main__':
    print("Szyfry blokowe")

    text = "000000000001"
    key = "11111111"
    permutation_pattern = (0, 4, 3, 2, 3, 5, 4, 1)
    sbox1 = "101 010 001 110 011 100 111 000 001 100 110 010 000 111 101 011"
    sbox2 = "100 000 110 101 111 001 011 010 101 011 000 111 110 010 001 100"
    rounds = 8

    ciag_IV = "111011010010"

    print(mini_des_CBC(text, key, permutation_pattern, sbox1, sbox2, rounds, ciag_IV))

    text = "011100010110"
    text2 = "111100010110"
    key = "10101010"
    permutation_pattern = (0, 1, 3, 2, 3, 2, 4, 5)
    sbox1 = "101 010 001 110 011 100 111 000 001 100 110 010 000 111 101 011"
    sbox2 = "100 000 110 101 111 001 011 010 101 011 000 111 110 010 001 100"
    rounds = 8

    print(mini_des_ECB(text, key, permutation_pattern, sbox1, sbox2, rounds))
    print(mini_des_ECB(text2, key, permutation_pattern, sbox1, sbox2, rounds))

    # outfileName = "first"
    root_folder = Path(__file__).parents[0]
    # print(Path(__file__).parents[0])
    resource_path = root_folder / "resources"
    out_path = root_folder / 'out'  # / (outfileName + '.pbm')
    #
    full_name = "seahorse.pbm"
    param = ""
    size = ""
    binary_image = []
    with open(resource_path / full_name, 'rb') as f:
        param = f.readline()[:-1]
        size = f.readline()[:-1]
        binary_data = f.read()
        # Convert binary data to list of 0s and 1s
        bits = []
        for byte in binary_data:
            byte_bits = format(byte, '08b')  # Convert byte to binary string
            bits.extend(map(int, byte_bits))

        # byte = f.read(1)
        # while byte:
        #     byte_value = ord(byte)
        #     binary_image.append(format(byte_value, '08b'))  # Convert byte to binary string
        #     byte = f.read(1)
    size = (size.decode('utf-8')).split()
    size = [int(num_str) for num_str in size]
    print(param.decode('utf-8'))
    print(size)
    print(bits[5500:6000])

    #
    # with open(out_path, 'w+') as output:
    #     output.writelines(['P1\n', '# ' + outfileName + '\n'])
    #     output.write(str(len(result[0])) + ' 12\n')
    #     for line in result:
    #         line = ''.join(line)
    #         output.write(line + '\n')

    name = "seahorse"
    print_pbm("resources/" + name + ".pbm")
