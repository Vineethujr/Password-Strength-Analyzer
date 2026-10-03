from __future__ import annotations
from pathlib import Path
import re

DEFAULT_PATH = Path(__file__).resolve().parents[2] / "data" / "common_passwords.txt"


def load_common_passwords(path: Path | str = DEFAULT_PATH) -> set[str]:
    p = Path(path)
    return {
        line.strip().lower()
        for line in p.read_text(encoding="utf-8", errors="ignore").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


def is_common_password(password: str, common_passwords: set[str]) -> bool:
    return password.casefold() in common_passwords


def find_dictionary_words(password: str, common_passwords: set[str]) -> list[str]:
    """Educational token check; whole-password blocklisting is separate.

    This is intentionally conservative so ordinary long passphrases are not
    rejected just because they contain a common word.
    """
    tokens = [t for t in re.split(r"[^\w]+", password.casefold(), flags=re.UNICODE) if t]
    matches = []
    for token in tokens:
        if len(token) >= 4 and token in common_passwords and token not in matches:
            matches.append(token)
    return matches[:5]
