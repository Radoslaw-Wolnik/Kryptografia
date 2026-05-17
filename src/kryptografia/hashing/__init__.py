"""Hashing lab helpers."""

from kryptografia.hashing.credentials import (
    CredentialRecord,
    change_password,
    check_credentials,
    hash_password,
    register_user,
)
from kryptografia.hashing.dictionary_attack import AttackResult, dictionary_attack, load_dictionary
from kryptografia.hashing.similarity import (
    hash_similarity_percent,
    hash_to_bits,
    md5_hex,
    normalize_hash,
)

__all__ = [
    "AttackResult",
    "CredentialRecord",
    "change_password",
    "check_credentials",
    "dictionary_attack",
    "hash_password",
    "hash_similarity_percent",
    "hash_to_bits",
    "load_dictionary",
    "md5_hex",
    "normalize_hash",
    "register_user",
]

