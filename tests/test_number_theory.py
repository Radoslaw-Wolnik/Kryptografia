import pytest

from kryptografia.number_theory import (
    aks_via_binomial,
    chinese_remainder,
    coprime,
    euler_phi,
    extended_gcd,
    fast_mod_exp,
    fermat_primality_test,
    gcd,
    mod_inverse,
)


def test_gcd() -> None:
    assert gcd(48, 18) == 6


def test_extended_gcd_identity() -> None:
    divisor, x, y = extended_gcd(240, 46)
    assert divisor == 2
    assert 240 * x + 46 * y == divisor


def test_mod_inverse() -> None:
    assert mod_inverse(17, 3120) == 2753


def test_coprime() -> None:
    assert coprime(17, 3120)
    assert not coprime(18, 3120)


def test_euler_phi() -> None:
    assert euler_phi(9) == 6
    assert euler_phi(10) == 4


def test_chinese_remainder() -> None:
    assert chinese_remainder([2, 3, 2], [3, 5, 7]) == 23


def test_chinese_remainder_rejects_non_coprime_moduli() -> None:
    with pytest.raises(ValueError):
        chinese_remainder([1, 2], [4, 6])


def test_fast_mod_exp_and_primality_helpers() -> None:
    assert fast_mod_exp(7, 128, 13) == pow(7, 128, 13)
    assert fermat_primality_test(13, bases=[2, 3])
    assert not fermat_primality_test(9, bases=[2])
    assert aks_via_binomial(7)
    assert not aks_via_binomial(9)
