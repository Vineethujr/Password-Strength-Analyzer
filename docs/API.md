# API Guide

## POST `/api/analyze`

Accepts a password transiently plus optional demo context and policy settings.

Example:

```json
{
  "password": "synthetic-demo-value",
  "context": {
    "first_name": "Rahul",
    "birth_year": "2001",
    "company_or_college": "Demo College"
  },
  "check_local_breach": true
}
```

The response does not contain the password.

## POST `/api/generate`

```json
{
  "mode": "complex",
  "length": 20,
  "uppercase": true,
  "lowercase": true,
  "numbers": true,
  "symbols": true,
  "words": 6
}
```

## POST `/api/breach-check`

Separate from live typing. Sends only a 5-character SHA-1 hash prefix to Pwned Passwords when manually invoked. The returned suffix list is compared locally.

## GET `/api/dashboard/stats`

Returns aggregate statistics and safe recent metadata.

## Status codes

- `200`: success
- `422`: invalid request; generic response does not echo the body
- `429`: rate limit
- `503`: explicit remote breach check unavailable
