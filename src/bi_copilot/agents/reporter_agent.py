from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from bi_copilot.agents.base import BaseAgent
from bi_copilot.graph.state import BIState


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
                    """,
                ),
            ]
        )
        return prompt | self.llm | StrOutputParser()

    def build_input(self, state: BIState):
        return {
            "question": state.user_question,
            "plan": state.plan,
            "generated_sql": state.generated_sql,
            "query_result": state.query_result,
            "verification_result": state.verification_result,
        }

    def parse_output(self, output: str, state: BIState):
        return {
            "analysis_summary": output,
            "final_answer": output,
        }