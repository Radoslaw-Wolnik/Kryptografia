"""Number-theory algorithms for cryptography exercises."""

from __future__ import annotations

from collections.abc import Sequence

from kryptografia.common.modular import gcd, mod_inverse


def coprime(a: int, b: int) -> bool:
    return gcd(a, b) == 1


def euler_phi(number: int) -> int:
    """Compute Euler's totient function by trial division."""

    if number <= 0:
        raise ValueError("number must be positive")

    result = number
    candidate = 2
    remaining = number
    while candidate * candidate <= remaining:
        if remaining % candidate == 0:
            while remaining % candidate == 0:
                remaining //= candidate
            result -= result // candidate
        candidate += 1

    if remaining > 1:
        result -= result // remaining

    return result


def chinese_remainder(remainders: Sequence[int], moduli: Sequence[int]) -> int:
    """Solve a CRT system for pairwise-coprime moduli."""

    if len(remainders) != len(moduli):
        raise ValueError("remainders and moduli must have the same length")
    if not remainders:
        raise ValueError("at least one congruence is required")

    product = 1
    for modulus in moduli:
        if modulus <= 0:
            raise ValueError("moduli must be positive")
        product *= modulus

    total = 0
    for index, (remainder, modulus) in enumerate(zip(remainders, moduli, strict=True)):
        for other in moduli[index + 1 :]:
            if gcd(modulus, other) != 1:
                raise ValueError("moduli must be pairwise coprime")

        partial = product // modulus
        total += remainder * mod_inverse(partial, modulus) * partial

    return total % product
