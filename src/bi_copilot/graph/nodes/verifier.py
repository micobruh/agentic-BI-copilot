# - Did the SQL use the correct tables?
# - Did it use the correct metric definition?
# - Did it apply the right filters?
# - Could the query cause duplicated rows?
# - Does the final answer match the query result?

from bi_copilot.agents.sql_agent import VerifierAgent
from bi_copilot.config.settings import settings
from bi_copilot.llms.model_router import LLMRouter


llm_router = LLMRouter(settings)
verifier_agent = VerifierAgent(llm=llm_router.for_task("verifier"))

verifier_node = verifier_agent.as_node()