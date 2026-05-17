"""Vigenere cipher and educational analysis helpers."""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Iterable

from kryptografia.common.text import (
    affine_alphabet_index,
    affine_index_to_char,
    english_letters_only,
    is_english_letter,
)

ALPHABET_SIZE = 26
ENGLISH_FREQUENCIES = {
    "E": 12.70,
    "T": 9.06,
    "A": 8.17,
    "O": 7.51,
    "I": 6.97,
    "N": 6.75,
    "S": 6.33,
    "H": 6.09,
    "R": 5.99,
    "D": 4.25,
    "L": 4.03,
    "C": 2.78,
    "U": 2.76,
    "M": 2.41,
    "W": 2.36,
    "F": 2.23,
    "G": 2.02,
    "Y": 1.97,
    "P": 1.93,
    "B": 1.49,
    "V": 0.98,
    "K": 0.77,
    "J": 0.15,
    "X": 0.15,
    "Q": 0.10,
    "Z": 0.07,
}


def _key_shifts(key: str) -> list[int]:
    shifts: list[int] = []
    for char in key:
        if not is_english_letter(char):
            raise ValueError("Vigenere keys must contain only English letters")
        shifts.append(affine_alphabet_index(char))
    if not shifts:
        raise ValueError("Vigenere key cannot be empty")
    return shifts


def _shift_char(char: str, shift: int) -> str:
    if not is_english_letter(char):
        return char
    index = affine_alphabet_index(char)
    transformed = (index + shift) % ALPHABET_SIZE
    return affine_index_to_char(transformed, uppercase=char.isupper())


def vigenere_encrypt(text: str, key: str) -> str:
    """Encrypt text with the Vigenere cipher."""

    shifts = _key_shifts(key)
    result: list[str] = []
    key_index = 0
    for char in text:
        if not is_english_letter(char):
            result.append(char)
            continue
        result.append(_shift_char(char, shifts[key_index % len(shifts)]))
        key_index += 1
    return "".join(result)


def vigenere_decrypt(text: str, key: str) -> str:
    """Decrypt text with the Vigenere cipher."""

    shifts = _key_shifts(key)
    result: list[str] = []
    key_index = 0
    for char in text:
        if not is_english_letter(char):
            result.append(char)
            continue
        result.append(_shift_char(char, -shifts[key_index % len(shifts)]))
        key_index += 1
    return "".join(result)


def repeated_substrings(
    text: str, min_length: int = 3, max_length: int | None = None
) -> dict[str, list[int]]:
    """Find repeated substrings and their starting positions."""

    sanitized = english_letters_only(text).upper()
    if max_length is None:
        max_length = max(min_length, min(12, len(sanitized)))
    if min_length < 2:
        raise ValueError("min_length must be at least 2")
    if max_length < min_length:
        raise ValueError("max_length must be >= min_length")

    occurrences: defaultdict[str, list[int]] = defaultdict(list)
    for length in range(min_length, max_length + 1):
        for start in range(0, len(sanitized) - length + 1):
            substring = sanitized[start : start + length]
            occurrences[substring].append(start)
    return {substring: starts for substring, starts in occurrences.items() if len(starts) > 1}


def kasiski_candidate_key_lengths(
    text: str, min_length: int = 3, max_length: int | None = None
) -> list[int]:
    """Return likely key lengths using a simple Kasiski examination."""

    repeated = repeated_substrings(text, min_length=min_length, max_length=max_length)
    if not repeated:
        return []

    counts: Counter[int] = Counter()
    for starts in repeated.values():
        if len(starts) < 2:
            continue
        for i in range(len(starts)):
            for j in range(i + 1, len(starts)):
                distance = starts[j] - starts[i]
                for divisor in _divisors(distance):
                    if divisor >= min_length:
                        counts[divisor] += 1

    return [length for length, _ in counts.most_common()]


def _divisors(number: int) -> list[int]:
    if number <= 0:
        return []

    divisors: set[int] = set()
    limit = int(number**0.5)
    for candidate in range(1, limit + 1):
        if number % candidate == 0:
            divisors.add(candidate)
            divisors.add(number // candidate)
    return sorted(divisors)


def _chi_squared_score(segment: str) -> float:
    letter_counts = Counter(char.upper() for char in segment if is_english_letter(char))
    total = sum(letter_counts.values())
    if total == 0:
        return float("inf")

    score = 0.0
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        observed = letter_counts.get(letter, 0)
        expected = total * (ENGLISH_FREQUENCIES[letter] / 100.0)
        if expected > 0:
            score += ((observed - expected) ** 2) / expected
    return score


def _best_shift_for_segment(segment: str) -> int:
    best_shift = 0
    best_score = float("inf")
    for shift in range(ALPHABET_SIZE):
        decrypted = "".join(_shift_char(char, -shift) for char in segment)
        score = _chi_squared_score(decrypted)
        if score < best_score:
            best_score = score
            best_shift = shift
    return best_shift


def guess_vigenere_key(text: str, key_length: int) -> str:
    """Guess a Vigenere key using chi-squared scoring against English frequencies."""

    if key_length <= 0:
        raise ValueError("key_length must be positive")

    letters = [char.upper() for char in text if is_english_letter(char)]
    if len(letters) < key_length:
        raise ValueError("text is too short for the requested key length")

    columns = ["" for _ in range(key_length)]
    for index, char in enumerate(letters):
        columns[index % key_length] += char

    shifts = [_best_shift_for_segment(column) for column in columns]
    return "".join(affine_index_to_char(shift, uppercase=True) for shift in shifts)


def dictionary_attack(
    text: str,
    candidate_keys: Iterable[str],
    *,
    minimum_word_ratio: float = 0.69,
) -> str | None:
    """Try candidate keys and return the first one that looks readable."""

    best_key: str | None = None
    best_ratio = 0.0
    for key in candidate_keys:
        try:
            decrypted = vigenere_decrypt(text, key)
        except ValueError:
            continue

        words = [word for word in decrypted.upper().split() if word]
        if not words:
            continue
        ratio = sum(1 for word in words if word.isalpha()) / len(words)
        if ratio >= minimum_word_ratio:
            return key
        if ratio > best_ratio:
            best_ratio = ratio
            best_key = key

    return best_key
