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
        history: list
    ) -> str:

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        messages.extend(history)

        messages.append(
            {
                "role": "user",
                "content": user_prompt,
            }
        )
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0,
        )

        return response.choices[0].message.content

    async def stream(
    self,
    system_prompt: str,
    history: list,
    user_prompt: str,
    ):
        messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        messages.extend(history)

        messages.append(
            {
                "role": "user",
                "content": user_prompt,
            }
        )

        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0,
            stream=True,
        )

        async for chunk in stream:
            delta = chunk.choices[0].delta.content

            if delta:
                yield delta
        