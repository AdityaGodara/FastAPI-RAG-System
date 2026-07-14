from groq import AsyncGroq

from app.core.config import settings
from app.llm.base import BaseLLM


class GroqProvider(BaseLLM):

    def __init__(self):
        self.client = AsyncGroq(
            api_key=settings.groq_api_key,
        )

        self.model = "llama-3.3-70b-versatile"

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0,
        )

        return response.choices[0].message.content