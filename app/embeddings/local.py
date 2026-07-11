from sentence_transformers import SentenceTransformer

from app.embeddings.base import BaseEmbeddingProvider


class LocalEmbeddingProvider(BaseEmbeddingProvider):

    def __init__(self):
        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )

    async def embed(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )

        return embeddings.tolist()