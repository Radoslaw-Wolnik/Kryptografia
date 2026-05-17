from kryptografia.classical.vigenere import (
    guess_vigenere_key,
    kasiski_candidate_key_lengths,
    vigenere_decrypt,
    vigenere_encrypt,
)


def test_vigenere_roundtrip_preserves_punctuation_and_case() -> None:
    plaintext = "We are discovered. Flee at once!"
    key = "LEMON"

    ciphertext = vigenere_encrypt(plaintext, key)
    assert ciphertext == "Hi mfr omeqbgidsq. Qpqs ne szqr!"
    assert vigenere_decrypt(ciphertext, key) == plaintext


def test_kasiski_finds_repeated_structure() -> None:
    plaintext = "WEAREDISCOVEREDWEAREDISCOVERED"
    ciphertext = vigenere_encrypt(plaintext, "CAT")

    candidates = kasiski_candidate_key_lengths(ciphertext)
    assert 3 in candidates


def test_guess_key_recovers_known_key_length() -> None:
    plaintext = (
        "WHEN IN THE COURSE OF HUMAN EVENTS IT BECOMES NECESSARY "
        "WHEN IN THE COURSE OF HUMAN EVENTS IT BECOMES NECESSARY "
        "WHEN IN THE COURSE OF HUMAN EVENTS IT BECOMES NECESSARY "
    )
    key = "LEMON"
    ciphertext = vigenere_encrypt(plaintext, key)

    guessed = guess_vigenere_key(ciphertext, len(key))
    assert guessed == key

