"""Hash normalization and bit-similarity helpers."""

from __future__ import annotations

import hashlib
import re

_HEX_RE = re.compile(r"^[0-9a-fA-F]+$")


def normalize_hash(value: str) -> str:
    """Normalize a hexadecimal hash string for comparison."""

    if not isinstance(value, str):
        raise TypeError("value must be a string")

    normalized = value.strip().lower()
    if normalized.startswith("0x"):
        normalized = normalized[2:]

    if len(normalized) == 0 or len(normalized) % 2 != 0 or not _HEX_RE.fullmatch(normalized):
        raise ValueError("value must be a hexadecimal string with even length")

    return normalized


def hash_to_bits(value: str) -> str:
    """Convert a hexadecimal hash to a bit string."""

    normalized = normalize_hash(value)
    return "".join(f"{int(normalized[i : i + 2], 16):08b}" for i in range(0, len(normalized), 2))


def hash_similarity_percent(left: str, right: str) -> float:
    """Return percent of matching bit positions between two hex hashes."""

    left_bits = hash_to_bits(left)
    right_bits = hash_to_bits(right)

    if len(left_bits) != len(right_bits):
        raise ValueError("hashes must have the same length")

    matches = sum(1 for a, b in zip(left_bits, right_bits, strict=True) if a == b)
    return (matches / len(left_bits)) * 100.0


def md5_hex(data: str) -> str:
    """Compute an MD5 digest in hexadecimal form."""

    if not isinstance(data, str):
        raise TypeError("data must be a string")
    return hashlib.md5(data.encode("utf-8")).hexdigest()

