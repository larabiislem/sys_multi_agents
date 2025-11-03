# openrouter_llm.py
import os
from crewai import LLM

class OpenRouterLLM(LLM):
    def __init__(self, model="gpt-4o-mini", temperature=0.7):
        super().__init__(
            model=model,
            temperature=temperature,
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )
