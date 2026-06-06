from pathlib import Path
from typing import Any, Literal

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from bi_copilot.agents.base import BaseAgent
from bi_copilot.graph.state import AgentState


VERIFIER_PROMPT_PATH = Path(__file__).parents[1] / "prompts" / "verifier.md"


class VerifierOutput(BaseModel):
    passed: bool
    status: Literal["pass", "warning", "fail"]
    issues: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)


class VerifierAgent(BaseAgent):
    name = "verifier_agent"

    def build_chain(self):
        parser = PydanticOutputParser(pydantic_object=VerifierOutput)

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    VERIFIER_PROMPT_PATH.read_text(encoding="utf-8")
                    + "\n\n{format_instructions}",
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

SQL validation result:
{sql_validation_result}

Query result:
{query_result}

Current analysis summary:
{analysis_summary}

Draft answer:
{draft_answer}
""",
                ),
            ]
        ).partial(format_instructions=parser.get_format_instructions())

        return prompt | self.llm | parser

    def build_input(self, state: AgentState) -> dict[str, Any]:
        return {
            "question": state["user_question"],
            "plan": state.get("plan", {}),
            "generated_sql": state.get("generated_sql"),
            "sql_validation_result": state.get("sql_validation_result", {}),
            "query_result": state.get("query_result", []),
            "analysis_summary": state.get("analysis_summary"),
            "draft_answer": state.get("draft_answer"),
        }

    def parse_output(self, output: VerifierOutput, state: AgentState) -> dict[str, Any]:
        updates: dict[str, Any] = {
            "verification_result": output.model_dump(),
        }

        if output.passed:
            updates["final_answer"] = (
                state.get("draft_answer")
                or state.get("analysis_summary")
                or ""
            )

        return updates