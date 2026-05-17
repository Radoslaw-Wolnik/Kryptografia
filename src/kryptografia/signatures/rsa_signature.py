"""Educational textbook-RSA signature helpers."""

from __future__ import annotations

from kryptografia.signatures.digest import sha256_hex


def rsa_sign(message: str | bytes, private_exponent: int, modulus: int) -> int:
    """Sign a digest with textbook RSA.

    This deliberately omits real signature padding and exists only for lab demonstrations.
    """

    digest_int = int(sha256_hex(message), 16)
    return pow(digest_int, private_exponent, modulus)


def rsa_verify(message: str | bytes, signature: int, public_exponent: int, modulus: int) -> bool:
    expected = int(sha256_hex(message), 16) % modulus
    return pow(signature, public_exponent, modulus) == expected

