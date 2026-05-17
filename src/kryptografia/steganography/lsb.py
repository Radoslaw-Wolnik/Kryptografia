"""Least-significant-bit steganography helpers."""

from __future__ import annotations


def text_to_bits(text: str) -> str:
    return "".join(f"{ord(char):08b}" for char in text)


def bits_to_text(bits: str) -> str:
    if len(bits) % 8 != 0:
        raise ValueError("bit length must be divisible by 8")

    chars = [chr(int(bits[index : index + 8], 2)) for index in range(0, len(bits), 8)]
    return "".join(chars)


def embed_message_lsb(carrier: bytes, message: str) -> bytes:
    """Embed a message into carrier bytes using least-significant bits."""

    message_bits = text_to_bits(message) + "00000000"
    if len(message_bits) > len(carrier):
        raise ValueError("carrier is too small for message")

    modified = bytearray(carrier)
    for index, bit in enumerate(message_bits):
        modified[index] = (modified[index] & 0b11111110) | int(bit)

    return bytes(modified)


def extract_message_lsb(carrier: bytes) -> str:
    bits = "".join(str(byte & 1) for byte in carrier)
    chars: list[str] = []

    for index in range(0, len(bits), 8):
        chunk = bits[index : index + 8]
        if len(chunk) < 8 or chunk == "00000000":
            break
        chars.append(chr(int(chunk, 2)))

    return "".join(chars)

