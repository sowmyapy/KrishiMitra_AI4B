"""
Logging configuration
"""
import logging
import sys
from .settings import settings

# Try to import pythonjsonlogger, but make it optional
try:
    from pythonjsonlogger import jsonlogger
    HAS_JSON_LOGGER = True
except ImportError:
    HAS_JSON_LOGGER = False


def setup_logging():
    """Configure application logging"""
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.log_level.upper()))
    
    # Remove existing handlers
    logger.handlers = []
    
    # Console handler with JSON formatting
    console_handler = logging.StreamHandler(sys.stdout)
    
    if settings.environment == "production" and HAS_JSON_LOGGER:
        # JSON format for production (easier to parse)
        formatter = jsonlogger.JsonFormatter(
            '%(timestamp)s %(level)s %(name)s %(message)s',
            rename_fields={"levelname": "level", "asctime": "timestamp"}
        )
    else:
        # Human-readable format for development
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler for errors
    if settings.environment == "production":
        try:
            import os
            os.makedirs('logs', exist_ok=True)
            error_handler = logging.FileHandler('logs/error.log')
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(formatter)
            logger.addHandler(error_handler)
        except Exception as e:
            # If we can't create the log file, just skip it
            logger.warning(f"Could not create error log file: {e}")
    
    return logger


# Initialize logging
logger = setup_logging()
