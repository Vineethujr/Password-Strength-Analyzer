# Security Testing Checklist

## Automated checks

Run `pytest -q`.

## Manual checks

| Check | Procedure | Expected |
|---|---|---|
| Plaintext DB storage | Inspect SQLite schema | No `password` column |
| Password logging | Run with a unique synthetic secret and inspect terminal/log files | Secret absent |
| API response | Capture `/api/analyze` response | Secret absent |
| URL leakage | Inspect browser network URLs | Password absent from URL |
| Password field | Inspect DOM | `type="password"` by default |
| localStorage | DevTools → Application | No password entry |
| sessionStorage | DevTools → Application | No password entry |
| Analytics | Inspect `analyses` and `findings` | Metadata only |
| Remote breach default | Type a password without clicking remote check | No request to HIBP |
| Remote breach explicit | Click remote check | Only SHA-1 prefix sent |
| Error disclosure | Submit invalid oversized input | Generic validation error |

## What not to test

Do not test using real production credentials, real employee data, or real account login attempts. This project intentionally has no cracking or credential-stuffing functionality.
