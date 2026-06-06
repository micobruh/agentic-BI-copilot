from typing import Any
from pydantic import BaseModel, Field


class PlannerOutput(BaseModel):
    intent: str
    plan: dict[str, Any] = Field(default_factory=dict)
    retrieval_targets: list[dict[str, Any]] = Field(default_factory=list)


class SQLValidationResult(BaseModel):
    is_valid: bool
    errors: list[str] = Field(default_factory=list)
    risk_level: str | None = None


class VerificationResult(BaseModel):
    passed: bool
    issues: list[str] = Field(default_factory=list)
    needs_revision: bool = False