# Interview Preparation — Exactly 10 Questions

## 1. Explain your project.

I developed a Password Strength Analyzer & Security Suggestion Tool that evaluates passwords using several security signals instead of only checking uppercase, lowercase, numbers, and symbols. The system analyzes length, character diversity, unique-character ratio, common-password matches, dictionary words, keyboard patterns, sequential characters, repeated patterns, predictable word-number or year structures, optional personal-context overlap, and an entropy-style estimate. It combines those signals into a project-defined 0–100 score and produces specific security recommendations. A major privacy feature is that submitted passwords are processed transiently and are not stored in the database, logs, URLs, or browser storage.

## 2. How does your analyzer determine password strength?

It uses a transparent weighted scoring model. Length can contribute up to 35 points, character diversity up to 15, unique-character ratio up to 10, pattern resistance up to 20, non-common-password status up to 10, and an additional unpredictability contribution up to 10. Then the engine applies penalties for common passwords, keyboard patterns, sequences, repetition, predictable structures, dictionary words, personal-context overlap, dates, and phone-like values. The final score is capped between 0 and 100 and mapped to five project-defined classifications.

## 3. What is password entropy, and why did you not use it alone?

Password entropy describes uncertainty or theoretical search-space size. A simplified estimate is `L × log2(N)`, where `L` is length and `N` is an assumed character pool. The problem is that the calculation assumes characters are selected randomly. Human-created passwords often follow common patterns, so the theoretical number can be optimistic. My project therefore presents entropy as an educational metric and combines it with blocklist and pattern analysis.

## 4. Why can `Password123!` still be weak?

A composition-only checker sees uppercase, lowercase, numbers, and a symbol and may mark it as acceptable. My analyzer recognizes that it uses a very common word followed by a predictable number sequence and symbol. That is an example of how people often satisfy composition requirements predictably. The project therefore gives more importance to length and resistance to common patterns than to mandatory composition rules.

## 5. What is the difference between hashing and encryption?

Encryption is intended to be reversible with the right key, while password hashing is intended for one-way verification. A production authentication system should not need to recover the original password. Instead, it stores a salted result from a dedicated password-hashing or key-derivation function and verifies future login attempts against that stored representation.

## 6. What is salting, and why is it important?

A salt is a unique random value incorporated into password hashing. It prevents equal passwords from producing the same stored representation when different users choose them, and it reduces the usefulness of precomputed lookup tables. Modern password-hashing libraries can manage salts as part of the hashing process, which is preferable to custom cryptographic code.

## 7. Why are Argon2id, bcrypt, scrypt, or PBKDF2 better suited to password storage than a fast hash?

Fast hashes such as SHA-256 are optimized to be fast. That is useful for integrity checks but undesirable for password storage because an attacker with a stolen password database can try guesses very quickly. Dedicated password-hashing functions are deliberately more expensive and use configurable work factors. OWASP recommends Argon2id, bcrypt, or PBKDF2 for password storage rather than fast general-purpose hashing alone.

## 8. How did you protect user privacy?

The analyzer never stores the submitted password. The SQLite schema has no password column, the API response never returns the password, and the frontend does not persist it in localStorage or sessionStorage. Validation errors are generic so secret values are not echoed. The real-time analyzer uses a local demonstration breach set, while any external Pwned Passwords check is a separate explicit action that sends only a 5-character SHA-1 hash prefix.

## 9. What is the role of password policy, and how is it different from strength scoring?

Policy is a configurable compliance check, while strength scoring is an educational heuristic. For example, the demo policy can require at least 15 characters for a single-factor password and reject exact common-password blocklist matches. A password can have a certain score but still fail a policy requirement, or pass a simple length requirement while having predictable patterns. Keeping the two separate makes the design easier to explain and change.

## 10. How would you improve the project for production?

I would replace the small educational blocklist with an audited and regularly updated source, use a mature strength estimator, add a production-grade distributed rate limiter, deploy behind TLS, and integrate enterprise IAM/SSO controls. I would also make the breach corpus locally hosted or use the Pwned Passwords k-anonymity API deliberately rather than during keystrokes. For a broader identity-security solution I would add MFA, passkey/WebAuthn awareness, secure account recovery, monitoring, accessibility, and organization-level aggregate reporting without collecting passwords.
