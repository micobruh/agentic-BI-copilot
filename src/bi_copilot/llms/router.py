class LLMRouter:
    def __init__(self, settings):
        self.settings = settings

    def for_task(self, task: str):
        if task == "planner":
            return self._get_strong_model()
        if task == "sql":
            return self._get_sql_model()
        if task == "verifier":
            return self._get_strong_model()
        if task == "reporter":
            return self._get_fast_model()

        return self._get_default_model()