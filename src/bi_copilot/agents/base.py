from abc import ABC, abstractmethod
from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import Runnable
from pydantic import BaseModel

from bi_copilot.graph.state import BIState


class AgentResult(BaseModel):
    updates: dict[str, Any]
    audit: dict[str, Any] = {}


class BaseAgent(ABC):
    name: str

    def __init__(self, llm: BaseChatModel, tools: list[Any] | None = None):
        self.llm = llm
        self.tools = tools or []
        self.chain = self.build_chain()

    @abstractmethod
    def build_chain(self) -> Runnable:
        """Build the LangChain runnable used by this agent."""

    @abstractmethod
    def build_input(self, state: BIState) -> dict[str, Any]:
        """Extract the agent-specific input from graph state."""

    @abstractmethod
    def parse_output(self, output: Any, state: BIState) -> dict[str, Any]:
        """Convert chain output into a LangGraph partial state update."""

    async def ainvoke(self, state: BIState) -> dict[str, Any]:
        try:
            agent_input = self.build_input(state)
            output = await self.chain.ainvoke(agent_input)
            updates = self.parse_output(output, state)

            updates.setdefault("audit_trace", [])
            updates["audit_trace"].append(
                {
                    "agent": self.name,
                    "status": "success",
                }
            )
            return updates

        except Exception as exc:
            return {
                "errors": [f"{self.name}: {exc}"],
                "audit_trace": [
                    {
                        "agent": self.name,
                        "status": "error",
                        "error": str(exc),
                    }
                ],
            }

    def as_node(self):
        return self.ainvoke