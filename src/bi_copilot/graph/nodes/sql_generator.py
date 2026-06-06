from bi_copilot.agents.sql_agent import SQLAgent
from bi_copilot.config.settings import settings
from bi_copilot.llms.model_router import LLMRouter


llm_router = LLMRouter(settings)
sql_agent = SQLAgent(llm=llm_router.for_task("sql"))
generate_sql_node = sql_agent.as_node()