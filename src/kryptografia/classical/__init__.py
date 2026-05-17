"""Classical cipher implementations."""

from kryptografia.classical.affine import affine_decrypt, affine_encrypt, recover_affine_key
from kryptografia.classical.caesar import (
    caesar_decrypt,
    caesar_encrypt,
    caesar_shift_from_pair,
    recover_caesar_shift,
)
from kryptografia.classical.vigenere import (
    dictionary_attack,
    guess_vigenere_key,
    kasiski_candidate_key_lengths,
    repeated_substrings,
    vigenere_decrypt,
    vigenere_encrypt,
)

__all__ = [
    "affine_decrypt",
    "affine_encrypt",
    "caesar_decrypt",
    "caesar_encrypt",
    "caesar_shift_from_pair",
    "dictionary_attack",
    "guess_vigenere_key",
    "kasiski_candidate_key_lengths",
    "recover_affine_key",
    "recover_caesar_shift",
    "repeated_substrings",
    "vigenere_decrypt",
    "vigenere_encrypt",
]

