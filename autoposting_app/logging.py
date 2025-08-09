import logging
import sys
from typing import Optional


def setup_logging(
    level: str = "INFO",
    component: Optional[str] = None,
    format_type: str = "json"
) -> logging.Logger:
    """
    Setup structured logging for the application.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        component: Component name to include in logs (e.g., 'scheduler', 'cli')
        format_type: 'json' for structured JSON logs or 'text' for human-readable
    
    Returns:
        Configured logger instance
    """
    logger_name = f"autoposting.{component}" if component else "autoposting"
    logger = logging.getLogger(logger_name)
    
    # Avoid adding multiple handlers if already configured
    if logger.handlers:
        return logger
    
    # Set log level
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    
    # Set format based on type
    if format_type == "json":
        # JSON format for production/Fly.io
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
            '"component": "%(name)s", "message": "%(message)s"}'
        )
    else:
        # Human-readable format for development
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Prevent duplicate logs from parent loggers
    logger.propagate = False
    
    return logger


def get_logger(component: str) -> logging.Logger:
    """
    Get or create a logger for a specific component.
    Uses configuration from AppConfig if available.
    
    Args:
        component: Component name (e.g., 'scheduler', 'cli', 'telegram')
    
    Returns:
        Logger instance
    """
    # Try to get configuration from AppConfig
    try:
        from .config import load_config
        cfg = load_config()
        return setup_logging(
            level=cfg.log_level,
            component=component,
            format_type=cfg.log_format
        )
    except Exception:
        # Fallback to defaults if config loading fails
        return setup_logging(component=component)
