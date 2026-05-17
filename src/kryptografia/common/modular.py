"""Reusable modular-arithmetic helpers."""

from __future__ import annotations


def normalize_mod(value: int, modulus: int) -> int:
    """Return value normalized into the range [0, modulus)."""

    if modulus <= 0:
        raise ValueError("modulus must be positive")
    return value % modulus


def gcd(a: int, b: int) -> int:
    """Greatest common divisor using Euclid's algorithm."""

    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Return ``(g, x, y)`` such that ``a*x + b*y == g == gcd(a, b)``."""

    old_r, r = abs(a), abs(b)
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    x = old_s if a >= 0 else -old_s
    y = old_t if b >= 0 else -old_t
    return old_r, x, y


def mod_inverse(value: int, modulus: int) -> int:
    """Return the multiplicative inverse of ``value`` modulo ``modulus``."""

    if modulus <= 0:
        raise ValueError("modulus must be positive")

    divisor, coefficient, _ = extended_gcd(value, modulus)
    if divisor != 1:
        raise ValueError(f"{value} has no inverse modulo {modulus}")
    return coefficient % modulus

