from typing import Any

from bi_copilot.graph.state import AgentState
from bi_copilot.tools.metadata import (
    load_table_descriptions,
    load_metric_glossary,
)


async def retrieve_metadata_node(state: AgentState) -> dict[str, Any]:
    table_descriptions = load_table_descriptions()
    metric_glossary = load_metric_glossary()

    return {
        "database_schema": table_descriptions,
        "metric_definitions": metric_glossary,
        "current_step": "metadata_retrieved",
        "audit_trace": [
            {
                "agent": "metadata_retriever",
                "status": "success",
                "tables_loaded": len(table_descriptions),
                "metrics_loaded": len(metric_glossary),
            }
        ],
    }