from __future__ import annotations
from .character_analyzer import analyze_characters
from .common_password_checker import find_dictionary_words, is_common_password
from .entropy_estimator import estimate_theoretical_entropy
from .length_analyzer import analyze_length
from .pattern_detector import (
    detect_date_like,
    detect_keyboard_patterns,
    detect_phone_like,
    detect_predictable_structure,
    detect_repetition,
    detect_sequences,
)
from .policy_checker import Policy, evaluate_policy
from .scoring_engine import calculate_score, classify_score
from .suggestion_engine import generate_suggestions


def _context_overlap(password: str, context: dict | None) -> list[str]:
    if not context:
        return []
    s = password.casefold()
    overlaps = []
    first_name = str(context.get("first_name", "")).strip().casefold()
    if len(first_name) >= 3 and first_name in s:
        overlaps.append("first_name")
    company = str(context.get("company_or_college", "")).strip().casefold()
    if len(company) >= 4:
        compact = "".join(ch for ch in company if ch.isalnum())
        if compact and compact in "".join(ch for ch in s if ch.isalnum()):
            overlaps.append("company_or_college")
    birth_year = str(context.get("birth_year", "")).strip()
    if birth_year.isdigit() and len(birth_year) == 4 and birth_year in password:
        overlaps.append("birth_year")
    return overlaps


def analyze_password(password: str, *, common_passwords: set[str], breach_hashes: set[str] | None = None, context: dict | None = None, policy: Policy | None = None, include_breach: bool = False) -> dict:
    password = password or ""
    if policy is None:
        policy = Policy()
    if not password:
        return {
            "score": 0,
            "classification": "VERY WEAK",
            "findings": [{"type": "length", "severity": "critical", "description": "Password input is empty."}],
            "suggestions": ["Enter a password or generate a secure demo password.", "Consider a long unique password or random-word passphrase."],
            "metrics": {"length": 0, "length_band": "empty", "uppercase_present": False, "lowercase_present": False, "digits_present": False, "symbols_present": False, "spaces_present": False, "character_type_count": 0, "unique_character_count": 0, "unique_character_ratio": 0.0, "theoretical_entropy_bits": 0.0, "estimated_character_pool": 1, "pattern_penalties": []},
            "patterns": {"sequence": {"detected": False}, "keyboard": {"detected": False}, "repetition": {"detected": False}, "predictable_structure": {"detected": False}, "date_like": {"detected": False}, "phone_like": {"detected": False}},
            "common_password": False,
            "dictionary_words_detected": [],
            "personal_information": False,
            "personal_context_fields": [],
            "breach_check": {"checked": False, "compromised": False, "source": "disabled"},
            "entropy_explanation": "No entropy is meaningful for an empty input.",
            "scoring_note": "The 0-100 score and classification bands are project-defined educational heuristics, not a universal security standard.",
            "policy": {"passed": False, "checks": [{"name": "minimum_length", "passed": False, "message": f"Use at least {policy.minimum_length} characters."}], "note": "Policy compliance is separate from the educational strength score."},
        }
        policy = Policy()

    length = analyze_length(password)
    character = analyze_characters(password)
    common = is_common_password(password, common_passwords) if password else False
    dictionary_words = find_dictionary_words(password, common_passwords) if password else []
    sequences = detect_sequences(password)
    keyboard = detect_keyboard_patterns(password)
    repetition = detect_repetition(password)
    predictable = detect_predictable_structure(password, dictionary_words)
    date_like = detect_date_like(password)
    phone_like = detect_phone_like(password)
    context_fields = _context_overlap(password, context)
    personal_info = bool(context_fields)
    entropy = estimate_theoretical_entropy(password)

    local_breach = {"checked": False, "compromised": False, "source": "disabled"}
    if include_breach and breach_hashes is not None:
        from .breach_checker import local_breach_check
        local_breach = local_breach_check(password, breach_hashes)

    score, penalties = calculate_score(
        length_contribution=length["contribution"],
        diversity_contribution=character["diversity_contribution"],
        unique_contribution=character["unique_contribution"],
        common_password=common,
        keyboard=keyboard["detected"],
        sequences=sequences["detected"],
        repetition=repetition["detected"],
        predictable_structure=predictable["detected"],
        dictionary_words=bool(dictionary_words),
        personal_info=personal_info,
        date_like=date_like["detected"],
        phone_like=phone_like["detected"],
    )

    findings = []
    def add(ftype, severity, description):
        findings.append({"type": ftype, "severity": severity, "description": description})

    if length["length"] < 15:
        add("length", "medium", "Password is below the configured 15-character single-factor policy target.")
    if character["character_type_count"] == 1:
        add("character_diversity", "low", "Only one character type is present. This is informational, not a mandatory composition failure.")
    if common:
        add("common_password", "critical", "Your password matches a commonly used password pattern and should not be used.")
    if dictionary_words:
        add("dictionary_word", "medium", "A common dictionary word appears in the password structure.")
    if sequences["detected"]:
        add("sequence", "high", "A predictable ascending or descending sequence was detected.")
    if keyboard["detected"]:
        add("keyboard_pattern", "high", "A predictable keyboard pattern was detected.")
    if repetition["detected"]:
        add("repetition", "high", "Repeated characters or substrings were detected.")
    if predictable["detected"]:
        add("predictable_structure", "medium", "A common word + number/year/symbol structure was detected.")
    if date_like["detected"]:
        add("date_like", "medium", "A date-like value was detected.")
    if phone_like["detected"]:
        add("phone_like", "medium", "A phone-like numeric pattern was detected.")
    if personal_info:
        add("personal_information", "high", "The password overlaps with voluntarily supplied personal context.")
    if local_breach["compromised"]:
        add("breach_exposure", "critical", "The password matched the local demonstration breach hash set.")
        score = 0

    result = {
        "score": score,
        "classification": classify_score(score),
        "findings": findings,
        "suggestions": [],
        "metrics": {
            "length": length["length"],
            "length_band": length["band"],
            "uppercase_present": character["has_uppercase"],
            "lowercase_present": character["has_lowercase"],
            "digits_present": character["has_digits"],
            "symbols_present": character["has_symbols"],
            "spaces_present": character["has_spaces"],
            "character_type_count": character["character_type_count"],
            "unique_character_count": character["unique_character_count"],
            "unique_character_ratio": character["unique_character_ratio"],
            "theoretical_entropy_bits": entropy["theoretical_bits"],
            "estimated_character_pool": entropy["estimated_character_pool"],
            "pattern_penalties": penalties,
        },
        "patterns": {
            "sequence": sequences,
            "keyboard": keyboard,
            "repetition": repetition,
            "predictable_structure": predictable,
            "date_like": date_like,
            "phone_like": phone_like,
        },
        "common_password": common,
        "dictionary_words_detected": dictionary_words,
        "personal_information": personal_info,
        "personal_context_fields": context_fields,
        "breach_check": local_breach,
        "entropy_explanation": entropy["limitation"],
        "scoring_note": "The 0-100 score and classification bands are project-defined educational heuristics, not a universal security standard.",
    }
    result["policy"] = evaluate_policy(password, policy=policy, common_password=common, personal_info=personal_info)
    result["suggestions"] = generate_suggestions({**result, "metrics": {**result["metrics"], "character": character}})

    # Do not include the raw password anywhere in the returned object.
    return result
