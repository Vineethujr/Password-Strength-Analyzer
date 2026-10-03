# Project Report — Password Strength Analyzer & Security Suggestion Tool

## Abstract

The Password Strength Analyzer & Security Suggestion Tool is a defensive cybersecurity web application designed to provide transparent, privacy-conscious password feedback. Instead of relying solely on composition rules, the system analyzes length, character diversity, unique-character ratio, common-password membership, dictionary terms, sequential patterns, keyboard walks, repetition, predictable word-number/year structures, optional personal context, and an entropy-style theoretical estimate. A project-defined score from 0 to 100 is mapped to five strength classifications and combined with actionable recommendations. Passwords are processed transiently and excluded from logs and persistent analytics. The system also includes secure random password generation, policy evaluation, a metadata-only analytics dashboard, automated security tests, and a separate Argon2id storage demonstration.

## 1. Introduction

Passwords remain an important authentication factor, but human-chosen values are often predictable. Current NIST SP 800-63B-4 guidance emphasizes sufficient length, blocklists of commonly used or compromised passwords, acceptance of long secrets, and avoidance of composition rules.

## 2. Problem Statement

Users often believe a password is strong when it contains several character categories. Predictable transformations such as a common word plus a year and symbol can still be easy to guess. A practical educational tool should explain the specific weakness rather than giving only a single opaque meter.

## 3. Objectives

- Evaluate password strength using multiple explainable signals.
- Detect common and predictable patterns.
- Provide actionable security recommendations.
- Demonstrate privacy-by-design.
- Demonstrate secure random password generation.
- Teach password hashing and MFA concepts without creating credential-stealing or password-cracking functionality.
- Provide a portfolio-ready REST API, UI, tests, analytics and documentation.

## 4. Password Security Background

Authentication verifies identity; authorization determines what an authenticated subject may access. Passwords should be stored using dedicated salted password-hashing approaches rather than plaintext or fast general-purpose hashes. OWASP recommends Argon2id, bcrypt, or PBKDF2 for password storage.

MFA adds another authentication factor. Password strength is therefore only one part of the security model.

## 5. Existing Approaches

Simple password meters frequently emphasize character classes. More complete systems combine length guidance, blocklists and contextual feedback. This project implements a transparent educational version intended for learning and demonstration rather than certification or production deployment.

## 6. Proposed System

The proposed system uses a React frontend and FastAPI backend. The frontend sends a password to the backend for immediate analysis. The backend calculates derived metrics and returns findings and suggestions. SQLite stores only aggregate-safe metadata. A separate explicit breach-check endpoint can use Pwned Passwords k-anonymity without sending the full password or full hash.

## 7. Architecture

User → React → FastAPI → Analysis Services → Scoring → Suggestions → React. Optional safe metadata → SQLite → Dashboard.

## 8. Password Analysis

The analyzer includes modules for length, character diversity, common-password matching, dictionary terms, sequences, keyboard patterns, repetition, predictable structures, date-like values, phone-like values and optional user-context overlap.

## 9. Feature Extraction

Metrics include length, character-type count, unique-character count, unique-character ratio and a theoretical entropy estimate. Character diversity is treated as one signal rather than a mandatory policy.

## 10. Pattern Detection

The pattern engine checks common keyboard walks, ascending/descending sequences, repeated characters, repeated substrings, common word-number/year structures and simple date or phone-like patterns.

## 11. Common Password Detection

The project contains a small educational blocklist in `data/common_passwords.txt`. It intentionally avoids shipping personal data or claiming to represent a complete current breach corpus.

## 12. Entropy Concepts

The project shows the formula `L × log2(N)` as an educational theoretical estimate. It explicitly warns that human-selected passwords violate the random-selection assumption. NIST states that entropy estimation for user-chosen passwords is challenging and describes length and blocklists as more straightforward controls.

## 13. Strength Scoring

The 0–100 score is produced from positive contributions for length, diversity, unique-character ratio, pattern resistance, non-common status and additional unpredictability, followed by penalties for detected weak signals. The resulting categories are VERY WEAK, WEAK, MODERATE, STRONG and VERY STRONG. These bands are project-defined and not a universal standard.

## 14. Recommendation Engine

Recommendations are generated from actual findings. Examples include avoiding keyboard walks, increasing length, avoiding personal information, using unique credentials and enabling MFA.

## 15. Password Generator

The generator uses Python `secrets`, provides complex-password and passphrase modes, and never stores generated values.

## 16. Policy Checker

Policy is separate from strength. The default project policy uses a 15-character target, a common-password check and optional personal-context checking. NIST SP 800-63B-4 requires 15 characters for passwords used as a single factor and says composition rules should not be imposed.

## 17. Secure Password Storage Concepts

The report demonstrates hashing separately using Argon2id and a synthetic password. It does not turn the analyzer into an authentication store.

## 18. Privacy Design

No database field exists for passwords. Passwords are not written to analytics, URLs, localStorage, or sessionStorage. Generic validation errors avoid accidental secret reflection.

## 19. Dashboard

The dashboard displays total analyses, average score, strength distribution, weakness frequency and recent metadata. No password value is shown.

## 20. Testing

Automated tests cover more than 30 scenarios, including edge cases, pattern detection, Unicode, spaces, generator behavior, privacy, schema structure, breach-demo matching and score boundaries.

## 21. Security Testing

The project verifies the absence of plaintext storage, log leakage and browser persistence. The optional remote breach endpoint is separated from real-time analysis to avoid repeated external requests during typing. HIBP warns that incremental searching can create observable request patterns; completed-password checks reduce this exposure.

## 22. Results

Expected demonstrations include: `123456` as VERY WEAK; `Password123!` as a weak predictable construction despite composition diversity; `aaaaaaaaaaaaaaaa` as weak due to repetition; `qwerty2026!` as weak due to keyboard/year patterns; and fresh generated random strings as strong or very strong under the project's heuristic model.

## 23. Limitations

The score cannot perfectly model real attackers. The entropy estimate is illustrative. The local common-password and breach-demo files are intentionally small. Production deployments need stronger data sources, TLS, distributed rate limiting, monitoring and secure infrastructure.

## 24. Future Scope

Future work includes mature password-strength estimation, enterprise password policies, privacy-preserving breach checks, IAM/SSO integration, MFA and passkey education, localization, accessibility, password-manager integrations and organization-level reporting.

## 25. Conclusion

The project demonstrates a defensive, modular approach to password security education. Its central design principle is that better password assessment combines length, unpredictability, pattern resistance, common-password screening and context, while privacy remains a first-class requirement.
