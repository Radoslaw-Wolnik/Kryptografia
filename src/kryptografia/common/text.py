"""Text helpers shared by the classical and byte-oriented labs."""

from __future__ import annotations

import ast
import re


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def remove_non_letters(text: str) -> str:
    return "".join(character for character in text if character.isalpha())


def uppercase_letters(text: str) -> str:
    return text.upper()


def is_english_letter(char: str) -> bool:
    return len(char) == 1 and "a" <= char.lower() <= "z"


def english_letters_only(text: str) -> str:
    """Return only ASCII letters from text, preserving order and case."""

    return "".join(char for char in text if is_english_letter(char))


def affine_alphabet_index(char: str) -> int:
    if not is_english_letter(char):
        raise ValueError(f"Expected an English alphabet letter, got {char!r}")
    return ord(char.lower()) - ord("a")


def affine_index_to_char(index: int, uppercase: bool = False) -> str:
    base = ord("A") if uppercase else ord("a")
    return chr(base + index)


def escape_string_to_bytes(text: str) -> bytes:
    """Parse a Python-style escaped string into bytes."""

    if not isinstance(text, str):
        raise TypeError("text must be a string")

    try:
        value = ast.literal_eval(f"'{text}'")
    except (SyntaxError, ValueError) as exc:
        raise ValueError("invalid escape string") from exc

    if not isinstance(value, str):
        raise ValueError("invalid escape string")

    return value.encode("latin1", errors="strict")


def bytes_to_escape_string(data: bytes) -> str:
    """Render bytes using printable ASCII plus escape sequences."""

    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes-like")

    parts: list[str] = []
    for byte in bytes(data):
        if byte == 0x0A:
            parts.append("\\n")
        elif byte == 0x09:
            parts.append("\\t")
        elif byte == 0x0D:
            parts.append("\\r")
        elif byte == 0x07:
            parts.append("\\a")
        elif byte == 0x5C:
            parts.append("\\\\")
        elif byte == 0x22:
            parts.append('\\"')
        elif byte == 0x27:
            parts.append("\\'")
        elif 32 <= byte <= 126:
            parts.append(chr(byte))
        else:
            parts.append(f"\\x{byte:02x}")
    return "".join(parts)

