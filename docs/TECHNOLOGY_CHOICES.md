# Technology Choices

## Option A: Flask + HTML/CSS/JS

Simpler setup and easier for a first Python project. Smaller dependency footprint.

## Option B: FastAPI + React

Stronger separation of concerns, typed request validation, API documentation, modern frontend development and a realistic portfolio architecture. This repository uses Option B.

## Why SQLite?

The tool only needs local aggregate analytics for a student project. SQLite avoids external infrastructure while still demonstrating relational design. The schema intentionally has no password field.

## Why `secrets`?

Python's `secrets` module is intended for security-sensitive randomness. The generator therefore does not use `random`.
