import pytest

from kryptografia.hashing.credentials import (
    change_password,
    check_credentials,
    hash_password,
    register_user,
)
from kryptografia.hashing.dictionary_attack import dictionary_attack, load_dictionary
from kryptografia.hashing.similarity import (
    hash_similarity_percent,
    hash_to_bits,
    md5_hex,
    normalize_hash,
)


def test_normalize_hash() -> None:
    assert normalize_hash("  0xABCD  ") == "abcd"


def test_hash_to_bits_length() -> None:
    bits = hash_to_bits("abcd")
    assert len(bits) == 16


def test_similarity_exact_match() -> None:
    assert hash_similarity_percent("abcd", "abcd") == 100.0


def test_similarity_length_mismatch() -> None:
    with pytest.raises(ValueError):
        hash_similarity_percent("abcd", "abcdef")


def test_md5_hex() -> None:
    assert md5_hex("secret") == "5ebe2294ecd0e0f08eab7690d2a6ee69"


def test_dictionary_attack_finds_exact_match() -> None:
    dictionary = ["alpha", "beta", "gamma", "secret"]
    target = md5_hex("secret")

    result = dictionary_attack(target, dictionary)

    assert result.guess == "secret"
    assert result.exact_match is True
    assert result.similarity == 100.0


def test_dictionary_attack_handles_no_candidates() -> None:
    result = dictionary_attack("abcd", [])
    assert result.guess == ""
    assert result.similarity == 0.0
    assert result.exact_match is False


def test_load_dictionary_strips_empty_lines(tmp_path) -> None:
    path = tmp_path / "words.txt"
    path.write_text("\nalpha\n\n beta \n", encoding="utf-8")

    assert load_dictionary(path) == ["alpha", "beta"]


def test_credential_store_workflow() -> None:
    records = register_user([], "alice", "correct horse", salt="lab")

    assert check_credentials(records, "alice", "correct horse")
    assert not check_credentials(records, "alice", "wrong")
    assert records[0].password_hash == hash_password("correct horse", "lab")

    records = change_password(records, "alice", "correct horse", "new secret")

    assert check_credentials(records, "alice", "new secret")
    assert not check_credentials(records, "alice", "correct horse")


def test_duplicate_registration_rejected() -> None:
    records = register_user([], "alice", "pw")

    with pytest.raises(ValueError):
        register_user(records, "alice", "other")
