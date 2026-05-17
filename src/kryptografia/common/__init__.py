"""Shared helpers for the educational cryptography package."""

from kryptografia.common.bytes import chunk_bytes, pad_zero_bytes
from kryptografia.common.encodings import bits_to_text, bytes_to_text, text_to_bits, text_to_bytes
from kryptografia.common.exceptions import (
    CryptographyMathError,
    EncodingError,
    KryptografiaError,
    ValidationError,
)
from kryptografia.common.modular import extended_gcd, gcd, mod_inverse, normalize_mod
from kryptografia.common.text import (
    affine_alphabet_index,
    affine_index_to_char,
    bytes_to_escape_string,
    english_letters_only,
    escape_string_to_bytes,
    is_english_letter,
)
from kryptografia.common.xor import repeating_key_xor, xor_bytes

__all__ = [
    "CryptographyMathError",
    "EncodingError",
    "KryptografiaError",
    "ValidationError",
    "affine_alphabet_index",
    "affine_index_to_char",
    "bits_to_text",
    "bytes_to_escape_string",
    "bytes_to_text",
    "chunk_bytes",
    "english_letters_only",
    "escape_string_to_bytes",
    "extended_gcd",
    "gcd",
    "is_english_letter",
    "mod_inverse",
    "normalize_mod",
    "pad_zero_bytes",
    "repeating_key_xor",
    "text_to_bits",
    "text_to_bytes",
    "xor_bytes",
]

