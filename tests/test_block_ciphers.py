import pytest

from kryptografia.block_ciphers.mini_des import (
    bit_expansion,
    mini_des_block,
    mini_des_cbc,
    mini_des_ctr,
    mini_des_ecb,
    mini_des_ofb,
    rotate_key,
    xor_bits,
)
from kryptografia.block_ciphers.modes import xor_block_cipher_decrypt, xor_block_cipher_encrypt
from kryptografia.block_ciphers.padding import pkcs7_pad, pkcs7_unpad

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


def test_padding_round_trip() -> None:
    data = b"hello world"
    padded = pkcs7_pad(data, 16)
    assert pkcs7_unpad(padded, 16) == data


def test_padding_aligned_block() -> None:
    data = b"A" * 16
    padded = pkcs7_pad(data, 16)
    assert len(padded) == 32
    assert pkcs7_unpad(padded, 16) == data


def test_invalid_padding() -> None:
    with pytest.raises(ValueError):
        pkcs7_unpad(b"invalid", 16)


def test_block_cipher_round_trip() -> None:
    plaintext = b"educational block cipher test"
    key = b"0123456789abcdef"

    ciphertext = xor_block_cipher_encrypt(plaintext, key)
    recovered = xor_block_cipher_decrypt(ciphertext, key)

    assert recovered == plaintext


def test_invalid_key_length() -> None:
    with pytest.raises(ValueError):
        xor_block_cipher_encrypt(b"plaintext", b"short")


def test_ciphertext_alignment() -> None:
    with pytest.raises(ValueError):
        xor_block_cipher_decrypt(b"misaligned", b"0123456789abcdef")


def test_mini_des_block_and_modes() -> None:
    block = "011100010110"
    key = "10101010"

    assert rotate_key(key, 2) == "10101010"
    assert bit_expansion("010110", PERMUTATION) == "01101010"
    assert xor_bits("1010", "0011") == "1001"
    assert mini_des_block(block, key, PERMUTATION, SBOX1, SBOX2, 8) == "011011000100"

    bits = block * 2
    assert len(mini_des_ecb(bits, key, PERMUTATION, SBOX1, SBOX2, 8)) == 24
    assert len(mini_des_cbc(bits, key, PERMUTATION, SBOX1, SBOX2, 8, "000000000000")) == 24
    assert len(mini_des_ofb(bits, key, PERMUTATION, SBOX1, SBOX2, 8, "000000000000")) == 24
    assert len(mini_des_ctr(bits, key, PERMUTATION, SBOX1, SBOX2, 8, 3)) == 24
