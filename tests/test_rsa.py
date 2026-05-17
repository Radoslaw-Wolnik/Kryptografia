import pytest

from kryptografia.rsa import (
    decode_cipher_blocks,
    encode_cipher_blocks,
    generate_rsa_keypair,
    rsa_decrypt,
    rsa_decrypt_text,
    rsa_encrypt,
    rsa_encrypt_text,
)


def test_rsa_round_trip() -> None:
    keys = generate_rsa_keypair(61, 53)
    message = 123

    ciphertext = rsa_encrypt(message, keys.public_exponent, keys.modulus)
    recovered = rsa_decrypt(ciphertext, keys.private_exponent, keys.modulus)

    assert recovered == message


def test_message_must_fit_modulus() -> None:
    keys = generate_rsa_keypair(61, 53)

    with pytest.raises(ValueError):
        rsa_encrypt(keys.modulus, keys.public_exponent, keys.modulus)


def test_equal_primes_rejected() -> None:
    with pytest.raises(ValueError):
        generate_rsa_keypair(11, 11)


def test_rsa_text_blocks_round_trip() -> None:
    keys = generate_rsa_keypair(61, 53)
    message = "Hello RSA!"

    encoded = rsa_encrypt_text(message, keys.public_exponent, keys.modulus)

    assert rsa_decrypt_text(encoded, keys.private_exponent, keys.modulus) == message


def test_cipher_block_encoding_round_trip() -> None:
    blocks = [1, 255, 1024]
    encoded = encode_cipher_blocks(blocks, 3233)

    assert decode_cipher_blocks(encoded, 3233) == blocks
