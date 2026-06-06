from pathlib import Path
from typing import Any

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from bi_copilot.agents.base import BaseAgent
from bi_copilot.graph.state import AgentState


REPORTER_PROMPT_PATH = Path(__file__).parents[1] / "prompts" / "reporter.md"


class ReporterAgent(BaseAgent):
    name = "reporter_agent"

    def build_chain(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    REPORTER_PROMPT_PATH.read_text(encoding="utf-8"),
                ),
                (
                    "human",
                    """
User question:
{question}

Plan:
{plan}

Generated SQL:
{generated_sql}

Query result:
{query_result}

Verification result:
{verification_result}

Errors:
{errors}
""",
                ),
            ]
        )

        return prompt | self.llm | StrOutputParser()

    def build_input(self, state: AgentState) -> dict[str, Any]:
        return {
            "question": state["user_question"],
            "plan": state.get("plan", {}),
            "generated_sql": state.get("generated_sql"),
            "query_result": state.get("query_result", []),
            "verification_result": state.get("verification_result", {}),
            "errors": state.get("errors", []),
        }

    def parse_output(self, output: str, state: AgentState) -> dict[str, Any]:
        return {
            "analysis_summary": output,
            "final_answer": output,
        }