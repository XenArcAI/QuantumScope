"""Custom exceptions for QuantumScope."""
from typing import Optional, Dict, Any, List

class QuantumScopeError(Exception):
    """Base exception for all QuantumScope errors."""
    
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None,
    ):
        """Initialize the exception.
        
        Args:
            message: Human-readable error message
            details: Additional error details
            cause: The original exception that caused this error
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}
        self.cause = cause
        
        # Add cause details if available
        if cause is not None:
            self.details['cause'] = str(cause)
            if hasattr(cause, '__traceback__'):
                self.details['traceback'] = self._format_traceback(cause.__traceback__)
    
    def __str__(self) -> str:
        """String representation of the error."""
        if self.details:
            return f"{self.message} | Details: {self.details}"
        return self.message
    
    @staticmethod
    def _format_traceback(tb) -> List[str]:
        """Format traceback for error details."""
        import traceback
        return traceback.format_tb(tb)


class ConnectionError(QuantumScopeError):
    """Raised when there's a connection-related error."""
    pass

class AuthenticationError(QuantumScopeError):
    """Raised when authentication fails."""
    pass

class TimeoutError(QuantumScopeError):
    """Raised when an operation times out."""
    pass

class ValidationError(QuantumScopeError):
    """Raised when input validation fails."""
    pass

class RateLimitError(QuantumScopeError):
    """Raised when rate limits are exceeded."""
    
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
        **kwargs
    ):
        """Initialize rate limit error.
        
        Args:
            message: Error message
            retry_after: Number of seconds to wait before retrying
            **kwargs: Additional error details
        """
        if retry_after is not None:
            kwargs['retry_after'] = retry_after
            message = f"{message}. Please try again in {retry_after} seconds."
            
        super().__init__(message, details=kwargs)
        self.retry_after = retry_after

class ConfigurationError(QuantumScopeError):
    """Raised when there's a configuration error."""
    pass

class CacheError(QuantumScopeError):
    """Raised when there's an error with the cache."""
    pass

def handle_errors(func):
    """Decorator to handle and wrap exceptions with QuantumScopeError."""
    from functools import wraps
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except QuantumScopeError:
            # Re-raise QuantumScope errors as-is
            raise
        except ConnectionError as e:
            raise ConnectionError("Connection failed") from e
        except TimeoutError as e:
            raise TimeoutError("Operation timed out") from e
        except Exception as e:
            # Wrap other exceptions
            raise QuantumScopeError(str(e)) from e
    
    return wrapper
