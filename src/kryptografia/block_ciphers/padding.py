"""Padding helpers for block-cipher labs."""

from __future__ import annotations


def pkcs7_pad(data: bytes, block_size: int) -> bytes:
    """Pad data using PKCS#7."""

    if block_size <= 0 or block_size > 255:
        raise ValueError("block_size must be in range 1..255")

    padding_length = block_size - (len(data) % block_size)
    return data + bytes([padding_length]) * padding_length


def pkcs7_unpad(data: bytes, block_size: int) -> bytes:
    """Remove PKCS#7 padding."""

    if block_size <= 0 or block_size > 255:
        raise ValueError("block_size must be in range 1..255")
    if not data:
        raise ValueError("data must not be empty")
    if len(data) % block_size != 0:
        raise ValueError("data length must be divisible by block size")

    padding_length = data[-1]
    if padding_length == 0 or padding_length > block_size:
        raise ValueError("invalid padding")

    expected = bytes([padding_length]) * padding_length
    if data[-padding_length:] != expected:
        raise ValueError("invalid padding")

    return data[:-padding_length]

