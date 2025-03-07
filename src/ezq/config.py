import logging
import os
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")

@dataclass
class QueueConfig:
    """Configuration for the queue connection"""
    host: str = "localhost"
    port: int = 5432
    username: str = "postgres"
    password: str = "postgres"
    database: str = "postgres"
    default_queue_name: str = "ezq"
    connection_timeout: int = 10
    connection_retries: int = 3
    connection_retry_delay: int = 1


@dataclass
class ConsumerConfig:
    """Configuration for the event consumer"""
    poll_interval: float = 1.0
    batch_size: int = 100
    concurrent_handlers: int = 5
    timeout: int = 30
    shutdown_grace_period: int = 5


@dataclass
class LoggingConfig:
    """Configuration for logging"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    enable_file_logging: bool = False
    log_file: Optional[str] = None


@dataclass
class EZQConfig:
    """Main configuration class for EZQ"""
    queue: QueueConfig = field(default_factory=QueueConfig)
    consumer: ConsumerConfig = field(default_factory=ConsumerConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    
    # Any additional configurations can be stored here
    extras: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_env(cls) -> "EZQConfig":
        """Create a configuration instance from environment variables"""
        config = cls()
        
        # Queue configuration
        config.queue.host = os.environ.get("EZQ_QUEUE_HOST", config.queue.host)
        config.queue.port = int(os.environ.get("EZQ_QUEUE_PORT", str(config.queue.port)))
        config.queue.username = os.environ.get("EZQ_QUEUE_USERNAME", config.queue.username)
        config.queue.password = os.environ.get("EZQ_QUEUE_PASSWORD", config.queue.password)
        config.queue.database = os.environ.get("EZQ_QUEUE_DATABASE", config.queue.database)
        config.queue.default_queue_name = os.environ.get("EZQ_DEFAULT_QUEUE_NAME", config.queue.default_queue_name)
        
        # Consumer configuration
        config.consumer.poll_interval = float(os.environ.get("EZQ_CONSUMER_POLL_INTERVAL", str(config.consumer.poll_interval)))
        config.consumer.batch_size = int(os.environ.get("EZQ_CONSUMER_BATCH_SIZE", str(config.consumer.batch_size)))
        config.consumer.concurrent_handlers = int(os.environ.get("EZQ_CONSUMER_CONCURRENT_HANDLERS", str(config.consumer.concurrent_handlers)))
        config.consumer.timeout = int(os.environ.get("EZQ_CONSUMER_TIMEOUT", str(config.consumer.timeout)))
        config.consumer.shutdown_grace_period = int(os.environ.get("EZQ_CONSUMER_SHUTDOWN_GRACE_PERIOD", str(config.consumer.shutdown_grace_period)))
        
        # Logging configuration
        config.logging.level = os.environ.get("EZQ_LOG_LEVEL", config.logging.level)
        config.logging.format = os.environ.get("EZQ_LOG_FORMAT", config.logging.format)
        config.logging.enable_file_logging = os.environ.get("EZQ_LOG_ENABLE_FILE_LOGGING", "").lower() == "true"
        if config.logging.enable_file_logging:
            config.logging.log_file = os.environ.get("EZQ_LOG_FILE", config.logging.log_file)
        
        return config

    @classmethod
    def load(cls) -> "EZQConfig":
        """
        Load configuration from environment variables or use defaults
        """
        return cls.from_env()


# Global configuration instance
_config: Optional[EZQConfig] = None


def get_config(reload: bool = False) -> EZQConfig:
    """
    Get the global configuration instance.
    
    Args:
        reload: Whether to reload the configuration from environment variables
        
    Returns:
        The global configuration instance
    """
    global _config
    if _config is None or reload:
        _config = EZQConfig.load()
    return _config


def configure(**kwargs: Any) -> None:
    """
    Configure EZQ programmatically.
    
    Args:
        **kwargs: Configuration values to override
        
    Example:
        configure(queue_host="postgres.example.com", queue_port=5433)
    """
    global _config
    
    # Start with current config or create a new one
    if _config is None:
        _config = EZQConfig.load()
        
    # Apply individual overrides
    for key, value in kwargs.items():
        # Handle queue configuration
        if key.startswith("queue_"):
            attr_name = key[6:]  # Remove 'queue_' prefix
            if hasattr(_config.queue, attr_name):
                setattr(_config.queue, attr_name, value)
                
        # Handle consumer configuration
        elif key.startswith("consumer_"):
            attr_name = key[9:]  # Remove 'consumer_' prefix
            if hasattr(_config.consumer, attr_name):
                setattr(_config.consumer, attr_name, value)
                
        # Handle logging configuration
        elif key.startswith("logging_"):
            attr_name = key[8:]  # Remove 'logging_' prefix
            if hasattr(_config.logging, attr_name):
                setattr(_config.logging, attr_name, value)
                
        # Handle top-level configuration
        elif hasattr(_config, key):
            setattr(_config, key, value)
            
        # Store unknown configuration in extras
        else:
            _config.extras[key] = value 