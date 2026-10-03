from __future__ import annotations


def calculate_score(
    *,
    length_contribution: int,
    diversity_contribution: int,
    unique_contribution: float,
    common_password: bool,
    keyboard: bool,
    sequences: bool,
    repetition: bool,
    predictable_structure: bool,
    dictionary_words: bool,
    personal_info: bool,
    date_like: bool,
    phone_like: bool,
) -> tuple[int, list[dict]]:
    """Project-defined 0-100 score; not a universal security standard."""
    pattern_resistance = 20
    pattern_resistance -= 5 if keyboard else 0
    pattern_resistance -= 5 if sequences else 0
    pattern_resistance -= 10 if repetition else 0
    pattern_resistance -= 3 if predictable_structure else 0
    pattern_resistance -= 2 if date_like else 0
    pattern_resistance -= 2 if phone_like else 0
    pattern_resistance = max(0, pattern_resistance)

    non_common_contribution = 0 if common_password else 10
    additional_unpredictability = 10
    if dictionary_words:
        additional_unpredictability -= 5
    if personal_info:
        additional_unpredictability -= 5
    additional_unpredictability = max(0, additional_unpredictability)

    raw = (
        length_contribution
        + diversity_contribution
        + unique_contribution
        + pattern_resistance
        + non_common_contribution
        + additional_unpredictability
    )

    penalties = []
    if common_password:
        penalties.append({"type": "common_password", "severity": "critical", "points": 35})
        raw -= 35
    if keyboard:
        penalties.append({"type": "keyboard_pattern", "severity": "high", "points": 8})
        raw -= 8
    if sequences:
        penalties.append({"type": "sequence", "severity": "high", "points": 10})
        raw -= 10
    if repetition:
        penalties.append({"type": "repetition", "severity": "high", "points": 35})
        raw -= 35
    if dictionary_words:
        penalties.append({"type": "dictionary_word", "severity": "medium", "points": 5})
        raw -= 5
    if personal_info:
        penalties.append({"type": "personal_information", "severity": "high", "points": 8})
        raw -= 8
    if predictable_structure:
        penalties.append({"type": "predictable_structure", "severity": "medium", "points": 15})
        raw -= 15
    if date_like:
        penalties.append({"type": "date_like", "severity": "medium", "points": 6})
        raw -= 6
    if phone_like:
        penalties.append({"type": "phone_like", "severity": "medium", "points": 6})
        raw -= 6

    if length_contribution == 0:
        raw -= 35
    elif length_contribution == 10:
        raw -= 5
    elif length_contribution == 22:
        raw -= 3

    score = max(0, min(100, round(raw)))
    return score, penalties


def classify_score(score: int) -> str:
    if score <= 20:
        return "VERY WEAK"
    if score <= 40:
        return "WEAK"
    if score <= 60:
        return "MODERATE"
    if score <= 80:
        return "STRONG"
    return "VERY STRONG"
