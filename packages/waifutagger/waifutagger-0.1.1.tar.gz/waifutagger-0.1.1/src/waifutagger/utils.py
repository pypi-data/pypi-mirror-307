import logging
import time
from typing import Optional

def setup_logger() -> logging.Logger:
    """Setup and return logger instance."""
    logger = logging.getLogger('waifutagger')
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

def get_elapsed_time(start_time: float) -> str:
    """Get formatted elapsed time string."""
    elapsed = time.time() - start_time
    return f"{elapsed:.2f}s"

def is_valid_image_file(filepath: str) -> bool:
    """Check if file is a valid image file by extension."""
    return filepath.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))