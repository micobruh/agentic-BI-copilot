from bi_copilot.graph.state import AgentState


async def increment_retry_node(state: AgentState) -> dict:
    return {
        "retry_count": state.get("retry_count", 0) + 1,
        "current_step": "retrying_sql_generation",
    }