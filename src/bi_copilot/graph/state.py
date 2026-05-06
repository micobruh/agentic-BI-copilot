from typing import Any, Optional
from pydantic import BaseModel


class BIState(BaseModel):
    user_question: str
    intent: Optional[str] = None
    relevant_tables: list[str] = []
    metric_definitions: dict[str, Any] = {}

    generated_sql: Optional[str] = None
    sql_validation_result: dict[str, Any] = {}
    query_result: list[dict[str, Any]] = []

    analysis_summary: Optional[str] = None
    chart_spec: Optional[dict[str, Any]] = None

    verification_result: dict[str, Any] = {}
    final_answer: Optional[str] = None

    errors: list[str] = []
    audit_trace: list[dict[str, Any]] = []