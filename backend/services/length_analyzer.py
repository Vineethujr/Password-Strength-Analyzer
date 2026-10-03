from __future__ import annotations


def analyze_length(password: str) -> dict:
    """Return length metrics and an educational length contribution (0-35)."""
    length = len(password)
    if length == 0:
        band, contribution = "empty", 0
    elif length < 8:
        band, contribution = "very short", 0
    elif length <= 11:
        band, contribution = "short", 10
    elif length <= 15:
        band, contribution = "better length", 22
    elif length <= 19:
        band, contribution = "strong length", 30
    else:
        band, contribution = "very long", 35

    return {
        "length": length,
        "band": band,
        "contribution": contribution,
        "guidance": (
            "Length is an important signal, but length alone cannot make a predictable password secure."
        ),
    }
