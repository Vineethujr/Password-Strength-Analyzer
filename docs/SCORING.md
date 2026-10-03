# Scoring Model

The score is **0–100** and is intentionally a transparent educational heuristic.

## Positive contributions

| Signal | Maximum |
|---|---:|
| Length | 35 |
| Character diversity | 15 |
| Unique-character ratio | 10 |
| Pattern resistance | 20 |
| Not an exact common-password match | 10 |
| Additional unpredictability | 10 |
| **Total** | **100** |

## Classification bands

| Score | Classification |
|---:|---|
| 0–20 | VERY WEAK |
| 21–40 | WEAK |
| 41–60 | MODERATE |
| 61–80 | STRONG |
| 81–100 | VERY STRONG |

## Penalties

The engine reduces the score when it detects:

- exact common-password match
- keyboard walk
- ascending/descending sequence
- repeated characters/substrings
- dictionary-word signal
- personal-context overlap
- predictable word/number/year/symbol structure
- date-like pattern
- phone-like numeric pattern

The strongest penalty is applied to an exact common-password match. A long repeated password is also penalized heavily so the project demonstrates why length alone is not enough.

## Important limitation

These weights and bands are project-defined. They are not a NIST or OWASP numeric standard. Real production password-strength controls should use a mature estimator and an updated blocklist, with policy requirements defined separately.
