"""Utility functions for QuantumScope."""

from typing import Any, Dict, List, Optional, Union
import asyncio
import json
import logging
from pathlib import Path
import time
from functools import wraps

import aiohttp
from tqdm import tqdm

logger = logging.getLogger(__name__)

# Type aliases
JSONType = Union[Dict[str, Any], List[Any], str, int, float, bool, None]

def async_retry(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """Decorator for retrying async functions with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay between retries
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            retries = 0
            current_delay = delay
            last_exception = None
            
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:  # pylint: disable=broad-except
                    last_exception = e
                    retries += 1
                    if retries == max_retries:
                        logger.error(
                            "Max retries (%d) reached for %s", 
                            max_retries, 
                            func.__name__
                        )
                        raise
                    
                    logger.warning(
                        "Retry %d/%d for %s after error: %s",
                        retries,
                        max_retries,
                        func.__name__,
                        str(e)
                    )
                    
                    # Exponential backoff
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff
            
            # This should never be reached due to the raise above
            raise last_exception  # type: ignore
        return wrapper
    return decorator

async def download_file(
    url: str, 
    destination: Union[str, Path],
    session: Optional[aiohttp.ClientSession] = None,
    chunk_size: int = 8192,
    progress: bool = True
) -> Path:
    """Download a file with progress tracking.
    
    Args:
        url: URL of the file to download
        destination: Path to save the file
        session: Optional aiohttp ClientSession
        chunk_size: Size of chunks to download at once
        progress: Whether to show a progress bar
        
    Returns:
        Path to the downloaded file
    """
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    
    close_session = False
    if session is None:
        session = aiohttp.ClientSession()
        close_session = True
    
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            
            with tqdm(
                total=total_size, 
                unit='B', 
                unit_scale=True, 
                unit_divisor=1024,
                disable=not progress,
                desc=f"Downloading {destination.name}"
            ) as pbar:
                with open(destination, 'wb') as f:
                    async for chunk in response.content.iter_chunked(chunk_size):
                        f.write(chunk)
                        pbar.update(len(chunk))
                            
        return destination
    finally:
        if close_session and not session.closed:
            await session.close()

def format_duration(seconds: float) -> str:
    """Format a duration in seconds to a human-readable string."""
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    if minutes > 0:
        return f"{minutes}m {seconds}s"
    return f"{seconds}s"

def safe_json_loads(json_str: str) -> JSONType:
    """Safely parse a JSON string with error handling."""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error("Failed to parse JSON: %s", e)
        raise ValueError(f"Invalid JSON: {e}") from e

def human_readable_size(size: int, decimal_places: int = 2) -> str:
    """Convert a size in bytes to a human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"
