from openai import OpenAI

from app.core.config import settings
from app.services.chat.types import ChatMessages

class LLMService:
    """Handles communication with the LLM via OpenRouter."""

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url=settings.OPENROUTER_BASE_URL,
        )

    def generate(self, messages: ChatMessages) -> str:
        response = self.client.chat.completions.create(
            model=settings.OPENROUTER_MODEL,
            messages=messages,
            temperature=0.2,
            max_tokens=512,
        )

        return response.choices[0].message.content or ""