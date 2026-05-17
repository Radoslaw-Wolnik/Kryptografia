"""Affine cipher implementation used by the classical-crypto lab."""

from __future__ import annotations

from kryptografia.common.modular import gcd, mod_inverse, normalize_mod
from kryptografia.common.text import affine_alphabet_index, affine_index_to_char, is_english_letter

MODULUS = 26


def _transform_char(char: str, a: int, b: int) -> str:
    if not is_english_letter(char):
        return char

    index = affine_alphabet_index(char)
    transformed = normalize_mod(a * index + b, MODULUS)
    return affine_index_to_char(transformed, uppercase=char.isupper())


def affine_encrypt(text: str, a: int, b: int) -> str:
    """Encrypt text with the affine cipher."""

    if gcd(a, MODULUS) != 1:
        raise ValueError(f"a={a} is not invertible modulo {MODULUS}")

    return "".join(_transform_char(char, a, b) for char in text)


def affine_decrypt(text: str, a: int, b: int) -> str:
    """Decrypt text with the affine cipher."""

    inverse_a = mod_inverse(a, MODULUS)
    return "".join(_transform_char(char, inverse_a, -inverse_a * b) for char in text)


def recover_affine_key(plain_text: str, cipher_text: str) -> tuple[int, int]:
    """Recover a valid key pair ``(a, b)`` from matching samples."""

    pairs: list[tuple[int, int]] = []
    for plain_char, cipher_char in zip(plain_text, cipher_text, strict=False):
        if not (is_english_letter(plain_char) and is_english_letter(cipher_char)):
            continue

        plain_index = affine_alphabet_index(plain_char)
        cipher_index = affine_alphabet_index(cipher_char)
        pairs.append((plain_index, cipher_index))
        if len(pairs) == 2 and pairs[0][0] != pairs[1][0]:
            break

    if len(pairs) < 2:
        raise ValueError("Need at least two distinct alphabetic character pairs")

    (x1, y1), (x2, y2) = pairs[0], pairs[1]
    delta_x = normalize_mod(x1 - x2, MODULUS)
    delta_y = normalize_mod(y1 - y2, MODULUS)

    inverse_delta_x = mod_inverse(delta_x, MODULUS)
    a = normalize_mod(delta_y * inverse_delta_x, MODULUS)
    b = normalize_mod(y1 - a * x1, MODULUS)

    if gcd(a, MODULUS) != 1:
        raise ValueError("Recovered key is not valid")

    return a, b

