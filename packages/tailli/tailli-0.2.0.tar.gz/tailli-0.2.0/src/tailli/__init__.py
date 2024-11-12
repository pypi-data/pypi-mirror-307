"""
Tailli API client package.

This package provides a high-performance async client for Tailli API key management 
and usage tracking.

Example:
    >>> from tailli import TailliClient
    >>> async with TailliClient() as client:
    ...     async with client.validated_session("your-api-key") as session:
    ...         await client.record_usage("your-api-key", 1)
"""

# Direct imports to make classes available at package level
from tailli.client import TailliClient
from tailli.exceptions import TailliError, InvalidApiKeyError
from tailli.models import ApiKeyResponse, UsageResponse

# Explicitly define what gets imported with "from tailli import *"
__all__ = [
    "TailliClient",
    "TailliError",
    "InvalidApiKeyError",
    "ApiKeyResponse",
    "UsageResponse",
]

__version__ = "0.1.0"