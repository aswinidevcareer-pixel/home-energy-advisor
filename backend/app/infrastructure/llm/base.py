from abc import ABC, abstractmethod
from typing import Optional, Any, List
from app.infrastructure.llm.types import ChatMessage


class LLMProvider(ABC):
    @abstractmethod
    async def generate_completion(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        response_format: Optional[Any] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate completion from a list of chat messages.
        
        Args:
            messages: List of ChatMessage objects with role and content
                     Example: [ChatMessage(role="system", content="..."), ChatMessage(role="user", content="...")]
            temperature: Sampling temperature
            response_format: Optional response format specification
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated completion string
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        pass
