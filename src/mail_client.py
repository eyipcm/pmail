"""
Mail client for sending emails via Gmail SMTP.

Copyright (C) 2025 Ernest YIP eyipcm@gmail.com
SPDX-License-Identifier: MIT 
See the LICENSE file in the project root for full license text.
"""

import smtplib
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional, List, Union
from pathlib import Path
import sys

# Add project root to Python path
_project_root = Path(__file__).parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from config import EmailConfig
from config.logger_config import get_logger

# Initialize logger
logger = get_logger("pmail.mail_client")


class MailClient:
    """Client for sending emails via Gmail SMTP."""
    
    def __init__(self, config: Optional[EmailConfig] = None):
        """Initialize the mail client.
        
        Args:
            config: EmailConfig instance. If None, creates a new one.
        """
        logger.info("Initializing MailClient")
        self.config = config or EmailConfig()
        
        if not self.config.is_configured():
            logger.error("Gmail credentials not configured")
            raise ValueError(
                "Gmail credentials not configured. "
                "Set GMAIL_ADDRESS and GMAIL_PASSWORD environment variables."
            )
        
        is_valid, error_msg = self.config.validate()
        if not is_valid:
            logger.error(f"Invalid configuration: {error_msg}")
            raise ValueError(f"Invalid configuration: {error_msg}")
        
        logger.info(f"MailClient initialized successfully. SMTP Server: {self.config.smtp_server}:{self.config.smtp_port}")
    
    def send_email(
        self,
        to: Union[str, List[str]],
        subject: str,
        body: Optional[str] = None,
        body_html: Optional[str] = None,
        from_address: Optional[str] = None,
        cc: Optional[Union[str, List[str]]] = None,
        bcc: Optional[Union[str, List[str]]] = None,
        attachments: Optional[Union[str, List[str]]] = None,
    ) -> bool:
        """Send an email via Gmail SMTP.
        
        Args:
            to: Recipient email address(es) - string or list of strings
            subject: Email subject
            body: Plain text email body (optional if body_html is provided)
            body_html: Optional HTML email body
            from_address: Sender email address (defaults to configured Gmail address)
            cc: CC recipient(s) - string or list of strings
            bcc: BCC recipient(s) - string or list of strings
            attachments: File path(s) to attach - string or list of strings
        
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            # Validate that at least body or body_html is provided
            if not body and not body_html:
                logger.error("Either body or body_html must be provided")
                raise ValueError("Either body (plain text) or body_html must be provided")
            
            # If only HTML is provided, generate a simple plain text fallback
            if not body and body_html:
                # Extract text from HTML for plain text fallback
                import re
                # Simple HTML tag removal for plain text fallback
                body = re.sub(r'<[^>]+>', '', body_html).strip()
                if not body:
                    body = "This email contains HTML content. Please view in an HTML-compatible email client."
                logger.debug("Generated plain text fallback from HTML content")
            # Normalize recipients to lists
            if isinstance(to, str):
                to = [to]
            if cc and isinstance(cc, str):
                cc = [cc]
            if bcc and isinstance(bcc, str):
                bcc = [bcc]
            
            # Normalize attachments to list
            if attachments:
                if isinstance(attachments, str):
                    attachments = [attachments]
                # Convert to Path objects and validate
                attachment_paths = []
                for att_path in attachments:
                    path = Path(att_path)
                    if not path.exists():
                        logger.error(f"Attachment file not found: {att_path}")
                        return False
                    if not path.is_file():
                        logger.error(f"Attachment is not a file: {att_path}")
                        return False
                    attachment_paths.append(path)
            else:
                attachment_paths = []
            
            # Log email sending attempt
            logger.info(f"Attempting to send email - Subject: '{subject}'")
            logger.debug(f"To: {to}, CC: {cc}, BCC: {bcc if bcc else 'None'}")
            logger.debug(f"From: {from_address or self.config.default_sender or self.config.gmail_address}")
            logger.debug(f"Has HTML: {body_html is not None}, Has plain text: {body is not None}, Body length: {len(body) if body else 0}")
            logger.debug(f"Attachments: {len(attachment_paths)} file(s)")
            
            # Create message structure
            # If there are attachments, use 'mixed' as root container
            # If no attachments but HTML, use 'alternative' for body
            # If no attachments and no HTML, use plain MIMEText
            
            if attachment_paths:
                # Root message with 'mixed' subtype to contain body and attachments
                msg = MIMEMultipart("mixed")
                
                # Create body part (alternative or plain)
                if body_html:
                    body_part = MIMEMultipart("alternative")
                    body_part.attach(MIMEText(body, "plain"))
                    body_part.attach(MIMEText(body_html, "html"))
                    logger.debug("Created multipart body with HTML and plain text")
                else:
                    body_part = MIMEText(body, "plain")
                    logger.debug("Created plain text body")
                
                # Attach body to root message
                msg.attach(body_part)
                
                # Attach files
                for file_path in attachment_paths:
                    try:
                        # Determine content type
                        ctype, encoding = mimetypes.guess_type(str(file_path))
                        if ctype is None or encoding is not None:
                            ctype = 'application/octet-stream'
                        
                        maintype, subtype = ctype.split('/', 1)
                        
                        # Read and attach file
                        with open(file_path, 'rb') as f:
                            attachment = MIMEBase(maintype, subtype)
                            attachment.set_payload(f.read())
                        
                        # Encode attachment in base64
                        encoders.encode_base64(attachment)
                        
                        # Set filename
                        attachment.add_header(
                            'Content-Disposition',
                            f'attachment; filename={file_path.name}'
                        )
                        
                        msg.attach(attachment)
                        logger.debug(f"Attached file: {file_path.name} ({ctype})")
                    
                    except Exception as e:
                        logger.error(f"Error attaching file {file_path}: {e}", exc_info=True)
                        return False
                
                logger.debug(f"Created multipart email with {len(attachment_paths)} attachment(s)")
            
            elif body_html:
                # No attachments, but has HTML - use alternative
                msg = MIMEMultipart("alternative")
                msg.attach(MIMEText(body, "plain"))
                msg.attach(MIMEText(body_html, "html"))
                logger.debug("Created multipart email with HTML and plain text")
            
            else:
                # No attachments, no HTML - simple plain text
                msg = MIMEText(body, "plain")
                logger.debug("Created plain text email")
            
            # Set message headers
            msg["Subject"] = subject
            msg["From"] = from_address or self.config.default_sender or self.config.gmail_address
            msg["To"] = ", ".join(to)
            
            if cc:
                msg["Cc"] = ", ".join(cc)
            
            # Collect all recipients for sending
            recipients = to.copy()
            if cc:
                recipients.extend(cc)
            if bcc:
                recipients.extend(bcc)
            
            logger.debug(f"Connecting to SMTP server {self.config.smtp_server}:{self.config.smtp_port}")
            
            # Connect to SMTP server and send
            with smtplib.SMTP(self.config.smtp_server, self.config.smtp_port) as server:
                if self.config.use_tls:
                    logger.debug("Starting TLS encryption")
                    server.starttls()
                
                logger.debug(f"Logging in as {self.config.gmail_address}")
                server.login(self.config.gmail_address, self.config.gmail_password)
                logger.debug("Login successful")
                
                logger.debug(f"Sending email to {len(recipients)} recipient(s)")
                server.send_message(msg, to_addrs=recipients)
                logger.info(f"Email sent successfully - Subject: '{subject}', To: {to}")
            
            return True
        
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error occurred while sending email - Subject: '{subject}': {e}", exc_info=True)
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending email - Subject: '{subject}': {e}", exc_info=True)
            return False
    
    def send_email_to_ymail(
        self,
        ymail_address: str,
        subject: str,
        body: Optional[str] = None,
        body_html: Optional[str] = None,
        from_address: Optional[str] = None,
        cc: Optional[Union[str, List[str]]] = None,
        bcc: Optional[Union[str, List[str]]] = None,
        attachments: Optional[Union[str, List[str]]] = None,
    ) -> bool:
        """Convenience method to send email to Yahoo Mail address.
        
        Args:
            ymail_address: Yahoo Mail recipient address
            subject: Email subject
            body: Plain text email body (optional if body_html is provided)
            body_html: Optional HTML email body
            from_address: Sender email address
            cc: CC recipient(s)
            bcc: BCC recipient(s)
            attachments: File path(s) to attach - string or list of strings
        
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        logger.info(f"Using send_email_to_ymail convenience method for {ymail_address}")
        return self.send_email(
            to=ymail_address,
            subject=subject,
            body=body,
            body_html=body_html,
            from_address=from_address,
            cc=cc,
            bcc=bcc,
            attachments=attachments,
        )

