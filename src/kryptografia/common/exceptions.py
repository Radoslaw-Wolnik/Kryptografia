class KryptografiaError(Exception):
    """Base exception for repository-specific errors."""


class ValidationError(KryptografiaError, ValueError):
    """Raised when invalid input is supplied."""


class EncodingError(KryptografiaError, ValueError):
    """Raised for encoding or decoding problems."""


class CryptographyMathError(KryptografiaError, ValueError):
    """Raised for mathematical cryptography errors."""

