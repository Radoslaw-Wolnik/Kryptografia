"""Toy block-cipher modes used for educational demonstrations."""

from __future__ import annotations

from kryptografia.block_ciphers.padding import pkcs7_pad, pkcs7_unpad
from kryptografia.common.bytes import chunk_bytes
from kryptografia.common.xor import xor_bytes


def xor_block_cipher_encrypt(plaintext: bytes, key: bytes, *, block_size: int = 16) -> bytes:
    """Encrypt with an intentionally insecure XOR-based block-cipher example."""

    if len(key) != block_size:
        raise ValueError("key length must match block size")

    padded = pkcs7_pad(plaintext, block_size)
    encrypted_blocks = [xor_bytes(block, key) for block in chunk_bytes(padded, block_size)]
    return b"".join(encrypted_blocks)


def xor_block_cipher_decrypt(ciphertext: bytes, key: bytes, *, block_size: int = 16) -> bytes:
    """Decrypt the educational XOR block cipher."""

    if len(ciphertext) % block_size != 0:
        raise ValueError("ciphertext length must align to block size")
    if len(key) != block_size:
        raise ValueError("key length must match block size")

    decrypted_blocks = [xor_bytes(block, key) for block in chunk_bytes(ciphertext, block_size)]
    return pkcs7_unpad(b"".join(decrypted_blocks), block_size)

