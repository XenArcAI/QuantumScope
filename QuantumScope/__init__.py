"""
QuantumScope - AI-Powered Research Platform

QuantumScope is a powerful CLI tool that leverages artificial intelligence to perform
in-depth research on any topic, analyze information from multiple sources, and generate
detailed, well-structured reports.
"""

__version__ = "1.0.2"  # Keep in sync with pyproject.toml
__author__ = "Parvesh Rawal"
__email__ = "team@xenarcai.com"
__license__ = "MIT"
__status__ = "Production"

# Configure logging
import logging
from logging import NullHandler

# Set default logging handler to avoid "No handler found" warnings
logging.getLogger(__name__).addHandler(NullHandler())

# Main package imports
from .main import QuantumScopeEngine, QuantumScopeConfig, QuantumScopeCLI, main
from . import exceptions  # noqa: F401

# Re-export commonly used exceptions
from .exceptions import (  # noqa: F401
    QuantumScopeError,
    ConnectionError,
    AuthenticationError,
    TimeoutError,
    ValidationError,
    RateLimitError,
    ConfigurationError,
    CacheError
)

# Re-export config and cache modules
from . import config as config  # noqa: F401
from . import cache as cache  # noqa: F401

# Public API
__all__ = [
    # Main classes
    "QuantumScopeEngine",
    "QuantumScopeConfig",
    "QuantumScopeCLI",
    "main",
    
    # Modules
    "config",
    "cache",
    "exceptions",
    
    # Common exceptions
    "QuantumScopeError",
    "ConnectionError",
    "AuthenticationError",
    "TimeoutError",
    "ValidationError",
    "RateLimitError",
    "ConfigurationError",
    "CacheError",
    
    # Metadata
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__status__"
]

# Initialize default config
from .config import config as default_config  # noqa: E402

try:
    default_config = default_config
    """Default configuration instance."""
    
    # Ensure config directory exists
    from pathlib import Path
    config_dir = Path("~").expanduser() / ".config" / "quantumscope"
    config_dir.mkdir(parents=True, exist_ok=True)
    
except Exception as e:  # pylint: disable=broad-except
    # Don't fail if config can't be loaded
    import warnings
    warnings.warn(f"Failed to initialize default config: {e}")