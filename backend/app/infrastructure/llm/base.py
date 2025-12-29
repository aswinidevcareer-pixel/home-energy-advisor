from abc import ABC, abstractmethod
from typing import Optional, Any


class LLMProvider(ABC):
    @abstractmethod
    async def generate_completion(
        self,
        prompt: str,
        temperature: float = 0.7,
        response_format: Optional[Any] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        pass
