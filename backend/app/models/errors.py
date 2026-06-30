"""Custom exceptions for AndesContext backend."""


class AndesContextError(Exception):
    """Base exception for all AndesContext errors."""


class ConfigurationError(AndesContextError):
    """Raised when configuration is invalid or incomplete."""


class OllamaConnectionError(AndesContextError):
    """Raised when Ollama is unreachable."""


class ModelNotFoundError(AndesContextError):
    """Raised when a required Ollama model is not available."""


class TokenizerError(AndesContextError):
    """Raised when the HuggingFace tokenizer is missing or invalid."""


class CogneeServiceError(AndesContextError):
    """Raised when a Cognee operation fails."""
