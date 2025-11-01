"""
Command-line interface for sending emails with attachments.

Copyright (C) 2025 Ernest YIP <eyipcm@gmail.com>
SPDX-License-Identifier: MIT 
See the LICENSE file in the project root for full license text.
"""

import sys
import argparse
from pathlib import Path

# Add project root to Python path
_project_root = Path(__file__).parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.mail_client import MailClient
from src import __version__, __license__
from config import EmailConfig
from config.logger_config import get_logger

logger = get_logger("pmail.cli")


def main():
    """Command-line interface for sending emails."""
    parser = argparse.ArgumentParser(
        description='Send email via Gmail SMTP',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Send plain text email
  python src/send_email_cli.py -t recipient@example.com -s "Hello" -b "Test message"

  # Send email with single attachment
  python src/send_email_cli.py -t recipient@example.com -s "Hello" -b "Test" -a file.pdf

  # Send email with multiple attachments
  python src/send_email_cli.py -t recipient@example.com -s "Hello" -b "Test" -a file1.pdf file2.jpg file3.txt

  # Send HTML email with attachments
  python src/send_email_cli.py -t recipient@example.com -s "Hello" -b "Plain text" --html "<h1>HTML</h1>" -a file.pdf

  # Send to multiple recipients with attachments
  python src/send_email_cli.py -t recipient1@example.com recipient2@example.com -s "Hello" -b "Test" -a file.pdf
        """
    )
    
    parser.add_argument(
        '-t', '--to',
        required=True,
        nargs='+',
        help='Recipient email address(es)'
    )
    
    parser.add_argument(
        '-s', '--subject',
        required=True,
        help='Email subject'
    )
    
    parser.add_argument(
        '-b', '--body',
        required=False,
        help='Email body (plain text, optional if --html is provided)'
    )
    
    parser.add_argument(
        '--html',
        help='HTML email body (optional)'
    )
    
    parser.add_argument(
        '-a', '--attachments',
        nargs='*',
        default=[],
        help='Attachment file path(s)'
    )
    
    parser.add_argument(
        '-c', '--cc',
        nargs='+',
        help='CC recipient(s)'
    )
    
    parser.add_argument(
        '--bcc',
        nargs='+',
        help='BCC recipient(s)'
    )
    
    parser.add_argument(
        '-f', '--from',
        dest='from_address',
        help='Sender email address (defaults to configured Gmail address)'
    )
    
    parser.add_argument(
        '--ymail',
        action='store_true',
        help='Use send_email_to_ymail convenience method'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s version {__version__}\n{__license__}'
    )
    
    args = parser.parse_args()
    
    try:
        # Check configuration
        config = EmailConfig()
        if not config.is_configured():
            logger.error("Gmail credentials not configured")
            print("ERROR: Gmail credentials not configured.")
            print("Please set GMAIL_ADDRESS and GMAIL_PASSWORD environment variables.")
            sys.exit(1)
        
        # Initialize client
        logger.info("Initializing MailClient for CLI")
        client = MailClient()
        
        # Prepare attachments
        attachments = args.attachments if args.attachments else None
        
        # Validate attachment files exist
        if attachments:
            for att_path in attachments:
                path = Path(att_path)
                if not path.exists():
                    logger.error(f"Attachment file not found: {att_path}")
                    print(f"ERROR: Attachment file not found: {att_path}")
                    sys.exit(1)
                if not path.is_file():
                    logger.error(f"Attachment is not a file: {att_path}")
                    print(f"ERROR: Attachment is not a file: {att_path}")
                    sys.exit(1)
            logger.info(f"Found {len(attachments)} attachment(s) to send")
            print(f"Found {len(attachments)} attachment(s): {', '.join(attachments)}")
        
        # Validate that at least body or html is provided
        if not args.body and not args.html:
            logger.error("Either body or html must be provided")
            print("ERROR: Either --body or --html must be provided.")
            sys.exit(1)
        
        # Send email
        logger.info(f"Sending email - Subject: '{args.subject}', To: {args.to}, Attachments: {len(attachments) if attachments else 0}")
        print(f"\nSending email...")
        print(f"  To: {', '.join(args.to)}")
        print(f"  Subject: {args.subject}")
        if args.cc:
            print(f"  CC: {', '.join(args.cc)}")
        if args.bcc:
            print(f"  BCC: {', '.join(args.bcc)}")
        if attachments:
            print(f"  Attachments: {len(attachments)} file(s)")
        
        if args.ymail and len(args.to) == 1:
            # Use ymail convenience method for single recipient
            success = client.send_email_to_ymail(
                ymail_address=args.to[0],
                subject=args.subject,
                body=args.body,
                body_html=args.html,
                from_address=args.from_address,
                cc=args.cc,
                bcc=args.bcc,
                attachments=attachments,
            )
        else:
            # Use regular send_email method
            success = client.send_email(
                to=args.to,
                subject=args.subject,
                body=args.body,
                body_html=args.html,
                from_address=args.from_address,
                cc=args.cc,
                bcc=args.bcc,
                attachments=attachments,
            )
        
        if success:
            logger.info("Email sent successfully via CLI")
            print("\n[SUCCESS] Email sent successfully!")
            sys.exit(0)
        else:
            logger.error("Failed to send email via CLI")
            print("\n[ERROR] Failed to send email. Check logs for details.")
            sys.exit(1)
    
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print(f"\nERROR: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\nERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

