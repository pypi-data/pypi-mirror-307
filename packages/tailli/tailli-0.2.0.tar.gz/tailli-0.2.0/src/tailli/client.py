"""Client implementation for Tailli API."""

import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple

import httpx
from pydantic import BaseModel

from tailli.exceptions import TailliError, InvalidApiKeyError
from tailli.models import ApiKeyResponse, UsageResponse
from tailli.utils import BackgroundTask

logger = logging.getLogger(__name__)

class KeyCache(BaseModel):
    key: str
    expiry: datetime
    enabled: bool

class TailliClient:
    def __init__(
        self,
        base_url: str = "https://api.tailli.latentsearch.io",
        max_retries: int = 3,
        usage_batch_size: int = 10,
    ):
        self.base_url = base_url.rstrip('/')
        self.max_retries = max_retries
        self.usage_batch_size = usage_batch_size
        self._key_cache: Dict[str, KeyCache] = {}
        self._usage_queue: asyncio.Queue = asyncio.Queue()
        self._background_task: Optional[BackgroundTask] = None
        self._should_stop = False
    
    async def __aenter__(self):
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    async def start(self):
        """Start the background usage recording task."""
        if self._background_task is None:
            self._should_stop = False
            self._background_task = BackgroundTask(self._process_usage_queue())
            await self._background_task.start()
    
    async def close(self):
        """Shutdown the client and wait for pending usage records to be processed."""
        self._should_stop = True
        # Add a sentinel value to wake up the queue processor
        await self._usage_queue.put(None)
        if self._background_task is not None:
            await self._background_task.stop()
            self._background_task = None
    
    async def _process_usage_queue(self):
        """Background task to process the usage queue."""
        while not self._should_stop:
            try:
                # Wait for items in the queue
                item = await self._usage_queue.get()
                if item is None:  # Sentinel value
                    self._usage_queue.task_done()
                    break
                    
                api_key, units = item
                
                # Try to record the usage
                async with httpx.AsyncClient() as client:
                    for attempt in range(self.max_retries):
                        try:
                            response = await client.post(
                                f"{self.base_url}/api/ApiKeyUnitUsage",
                                params={"apikey": api_key, "units": units}
                            )
                            response.raise_for_status()
                            break
                        except httpx.HTTPError as e:
                            if attempt == self.max_retries - 1:
                                logger.error(f"Failed to record usage after {self.max_retries} attempts: {e}")
                            else:
                                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                                
                self._usage_queue.task_done()
                    
            except Exception as e:
                logger.error(f"Error processing usage queue: {e}")
    
    @asynccontextmanager
    async def validated_session(self, api_key: str):
        """
        Context manager that validates an API key and provides a session for using it.
        
        Args:
            api_key: The API key to validate
            
        Raises:
            InvalidApiKeyError: If the API key is invalid
            TailliError: If there's an error communicating with the API
        """
        if not await self.validate_key(api_key):
            raise InvalidApiKeyError("Invalid API key")
        try:
            yield self
        finally:
            pass

    async def validate_key(self, api_key: str) -> bool:
        """
        Validate an API key, using cached results when available.
        
        Args:
            api_key: The API key to validate
            
        Returns:
            bool: True if the key is valid
            
        Raises:
            TailliError: If there's an error communicating with the API
        """
        # Check cache first
        if api_key in self._key_cache:
            cache_entry = self._key_cache[api_key]
            if datetime.now() < cache_entry.expiry:
                return cache_entry.enabled
            else:
                del self._key_cache[api_key]
        
        # Validate with API
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/api/ApiKeyValidation",
                    params={"apikey": api_key}
                )
                response.raise_for_status()
                data = ApiKeyResponse.model_validate(response.json())
                
                # Cache the result
                self._key_cache[api_key] = KeyCache(
                    key=api_key,
                    expiry=datetime.now() + timedelta(hours=data.TTL),
                    enabled=data.Enabled
                )
                
                return data.Enabled
                
            except httpx.HTTPError as e:
                logger.error(f"Error validating API key: {e}")
                raise TailliError(f"Failed to validate API key: {e}")
    
    async def record_usage(self, api_key: str, units: int):
        """
        Record API usage for a key. This is done asynchronously in the background.
        
        Args:
            api_key: The API key to record usage for
            units: Number of units consumed
        """
        await self._usage_queue.put((api_key, units))