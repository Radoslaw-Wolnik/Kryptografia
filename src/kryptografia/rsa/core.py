"""Small integer RSA implementation for laboratory exercises."""

from __future__ import annotations

from dataclasses import dataclass

from kryptografia.number_theory import gcd, mod_inverse


@dataclass(frozen=True)
class RSAKeyPair:
    public_exponent: int
    private_exponent: int
    modulus: int


def generate_rsa_keypair(p: int, q: int, e: int = 65_537) -> RSAKeyPair:
    """Build an RSA key pair from supplied primes.

    The function assumes the caller supplies primes. It is intentionally educational and does
    not perform production-grade primality testing or key generation.
    """

    if p == q:
        raise ValueError("p and q must differ")

    modulus = p * q
    phi = (p - 1) * (q - 1)

    if gcd(e, phi) != 1:
        raise ValueError("e must be coprime with phi")

    return RSAKeyPair(public_exponent=e, private_exponent=mod_inverse(e, phi), modulus=modulus)


def rsa_encrypt(message: int, exponent: int, modulus: int) -> int:
    if message < 0:
        raise ValueError("message must be non-negative")
    if message >= modulus:
        raise ValueError("message must be smaller than modulus")

    return pow(message, exponent, modulus)


def rsa_decrypt(ciphertext: int, exponent: int, modulus: int) -> int:
    if ciphertext < 0:
        raise ValueError("ciphertext must be non-negative")

    return pow(ciphertext, exponent, modulus)

