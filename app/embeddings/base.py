from abc import ABC, abstractmethod


class BaseEmbeddingProvider(ABC):

    @abstractmethod
    async def embed(self, texts: list[str]) -> list[list[float]]:
        pass