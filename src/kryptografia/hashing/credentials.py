"""Pure credential-store helpers for the hash-function lab."""

from __future__ import annotations

from dataclasses import dataclass, replace

from kryptografia.signatures.digest import sha256_hex


@dataclass(frozen=True)
class CredentialRecord:
    username: str
    password_hash: str
    salt: str = ""


def hash_password(password: str, salt: str = "") -> str:
    """Hash a password for the educational credential examples."""

    return sha256_hex(f"{salt}{password}")


def register_user(
    records: list[CredentialRecord],
    username: str,
    password: str,
    *,
    salt: str = "",
) -> list[CredentialRecord]:
    if any(record.username == username for record in records):
        raise ValueError("username already exists")

    return [*records, CredentialRecord(username, hash_password(password, salt), salt)]


def check_credentials(records: list[CredentialRecord], username: str, password: str) -> bool:
    for record in records:
        if record.username == username:
            return record.password_hash == hash_password(password, record.salt)
    return False


def change_password(
    records: list[CredentialRecord],
    username: str,
    old_password: str,
    new_password: str,
) -> list[CredentialRecord]:
    updated: list[CredentialRecord] = []
    changed = False
    for record in records:
        if record.username != username:
            updated.append(record)
            continue

        if record.password_hash != hash_password(old_password, record.salt):
            raise ValueError("invalid username or old password")
        updated.append(replace(record, password_hash=hash_password(new_password, record.salt)))
        changed = True

    if not changed:
        raise ValueError("invalid username or old password")
    return updated

