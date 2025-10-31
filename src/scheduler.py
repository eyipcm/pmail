"""
Scheduler for sending regular emails.

Copyright (C) 2025 Ernest YIP 
SPDX-License-Identifier: MIT 
See the LICENSE file in the project root for full license text.
"""

import schedule
import time
import sys
from pathlib import Path
from typing import Callable, Optional, Union, List

# Add project root to Python path
_project_root = Path(__file__).parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

try:
    from .mail_client import MailClient
except ImportError:
    # If relative import fails (e.g., running directly), use absolute import
    from src.mail_client import MailClient

from config import EmailConfig
from config.logger_config import get_logger

# Initialize logger
logger = get_logger("pmail.scheduler")


class EmailScheduler:
    """Scheduler for sending scheduled emails."""
    
    def __init__(self, mail_client: Optional[MailClient] = None):
        """Initialize the email scheduler.
        
        Args:
            mail_client: MailClient instance. If None, creates a new one.
        """
        logger.info("Initializing EmailScheduler")
        self.mail_client = mail_client or MailClient()
        logger.info("EmailScheduler initialized successfully")
    
    def schedule_daily(
        self,
        time_str: str,
        to: Union[str, List[str]],
        subject: str,
        body: Optional[str] = None,
        body_html: Optional[str] = None,
    ):
        """Schedule an email to be sent daily at a specific time.
        
        Args:
            time_str: Time in HH:MM format (e.g., "09:30")
            to: Recipient email address(es)
            subject: Email subject
            body: Plain text email body
            body_html: Optional HTML email body
        """
        def send_email():
            logger.info(f"Executing scheduled daily email - Time: {time_str}, Subject: '{subject}'")
            self.mail_client.send_email(to=to, subject=subject, body=body, body_html=body_html, attachments=None)
        
        schedule.every().day.at(time_str).do(send_email)
        logger.info(f"Scheduled daily email - Time: {time_str}, Subject: '{subject}', To: {to}")
    
    def schedule_weekly(
        self,
        day: str,
        time_str: str,
        to: Union[str, List[str]],
        subject: str,
        body: Optional[str] = None,
        body_html: Optional[str] = None,
    ):
        """Schedule an email to be sent weekly on a specific day and time.
        
        Args:
            day: Day of the week (e.g., "monday", "tuesday")
            time_str: Time in HH:MM format (e.g., "09:30")
            to: Recipient email address(es)
            subject: Email subject
            body: Plain text email body
            body_html: Optional HTML email body
        """
        def send_email():
            logger.info(f"Executing scheduled weekly email - Day: {day}, Time: {time_str}, Subject: '{subject}'")
            self.mail_client.send_email(to=to, subject=subject, body=body, body_html=body_html, attachments=None)
        
        getattr(schedule.every(), day.lower()).at(time_str).do(send_email)
        logger.info(f"Scheduled weekly email - Day: {day}, Time: {time_str}, Subject: '{subject}', To: {to}")
    
    def schedule_interval(
        self,
        interval_minutes: int,
        to: Union[str, List[str]],
        subject: str,
        body: Optional[str] = None,
        body_html: Optional[str] = None,
    ):
        """Schedule an email to be sent at regular intervals.
        
        Args:
            interval_minutes: Interval in minutes
            to: Recipient email address(es)
            subject: Email subject
            body: Plain text email body
            body_html: Optional HTML email body
        """
        def send_email():
            logger.info(f"Executing scheduled interval email - Interval: {interval_minutes} minutes, Subject: '{subject}'")
            self.mail_client.send_email(to=to, subject=subject, body=body, body_html=body_html, attachments=None)
        
        schedule.every(interval_minutes).minutes.do(send_email)
        logger.info(f"Scheduled interval email - Interval: {interval_minutes} minutes, Subject: '{subject}', To: {to}")
    
    def schedule_custom(
        self,
        job_func: Callable,
        *args,
        **kwargs
    ):
        """Schedule a custom job function.
        
        Args:
            job_func: Callable function to execute
            *args: Arguments to pass to job_func
            **kwargs: Keyword arguments to pass to job_func
        """
        schedule.do(job_func, *args, **kwargs)
    
    def run_pending(self):
        """Run all pending scheduled tasks."""
        jobs = schedule.jobs
        if jobs:
            logger.debug(f"Checking for pending jobs. Total jobs: {len(jobs)}")
            schedule.run_pending()
        else:
            logger.debug("No scheduled jobs to run")
    
    def run_continuously(self, interval_seconds: int = 60):
        """Run the scheduler continuously, checking for pending jobs.
        
        Args:
            interval_seconds: Interval in seconds to check for pending jobs
        """
        logger.info(f"Scheduler started. Checking for jobs every {interval_seconds} seconds. Total jobs: {len(schedule.jobs)}")
        print(f"Scheduler started. Checking for jobs every {interval_seconds} seconds.")
        print("Press Ctrl+C to stop.")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user (Ctrl+C)")
            print("\nScheduler stopped.")
    
    def clear_all_jobs(self):
        """Clear all scheduled jobs."""
        job_count = len(schedule.jobs)
        schedule.clear()
        logger.info(f"Cleared all scheduled jobs ({job_count} jobs removed)")
        print("All scheduled jobs cleared.")
    
    def get_jobs(self):
        """Get list of all scheduled jobs.
        
        Returns:
            list: List of scheduled jobs
        """
        return schedule.jobs

