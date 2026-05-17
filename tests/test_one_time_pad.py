import pytest

from kryptografia.common.text import bytes_to_escape_string, escape_string_to_bytes
from kryptografia.one_time_pad.xor import generate_key, otp_decrypt, otp_encrypt, xor_bytes


def test_xor_round_trip() -> None:
    plaintext = b"attack at dawn"
    key = b"\x10" * len(plaintext)
    ciphertext = otp_encrypt(plaintext, key)
    assert otp_decrypt(ciphertext, key) == plaintext


def test_xor_requires_equal_length() -> None:
    with pytest.raises(ValueError):
        xor_bytes(b"abc", b"de")


def test_escape_helpers_round_trip() -> None:
    original = b"line1\nline2\t\x07\xff"
    escaped = bytes_to_escape_string(original)
    assert escape_string_to_bytes(escaped) == original


def test_generate_key_length() -> None:
    key = generate_key(32)
    assert isinstance(key, bytes)
    assert len(key) == 32

