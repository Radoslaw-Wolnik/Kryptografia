"""Byte sequence helpers."""

from __future__ import annotations

from collections.abc import Iterator


def chunk_bytes(data: bytes, size: int) -> Iterator[bytes]:
    if size <= 0:
        raise ValueError("size must be positive")

    for index in range(0, len(data), size):
        yield data[index : index + size]


def pad_zero_bytes(data: bytes, size: int) -> bytes:
    if size <= 0:
        raise ValueError("size must be positive")

    padding = (-len(data)) % size
    return data + bytes(padding)

