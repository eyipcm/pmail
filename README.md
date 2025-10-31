# PMail - Gmail Email Client

A Python mail client for sending emails via Gmail SMTP with support for scheduled email tasks.

> **Note:** This project requires **Python 3.11**. If you need to migrate from an older Python version or update your virtual environment, see [SETUP_PYTHON311.md](SETUP_PYTHON311.md) for detailed instructions.

## Features

- Send emails via Gmail SMTP using `smtplib`, `MIMEText`, and `MIMEMultipart`
- Support for plain text and HTML emails
- Scheduled email tasks (daily, weekly, custom intervals)
- Structured for future web client integration
- Python 3.11 compatible

## Setup

### Prerequisites

- Python 3.10 or higher (Python 3.11 recommended)
- pip (Python package installer)

### Step 1: Create Virtual Environment

**⚠️ Important:** This project requires **Python 3.11** (or Python 3.10+). The virtual environment will use whatever Python version you specify.

**Choose one method:**
- **Method A:** Using `venv` (Python's built-in virtual environment)
- **Method B:** Using `conda` (Conda environment manager)

#### Method A: Using venv (Standard Python Virtual Environment)

#### Check Your Python Version

First, check which Python version is available:

**Windows:**
```cmd
python --version
```

**Linux/Mac:**
```bash
python3 --version
```

If you see Python 3.8 or earlier, you need to install Python 3.11.

#### Install Python 3.11 (If Not Available)

**Windows:**
1. Download Python 3.11 from [python.org/downloads](https://www.python.org/downloads/)
2. Run the installer
3. **Important:** Check "Add Python to PATH" during installation
4. Verify installation:
   ```cmd
   python --version
   ```
   Should show: `Python 3.11.x`

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv
```

**Mac (using Homebrew):**
```bash
brew install python@3.11
```

#### Create Virtual Environment with Python 3.11

Once Python 3.11 is available, create the virtual environment:

**Windows (if Python 3.11 is the default):**
```cmd
cd D:\gitrepo\pmail
python -m venv pmail_py3_11
```

**Windows (if you have multiple Python versions):**
```cmd
cd D:\gitrepo\pmail
# Using Python Launcher (recommended)
py -3.11 -m venv pmail_py3_11

# Or if Python 3.11 is in your PATH with a different name
python3.11 -m venv pmail_py3_11

# Or specify full path
C:\Python311\python.exe -m venv pmail_py3_11
```

**Windows (PowerShell):**
```powershell
cd D:\gitrepo\pmail
# Using Python Launcher
py -3.11 -m venv pmail_py3_11

# Or if Python 3.11 is default
python -m venv pmail_py3_11
```

**Linux/Mac:**
```bash
cd /path/to/pmail
# If python3.11 command is available
python3.11 -m venv pmail_py3_11

# Or use python3 if it's version 3.11
python3 -m venv pmail_py3_11
```

#### Verify Virtual Environment Python Version

After creating the virtual environment, verify it's using Python 3.11:

**Method 1: Check Python executable version**
**Windows:**
```cmd
pmail_py3_11\Scripts\python.exe --version
```

**Linux/Mac:**
```bash
pmail_py3_11/bin/python --version
```

**Expected output:** `Python 3.11.x`

**Method 2: Check pyvenv.cfg file**

The `pyvenv.cfg` file in the virtual environment directory shows which Python version was used:

**Windows:**
```cmd
type pmail_py3_11\pyvenv.cfg
```

**Linux/Mac:**
```bash
cat pmail_py3_11/pyvenv.cfg
```

**Expected content:**
```
home = C:\Python311
include-system-site-packages = false
version = 3.11.x
```

**⚠️ If it shows a different version (e.g., `version = 3.8.19`):**

1. **Delete the existing virtual environment:**
   - **Windows:** `rmdir /s pmail_py3_11`
   - **Linux/Mac:** `rm -rf pmail_py3_11`

2. **Recreate it with Python 3.11:**
   - Use one of the methods in "Create Virtual Environment with Python 3.11" section above
   - Make sure to specify Python 3.11 explicitly

3. **Verify again** using the commands above

**Note:** You cannot manually edit `pyvenv.cfg` to change the Python version. You must recreate the virtual environment with the correct Python version.

### Step 2: Activate Virtual Environment

#### If Using venv (Method A):

**Windows (CMD):**
```cmd
pmail_py3_11\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
pmail_py3_11\Scripts\Activate.ps1
```

If you get an execution policy error in PowerShell, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Linux/Mac:**
```bash
source pmail_py3_11/bin/activate
```

**Verify activation:** Once activated, you should see `(pmail_py3_11)` at the beginning of your command prompt:
```
(pmail_py3_11) D:\gitrepo\pmail>
```

#### If Using Conda (Method B):

**Windows/Linux/Mac:**
```bash
conda activate pmail_py3_11
```

**Verify activation:** Once activated, you should see `(pmail_py3_11)` at the beginning of your command prompt:
```
(pmail_py3_11) D:\gitrepo\pmail>
```

### Step 3: Install Dependencies

With the virtual environment activated, install the required packages:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Verify installation:**
```bash
pip list
```

You should see `schedule` package installed.

### Step 4: Gmail Configuration

**IMPORTANT:** You MUST configure Gmail credentials before using the email client. These credentials are read from **environment variables** set in your terminal/command prompt.

#### Part A: Get Gmail App Password

**⚠️ Important:** You cannot use your regular Gmail password. You need to create a special "App Password" for this application.

**Step 1: Enable 2-Factor Authentication**
1. Go to [Google Account Security Settings](https://myaccount.google.com/security)
2. Sign in with your Gmail account
3. Under "How you sign in to Google", find "2-Step Verification"
4. Click "2-Step Verification" and enable it if not already enabled
   - Follow the prompts to set up 2-Step Verification (usually via phone)

**Step 2: Generate App Password**
1. After enabling 2-Step Verification, go back to [Google Account Security Settings](https://myaccount.google.com/security)
2. Under "How you sign in to Google", click on "App passwords"
   - If you don't see "App passwords", make sure 2-Step Verification is enabled first
3. You may be asked to sign in again for security
4. Under "Select app", choose **"Mail"**
5. Under "Select device", choose **"Other (Custom name)"**
6. Type: **"PMail"** (or any name you prefer)
7. Click **"Generate"**
8. **COPY the 16-character password** that appears (format: `xxxx xxxx xxxx xxxx`)
   - Remove spaces: `xxxxxxxxxxxxxxxx` (16 characters total)
   - Save this password - you won't be able to see it again!

**Example App Password format:**
```
abcd efgh ijkl mnop
```
Use it as: `abcdefghijklmnop` (without spaces)

#### Part B: Configure Environment Variables

**WHERE to set credentials:** Environment variables must be set **in the same terminal/command prompt window** where you will run the Python scripts.

**⚠️ Important Notes:**
- Environment variables set with `set` (CMD) or `$env:` (PowerShell) are **only valid for that specific terminal session**
- If you close the terminal, you'll need to set them again
- Use "Persistent Configuration" methods below if you want them to persist across sessions

**Method 1: Temporary (Current Session Only) - Recommended for Testing**

**Windows Command Prompt (CMD):**
```cmd
REM Make sure you're in the project directory
cd D:\gitrepo\pmail

REM Activate virtual environment first (if not already activated)
pmail_py3_11\Scripts\activate.bat

REM Set Gmail credentials
set GMAIL_ADDRESS=your-email@gmail.com
set GMAIL_PASSWORD=abcdefghijklmnop

REM Verify they are set
echo %GMAIL_ADDRESS%
echo %GMAIL_PASSWORD%
```

**Windows PowerShell:**
```powershell
# Make sure you're in the project directory
cd D:\gitrepo\pmail

# Activate virtual environment first (if not already activated)
pmail_py3_11\Scripts\Activate.ps1

# Set Gmail credentials
$env:GMAIL_ADDRESS="your-email@gmail.com"
$env:GMAIL_PASSWORD="abcdefghijklmnop"

# Verify they are set
echo $env:GMAIL_ADDRESS
echo $env:GMAIL_PASSWORD
```

**Linux/Mac:**
```bash
# Make sure you're in the project directory
cd /path/to/pmail

# Activate virtual environment first
source pmail_py3_11/bin/activate

# Set Gmail credentials
export GMAIL_ADDRESS=your-email@gmail.com
export GMAIL_PASSWORD=abcdefghijklmnop

# Verify they are set
echo $GMAIL_ADDRESS
echo $GMAIL_PASSWORD
```

**Method 2: Persistent Configuration (Survives Terminal Restarts)**

**Windows Command Prompt (CMD) - Persistent:**
```cmd
REM Set permanently for your user account
setx GMAIL_ADDRESS "your-email@gmail.com"
setx GMAIL_PASSWORD "abcdefghijklmnop"

REM IMPORTANT: Close and reopen your terminal for changes to take effect!
REM After reopening, activate venv and verify:
pmail_py3_11\Scripts\activate.bat
echo %GMAIL_ADDRESS%
```

**Windows PowerShell - Persistent:**
```powershell
# Set permanently for your user account
[System.Environment]::SetEnvironmentVariable("GMAIL_ADDRESS", "your-email@gmail.com", "User")
[System.Environment]::SetEnvironmentVariable("GMAIL_PASSWORD", "abcdefghijklmnop", "User")

# IMPORTANT: Close and reopen PowerShell for changes to take effect!
# After reopening, activate venv and verify:
pmail_py3_11\Scripts\Activate.ps1
echo $env:GMAIL_ADDRESS
```

**Windows GUI Method - Alternative:**
1. Press `Win + R`, type `sysdm.cpl`, press Enter
2. Go to "Advanced" tab → Click "Environment Variables"
3. Under "User variables", click "New"
4. Variable name: `GMAIL_ADDRESS`
5. Variable value: `your-email@gmail.com`
6. Click "OK"
7. Repeat for `GMAIL_PASSWORD` with your app password
8. Click "OK" on all dialogs
9. **Close and reopen** your terminal

**Linux/Mac - Persistent:**
Add to your shell configuration file:

```bash
# For bash users
nano ~/.bashrc

# For zsh users
nano ~/.zshrc

# Add these lines at the end:
export GMAIL_ADDRESS=your-email@gmail.com
export GMAIL_PASSWORD=abcdefghijklmnop

# Save and exit (Ctrl+X, then Y, then Enter for nano)
# Reload your shell configuration:
source ~/.bashrc  # or source ~/.zshrc
```

#### Part C: Verify Configuration

After setting the environment variables, verify they are configured correctly:

**Windows (CMD):**
```cmd
REM Make sure virtual environment is activated
pmail_py3_11\Scripts\activate.bat

REM Test configuration
python src/send_email_example.py
```

**Windows (PowerShell):**
```powershell
# Make sure virtual environment is activated
pmail_py3_11\Scripts\Activate.ps1

# Test configuration
python src/send_email_example.py
```

**Linux/Mac:**
```bash
# Make sure virtual environment is activated
source pmail_py3_11/bin/activate

# Test configuration
python src/send_email_example.py
```

**Expected Output (if configured correctly):**
```
PMail Email Client Examples
==================================================

Note: Examples are commented out. Uncomment the examples you want to test.
Make sure to replace 'recipient@example.com' with actual email addresses.
```

**If you see "Configuration Required" warning:**
- The environment variables are not set or not visible to Python
- Make sure you set them in the **same terminal window** where you run the script
- If using persistent method, make sure you **closed and reopened** the terminal

#### Troubleshooting Configuration

**Problem: "Gmail credentials not configured" error**
- **Solution:** Make sure you set `GMAIL_ADDRESS` and `GMAIL_PASSWORD` in the same terminal window
- Verify by running: `echo %GMAIL_ADDRESS%` (CMD) or `echo $env:GMAIL_ADDRESS` (PowerShell)

**Problem: Environment variables not persisting after closing terminal**
- **Solution:** Use the "Persistent Configuration" methods above, or set them each time you open a new terminal

**Problem: "Invalid App Password" or authentication errors**
- **Solution:** 
  - Make sure you're using the **App Password** (16 characters), not your regular Gmail password
  - App Password should have no spaces
  - Generate a new App Password if needed
  - Make sure 2-Step Verification is enabled

**Problem: Variables set but Python can't see them**
- **Solution:** 
  - Close and reopen the terminal (for persistent methods)
  - For temporary methods, set variables **after** activating virtual environment in the same session
  - On Windows, try restarting your IDE/editor if it has its own terminal

### Step 5: Optional Configuration

You can also set these optional environment variables (same methods as above):

**Windows (CMD):**
```cmd
set SMTP_SERVER=smtp.gmail.com
set SMTP_PORT=587
set DEFAULT_SENDER=your-email@gmail.com
set USE_TLS=true
```

**Windows (PowerShell):**
```powershell
$env:SMTP_SERVER="smtp.gmail.com"
$env:SMTP_PORT="587"
$env:DEFAULT_SENDER="your-email@gmail.com"
$env:USE_TLS="true"
```

**Linux/Mac:**
```bash
export SMTP_SERVER=smtp.gmail.com
export SMTP_PORT=587
export DEFAULT_SENDER=your-email@gmail.com
export USE_TLS=true
```

**Default values:**
- `SMTP_SERVER`: `smtp.gmail.com`
- `SMTP_PORT`: `587`
- `USE_TLS`: `true`
- `DEFAULT_SENDER`: Same as `GMAIL_ADDRESS`

### Step 6: Verify Setup

Test your setup by running the example script:

```bash
python src/send_email_example.py
```

If everything is configured correctly, the script will check your configuration. You can uncomment the example functions in the script to test sending emails.

### Deactivating Virtual Environment

When you're done working with the project, deactivate the virtual environment:

#### If Using venv:
**Windows/Linux/Mac:**
```cmd
deactivate
```

#### If Using Conda:
**Windows/Linux/Mac:**
```bash
conda deactivate
```

The `(pmail_py3_11)` prefix will disappear from your command prompt.

## Usage

### Basic Email Sending

```python
from src.mail_client import MailClient

# Initialize client
client = MailClient()

# Send a simple email
client.send_email(
    to="recipient@example.com",
    subject="Hello",
    body="This is a test email."
)

# Send HTML email (with optional plain text)
client.send_email(
    to="recipient@example.com",
    subject="Hello",
    body="Plain text version",  # Optional if body_html is provided
    body_html="<h1>HTML version</h1><p>This is HTML.</p>"
)

# Send HTML-only email (plain text auto-generated from HTML)
client.send_email(
    to="recipient@example.com",
    subject="Hello",
    body_html="<h1>HTML only</h1><p>Plain text will be auto-generated.</p>"
)

# Send email with multiple attachments
client.send_email(
    to="recipient@example.com",
    subject="Email with Attachments",
    body="Please find attached files.",
    attachments=["/path/to/file1.pdf", "/path/to/file2.jpg"]  # List of file paths
)

# Send email with HTML and attachments
client.send_email(
    to="recipient@example.com",
    subject="Email with HTML and Attachments",
    body="Plain text version",
    body_html="<h1>HTML version</h1><p>With attachments.</p>",
    attachments=["/path/to/file1.pdf", "/path/to/file2.jpg"]
)

# Send to Yahoo Mail
client.send_email_to_ymail(
    ymail_address="recipient@yahoo.com",
    subject="Hello",
    body="Test email to Yahoo Mail",
    attachments=["/path/to/file.pdf"]  # Optional attachments
)
```

### Scheduled Emails

```python
from src.scheduler import EmailScheduler

# Initialize scheduler
scheduler = EmailScheduler()

# Schedule daily email at 9:30 AM
scheduler.schedule_daily(
    time_str="09:30",
    to="recipient@yahoo.com",
    subject="Daily Report",
    body="Your daily report is ready."
)

# Schedule weekly email (every Monday at 10:00 AM)
scheduler.schedule_weekly(
    day="monday",
    time_str="10:00",
    to="recipient@yahoo.com",
    subject="Weekly Summary",
    body="Your weekly summary."
)

# Schedule interval email (every 30 minutes)
scheduler.schedule_interval(
    interval_minutes=30,
    to="recipient@yahoo.com",
    subject="Regular Update",
    body="Regular update message."
)

# Run scheduler continuously
scheduler.run_continuously(interval_seconds=60)
```

### Example Script

See `src/send_email_example.py` for a complete example.

Run the example:
```bash
python src/send_email_example.py
```

### Command-Line Interface

Use the CLI tool to send emails directly from the command line:

**Basic usage:**
```cmd
python src/send_email_cli.py -t recipient@example.com -s "Subject" -b "Body text"
```

**With single attachment:**
```cmd
python src/send_email_cli.py -t recipient@example.com -s "Subject" -b "Body text" -a file.pdf
```

**With multiple attachments:**
```cmd
python src/send_email_cli.py -t recipient@example.com -s "Subject" -b "Body text" -a file1.pdf file2.jpg file3.txt
```

**HTML-only email (no plain text needed):**
```cmd
python src/send_email_cli.py -t recipient@example.com -s "Subject" --html "<h1>HTML Only</h1><p>No plain text needed!</p>"
```

**With HTML body and attachments:**
```cmd
python src/send_email_cli.py -t recipient@example.com -s "Subject" -b "Plain text" --html "<h1>HTML</h1>" -a file.pdf
```

**HTML-only with attachments:**
```cmd
python src/send_email_cli.py -t recipient@example.com -s "Subject" --html "<h1>HTML</h1>" -a file.pdf
```

**With CC/BCC:**
```cmd
python src/send_email_cli.py -t recipient@example.com -c cc@example.com --bcc bcc@example.com -s "Subject" -b "Body" -a file.pdf
```

**Multiple recipients:**
```cmd
python src/send_email_cli.py -t recipient1@example.com recipient2@example.com -s "Subject" -b "Body" -a file.pdf
```

**Full options:**
```cmd
python src/send_email_cli.py --help
```

## Project Structure

```
pmail/
├── config/
│   ├── __init__.py
│   ├── email_config.py        # Configuration management
│   └── logger_config.py       # Logging configuration
├── src/
│   ├── __init__.py
│   ├── mail_client.py          # Main email client
│   ├── scheduler.py            # Email scheduler
│   └── send_email_example.py   # Example usage script
├── log/                        # Log files directory
│   └── email_YYYYMMDD.log     # Daily log files (auto-created)
├── pmail_py3_11/              # Virtual environment (created during setup)
├── requirements.txt
└── README.md
```

**Note:** The `pmail_py3_11/` directory is the virtual environment and should be added to `.gitignore` if using version control.

## Future Web Client

The project is structured to support a future web client. The core functionality is separated into:
- `config/email_config.py`: Configuration management
- `src/mail_client.py`: Email sending logic
- `src/scheduler.py`: Scheduled task management

These modules can be easily integrated into a web framework (Flask, FastAPI, etc.) in the future.

## Notes

- Always use Gmail App Passwords, not your regular Gmail password
- The scheduler runs in a loop and checks for pending jobs at regular intervals
- For production use, consider using a proper task queue (Celery, RQ, etc.) instead of the simple scheduler

## License

MIT

