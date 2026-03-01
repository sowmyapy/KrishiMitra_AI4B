"""
Logging configuration
"""
import logging
import sys
from pythonjsonlogger import jsonlogger
from .settings import settings


def setup_logging():
    """Configure application logging"""
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.log_level.upper()))
    
    # Remove existing handlers
    logger.handlers = []
    
    # Console handler with JSON formatting
    console_handler = logging.StreamHandler(sys.stdout)
    
    if settings.environment == "production":
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
        error_handler = logging.FileHandler('logs/error.log')
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        logger.addHandler(error_handler)
    
    return logger


# Initialize logging
logger = setup_logging()
