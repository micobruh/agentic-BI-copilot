from pathlib import Path
from typing import Any, Literal

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from bi_copilot.agents.base import BaseAgent
from bi_copilot.graph.state import BIState


PLANNER_PROMPT_PATH = Path(__file__).parents[1] / "prompts" / "planner.md"


class RetrievalTarget(BaseModel):
    source_type: Literal["database", "document", "metric_catalog", "unknown"]
    target: str
    reason: str


class PlannerOutput(BaseModel):
    intent: str
    question_type: Literal[
        "lookup",
        "aggregation",
        "trend",
        "ranking",
        "comparison",
        "diagnostic",
        "unknown",
    ]
    evidence_needed: list[str] = Field(default_factory=list)
    metrics_needed: list[str] = Field(default_factory=list)
    dimensions_needed: list[str] = Field(default_factory=list)
    filters_needed: list[str] = Field(default_factory=list)
    relevant_tables: list[str] = Field(default_factory=list)
    plan: dict[str, Any] = Field(default_factory=dict)
    retrieval_targets: list[RetrievalTarget] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    answerable: bool
    next_action: Literal[
        "retrieve_evidence",
        "retrieve_metadata",
        "generate_sql",
        "ask_clarification",
        "stop",
    ]


class PlannerAgent(BaseAgent):
    name = "planner_agent"

    def build_chain(self):
        parser = PydanticOutputParser(pydantic_object=PlannerOutput)
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    PLANNER_PROMPT_PATH.read_text(encoding="utf-8")
                    + "\n\n{format_instructions}",
                ),
                (
                    "human",
                    """
                    User question:
                    {question}

                    Available database tables:
                    {available_tables}

                    Metric definitions:
                    {metric_definitions}
                    """,
                ),
            ]
        ).partial(format_instructions=parser.get_format_instructions())
        return prompt | self.llm | parser

    def build_input(self, state: BIState):
        return {
            "question": state.user_question,
            "available_tables": list(state.database_schema),
            "metric_definitions": state.metric_definitions,
        }

    def parse_output(self, output: PlannerOutput, state: BIState):
        return {
            "intent": output.intent,
            "relevant_tables": output.relevant_tables,
            "retrieval_targets": [
                target.model_dump() for target in output.retrieval_targets
            ],
            "plan": output.model_dump(),
        }
