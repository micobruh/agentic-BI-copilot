# src/bi_copilot/graph/state.py

from typing import Any, Annotated, TypedDict
from operator import add


def merge_dicts(left: dict, right: dict) -> dict:
    return {**left, **right}


class AgentState(TypedDict, total=False):
    # Input
    user_question: str

    # Planning
    intent: str | None
    plan: dict[str, Any]
    retrieval_targets: list[dict[str, Any]]

    # Retrieval / metadata
    retrieved_context: Annotated[list[dict[str, Any]], add]
    database_schema: Annotated[dict[str, list[str]], merge_dicts]
    relevant_tables: list[str]
    metric_definitions: Annotated[dict[str, Any], merge_dicts]

    # SQL generation / validation / execution
    generated_sql: str | None
    sql_validation_result: dict[str, Any]
    query_result: list[dict[str, Any]]

    # Reporting
    analysis_summary: str | None
    chart_spec: str | None
    final_answer: str | None

    # Verification
    verification_result: dict[str, Any]

    # Control fields
    retry_count: int
    current_step: str

    # Accumulated diagnostics
    errors: Annotated[list[str], add]
    audit_trace: Annotated[list[dict[str, Any]], add]