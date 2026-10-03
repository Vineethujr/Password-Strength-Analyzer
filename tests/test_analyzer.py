import sqlite3
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from backend.app import app
from backend.routes.api import COMMON_PASSWORDS
from backend.services.password_analyzer import analyze_password
from backend.services.password_generator import generate_complex_password, generate_passphrase
from backend.services.breach_checker import load_breach_hashes
from backend.services.policy_checker import Policy, evaluate_policy
from backend.services.character_analyzer import analyze_characters

client = TestClient(app)

CASES = [
    ("empty", "", "VERY WEAK"),
    ("one_char", "A", "VERY WEAK"),
    ("short_numeric", "1234", "VERY WEAK"),
    ("common", "password", "VERY WEAK"),
    ("long_repeated", "aaaaaaaaaaaaaaaa", "WEAK"),
    ("lowercase_only", "simplelowercase", None),
    ("uppercase_only", "SIMPLEUPPERCASE", None),
    ("numbers_only", "83746291827364", None),
    ("symbols_only", "!@#$%^&*()_+", None),
    ("mixed", "Mosaic!River7Glass", None),
    ("ascending_numbers", "abcd1234xyz", None),
    ("descending_numbers", "9876Alpha", None),
    ("ascending_letters", "abcdRIVER!", None),
    ("keyboard", "qwertyZX9", None),
    ("repeated_chars", "AAAAAA123!", None),
    ("repeated_substring", "abcabcabc!", None),
    ("common_word_number", "welcome123", None),
    ("word_year", "summer2026!", None),
    ("demo_keyboard_year", "qwerty2026!", "WEAK"),
    ("personal_name", "Rahul@123456789", None),
    ("birth_year", "BlueRiver2001!", None),
    ("passphrase", "velvet-galaxy-harbor-orchid-raven-meadow", "VERY STRONG"),
    ("unicode", "Δελτα-رود-森林-7!", None),
    ("spaces", "velvet galaxy harbor orchid", None),
    ("max_length", "A" * 128, None),
]

@pytest.mark.parametrize("name,password,expected", CASES)
def test_analysis_matrix(name, password, expected):
    result = analyze_password(password, common_passwords=COMMON_PASSWORDS, context={"first_name":"Rahul","birth_year":"2001","company_or_college":"Demo College"})
    assert "score" in result and 0 <= result["score"] <= 100
    assert "SyntheticSecretOnly" not in str(result)
    if expected:
        assert result["classification"] == expected


def test_strength_score_boundaries():
    from backend.services.scoring_engine import classify_score
    assert classify_score(0) == "VERY WEAK"
    assert classify_score(20) == "VERY WEAK"
    assert classify_score(21) == "WEAK"
    assert classify_score(40) == "WEAK"
    assert classify_score(41) == "MODERATE"
    assert classify_score(60) == "MODERATE"
    assert classify_score(61) == "STRONG"
    assert classify_score(80) == "STRONG"
    assert classify_score(81) == "VERY STRONG"
    assert classify_score(100) == "VERY STRONG"


def test_suggestion_generation():
    result = analyze_password("qwerty123", common_passwords=COMMON_PASSWORDS)
    assert any("sequence" in s.lower() or "keyboard" in s.lower() for s in result["suggestions"])


def test_secure_generator_complex():
    value = generate_complex_password(20, True, True, True, True)
    assert len(value) == 20
    assert any(c.isupper() for c in value)
    assert any(c.islower() for c in value)
    assert any(c.isdigit() for c in value)


def test_secure_generator_passphrase():
    value = generate_passphrase(6)
    assert len(value.split("-")) == 6


def test_password_not_stored_in_database(tmp_path, monkeypatch):
    import backend.db as db
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "analytics.db")
    db.init_db()
    result = analyze_password("SyntheticSecretOnly123!", common_passwords=COMMON_PASSWORDS)
    db.record_analysis(result)
    with sqlite3.connect(db.DB_PATH) as conn:
        columns_a = {r[1] for r in conn.execute("PRAGMA table_info(analyses)")}
        columns_f = {r[1] for r in conn.execute("PRAGMA table_info(findings)")}
        assert "password" not in columns_a
        assert "password" not in columns_f
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        assert {r[0] for r in tables} >= {"analyses", "findings"}


def test_password_not_in_api_response():
    secret = "SyntheticAPISecret-DoNotStore-2026!"
    response = client.post("/api/analyze", json={"password": secret})
    assert response.status_code == 200
    assert secret not in response.text


def test_password_not_logged(caplog):
    secret = "SyntheticLogCheck-DoNotLog-2026!"
    import logging
    caplog.set_level(logging.DEBUG)
    analyze_password(secret, common_passwords=COMMON_PASSWORDS)
    assert secret not in caplog.text


def test_breach_demo():
    hashes = load_breach_hashes()
    result = analyze_password("123456", common_passwords=COMMON_PASSWORDS, breach_hashes=hashes, include_breach=True)
    assert result["breach_check"]["compromised"] is True


def test_policy_separate_from_strength():
    result = analyze_password("LongEnoughButPredictable1234!", common_passwords=COMMON_PASSWORDS)
    assert "policy" in result and "score" in result
    assert result["policy"]["passed"] in {True, False}


def test_local_storage_contract_is_documented_by_schema():
    from backend.db import SCHEMA
    import re
    analysis_columns = re.findall(r"\b([a-z_]+)\s+(?:TEXT|INTEGER|REAL)", SCHEMA, flags=re.I)
    assert "password" not in {name.lower() for name in analysis_columns}
