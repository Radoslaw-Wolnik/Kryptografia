"""HTML/text whitespace steganography helpers."""

from __future__ import annotations


def hex_to_bits(hex_message: str) -> str:
    normalized = hex_message.strip().lower()
    if normalized.startswith("0x"):
        normalized = normalized[2:]
    if any(char not in "0123456789abcdef" for char in normalized):
        raise ValueError("message must be hexadecimal")
    return "".join(f"{int(char, 16):04b}" for char in normalized)


def bits_to_hex(bits: str) -> str:
    if len(bits) % 4 != 0:
        raise ValueError("bit length must be divisible by 4")
    return "".join(f"{int(bits[index : index + 4], 2):x}" for index in range(0, len(bits), 4))


def embed_bits_line_endings(carrier: str, bits: str) -> str:
    """Encode 1 bits as one trailing space per line and 0 bits as no trailing space."""

    lines = [line.rstrip(" ") for line in carrier.splitlines()]
    if len(bits) > len(lines):
        raise ValueError("carrier has too few lines for message bits")
    if set(bits) - {"0", "1"}:
        raise ValueError("bits may contain only 0 and 1")

    encoded = lines[:]
    for index, bit in enumerate(bits):
        if bit == "1":
            encoded[index] += " "
    return "\n".join(encoded)


def extract_bits_line_endings(watermark: str, bit_count: int) -> str:
    if bit_count < 0:
        raise ValueError("bit_count must be non-negative")

    lines = watermark.splitlines()
    if bit_count > len(lines):
        raise ValueError("watermark has fewer lines than requested bits")
    return "".join("1" if lines[index].endswith(" ") else "0" for index in range(bit_count))


def embed_hex_line_endings(carrier: str, hex_message: str) -> str:
    return embed_bits_line_endings(carrier, hex_to_bits(hex_message))


def extract_hex_line_endings(watermark: str, hex_length: int) -> str:
    return bits_to_hex(extract_bits_line_endings(watermark, hex_length * 4))

