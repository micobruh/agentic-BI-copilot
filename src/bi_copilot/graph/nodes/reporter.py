from bi_copilot.agents.reporter_agent import ReporterAgent
from bi_copilot.config.settings import settings
from bi_copilot.llms.model_router import LLMRouter


llm_router = LLMRouter(settings)
reporter_agent = ReporterAgent(llm=llm_router.for_task("reporter"))
reporter_node = reporter_agent.as_node()