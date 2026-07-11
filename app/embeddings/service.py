from app.embeddings.local import LocalEmbeddingProvider


class EmbeddingService:

    def __init__(self):
        self.provider = LocalEmbeddingProvider()

    async def embed(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        return await self.provider.embed(texts)