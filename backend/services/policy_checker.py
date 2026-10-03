from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Policy:
    minimum_length: int = 15
    common_password_check: bool = True
    personal_info_check: bool = True
    maximum_length: int = 128


def evaluate_policy(password: str, *, policy: Policy, common_password: bool, personal_info: bool) -> dict:
    checks = []
    if len(password) >= policy.minimum_length:
        checks.append({"name": "minimum_length", "passed": True, "message": f"At least {policy.minimum_length} characters."})
    else:
        checks.append({"name": "minimum_length", "passed": False, "message": f"Use at least {policy.minimum_length} characters for the configured single-factor policy."})

    if policy.common_password_check:
        checks.append({"name": "common_password", "passed": not common_password, "message": "Not an exact match for the local common-password blocklist." if not common_password else "Matches a local common-password blocklist entry."})

    if policy.personal_info_check:
        checks.append({"name": "personal_information", "passed": not personal_info, "message": "No supplied context overlap detected." if not personal_info else "Supplied personal-context overlap detected."})

    return {
        "passed": all(c["passed"] for c in checks),
        "checks": checks,
        "note": "Policy compliance is separate from the educational strength score.",
    }
