from langgraph.graph import END
from bi_copilot.graph.state import AgentState


def route_after_sql_validation(state: AgentState) -> str:
    validation = state.get("sql_validation_result", {})

    if validation.get("is_valid"):
        return "sql_executor"

    if state.get("retry_count", 0) >= 3:
        return "reporter"

    return "increment_retry"


def route_after_verification(state: AgentState) -> str:
    verification = state.get("verification_result", {})

    if verification.get("passed"):
        return END

    return "reporter"