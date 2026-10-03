from __future__ import annotations
import string


def analyze_characters(password: str) -> dict:
    length = len(password)
    lower = any(ch.islower() for ch in password)
    upper = any(ch.isupper() for ch in password)
    digit = any(ch.isdigit() for ch in password)
    symbol = any((ch in string.punctuation) and not ch.isspace() for ch in password)
    space = any(ch.isspace() for ch in password)
    types = [lower, upper, digit, symbol]
    character_type_count = sum(types)
    unique_count = len(set(password)) if password else 0
    unique_ratio = (unique_count / length) if length else 0.0

    diversity_contribution = {0: 0, 1: 3, 2: 7, 3: 11, 4: 15}[character_type_count]
    unique_contribution = round(10 * unique_ratio, 2)

    return {
        "has_lowercase": lower,
        "has_uppercase": upper,
        "has_digits": digit,
        "has_symbols": symbol,
        "has_spaces": space,
        "character_type_count": character_type_count,
        "unique_character_count": unique_count,
        "unique_character_ratio": round(unique_ratio, 3),
        "diversity_contribution": diversity_contribution,
        "unique_contribution": unique_contribution,
        "note": "Character diversity helps, but it is not used as a mandatory composition rule.",
    }
