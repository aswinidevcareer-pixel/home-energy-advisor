import httpx
from typing import Optional, Any, List
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)
import logging
from app.infrastructure.llm.base import LLMProvider
from app.infrastructure.llm.types import ChatMessage
from app.domain.exceptions import (
    LLMConnectionError,
    LLMTimeoutError,
    LLMServiceUnavailableError
)
from app.constants import (
    LLM_TIMEOUT_SECONDS,
    LLM_RETRY_ATTEMPTS,
    LLM_RETRY_MIN_WAIT,
    LLM_RETRY_MAX_WAIT
)

logger = logging.getLogger(__name__)


class OllamaProvider(LLMProvider):
    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "llama3.2",
        timeout: int = LLM_TIMEOUT_SECONDS
    ):
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.timeout = timeout

    @retry(
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError)),
        stop=stop_after_attempt(LLM_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=1, min=LLM_RETRY_MIN_WAIT, max=LLM_RETRY_MAX_WAIT),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True
    )
    async def generate_completion(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        response_format: Optional[Any] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate completion from chat messages.
        
        Args:
            messages: List of ChatMessage objects with role and content
                     Example: [ChatMessage(role="system", content="..."), ChatMessage(role="user", content="...")]
            temperature: Sampling temperature
            response_format: Optional JSON schema for structured output
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated completion string
        """
        # Ollama supports /api/chat endpoint which natively accepts messages array
        url = f"{self.base_url}/api/chat"
        
        # Convert ChatMessage objects to dict format for Ollama
        messages_dict = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        payload = {
            "model": self.model,
            "messages": messages_dict,
            "stream": False,
            "options": {
                "temperature": temperature,
            }
        }
        
        # Enable JSON mode if schema provided
        if response_format:
            payload["format"] = response_format
        
        if max_tokens:
            payload["options"]["num_predict"] = max_tokens

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                result = response.json()
                # /api/chat returns message in result["message"]["content"]
                return result.get("message", {}).get("content", "")
            except httpx.TimeoutException:
                # Will be retried by tenacity, but if all retries fail, raise custom error
                raise LLMTimeoutError(
                    f"Ollama request timed out after {self.timeout} seconds. "
                    f"Model '{self.model}' may be too slow or overloaded."
                )
            except httpx.NetworkError as e:
                # Will be retried by tenacity, but if all retries fail, raise custom error
                raise LLMConnectionError(
                    f"Failed to connect to Ollama at {self.base_url}. "
                    f"Please ensure Ollama is running. Error: {str(e)}"
                )
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise LLMServiceUnavailableError(
                        f"Model '{self.model}' not found. Please run: ollama pull {self.model}"
                    )
                elif e.response.status_code >= 500:
                    raise LLMServiceUnavailableError(
                        f"Ollama service error (status {e.response.status_code}): {e.response.text}"
                    )
                else:
                    raise LLMConnectionError(
                        f"Ollama API error (status {e.response.status_code}): {e.response.text}"
                    )
            except httpx.HTTPError as e:
                raise LLMConnectionError(f"Ollama HTTP error: {str(e)}")
            except Exception as e:
                raise LLMConnectionError(f"Unexpected Ollama error: {str(e)}")

    def get_provider_name(self) -> str:
        return f"ollama-{self.model}"

    async def health_check(self) -> bool:
        url = f"{self.base_url}/api/tags"
        async with httpx.AsyncClient(timeout=5) as client:
            try:
                response = await client.get(url)
                return response.status_code == 200
            except Exception:
                return False
