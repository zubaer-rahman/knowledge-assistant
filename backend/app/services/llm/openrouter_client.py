import httpx
from app.core.config import settings


class OpenRouterClient:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    async def generate(self, question: str, context: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        prompt = f"""
You are a helpful assistant.

Use the context below to answer the question.

Context:
{context}

Question:
{question}
"""

        payload = {
            "model": "openai/gpt-4o-mini",
            "messages": [
                {"role": "user", "content": prompt}
            ],
        }

        async with httpx.AsyncClient() as client:
            res = await client.post(self.url, json=payload, headers=headers)

        return res.json()["choices"][0]["message"]["content"]