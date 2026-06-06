# src/bi_copilot/tools/langchain_tools.py

from langchain_core.tools import tool
from bi_copilot.tools.database import run_query


@tool
def execute_sql_tool(sql: str) -> str:
    """Execute a read-only SQL query."""
    return run_query(sql)