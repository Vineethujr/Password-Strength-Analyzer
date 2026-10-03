from __future__ import annotations
import secrets
import string
from pathlib import Path

SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?"
WORD_PATH = Path(__file__).resolve().parents[2] / "data" / "passphrase_words.txt"


def _secure_shuffle(items: list[str]) -> list[str]:
    secrets.SystemRandom().shuffle(items)
    return items


def generate_complex_password(length: int = 20, uppercase: bool = True, lowercase: bool = True, numbers: bool = True, symbols: bool = True) -> str:
    length = max(16, min(128, int(length)))
    pools = []
    if uppercase:
        pools.append(string.ascii_uppercase)
    if lowercase:
        pools.append(string.ascii_lowercase)
    if numbers:
        pools.append(string.digits)
    if symbols:
        pools.append(SYMBOLS)
    if not pools:
        raise ValueError("Select at least one character set.")
    if sum(len(p) for p in pools) < 1:
        raise ValueError("Invalid character pool.")

    chars = [secrets.choice(pool) for pool in pools]
    alphabet = "".join(pools)
    chars.extend(secrets.choice(alphabet) for _ in range(length - len(chars)))
    return "".join(_secure_shuffle(chars))


def generate_passphrase(words: int = 6, separator: str = "-") -> str:
    word_list = [
        line.strip().lower()
        for line in WORD_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    words = max(5, min(10, int(words)))
    return separator.join(secrets.choice(word_list) for _ in range(words))
