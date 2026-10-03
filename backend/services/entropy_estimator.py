from __future__ import annotations
import math
import string


def estimate_theoretical_entropy(password: str) -> dict:
    pool = 0
    if any(ch.islower() for ch in password):
        pool += 26
    if any(ch.isupper() for ch in password):
        pool += 26
    if any(ch.isdigit() for ch in password):
        pool += 10
    if any((ch in string.punctuation) and not ch.isspace() for ch in password):
        pool += len(string.punctuation)
    if any(ch.isspace() for ch in password):
        pool += 1
    pool = max(pool, 1)
    bits = len(password) * math.log2(pool) if password else 0.0
    return {
        "theoretical_bits": round(bits, 1),
        "estimated_character_pool": pool,
        "formula": "L × log2(N)",
        "limitation": (
            "Illustrative only: the formula assumes independent random selection. "
            "Human-created passwords are often much more predictable."
        ),
    }
