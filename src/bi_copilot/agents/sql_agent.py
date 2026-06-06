from pathlib import Path
from typing import Any

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from bi_copilot.agents.base import BaseAgent
from bi_copilot.graph.state import AgentState


SQL_PROMPT_PATH = Path(__file__).parents[1] / "prompts" / "sql_generator.md"


def clean_sql(sql: str) -> str:
    sql = sql.strip()

    if sql.startswith("```"):
        lines = sql.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]

        sql = "\n".join(lines).strip()

    return sql


class SQLAgent(BaseAgent):
    name = "sql_agent"

    def build_chain(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    SQL_PROMPT_PATH.read_text(encoding="utf-8"),
                ),
                (
                    "human",
                    """
User question:
{question}

Relevant table metadata:
{relevant_tables}

Relevant metric metadata:
{metric_definitions}

Database schema:
{database_schema}

Previous SQL validation result:
{sql_validation_result}

Previous errors:
{errors}
""",
                ),
            ]
        )

        return prompt | self.llm | StrOutputParser()

    def build_input(self, state: AgentState) -> dict[str, Any]:
        return {
            "question": state["user_question"],
            "relevant_tables": state.get("relevant_tables", []),
            "metric_definitions": state.get("metric_definitions", {}),
            "database_schema": state.get("database_schema", {}),
            "sql_validation_result": state.get("sql_validation_result", {}),
            "errors": state.get("errors", []),
        }

    def parse_output(self, output: str, state: AgentState) -> dict[str, Any]:
        return {
            "generated_sql": clean_sql(output),
        }