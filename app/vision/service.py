from app.vision.gemini import GeminiVisionProvider


class VisionService:

    def __init__(self):
        self.provider = GeminiVisionProvider()

    async def describe_image(
        self,
        image: bytes,
        media_type: str,
    ) -> str:

        return await self.provider.describe_image(
            image=image,
            media_type=media_type,
        )