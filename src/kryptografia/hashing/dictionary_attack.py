"""Dictionary attack helpers for hash labs."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from kryptografia.hashing.similarity import hash_similarity_percent, md5_hex


@dataclass(frozen=True)
class AttackResult:
    guess: str
    similarity: float
    exact_match: bool


def load_dictionary(words: Iterable[str] | str | Path) -> list[str]:
    """Load candidate words from an iterable or a text file path."""

    if isinstance(words, (str, Path)):
        candidates = Path(words).read_text(encoding="utf-8").splitlines()
    else:
        candidates = list(words)

    return [candidate.strip() for candidate in candidates if candidate.strip()]


def dictionary_attack(target_hash: str, candidates: Iterable[str] | str | Path) -> AttackResult:
    """Find the best dictionary candidate for a target MD5 hash."""

    dictionary = load_dictionary(candidates)
    if not dictionary:
        return AttackResult(guess="", similarity=0.0, exact_match=False)

    best_guess = ""
    best_similarity = -1.0
    exact_match = False

    for word in dictionary:
        candidate_hash = md5_hex(word)
        similarity = hash_similarity_percent(target_hash, candidate_hash)

        if similarity > best_similarity:
            best_similarity = similarity
            best_guess = word
            exact_match = similarity == 100.0

        if exact_match:
            break

    return AttackResult(guess=best_guess, similarity=best_similarity, exact_match=exact_match)

