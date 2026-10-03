from __future__ import annotations
import hashlib
from pathlib import Path
import httpx

DEMO_PATH = Path(__file__).resolve().parents[2] / "data" / "breached_sha1.txt"


def load_breach_hashes(path: Path | str = DEMO_PATH) -> set[str]:
    p = Path(path)
    return {line.strip().upper() for line in p.read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip()}


def local_breach_check(password: str, hashes: set[str]) -> dict:
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    return {
        "checked": True,
        "compromised": sha1 in hashes,
        "source": "local_demo_hash_set",
        "privacy": "Password and full hash stay local.",
    }


def hibp_k_anonymity_check(password: str, timeout: float = 5.0) -> dict:
    """Optional explicit online check. Never send the password or complete hash."""
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    headers = {"user-agent": "Password-Strength-Analyzer-Security-Tool/1.0"}
    with httpx.Client(timeout=timeout, headers=headers) as client:
        response = client.get(f"https://api.pwnedpasswords.com/range/{prefix}")
        response.raise_for_status()
    count = 0
    for line in response.text.splitlines():
        if ":" not in line:
            continue
        remote_suffix, remote_count = line.strip().split(":", 1)
        if remote_suffix.upper() == suffix:
            count = int(remote_count)
            break
    return {
        "checked": True,
        "compromised": count > 0,
        "exposure_count": count,
        "source": "have_i_been_pwned_k_anonymity_range",
        "privacy": "Only the first 5 characters of the SHA-1 hash were sent; comparison was local.",
    }
