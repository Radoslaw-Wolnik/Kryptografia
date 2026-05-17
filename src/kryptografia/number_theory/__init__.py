"""Number-theory helpers used across cryptography labs."""

from kryptografia.common.modular import extended_gcd, gcd, mod_inverse
from kryptografia.number_theory.euclid import chinese_remainder, coprime, euler_phi
from kryptografia.number_theory.primality import (
    aks_via_binomial,
    fast_mod_exp,
    fermat_primality_test,
)

__all__ = [
    "aks_via_binomial",
    "chinese_remainder",
    "coprime",
    "euler_phi",
    "extended_gcd",
    "fast_mod_exp",
    "fermat_primality_test",
    "gcd",
    "mod_inverse",
]
