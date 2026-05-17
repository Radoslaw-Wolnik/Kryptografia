"""Encoding helpers for text, bytes, and bit strings."""

from __future__ import annotations

from kryptografia.common.exceptions import EncodingError


def text_to_bytes(text: str) -> bytes:
    try:
        return text.encode("utf-8")
    except UnicodeEncodeError as error:
        raise EncodingError(str(error)) from error


def bytes_to_text(data: bytes) -> str:
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise EncodingError(str(error)) from error


def text_to_bits(text: str) -> str:
    return "".join(f"{byte:08b}" for byte in text_to_bytes(text))


def bits_to_text(bits: str) -> str:
    if len(bits) % 8 != 0:
        raise EncodingError("bit length must be divisible by 8")

    data = bytes(int(bits[index : index + 8], 2) for index in range(0, len(bits), 8))
    return bytes_to_text(data)

