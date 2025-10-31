"""
Configuration package for the email client.

Copyright (C) 2025 Ernest YIP 
SPDX-License-Identifier: MIT 
See the LICENSE file in the project root for full license text.
"""

from .email_config import EmailConfig
from .logger_config import get_logger, setup_logger

__all__ = ['EmailConfig', 'get_logger', 'setup_logger']

