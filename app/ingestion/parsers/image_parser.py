from app.ingestion.parsers.base import BaseParser
from app.vision.service import VisionService


class ImageParser(BaseParser):

    def __init__(self):
        self.vision = VisionService()

    async def parse(
        self,
        file_bytes: bytes,
        media_type: str,
    ) -> str:

        return await self.vision.describe_image(
            image=file_bytes,
            media_type=media_type,
        )