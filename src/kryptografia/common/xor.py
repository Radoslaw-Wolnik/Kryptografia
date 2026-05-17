"""Shared XOR helpers."""

from __future__ import annotations

from kryptografia.common.validation import ensure_non_empty


def xor_bytes(left: bytes, right: bytes) -> bytes:
    """XOR two equal-length byte strings."""

    if not isinstance(left, (bytes, bytearray)) or not isinstance(right, (bytes, bytearray)):
        raise TypeError("left and right must be bytes-like")

    left_b = bytes(left)
    right_b = bytes(right)
    if len(left_b) != len(right_b):
        raise ValueError("xor_bytes requires inputs of the same length")

    return bytes(a ^ b for a, b in zip(left_b, right_b, strict=True))


def repeating_key_xor(plaintext: bytes, key: bytes) -> bytes:
    """XOR data with a repeating key."""

    ensure_non_empty(key, "key")
    return bytes(byte ^ key[index % len(key)] for index, byte in enumerate(plaintext))
