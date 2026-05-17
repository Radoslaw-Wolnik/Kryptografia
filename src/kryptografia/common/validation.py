"""Small validation helpers."""

from __future__ import annotations

from kryptografia.common.exceptions import ValidationError


def ensure_positive_integer(value: int, name: str) -> None:
    if not isinstance(value, int):
        raise ValidationError(f"{name} must be an integer")

    if value <= 0:
        raise ValidationError(f"{name} must be positive")


def ensure_non_empty(value: object, name: str) -> None:
    if not value:
        raise ValidationError(f"{name} must not be empty")

