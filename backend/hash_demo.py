"""Standalone education-only Argon2id demonstration.

It deliberately uses a synthetic fixed demo password and is not connected to
an authentication database or the analyzer API.
"""
from __future__ import annotations
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

DEMO_PASSWORD = "SyntheticDemo-DoNotReuse-2026!"
ph = PasswordHasher()


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        return ph.verify(stored_hash, password)
    except VerifyMismatchError:
        return False


if __name__ == "__main__":
    stored = hash_password(DEMO_PASSWORD)
    print("Synthetic demo password was hashed with Argon2id.")
    print("Stored hash:", stored)
    print("Verification succeeds:", verify_password(DEMO_PASSWORD, stored))
    print("Verification with wrong password:", verify_password("wrong-demo-password", stored))
