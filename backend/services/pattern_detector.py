from __future__ import annotations
import re

KEYBOARD_PATTERNS = [
    "qwerty", "asdfgh", "zxcv", "qwertyuiop", "asdfghjkl", "zxcvbnm",
    "1234", "2345", "3456", "4567", "5678", "6789", "7890",
    "1qaz", "2wsx", "3edc", "4rfv", "5tgb", "6yhn", "7ujm",
]

SEQUENCE_CHARS = "abcdefghijklmnopqrstuvwxyz0123456789"


def _contains_linear_sequence(text: str, minimum: int = 4) -> tuple[bool, list[str]]:
    s = text.casefold()
    hits: list[str] = []
    for i in range(len(SEQUENCE_CHARS) - minimum + 1):
        seq = SEQUENCE_CHARS[i : i + minimum]
        rev = seq[::-1]
        if seq in s:
            hits.append(seq)
        if rev in s:
            hits.append(rev)
    return bool(hits), list(dict.fromkeys(hits))[:6]


def detect_sequences(password: str, minimum: int = 4) -> dict:
    found, hits = _contains_linear_sequence(password, minimum)
    return {
        "detected": found,
        "hits": hits,
        "ascending_or_descending": found,
        "description": "Ascending/descending letter or number sequences are predictable guessing targets.",
    }


def detect_keyboard_patterns(password: str) -> dict:
    s = password.casefold()
    hits: list[str] = []
    for pattern in KEYBOARD_PATTERNS:
        if pattern in s or pattern[::-1] in s:
            hits.append(pattern)
    return {
        "detected": bool(hits),
        "hits": list(dict.fromkeys(hits))[:6],
        "description": "Keyboard walks and adjacent-key patterns are commonly guessed.",
    }


def detect_repetition(password: str) -> dict:
    repeated_chars = re.findall(r"(.)\1{2,}", password, flags=re.DOTALL)

    repeated_substrings: list[str] = []
    n = len(password)
    for unit_len in range(1, min(8, n // 2 + 1)):
        for i in range(0, n - unit_len * 3 + 1):
            unit = password[i : i + unit_len]
            if unit and password[i : i + unit_len * 3] == unit * 3:
                repeated_substrings.append(unit)
    repeated_substrings = list(dict.fromkeys(repeated_substrings))[:6]

    return {
        "detected": bool(repeated_chars or repeated_substrings),
        "repeated_characters": list(dict.fromkeys(repeated_chars))[:6],
        "repeated_substrings": repeated_substrings,
        "description": "Repeated characters or repeated substrings reduce effective unpredictability.",
    }


def detect_predictable_structure(password: str, dictionary_words: list[str]) -> dict:
    s = password.casefold()
    year_hits = re.findall(r"(?:19|20)\d{2}", s)
    suffix_number = bool(re.search(r"\D+\d{2,4}[!@#$%^&*()_+\-=\[\]{};:,.?]*$", s))
    word_number = bool(dictionary_words and re.search(r"\d{2,4}", s))
    common_suffixes = ["!", "123", "1234", "1", "01", "2024", "2025", "2026"]
    common_suffix = any(s.endswith(x) for x in common_suffixes)
    detected = bool(year_hits or suffix_number or word_number or common_suffix)
    return {
        "detected": detected,
        "year_hits": list(dict.fromkeys(year_hits))[:4],
        "word_plus_number": word_number,
        "predictable_suffix": suffix_number or common_suffix,
        "description": "Word + number/year/symbol transformations are common password-guessing patterns.",
    }


def detect_date_like(password: str) -> dict:
    patterns = [
        r"(?:19|20)\d{2}[-/ ]?(?:0[1-9]|1[0-2])[-/ ]?(?:0[1-9]|[12]\d|3[01])",
        r"(?:0[1-9]|[12]\d|3[01])[-/ ]?(?:0[1-9]|1[0-2])[-/ ]?(?:19|20)\d{2}",
    ]
    hits = [p for p in patterns if re.search(p, password)]
    return {
        "detected": bool(hits),
        "patterns": len(hits),
        "description": "Date-like values can expose birthdays or other predictable information.",
    }


def detect_phone_like(password: str) -> dict:
    digit_count = sum(ch.isdigit() for ch in password)
    cleaned = re.sub(r"[\s()\-+]", "", password)
    digits_only = cleaned.isdigit()
    detected = digits_only and digit_count >= 9
    return {
        "detected": detected,
        "digit_count": digit_count,
        "description": "Long phone-like numeric strings may be predictable personal information.",
    }
