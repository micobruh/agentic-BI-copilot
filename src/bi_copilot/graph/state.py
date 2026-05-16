from typing import Any
from pydantic import BaseModel, Field

class BIState(BaseModel):
    user_question: str
    intent: str | None = None
    plan: dict[str, Any] = Field(default_factory=dict)
    retrieval_targets: list[dict[str, Any]] = Field(default_factory=list)
    retrieved_context: list[dict[str, Any]] = Field(default_factory=list)

    database_schema: dict[str, list[str]] = Field(default_factory=dict)
    relevant_tables: list[str] = Field(default_factory=list)
    metric_definitions: dict[str, Any] = Field(default_factory=dict)

    generated_sql: str | None = None
    sql_validation_result: dict[str, Any] = Field(default_factory=dict)
    query_result: list[dict[str, Any]] = Field(default_factory=list)

    analysis_summary: str | None = None
    chart_spec: str | None = None

    verification_result: dict[str, Any] = Field(default_factory=dict)
    final_answer: str | None = None

    errors: list[str] = Field(default_factory=list)
    audit_trace: list[dict[str, Any]] = Field(default_factory=list)
