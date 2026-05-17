"""Digest helpers for signature labs."""

from __future__ import annotations

import hashlib


def sha256_hex(message: str | bytes) -> str:
    data = message if isinstance(message, bytes) else message.encode("utf-8")
    return hashlib.sha256(data).hexdigest()

