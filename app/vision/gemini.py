from email import mime
from google import genai
from google.genai import types

from app.core.config import settings
from app.vision.base import BaseVisionModel


class GeminiVisionProvider(BaseVisionModel):

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )

        self.model = "gemini-2.5-flash"

    async def describe_image(
        self,
        image: bytes,
        media_type: str,
    ) -> str:

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=[
                types.Part.from_bytes(
                    data=image,
                    mime_type=media_type,
                ),
                self._prompt(),
            ],
        )

        return response.text

    def _prompt(self) -> str:
        return """
You are an expert document understanding AI.

Analyze this image thoroughly.

Your goal is NOT just OCR.

Extract all useful semantic information.

Return the result as Markdown.

Include:

# OCR
Extract all visible text exactly.

# Objects
Describe important objects.

# Layout
Describe the spatial arrangement.

# Tables
Reconstruct tables.

# Charts
Explain charts and graphs.

# Diagrams
Explain nodes, arrows, relationships and flow.

# UI
If this is a screenshot, explain the interface and workflow.

# Code
Extract visible code.

# Handwriting
Transcribe handwritten text.

# Important Information
Extract names, numbers, labels, dates, addresses.

# Summary
Write a semantic summary useful for retrieval.

If something is uncertain, explicitly mention it.
"""