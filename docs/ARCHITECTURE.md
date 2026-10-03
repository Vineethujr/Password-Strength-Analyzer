# System Architecture

## Data flow

User → React UI → `POST /api/analyze` → local analysis services → score/classification/findings/suggestions → UI.

The only persistence path is metadata-only SQLite analytics. The password does not enter that path.

## Services

- `length_analyzer.py`: length bands and contribution.
- `character_analyzer.py`: character types, unique count and ratio.
- `common_password_checker.py`: small local educational blocklist.
- `pattern_detector.py`: keyboard, sequence, repetition, date, phone and predictable structure signals.
- `entropy_estimator.py`: theoretical `L × log2(N)` estimate with explicit limitations.
- `scoring_engine.py`: project-defined 0–100 score and classification.
- `suggestion_engine.py`: specific actionable guidance.
- `password_generator.py`: cryptographically secure demo generation via `secrets`.
- `policy_checker.py`: configurable policy pass/fail, separate from score.
- `breach_checker.py`: local demo hash set plus explicit optional HIBP k-anonymity check.

## Threat model

### Protect

- Password value entered by a user.
- User-provided demo context.
- Analytics integrity.
- API availability.

### Main threats considered

- accidental secret logging
- accidental secret persistence
- URL leakage
- overly verbose errors
- external breach-service leakage during real-time typing
- automated abuse of the analyzer endpoint

### Controls

- transient in-memory processing
- no password database column
- generic validation errors
- POST body rather than query parameters
- no frontend storage APIs for the password
- explicit remote breach-check action only
- simple per-process rate limit
- production guidance for HTTPS and a distributed limiter
