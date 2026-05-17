from kryptografia.rsa import generate_rsa_keypair
from kryptografia.signatures import rsa_sign, rsa_verify, sha256_hex, verify_message_integrity


def test_sha256_hex() -> None:
    assert len(sha256_hex("hello")) == 64


def test_integrity() -> None:
    assert verify_message_integrity("hello", "hello")
    assert not verify_message_integrity("hello", "hullo")


def test_rsa_signature_round_trip() -> None:
    keys = generate_rsa_keypair(61, 53, e=17)
    message = "signed lab message"

    signature = rsa_sign(message, keys.private_exponent, keys.modulus)

    assert rsa_verify(message, signature, keys.public_exponent, keys.modulus)
    assert not rsa_verify("changed", signature, keys.public_exponent, keys.modulus)

