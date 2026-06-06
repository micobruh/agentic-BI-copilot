from functools import cached_property

from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq


class LLMRouter:
    def __init__(self, settings):
        self.settings = settings

    def for_task(self, task: str) -> BaseChatModel:
        task = task.lower()

        if self.settings.LLM_MODE == "free":
            return self._free_model_for_task(task)

        if self.settings.LLM_MODE == "quality":
            return self._quality_model_for_task(task)

        return self.default_model

    def _free_model_for_task(self, task: str) -> BaseChatModel:
        if task in {"planner", "sql", "verifier"}:
            return self.gemini_free_model

        if task == "reporter":
            return self.groq_fast_model

        return self.gemini_free_model

    def _quality_model_for_task(self, task: str) -> BaseChatModel:
        if task == "planner":
            return self.gemini_free_model

        if task == "sql":
            return self.openai_sql_model

        if task == "verifier":
            return self.gemini_free_model

        if task == "reporter":
            return self.openai_fast_model

        return self.default_model

    @cached_property
    def gemini_free_model(self) -> BaseChatModel:
        return ChatGoogleGenerativeAI(
            model=self.settings.GEMINI_MODEL,
            temperature=0,
            google_api_key=self.settings.GOOGLE_API_KEY,
        )

    @cached_property
    def groq_fast_model(self) -> BaseChatModel:
        return ChatGroq(
            model=self.settings.GROQ_MODEL,
            temperature=0.2,
            api_key=self.settings.GROQ_API_KEY,
        )

    @cached_property
    def openai_sql_model(self) -> BaseChatModel:
        return ChatOpenAI(
            model=self.settings.OPENAI_SQL_MODEL,
            temperature=0,
            api_key=self.settings.OPENAI_API_KEY,
        )

    @cached_property
    def openai_fast_model(self) -> BaseChatModel:
        return ChatOpenAI(
            model=self.settings.OPENAI_FAST_MODEL,
            temperature=0.2,
            api_key=self.settings.OPENAI_API_KEY,
        )

    @cached_property
    def default_model(self) -> BaseChatModel:
        return self.gemini_free_model