import subprocess
from pathlib import Path
from block_cipher import mini_des_CBC, mini_des_ECB, mini_des_OFB, mini_des_CTR
from file_menager import *


def process_and_write_pbm(input_file, output_file):
    header, size, bits = read_pbm(input_file)
    cipher_bits = mini_des_ECB(bits, "10101010", (0, 1, 3, 2, 3, 2, 4, 5),
                               "101 010 001 110 011 100 111 000 001 100 110 010 000 111 101 011",
                               "100 000 110 101 111 001 011 010 101 011 000 111 110 010 001 100",
                               8)  # (0, 4, 3, 2, 3, 5, 4, 1), (0, 1, 3, 2, 3, 2, 4, 5),
    write_pbm(header, size, cipher_bits, output_file)


def process_and_write_img(input_file, output_file):
    bits, size = image_to_bits(input_file)
    cipher_bits = mini_des_CBC(bits, "10101010", (0, 1, 3, 2, 3, 2, 4, 5),
                               "101 010 001 110 011 100 111 000 001 100 110 010 000 111 101 011",
                               "100 000 110 101 111 001 011 010 101 011 000 111 110 010 001 100", 8, "111011010010")
    bits_to_image(cipher_bits, size, output_file)


def process_and_write_img_OFB(input_file, output_file):
    bits, size = image_to_bits(input_file)
    cipher_bits = mini_des_OFB(bits, "10101010", (0, 1, 3, 2, 3, 2, 4, 5),
                               "101 010 001 110 011 100 111 000 001 100 110 010 000 111 101 011",
                               "100 000 110 101 111 001 011 010 101 011 000 111 110 010 001 100", 8, "111011010010")
    bits_to_image(cipher_bits, size, output_file)


def process_and_write_img_CTR(input_file, output_file):
    bits, size = image_to_bits(input_file)
    cipher_bits = mini_des_CTR(bits, "10101010", (0, 1, 3, 2, 3, 2, 4, 5),
                               "101 010 001 110 011 100 111 000 001 100 110 010 000 111 101 011",
                               "100 000 110 101 111 001 011 010 101 011 000 111 110 010 001 100", 8, 127612213)
    bits_to_image(cipher_bits, size, output_file)


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

    process_and_write_pbm("resources/washington.pbm", "out/first.pbm")
    process_and_write_img("resources/washington.png", "out/scnd.png")
    process_and_write_img_OFB("resources/washington.png", "out/third.png")
    process_and_write_img_CTR("resources/washington.png", "out/fourth.png")

    # outfileName = "first"
    # root_folder = Path(__file__).parents[0]
    # print(Path(__file__).parents[0])
    # resource_path = root_folder / "resources"
    # out_path = root_folder / 'out'  # / (outfileName + '.pbm')
    #
    # full_name = "seahorse.pbm"
    # param = ""
    # size = ""
    # binary_image = []
    # with open(resource_path / full_name, 'rb') as f:
    #     param = f.readline()[:-1]
    #     size = f.readline()[:-1]
    #     binary_data = f.read()
    #     # Convert binary data to list of 0s and 1s
    #     bits = []
    #     for byte in binary_data:
    #         byte_bits = format(byte, '08b')  # Convert byte to binary string
    #          bits.extend(map(int, byte_bits))

    #     # byte = f.read(1)
    #     # while byte:
    #     #     byte_value = ord(byte)
    #     #     binary_image.append(format(byte_value, '08b'))  # Convert byte to binary string
    #     #     byte = f.read(1)
    # size = (size.decode('utf-8')).split()
    # size = [int(num_str) for num_str in size]
    # print(param.decode('utf-8'))
    # print(size)
    # print(bits[5500:6000])