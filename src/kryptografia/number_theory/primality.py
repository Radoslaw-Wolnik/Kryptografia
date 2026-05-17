"""Primality helpers used by the RSA lab."""

from __future__ import annotations

import random
from collections.abc import Iterable

from kryptografia.common.modular import gcd


def fast_mod_exp(base: int, exponent: int, modulus: int) -> int:
    """Compute ``base ** exponent mod modulus`` by repeated squaring."""

    if exponent < 0:
        raise ValueError("exponent must be non-negative")
    if modulus <= 0:
        raise ValueError("modulus must be positive")

    result = 1
    base %= modulus
    while exponent:
        if exponent & 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2
    return result


def fermat_primality_test(number: int, bases: Iterable[int] | None = None, rounds: int = 5) -> bool:
    """Return whether ``number`` is probably prime according to Fermat tests."""

    if number < 2:
        return False
    if number in (2, 3):
        return True
    if number % 2 == 0:
        return False

    tested_bases = (
        list(bases) if bases is not None else [random.randint(2, number - 2) for _ in range(rounds)]
    )
    for base in tested_bases:
        if gcd(number, base) != 1:
            return False
        if fast_mod_exp(base, number - 1, number) != 1:
            return False
    return True


def aks_via_binomial(number: int) -> bool:
    """Tiny binomial-coefficient primality check from the original lab.

    This is educational and intentionally inefficient.
    """

    if number < 2:
        return False

    coefficients = [1]
    for i in range(number):
        coefficients.append(1)
        for j in range(i, 0, -1):
            coefficients[j] = coefficients[j - 1] - coefficients[j]
        coefficients[0] = -coefficients[0]

    coefficients[0] += 1
    coefficients[-1] -= 1
    return all(coefficient % number == 0 for coefficient in coefficients)
