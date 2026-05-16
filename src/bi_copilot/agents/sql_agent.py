from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from bi_copilot.agents.base import BaseAgent
from bi_copilot.graph.state import BIState


SQL_PROMPT_PATH = Path(__file__).parents[1] / "prompts" / "sql_generator.md"


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
                    """
                ),
            ]
        )
        return prompt | self.llm | StrOutputParser()

    def build_input(self, state: BIState):
        return {
            "question": state.user_question,
            "relevant_tables": state.relevant_tables,
            "metric_definitions": state.metric_definitions,
            "database_schema": state.database_schema,
        }

    def parse_output(self, output: str, state: BIState):
        return {"generated_sql": output}