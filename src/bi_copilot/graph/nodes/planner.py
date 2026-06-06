from bi_copilot.agents.planner_agent import PlannerAgent
from bi_copilot.config.settings import settings
from bi_copilot.llms.model_router import LLMRouter


llm_router = LLMRouter(settings)
planner_agent = PlannerAgent(llm=llm_router.for_task("planner"))
planner_node = planner_agent.as_node()