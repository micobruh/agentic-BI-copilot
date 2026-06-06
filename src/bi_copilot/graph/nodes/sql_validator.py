from typing import Any

from bi_copilot.graph.state import AgentState
from bi_copilot.tools.sql_validator import validate_sql


async def validate_sql_node(state: AgentState) -> dict[str, Any]:
    sql = state.get("generated_sql")

    if not sql:
        return {
            "sql_validation_result": {
                "is_valid": False,
                "errors": ["No SQL query was generated."],
                "warnings": [],
                "risk_flags": ["missing_sql"],
                "referenced_tables": [],
                "safe_sql": None,
            },
            "errors": ["No SQL query was generated."],
            "current_step": "sql_validation_failed",
            "audit_trace": [
                {
                    "agent": "sql_validator",
                    "status": "error",
                    "error": "No SQL query was generated.",
                }
            ],
        }

    result = validate_sql(
        sql=sql,
        schema=state.get("database_schema"),
    )

    updates: dict[str, Any] = {
        "sql_validation_result": result,
        "current_step": "sql_validated",
        "audit_trace": [
            {
                "agent": "sql_validator",
                "status": "success" if result["is_valid"] else "failed",
                "risk_flags": result.get("risk_flags", []),
            }
        ],
    }

    if result["is_valid"]:
        updates["generated_sql"] = result.get("safe_sql") or sql
    else:
        updates["errors"] = result.get("errors", [])

    return updates