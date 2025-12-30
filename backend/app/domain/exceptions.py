"""Domain exceptions for the application"""


# Domain-level exceptions
class DomainError(Exception):
    """Base exception for domain-level errors"""
    pass


class HomeNotFoundError(DomainError):
    """Raised when a home profile is not found"""
    def __init__(self, home_id: str):
        self.resource_id = home_id
        super().__init__(f"Home profile with id '{home_id}' not found")


# LLM Provider exceptions
class LLMProviderError(Exception):
    """Base exception for LLM provider errors"""
    pass


class LLMConnectionError(LLMProviderError):
    """Raised when connection to LLM service fails"""
    pass


class LLMTimeoutError(LLMProviderError):
    """Raised when LLM service times out"""
    pass


class LLMValidationError(LLMProviderError):
    """Raised when LLM response validation fails"""
    pass


class LLMServiceUnavailableError(LLMProviderError):
    """Raised when LLM service is unavailable"""
    pass
