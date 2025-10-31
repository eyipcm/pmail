# Setting Up Python 3.11 Virtual Environment

## Current Status
- **Old venv:** `pmail_py3_10` (Python 3.8.19) - needs to be deleted
- **New venv:** `pmail_py3_11` (Python 3.11) - needs to be created
- **Python 3.11:** Not currently installed on your system

## Step 1: Install Python 3.11

### Windows:
1. Download Python 3.11 from: https://www.python.org/downloads/release/python-3118/
   - Or latest 3.11.x version from: https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT:** Check "Add Python 3.11 to PATH" during installation
4. Choose "Install for all users" or "Install just for me" (your choice)
5. Wait for installation to complete

### Verify Installation:
```cmd
python --version
```
Should show: `Python 3.11.x`

If it still shows 3.8.19, Python 3.11 may not be in PATH. Try:
```cmd
python3.11 --version
```

Or check if Python Launcher works:
```cmd
py -3.11 --version
```

## Step 2: Delete Old Virtual Environment

**Important:** Before deleting, make sure:
- No terminal/IDE is using the virtual environment
- The virtual environment is deactivated (you shouldn't see `(pmail_py3_10)` in your prompt)

### Delete Command:
**Windows CMD:**
```cmd
cd D:\gitrepo\pmail
rmdir /s /q pmail_py3_10
```

**Windows PowerShell:**
```powershell
cd D:\gitrepo\pmail
Remove-Item -Recurse -Force pmail_py3_10
```

**If you get "Access Denied" or "File in use" errors:**
1. Close all terminals/IDEs that might be using the venv
2. Deactivate any active virtual environment
3. Try the delete command again
4. If still fails, restart your computer and try again

## Step 3: Create New Virtual Environment with Python 3.11

Once Python 3.11 is installed and the old venv is deleted:

**Windows (if Python 3.11 is default):**
```cmd
cd D:\gitrepo\pmail
python -m venv pmail_py3_11
```

**Windows (if you have multiple Python versions):**
```cmd
cd D:\gitrepo\pmail
# Using Python Launcher (recommended)
py -3.11 -m venv pmail_py3_11

# Or if python3.11 command exists
python3.11 -m venv pmail_py3_11
```

**Windows PowerShell:**
```powershell
cd D:\gitrepo\pmail
py -3.11 -m venv pmail_py3_11
```

## Step 4: Verify Python Version

**Windows:**
```cmd
pmail_py3_11\Scripts\python.exe --version
```

**Expected output:** `Python 3.11.x`

Check pyvenv.cfg:
```cmd
type pmail_py3_11\pyvenv.cfg
```

Should show:
```
version = 3.11.x
```

## Step 5: Activate and Install Dependencies

**Windows CMD:**
```cmd
pmail_py3_11\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
```

**Windows PowerShell:**
```powershell
pmail_py3_11\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 6: Test

```cmd
python src/send_email_example.py
```

Should show configuration check (if credentials not set) or run examples (if configured).

