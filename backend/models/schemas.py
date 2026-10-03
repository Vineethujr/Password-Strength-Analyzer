from __future__ import annotations
from pydantic import BaseModel, Field, field_validator

class ContextInput(BaseModel):
    first_name: str = Field(default="", max_length=80)
    birth_year: str = Field(default="", max_length=4)
    company_or_college: str = Field(default="", max_length=120)

class PolicyInput(BaseModel):
    minimum_length: int = Field(default=15, ge=8, le=128)
    common_password_check: bool = True
    personal_info_check: bool = True
    maximum_length: int = Field(default=128, ge=64, le=256)

class AnalyzeRequest(BaseModel):
    password: str = Field(min_length=0, max_length=128)
    context: ContextInput | None = None
    policy: PolicyInput | None = None
    check_local_breach: bool = True

class GenerateRequest(BaseModel):
    mode: str = Field(default="complex")
    length: int = Field(default=20, ge=16, le=128)
    uppercase: bool = True
    lowercase: bool = True
    numbers: bool = True
    symbols: bool = True
    words: int = Field(default=6, ge=5, le=10)

    @field_validator("mode")
    @classmethod
    def valid_mode(cls, value: str) -> str:
        if value not in {"complex", "passphrase"}:
            raise ValueError("Unsupported generator mode")
        return value
