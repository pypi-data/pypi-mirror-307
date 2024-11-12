class TailliError(Exception):
    """Base exception for Tailli client errors."""
    pass

class InvalidApiKeyError(TailliError):
    """Raised when an API key is invalid."""
    pass