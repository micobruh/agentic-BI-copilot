from langgraph.graph import StateGraph, START, END

from bi_copilot.graph.state import AgentState
from bi_copilot.graph.router import (
    route_after_sql_validation,
    route_after_verification,
)

from bi_copilot.graph.nodes.metadata_retriever import retrieve_metadata_node
from bi_copilot.graph.nodes.planner import planner_node
from bi_copilot.graph.nodes.sql_generator import generate_sql_node
from bi_copilot.graph.nodes.sql_validator import validate_sql_node
from bi_copilot.graph.nodes.sql_executor import execute_sql_node
from bi_copilot.graph.nodes.reporter import reporter_node
from bi_copilot.graph.nodes.verifier import verifier_node
from bi_copilot.graph.nodes.retry import increment_retry_node


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("metadata_retriever", retrieve_metadata_node)
    graph.add_node("planner", planner_node)
    graph.add_node("sql_generator", generate_sql_node)
    graph.add_node("sql_validator", validate_sql_node)
    graph.add_node("sql_executor", execute_sql_node)
    graph.add_node("reporter", reporter_node)
    graph.add_node("verifier", verifier_node)
    graph.add_node("increment_retry", increment_retry_node)

    graph.add_edge(START, "metadata_retriever")
    graph.add_edge("metadata_retriever", "planner")
    graph.add_edge("planner", "sql_generator")
    graph.add_edge("sql_generator", "sql_validator")

    graph.add_conditional_edges(
        "sql_validator",
        route_after_sql_validation,
        {
            "sql_executor": "sql_executor",
            "increment_retry": "increment_retry",
            "reporter": "reporter",
        },
    )

    graph.add_edge("increment_retry", "sql_generator")
    graph.add_edge("sql_executor", "reporter")
    graph.add_edge("reporter", "verifier")

    graph.add_conditional_edges(
        "verifier",
        route_after_verification,
        {
            END: END,
            "reporter": "reporter",
        },
    )

    return graph


def compile_graph(checkpointer=None):
    graph = build_graph()

    if checkpointer is not None:
        return graph.compile(checkpointer=checkpointer)

    return graph.compile()