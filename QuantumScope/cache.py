"""Caching system for QuantumScope."""
import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any, Callable, Optional, TypeVar, cast
from functools import wraps

from .config import config

T = TypeVar('T')

def get_cache_key(*args: Any, **kwargs: Any) -> str:
    """Generate a cache key from function arguments."""
    key_parts = [str(arg) for arg in args] + [f"{k}={v}" for k, v in sorted(kwargs.items())]
    key_string = ":".join(key_parts).encode('utf-8')
    return hashlib.md5(key_string).hexdigest()

def get_cache_path(key: str) -> Path:
    """Get the filesystem path for a cache key."""
    cache_dir = Path.home() / ".cache" / "quantumscope"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / f"{key}.json"

class Cache:
    """Simple file-based caching system with TTL support."""
    
    def __init__(self, ttl: Optional[int] = None):
        """Initialize the cache.
        
        Args:
            ttl: Time to live in seconds. If None, uses default from config.
        """
        self.ttl = ttl or config.get("cache_ttl", 3600)
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache."""
        cache_file = get_cache_path(key)
        
        if not cache_file.exists():
            return None
            
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Check if cache is expired
            if time.time() - data['timestamp'] > self.ttl:
                cache_file.unlink()
                return None
                
            return data['value']
            
        except (json.JSONDecodeError, KeyError, OSError):
            # If there's any error reading the cache, remove the corrupted file
            try:
                cache_file.unlink()
            except OSError:
                pass
            return None
    
    def set(self, key: str, value: Any) -> None:
        """Store a value in the cache."""
        cache_file = get_cache_path(key)
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            data = {
                'value': value,
                'timestamp': time.time(),
                'ttl': self.ttl
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, default=str)
                
        except (TypeError, OSError) as e:
            # If we can't serialize the value or write to disk, just skip caching
            pass
    
    def clear(self) -> None:
        """Clear the entire cache."""
        cache_dir = Path.home() / ".cache" / "quantumscope"
        if cache_dir.exists():
            for file in cache_dir.glob("*.json"):
                try:
                    file.unlink()
                except OSError:
                    continue

def cached(ttl: Optional[int] = None):
    """Decorator to cache function results.
    
    Args:
        ttl: Time to live in seconds. If None, uses default from config.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        cache = Cache(ttl=ttl)
        
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            # Don't use cache if explicitly disabled
            if kwargs.pop('no_cache', False):
                return func(*args, **kwargs)
                
            # Generate cache key
            key_parts = [func.__module__, func.__name__] + list(args) + [f"{k}={v}" for k, v in sorted(kwargs.items())]
            key = get_cache_key(*key_parts)
            
            # Try to get from cache
            cached_result = cache.get(key)
            if cached_result is not None:
                return cached_result
                
            # Cache miss - call the function
            result = func(*args, **kwargs)
            
            # Cache the result
            try:
                cache.set(key, result)
            except Exception:  # pylint: disable=broad-except
                # Don't fail if caching fails
                pass
                
            return result
            
        return cast(Callable[..., T], wrapper)
    return decorator
