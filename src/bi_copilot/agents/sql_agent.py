class SQLAgent:
    def __init__(self, llm, schema_tool, metric_tool):
        self.llm = llm
        self.schema_tool = schema_tool
        self.metric_tool = metric_tool

    def generate_sql(self, question: str, schema: str, metrics: dict) -> str:
        ...