from abc import ABC, abstractmethod


class BaseParser(ABC):

    @abstractmethod
    async def parse(
        self,
        file_bytes: bytes,
        mime_type: str,
    ) -> str:
        pass