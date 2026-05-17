"""Byte and text block helpers for educational RSA examples."""

from __future__ import annotations

import base64
from math import ceil


def bytes_to_int(raw_bytes: bytes) -> int:
    return int.from_bytes(raw_bytes, "big", signed=False)


def int_to_bytes(number: int, fill_size: int = 0) -> bytes:
    if number < 0:
        raise ValueError("number must be non-negative")

    bytes_required = max(1, ceil(number.bit_length() / 8))
    return number.to_bytes(fill_size or bytes_required, "big")


def rsa_encrypt_bytes(data: bytes, exponent: int, modulus: int) -> list[int]:
    """Encrypt data one byte at a time with textbook RSA."""

    if modulus <= 255:
        raise ValueError("modulus must be larger than one byte")
    return [pow(byte, exponent, modulus) for byte in data]


def rsa_decrypt_bytes(cipher_blocks: list[int], exponent: int, modulus: int) -> bytes:
    decrypted = [pow(block, exponent, modulus) for block in cipher_blocks]
    if any(byte > 255 for byte in decrypted):
        raise ValueError("decrypted block does not fit in one byte")
    return bytes(decrypted)


def encode_cipher_blocks(cipher_blocks: list[int], modulus: int) -> str:
    """Encode fixed-width integer RSA blocks as base64."""

    width = (modulus.bit_length() + 7) // 8
    raw = b"".join(int_to_bytes(block, width) for block in cipher_blocks)
    return base64.b64encode(raw).decode("ascii")


def decode_cipher_blocks(encoded: str, modulus: int) -> list[int]:
    width = (modulus.bit_length() + 7) // 8
    raw = base64.b64decode(encoded.encode("ascii"))
    if len(raw) % width != 0:
        raise ValueError("encoded data does not align to RSA block width")
    return [bytes_to_int(raw[index : index + width]) for index in range(0, len(raw), width)]


def rsa_encrypt_text(message: str, exponent: int, modulus: int) -> str:
    blocks = rsa_encrypt_bytes(message.encode("utf-8"), exponent, modulus)
    return encode_cipher_blocks(blocks, modulus)


def rsa_decrypt_text(encoded: str, exponent: int, modulus: int) -> str:
    blocks = decode_cipher_blocks(encoded, modulus)
    return rsa_decrypt_bytes(blocks, exponent, modulus).decode("utf-8")

