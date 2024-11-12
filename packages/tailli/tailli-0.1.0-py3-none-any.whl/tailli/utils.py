import asyncio
from typing import Coroutine, Optional

class BackgroundTask:
    """Utility for managing background tasks."""
    
    def __init__(self, coro: Coroutine):
        self.coro = coro
        self.task: Optional[asyncio.Task] = None
    
    async def start(self):
        """Start the background task."""
        if self.task is None:
            self.task = asyncio.create_task(self.coro)
    
    async def stop(self):
        """Stop the background task and wait for it to complete."""
        if self.task is not None:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
            self.task = None