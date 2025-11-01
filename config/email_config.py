"""
Configuration management for the email client.

Copyright (C) 2025 Ernest YIP eyipcm@gmail.com
SPDX-License-Identifier: MIT 
See the LICENSE file in the project root for full license text.
"""

import os
from typing import Optional, Tuple
from pathlib import Path


class EmailConfig:
    """Configuration class for email settings."""
    
    def __init__(self):
        """Initialize configuration from environment variables or defaults."""
        # Gmail SMTP settings
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        
        # Gmail credentials
        self.gmail_address = os.getenv("GMAIL_ADDRESS", "")
        self.gmail_password = os.getenv("GMAIL_PASSWORD", "")  # App password, not regular password
        
        # Default sender (can be overridden)
        self.default_sender = os.getenv("DEFAULT_SENDER", self.gmail_address)
        
        # Email settings
        self.use_tls = os.getenv("USE_TLS", "true").lower() == "true"
        
    def is_configured(self) -> bool:
        """Check if Gmail credentials are configured."""
        return bool(self.gmail_address and self.gmail_password)
    
    def validate(self) -> Tuple[bool, Optional[str]]:
        """Validate configuration.
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not self.gmail_address:
            return False, "GMAIL_ADDRESS is not set"
        
        if not self.gmail_password:
            return False, "GMAIL_PASSWORD is not set"
        
        if "@" not in self.gmail_address:
            return False, "GMAIL_ADDRESS must be a valid email address"
        
        return True, None

