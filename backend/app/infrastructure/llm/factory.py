from typing import Optional
from app.infrastructure.llm.base import LLMProvider
from app.infrastructure.llm.ollama_provider import OllamaProvider
from app.config import settings


class LLMProviderFactory:
    @staticmethod
    def create_provider(
        provider_type: Optional[str] = None,
        **kwargs
    ) -> LLMProvider:
        provider_type = provider_type or settings.LLM_PROVIDER
        
        if provider_type == "ollama":
            return OllamaProvider(
                base_url=kwargs.get("base_url", settings.OLLAMA_BASE_URL),
                model=kwargs.get("model", settings.OLLAMA_MODEL),
                timeout=kwargs.get("timeout", 120)
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider_type}")
