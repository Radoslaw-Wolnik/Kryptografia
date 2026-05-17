from kryptografia.block_ciphers import (
    mini_des_cbc,
    mini_des_ctr,
    mini_des_ecb,
    mini_des_ofb,
    pkcs7_pad,
    pkcs7_unpad,
    xor_block_cipher_decrypt,
    xor_block_cipher_encrypt,
)

PERMUTATION = (0, 1, 3, 2, 3, 2, 4, 5)
SBOX1 = [
    "101",
    "010",
    "001",
    "110",
    "011",
    "100",
    "111",
    "000",
    "001",
    "100",
    "110",
    "010",
    "000",
    "111",
    "101",
    "011",
]
SBOX2 = [
    "100",
    "000",
    "110",
    "101",
    "111",
    "001",
    "011",
    "010",
    "101",
    "011",
    "000",
    "111",
    "110",
    "010",
    "001",
    "100",
]


def main() -> None:
    print("Lab 04 - Padding, toy block ciphers, and modes")
    print("=" * 50)

    plaintext = b"block cipher laboratory example"
    key = b"0123456789abcdef"
    padded = pkcs7_pad(plaintext, 16)
    ciphertext = xor_block_cipher_encrypt(plaintext, key)

    print("\n1. PKCS#7 padding")
    print(f"plaintext length: {len(plaintext)}")
    print(f"padded length:    {len(padded)}")
    print(f"padding bytes:    {padded[-padded[-1]:].hex()}")
    print(f"unpadded ok:      {pkcs7_unpad(padded, 16) == plaintext}")

    print("\n2. Educational XOR block transformation")
    print(f"ciphertext hex:   {ciphertext.hex()}")
    print(f"decrypted:        {xor_block_cipher_decrypt(ciphertext, key)}")

    print("\n3. Mini-DES style modes from the original lab")
    bits = "011100010110" * 3
    mini_key = "10101010"
    iv = "000000000000"
    print(f"ECB:              {mini_des_ecb(bits, mini_key, PERMUTATION, SBOX1, SBOX2, 8)}")
    print(f"CBC:              {mini_des_cbc(bits, mini_key, PERMUTATION, SBOX1, SBOX2, 8, iv)}")
    print(f"OFB:              {mini_des_ofb(bits, mini_key, PERMUTATION, SBOX1, SBOX2, 8, iv)}")
    print(f"CTR:              {mini_des_ctr(bits, mini_key, PERMUTATION, SBOX1, SBOX2, 8, 7)}")


if __name__ == "__main__":
    main()
