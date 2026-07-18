from abc import ABC, abstractmethod


class BaseVisionModel(ABC):

    @abstractmethod
    async def describe_image(
        self,
        image: bytes,
        media_type: str,
    ) -> str:
        pass