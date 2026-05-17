import pytest

from kryptografia.steganography import (
    bits_to_text,
    embed_hex_line_endings,
    embed_message_lsb,
    extract_hex_line_endings,
    extract_message_lsb,
    hex_to_bits,
    text_to_bits,
)


def test_text_bit_round_trip() -> None:
    text = "hello"
    assert bits_to_text(text_to_bits(text)) == text


def test_embed_extract_round_trip() -> None:
    carrier = bytes([255] * 512)
    message = "secret"

    embedded = embed_message_lsb(carrier, message)

    assert extract_message_lsb(embedded) == message


def test_small_carrier_rejected() -> None:
    with pytest.raises(ValueError):
        embed_message_lsb(bytes([0] * 8), "this message is too large")


def test_html_line_ending_steganography_round_trip() -> None:
    carrier = "\n".join(f"<p>line {index}</p>" for index in range(16))
    message = "a5"

    watermark = embed_hex_line_endings(carrier, message)

    assert hex_to_bits(message) == "10100101"
    assert extract_hex_line_endings(watermark, len(message)) == message
