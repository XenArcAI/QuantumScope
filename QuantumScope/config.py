"""Enhanced configuration management for QuantumScope."""
import os
import json
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class ConfigError(Exception):
    """Configuration error class."""
    pass

class ConfigManager:
    """Manages configuration with environment variable overrides."""
    
    DEFAULTS = {
        "websocket_url": "wss://searc.ai/ws",
        "timeout": 30,
        "max_retries": 3,
        "cache_ttl": 3600,  # 1 hour
        "log_level": "INFO",
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration.
        
        Args:
            config_path: Optional path to config file
        """
        self.config = self.DEFAULTS.copy()
        self.config_path = config_path or os.path.expanduser("~/.config/quantumscope/config.json")
        self._load_config()
        self._load_env_vars()
    
    def _load_config(self) -> None:
        """Load configuration from file if it exists."""
        try:
            config_dir = os.path.dirname(self.config_path)
            if not os.path.exists(config_dir):
                os.makedirs(config_dir, exist_ok=True)
                return
                
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                    self.config.update(file_config)
        except (json.JSONDecodeError, OSError) as e:
            raise ConfigError(f"Failed to load config: {e}") from e
    
    def _load_env_vars(self) -> None:
        """Load configuration from environment variables."""
        env_mapping = {
            "QUANTUMSCOPE_WEBSOCKET_URL": "websocket_url",
            "QUANTUMSCOPE_TIMEOUT": ("timeout", int),
            "QUANTUMSCOPE_MAX_RETRIES": ("max_retries", int),
            "QUANTUMSCOPE_CACHE_TTL": ("cache_ttl", int),
            "QUANTUMSCOPE_LOG_LEVEL": "log_level",
        }
        
        for env_var, config_key in env_mapping.items():
            value = os.getenv(env_var)
            if value is not None:
                if isinstance(config_key, tuple):
                    key, type_func = config_key
                    try:
                        value = type_func(value)
                    except (ValueError, TypeError) as e:
                        raise ConfigError(
                            f"Invalid value for {env_var}: {value}"
                        ) from e
                    self.config[key] = value
                else:
                    self.config[config_key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self.config[key] = value
    
    def save(self) -> None:
        """Save configuration to file."""
        try:
            config_dir = os.path.dirname(self.config_path)
            os.makedirs(config_dir, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
        except OSError as e:
            raise ConfigError(f"Failed to save config: {e}") from e
    
    def __getitem__(self, key: str) -> Any:
        """Get a configuration value using dict-like access."""
        if key not in self.config:
            raise KeyError(f"No such config key: {key}")
        return self.config[key]
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Set a configuration value using dict-like access."""
        self.config[key] = value
    
    def __contains__(self, key: str) -> bool:
        """Check if a configuration key exists."""
        return key in self.config

# Global configuration instance
config = ConfigManager()
