from typing import Any

from bi_copilot.graph.state import AgentState
from bi_copilot.tools.database import run_query


async def execute_sql_node(state: AgentState) -> dict[str, Any]:
    validation = state.get("sql_validation_result", {})

    if not validation.get("is_valid"):
        return {
            "errors": ["SQL execution skipped because validation failed."],
            "current_step": "sql_execution_skipped",
            "audit_trace": [
                {
                    "agent": "sql_executor",
                    "status": "skipped",
                    "reason": "validation_failed",
                }
            ],
        }

    sql = validation.get("safe_sql") or state.get("generated_sql")

    if not sql:
        return {
            "errors": ["SQL execution skipped because no safe SQL was available."],
            "current_step": "sql_execution_failed",
            "audit_trace": [
                {
                    "agent": "sql_executor",
                    "status": "error",
                    "error": "missing_safe_sql",
                }
            ],
        }

    try:
        query_result = run_query(sql)

        return {
            "query_result": query_result,
            "current_step": "sql_executed",
            "audit_trace": [
                {
                    "agent": "sql_executor",
                    "status": "success",
                }
            ],
        }

    except Exception as exc:
        return {
            "errors": [f"SQL execution failed: {exc}"],
            "current_step": "sql_execution_failed",
            "audit_trace": [
                {
                    "agent": "sql_executor",
                    "status": "error",
                    "error": str(exc),
                }
            ],
        }