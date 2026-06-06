from abc import ABC, abstractmethod
from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import Runnable

from bi_copilot.graph.state import AgentState


class BaseAgent(ABC):
    """
    Base class for BI Copilot agents.

    Each concrete agent:
    1. Builds a LangChain runnable.
    2. Extracts its own input from the LangGraph state.
    3. Parses the chain output into a LangGraph partial state update.

    The returned dictionary is directly compatible with LangGraph nodes.
    """

    name: str

    def __init__(self, llm: BaseChatModel, tools: list[Any] | None = None):
        self.llm = llm
        self.tools = tools or []
        self.chain = self.build_chain()

    @abstractmethod
    def build_chain(self) -> Runnable:
        """Build the LangChain runnable used by this agent."""
        raise NotImplementedError

    @abstractmethod
    def build_input(self, state: AgentState) -> dict[str, Any]:
        """Extract the agent-specific input from the LangGraph state."""
        raise NotImplementedError

    @abstractmethod
    def parse_output(self, output: Any, state: AgentState) -> dict[str, Any]:
        """Convert chain output into a LangGraph partial state update."""
        raise NotImplementedError

    async def ainvoke(self, state: AgentState) -> dict[str, Any]:
        """
        Execute the agent as a LangGraph node.

        Returns a partial state update.
        """
        try:
            agent_input = self.build_input(state)
            output = await self.chain.ainvoke(agent_input)
            updates = self.parse_output(output, state)

            return {
                **updates,
                "current_step": self.name,
                "audit_trace": [
                    {
                        "agent": self.name,
                        "status": "success",
                    }
                ],
            }

        except Exception as exc:
            return {
                "current_step": self.name,
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
        """
        Return this agent as a LangGraph-compatible async node function.
        """
        return self.ainvoke