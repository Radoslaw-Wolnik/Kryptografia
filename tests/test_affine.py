import pytest

from kryptografia.classical import caesar_decrypt, caesar_encrypt, recover_caesar_shift
from kryptografia.classical.affine import affine_decrypt, affine_encrypt, recover_affine_key


def test_caesar_round_trip_and_shift_recovery() -> None:
    plaintext = "Attack at Dawn!"
    ciphertext = caesar_encrypt(plaintext, 3)

    assert ciphertext == "Dwwdfn dw Gdzq!"
    assert caesar_decrypt(ciphertext, 3) == plaintext
    assert recover_caesar_shift(plaintext, ciphertext) == 3


def test_affine_round_trip_preserves_non_letters_and_case() -> None:
    text = "Hello, World!"
    cipher = affine_encrypt(text, a=5, b=8)
    assert cipher == "Rclla, Oaplx!"
    assert affine_decrypt(cipher, a=5, b=8) == text


def test_affine_encrypt_rejects_non_invertible_a() -> None:
    with pytest.raises(ValueError):
        affine_encrypt("test", a=13, b=2)


def test_recover_affine_key_from_sample_text() -> None:
    plain = "Hello, World!"
    cipher = affine_encrypt(plain, a=5, b=8)
    assert recover_affine_key(plain, cipher) == (5, 8)
