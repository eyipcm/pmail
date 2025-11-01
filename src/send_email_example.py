"""
Example script for sending emails via Gmail.

Copyright (C) 2025 Ernest YIP <eyipcm@gmail.com>
SPDX-License-Identifier: MIT 
See the LICENSE file in the project root for full license text.
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
_project_root = Path(__file__).parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.mail_client import MailClient
from src.scheduler import EmailScheduler
from config import EmailConfig
from config.logger_config import get_logger

# Initialize logger
logger = get_logger("pmail.example")


def example_send_email():
    """Example: Send a simple email."""
    logger.info("Running example_send_email()")
    print("Example 1: Sending a simple email...")
    
    try:
        client = MailClient()
        
        success = client.send_email(
            to="recipient1@example.com",  # Replace with actual email
            subject="Test Email from PMail",
            body="This is a test email sent using PMail email client."
        )
        
        if success:
            logger.info("example_send_email() completed successfully")
            print("[OK] Email sent successfully!")
        else:
            logger.warning("example_send_email() failed to send email")
            print("[ERROR] Failed to send email.")
    
    except ValueError as e:
        logger.error(f"Configuration error in example_send_email(): {e}")
        print(f"Configuration error: {e}")
        print("\nPlease set GMAIL_ADDRESS and GMAIL_PASSWORD environment variables.")
    except Exception as e:
        logger.error(f"Error in example_send_email(): {e}", exc_info=True)
        print(f"Error: {e}")


def example_send_html_email():
    """Example: Send an HTML email."""
    logger.info("Running example_send_html_email()")
    print("\nExample 2: Sending an HTML email...")
    
    try:
        client = MailClient()
        
        html_body = """
        <html>
          <body>
            <h1>Hello from PMail!</h1>
            <p>This is an <strong>HTML</strong> email.</p>
            <p>You can use any HTML formatting.</p>
          </body>
        </html>
        """
        
        success = client.send_email(
            to="recipient1@example.com",  # Replace with actual email
            subject="HTML Email Test",
            body="Plain text version (for email clients that don't support HTML)",
            body_html=html_body
        )
        
        if success:
            logger.info("example_send_html_email() completed successfully")
            print("[OK] HTML email sent successfully!")
        else:
            logger.warning("example_send_html_email() failed to send email")
            print("[ERROR] Failed to send email.")
    
    except ValueError as e:
        logger.error(f"Configuration error in example_send_html_email(): {e}")
        print(f"Configuration error: {e}")
    except Exception as e:
        logger.error(f"Error in example_send_html_email(): {e}", exc_info=True)
        print(f"Error: {e}")


def example_send_with_attachments():
    """Example: Send an email with multiple attachments."""
    logger.info("Running example_send_with_attachments()")
    print("\nExample 2b: Sending email with attachments...")
    
    try:
        client = MailClient()
        
        # Example: Create a test file to attach (in real usage, use actual file paths)
        from pathlib import Path
        import tempfile
        
        # Create temporary test files
        temp_dir = Path(tempfile.gettempdir())
        test_file1 = temp_dir / "test_file1.txt"
        test_file2 = temp_dir / "test_file2.txt"
        
        # Write test content
        test_file1.write_text("This is test attachment file 1")
        test_file2.write_text("This is test attachment file 2")
        
        print(f"Created test files: {test_file1}, {test_file2}")
        
        success = client.send_email(
            to="recipient1@example.com",  # Replace with actual email
            subject="Email with Attachments Test",
            body="This email contains multiple attachments.",
            attachments=[str(test_file1), str(test_file2)]  # List of file paths
        )
        
        # Clean up test files
        test_file1.unlink(missing_ok=True)
        test_file2.unlink(missing_ok=True)
        
        if success:
            logger.info("example_send_with_attachments() completed successfully")
            print("[OK] Email with attachments sent successfully!")
        else:
            logger.warning("example_send_with_attachments() failed to send email")
            print("[ERROR] Failed to send email.")
    
    except ValueError as e:
        logger.error(f"Configuration error in example_send_with_attachments(): {e}")
        print(f"Configuration error: {e}")
    except Exception as e:
        logger.error(f"Error in example_send_with_attachments(): {e}", exc_info=True)
        print(f"Error: {e}")


def example_send_to_ymail():
    """Example: Send email to Yahoo Mail."""
    logger.info("Running example_send_to_ymail()")
    print("\nExample 3: Sending email to Yahoo Mail...")
    
    try:
        client = MailClient()
        
        success = client.send_email_to_ymail(
            ymail_address="recipient1@example.com",  # Replace with actual email
            subject="Email to Yahoo Mail",
            body="This email was sent to a Yahoo Mail address."
        )
        
        if success:
            logger.info("example_send_to_ymail() completed successfully")
            print("[OK] Email sent to Yahoo Mail successfully!")
        else:
            logger.warning("example_send_to_ymail() failed to send email")
            print("[ERROR] Failed to send email.")
    
    except ValueError as e:
        logger.error(f"Configuration error in example_send_to_ymail(): {e}")
        print(f"Configuration error: {e}")
    except Exception as e:
        logger.error(f"Error in example_send_to_ymail(): {e}", exc_info=True)
        print(f"Error: {e}")


def example_scheduled_email():
    """Example: Schedule an email task."""
    logger.info("Running example_scheduled_email()")
    print("\nExample 4: Setting up scheduled email...")
    
    try:
        scheduler = EmailScheduler()
        
        # Schedule a daily email at 9:30 AM
        scheduler.schedule_daily(
            time_str="09:30",
            to="recipient@yahoo.com",  # Replace with actual email
            subject="Daily Scheduled Email",
            body="This is a daily scheduled email sent at 9:30 AM."
        )
        
        print("[OK] Scheduled daily email at 9:30 AM")
        print("Jobs scheduled:")
        for job in scheduler.get_jobs():
            print(f"  - {job}")
        
        logger.info("Starting scheduler demo (10 seconds)")
        print("\nStarting scheduler (will run for 10 seconds as demo)...")
        print("Press Ctrl+C to stop early.")
        
        # Run for demo purposes (in production, use run_continuously())
        import time
        start_time = time.time()
        while time.time() - start_time < 10:
            scheduler.run_pending()
            time.sleep(1)
        
        logger.info("Scheduler demo finished")
        print("\nDemo finished.")
    
    except ValueError as e:
        logger.error(f"Configuration error in example_scheduled_email(): {e}")
        print(f"Configuration error: {e}")
    except KeyboardInterrupt:
        logger.info("Scheduler demo stopped by user (Ctrl+C)")
        print("\nScheduler stopped.")
    except Exception as e:
        logger.error(f"Error in example_scheduled_email(): {e}", exc_info=True)
        print(f"Error: {e}")


if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("PMail Email Client Examples - Starting")
    logger.info("=" * 50)
    print("PMail Email Client Examples")
    print("=" * 50)
    
    # Check configuration
    config = EmailConfig()
    if not config.is_configured():
        logger.warning("Gmail credentials not configured")
        print("\n[WARNING] Configuration Required!")
        print("=" * 50)
        print("Gmail credentials are not configured.")
        print("You need to set the following environment variables:")
        print("  - GMAIL_ADDRESS: Your Gmail address")
        print("  - GMAIL_PASSWORD: Your Gmail App Password (16 characters, no spaces)")
        print("\nWHERE TO SET:")
        print("  Set these variables in THIS terminal window before running the script.")
        print("\nHOW TO SET (Windows CMD):")
        print("  set GMAIL_ADDRESS=your-email@gmail.com")
        print("  set GMAIL_PASSWORD=abcdefghijklmnop")
        print("\nHOW TO SET (Windows PowerShell):")
        print('  $env:GMAIL_ADDRESS="your-email@gmail.com"')
        print('  $env:GMAIL_PASSWORD="abcdefghijklmnop"')
        print("\nHOW TO SET (Linux/Mac):")
        print("  export GMAIL_ADDRESS=your-email@gmail.com")
        print("  export GMAIL_PASSWORD=abcdefghijklmnop")
        print("\nIMPORTANT NOTES:")
        print("  - You MUST use a Gmail App Password, not your regular password")
        print("  - To get App Password: Google Account > Security > 2-Step Verification > App passwords")
        print("  - Set variables in the SAME terminal window where you run this script")
        print("  - Variables set with 'set' or '$env:' are only valid for current session")
        print("  - See README.md for detailed setup instructions and persistent configuration")
        print("\nVERIFY:")
        print("  After setting, verify with:")
        print("    Windows CMD: echo %GMAIL_ADDRESS%")
        print("    Windows PS:  echo $env:GMAIL_ADDRESS")
        print("    Linux/Mac:   echo $GMAIL_ADDRESS")
        print("=" * 50)
        sys.exit(1)
    
    # Run examples (uncomment the ones you want to test)
    # example_send_email()  # Currently active - sends basic plain text email
    example_send_html_email()
    # example_send_with_attachments()  # Example with multiple attachments
    # example_send_to_ymail()
    # example_scheduled_email()

