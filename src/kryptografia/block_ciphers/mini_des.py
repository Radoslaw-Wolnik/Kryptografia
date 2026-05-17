"""Mini-DES style bit-block helpers from the block-cipher lab."""

from __future__ import annotations

from collections.abc import Sequence


def rotate_key(key: str, position: int) -> str:
    if not key:
        raise ValueError("key must not be empty")
    position %= len(key)
    return key[position:] + key[:position]


def bit_expansion(bits: str, pattern: Sequence[int]) -> str:
    """Expand or permute a bit string using zero-based indexes."""

    for index in pattern:
        if index < 0 or index >= len(bits):
            raise ValueError(f"pattern index {index} is outside bit string length {len(bits)}")
    return "".join(bits[index] for index in pattern)


def xor_bits(left: str, right: str) -> str:
    if len(left) != len(right):
        raise ValueError("bit strings must have equal length")
    if set(left + right) - {"0", "1"}:
        raise ValueError("bit strings may contain only 0 and 1")
    return "".join("1" if a != b else "0" for a, b in zip(left, right, strict=True))


def mini_des_block(
    block: str,
    key: str,
    permutation_pattern: Sequence[int],
    sbox1: Sequence[str],
    sbox2: Sequence[str],
    rounds: int,
) -> str:
    """Encrypt one 12-bit block with the lab's Feistel-style toy cipher."""

    if len(block) != 12:
        raise ValueError("block must contain exactly 12 bits")
    if rounds <= 0:
        raise ValueError("rounds must be positive")

    left = block[:6]
    right = block[6:]
    for round_index in range(1, rounds):
        expanded = bit_expansion(right, permutation_pattern)
        round_key = rotate_key(key, round_index)
        mixed = xor_bits(round_key[: len(expanded)], expanded)
        s1_index = int(mixed[:4], 2)
        s2_index = int(mixed[4:], 2)
        substitution = sbox1[s1_index] + sbox2[s2_index]
        left, right = right, xor_bits(left, substitution)

    return right + left


def mini_des_ecb(
    bits: str,
    key: str,
    permutation_pattern: Sequence[int],
    sbox1: Sequence[str],
    sbox2: Sequence[str],
    rounds: int,
) -> str:
    return "".join(
        mini_des_block(bits[index : index + 12], key, permutation_pattern, sbox1, sbox2, rounds)
        for index in range(0, len(bits) - 11, 12)
    )


def mini_des_cbc(
    bits: str,
    key: str,
    permutation_pattern: Sequence[int],
    sbox1: Sequence[str],
    sbox2: Sequence[str],
    rounds: int,
    iv: str,
) -> str:
    if len(iv) != 12:
        raise ValueError("iv must contain exactly 12 bits")

    result: list[str] = []
    vector = iv
    for index in range(0, len(bits) - 11, 12):
        mixed = xor_bits(bits[index : index + 12], vector)
        vector = mini_des_block(mixed, key, permutation_pattern, sbox1, sbox2, rounds)
        result.append(vector)
    return "".join(result)


def mini_des_ofb(
    bits: str,
    key: str,
    permutation_pattern: Sequence[int],
    sbox1: Sequence[str],
    sbox2: Sequence[str],
    rounds: int,
    iv: str,
) -> str:
    if len(iv) != 12:
        raise ValueError("iv must contain exactly 12 bits")

    result: list[str] = []
    vector = iv
    for index in range(0, len(bits) - 11, 12):
        vector = mini_des_block(vector, key, permutation_pattern, sbox1, sbox2, rounds)
        result.append(xor_bits(bits[index : index + 12], vector))
    return "".join(result)


def mini_des_ctr(
    bits: str,
    key: str,
    permutation_pattern: Sequence[int],
    sbox1: Sequence[str],
    sbox2: Sequence[str],
    rounds: int,
    nonce: int,
) -> str:
    if nonce < 0:
        raise ValueError("nonce must be non-negative")

    result: list[str] = []
    for block_index, index in enumerate(range(0, len(bits) - 11, 12)):
        counter = format(nonce + block_index, "012b")[-12:]
        stream = mini_des_block(counter, key, permutation_pattern, sbox1, sbox2, rounds)
        result.append(xor_bits(bits[index : index + 12], stream))
    return "".join(result)

