from app.llm.groq import GroqProvider
from app.llm.prompts import TITLE_PROMPT

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
    
    async def generate_title(
            self,
            question: str,
            answer: str
    ):
        system_prompt = TITLE_PROMPT.format(
            question=question,
            answer=answer
        )

        return await self.provider.generate(
            system_prompt=system_prompt,
            history=[],
            user_prompt=""
        )