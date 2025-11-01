"""
Logging configuration for the email client.

Copyright (C) 2025 Ernest YIP eyipcm@gmail.com
SPDX-License-Identifier: MIT 
See the LICENSE file in the project root for full license text.
"""

import logging
import os
from datetime import datetime
from pathlib import Path


def setup_logger(name: str = "pmail", log_dir: str = None) -> logging.Logger:
    """Set up logger with file and console handlers.
    
    Args:
        name: Logger name (default: "pmail")
        log_dir: Directory for log files (default: D:\gitrepo\pmail\log)
    
    Returns:
        Configured logger instance
    """
    # Default log directory
    if log_dir is None:
        log_dir = Path(__file__).parent.parent / "log"
    else:
        log_dir = Path(log_dir)
    
    # Create log directory if it doesn't exist
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Capture all levels
    
    # Avoid duplicate handlers if logger already exists
    if logger.handlers:
        return logger
    
    # Log file format: email_yyyymmdd.log
    today = datetime.now().strftime("%Y%m%d")
    log_file = log_dir / f"email_{today}.log"
    
    # File handler - detailed logs
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    
    # Console handler - info and above
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str = "pmail") -> logging.Logger:
    """Get or create a logger instance.
    
    Args:
        name: Logger name
    
    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logger(name)
    return logger

