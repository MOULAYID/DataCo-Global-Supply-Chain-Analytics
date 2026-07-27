"""
Logger utility module for DataCo Global Supply Chain Analytics project.
"""
import logging
import os
import sys

def get_logger(name: str = "DataCoSupplyChain") -> logging.Logger:
    """Configures and returns a standardized logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        # File handler
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        fh = logging.FileHandler(os.path.join(log_dir, "pipeline.log"))
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
    return logger
