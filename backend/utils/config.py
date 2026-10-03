from __future__ import annotations
from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    cors_origins: tuple[str, ...] = ("http://localhost:5173", "http://127.0.0.1:5173")
    analytics_enabled: bool = os.getenv("ENABLE_ANALYTICS", "true").lower() == "true"
    max_password_length: int = int(os.getenv("MAX_PASSWORD_LENGTH", "128"))

settings = Settings()
