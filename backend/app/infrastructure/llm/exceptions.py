"""Custom exceptions for LLM providers"""


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
