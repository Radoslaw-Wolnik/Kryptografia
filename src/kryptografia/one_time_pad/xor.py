"""One-time-pad helpers."""

from __future__ import annotations

import secrets
from dataclasses import dataclass

from kryptografia.common.text import bytes_to_escape_string, escape_string_to_bytes
from kryptografia.common.xor import xor_bytes


def generate_key(length: int) -> bytes:
    """Generate a random key of the requested length."""

    if not isinstance(length, int):
        raise TypeError("length must be an integer")
    if length < 0:
        raise ValueError("length must be non-negative")
    return secrets.token_bytes(length)


def otp_encrypt(plaintext: bytes, key: bytes) -> bytes:
    """Encrypt plaintext using a one-time-pad key of the same length."""

    return xor_bytes(plaintext, key)


def otp_decrypt(ciphertext: bytes, key: bytes) -> bytes:
    """Decrypt one-time-pad ciphertext using the same XOR operation."""

    return xor_bytes(ciphertext, key)


@dataclass(frozen=True)
class EncodedBytes:
    """Convenience wrapper for the original lab-style escaped text format."""

    raw: bytes

    @classmethod
    def from_escape_string(cls, text: str) -> EncodedBytes:
        return cls(escape_string_to_bytes(text))

    def to_escape_string(self) -> str:
        return bytes_to_escape_string(self.raw)

