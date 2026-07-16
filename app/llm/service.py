from app.llm.groq import GroqProvider


class LLMService:

    def __init__(self):
        self.provider = GroqProvider()

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        history: list
    ) -> str:

        return await self.provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            history=history
        )