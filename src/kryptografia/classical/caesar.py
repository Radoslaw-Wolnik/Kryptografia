"""Caesar-cipher helpers used by the first classical-cryptography lab."""

from __future__ import annotations

from kryptografia.common.text import affine_alphabet_index, affine_index_to_char, is_english_letter


def caesar_encrypt(text: str, shift: int) -> str:
    """Encrypt text with a standard 26-letter Caesar shift."""

    result: list[str] = []
    for char in text:
        if not is_english_letter(char):
            result.append(char)
            continue

        shifted = (affine_alphabet_index(char) + shift) % 26
        result.append(affine_index_to_char(shifted, uppercase=char.isupper()))
    return "".join(result)


def caesar_decrypt(text: str, shift: int) -> str:
    """Decrypt text encrypted by :func:`caesar_encrypt`."""

    return caesar_encrypt(text, -shift)


def caesar_shift_from_pair(plain_char: str, cipher_char: str) -> int:
    """Recover a Caesar shift from one known plaintext/ciphertext letter pair."""

    return (affine_alphabet_index(cipher_char) - affine_alphabet_index(plain_char)) % 26


def recover_caesar_shift(plain_text: str, cipher_text: str) -> int:
    """Recover and validate a Caesar shift from matching samples."""

    shift: int | None = None
    for plain_char, cipher_char in zip(plain_text, cipher_text, strict=False):
        if not (is_english_letter(plain_char) and is_english_letter(cipher_char)):
            continue

        candidate = caesar_shift_from_pair(plain_char, cipher_char)
        if shift is None:
            shift = candidate
        elif shift != candidate:
            raise ValueError("samples are not consistent with a single Caesar shift")

    if shift is None:
        raise ValueError("at least one alphabetic character pair is required")
    return shift

