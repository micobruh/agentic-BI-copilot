# src/bi_copilot/mcp/servers/db_server.py

from mcp.server.fastmcp import FastMCP
from bi_copilot.tools.database import get_database_schema, run_readonly_sql

mcp = FastMCP("bi-database-server")


@mcp.tool()
def get_schema() -> dict:
    return get_database_schema()


@mcp.tool()
def run_sql(sql: str) -> list[dict]:
    return run_readonly_sql(sql)


if __name__ == "__main__":
    mcp.run()