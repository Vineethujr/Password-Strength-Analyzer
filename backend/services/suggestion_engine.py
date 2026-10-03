from __future__ import annotations


def generate_suggestions(f: dict) -> list[str]:
    suggestions: list[str] = []
    length = f["metrics"]["length"]
    chars = f["metrics"]["character"]
    patterns = f["patterns"]

    if length < 15:
        suggestions.append("Consider a longer password; 15+ characters is a useful target for a single-factor password policy.")
    if f["common_password"]:
        suggestions.append("Choose a password that is not on a common or compromised-password blocklist.")
    if patterns["sequence"]["detected"]:
        suggestions.append("Remove predictable sequences such as 1234 or abcd.")
    if patterns["keyboard"]["detected"]:
        suggestions.append("Avoid keyboard walks such as qwerty or asdf.")
    if patterns["repetition"]["detected"]:
        suggestions.append("Avoid repeated characters or repeated substrings such as aaaa or abcabc.")
    if f["dictionary_words_detected"]:
        suggestions.append("Avoid building a password around a common dictionary word or an obvious word-number variation.")
    if patterns["predictable_structure"]["detected"]:
        suggestions.append("Avoid predictable word + number/year + symbol constructions.")
    if patterns["date_like"]["detected"]:
        suggestions.append("Avoid birthdays, dates, and other predictable date-like values.")
    if patterns["phone_like"]["detected"]:
        suggestions.append("Avoid phone-like numeric information.")
    if f["personal_information"]:
        suggestions.append("Do not include your name, birth year, company, or college information in a password.")

    if chars["character_type_count"] <= 2:
        suggestions.append("Consider a longer, randomly generated password or a random-word passphrase rather than relying on forced character types.")

    if not suggestions:
        suggestions.extend([
            "Use a unique password for this account and store it in a password manager.",
            "Enable MFA where available for additional account protection.",
        ])
    else:
        suggestions.append("Use a password manager to generate and store a unique password for each account.")
        suggestions.append("Enable MFA where available; password strength is only one layer of authentication security.")

    # Stable de-duplication.
    return list(dict.fromkeys(suggestions))[:8]
