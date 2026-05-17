"""Message-integrity helpers."""

from __future__ import annotations

from kryptografia.signatures.digest import sha256_hex


def verify_message_integrity(original: str | bytes, received: str | bytes) -> bool:
    return sha256_hex(original) == sha256_hex(received)

