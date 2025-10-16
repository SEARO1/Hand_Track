# Python Downgrade Guide - Install Python 3.10 for MediaPipe

## Why Downgrade?

MediaPipe has compatibility issues with Python 3.11 on Windows. Python 3.10 is the recommended version for this project.

## Step-by-Step Installation Guide

### Step 1: Download Python 3.10

1. Go to: https://www.python.org/downloads/release/python-31011/
2. Scroll down to "Files" section
3. Download: **Windows installer (64-bit)** - `python-3.10.11-amd64.exe`

### Step 2: Install Python 3.10

1. Run the downloaded installer
2. **IMPORTANT:** Check these boxes:
   - ✅ **"Add Python 3.10 to PATH"** (Very important!)
   - ✅ "Install launcher for all users"
3. Click **"Install Now"**
4. Wait for installation to complete
5. Click "Close"

### Step 3: Verify Python 3.10 Installation

Open a **NEW** Command Prompt or PowerShell window and run:

```bash
python --version
```

You should see: `Python 3.10.11`

If you still see Python 3.11, try:
```bash
py -3.10 --version
```

### Step 4: Install Required Packages

Navigate to your project folder:
```bash
cd C:\Users\SEARO\Desktop\Hand_Track
```

Install packages using Python 3.10:
```bash
python -m pip install --upgrade pip
python -m pip install opencv-python mediapipe numpy
```

Or if you have multiple Python versions:
```bash
py -3.10 -m pip install --upgrade pip
py -3.10 -m pip install opencv-python mediapipe numpy
```

### Step 5: Verify Installation

Run the test script:
```bash
python test_installation.py
```

Or with specific Python version:
```bash
py -3.10 test_installation.py
```

You should see:
```
✓ OpenCV installed successfully
✓ MediaPipe installed successfully
✓ NumPy installed successfully
✓ All packages are working correctly!
```

### Step 6: Run the Hand Tracking Program

```bash
python gesture_recognition_tracking.py
```

Or:
```bash
py -3.10 gesture_recognition_tracking.py
```

## Troubleshooting

### Issue 1: "python --version" still shows 3.11

**Solution A:** Use the Python Launcher
```bash
py -3.10 -m pip install opencv-python mediapipe numpy
py -3.10 gesture_recognition_tracking.py
```

**Solution B:** Modify PATH Environment Variable
1. Search "Environment Variables" in Windows
2. Click "Environment Variables"
3. Under "System variables", find "Path"
4. Move Python 3.10 path ABOVE Python 3.11 path
5. Restart Command Prompt

### Issue 2: Multiple Python Versions Conflict

**Solution:** Use Python Launcher with specific version
```bash
# Check available Python versions
py --list

# Use Python 3.10 specifically
py -3.10 script.py
```

### Issue 3: pip not found

**Solution:**
```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### Issue 4: Permission Denied

**Solution:** Run Command Prompt as Administrator
1. Search "cmd" or "PowerShell"
2. Right-click → "Run as administrator"
3. Run installation commands again

## Alternative: Virtual Environment (Recommended)

Create a virtual environment with Python 3.10:

```bash
# Navigate to project folder
cd C:\Users\SEARO\Desktop\Hand_Track

# Create virtual environment with Python 3.10
py -3.10 -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install packages
pip install opencv-python mediapipe numpy

# Run the program
python gesture_recognition_tracking.py
```

When you're done:
```bash
deactivate
```

## Quick Reference Commands

### Using Python 3.10 Directly
```bash
python --version                    # Check version
python -m pip install package       # Install package
python script.py                    # Run script
```

### Using Python Launcher (Multiple Versions)
```bash
py --list                          # List all Python versions
py -3.10 --version                 # Check Python 3.10
py -3.10 -m pip install package    # Install with Python 3.10
py -3.10 script.py                 # Run with Python 3.10
```

### Using Virtual Environment
```bash
py -3.10 -m venv venv              # Create venv
venv\Scripts\activate              # Activate
pip install package                # Install (uses venv Python)
python script.py                   # Run (uses venv Python)
deactivate                         # Deactivate
```

## What Happens to Python 3.11?

- Python 3.11 will remain installed
- You can use both versions side-by-side
- Use `py -3.11` for Python 3.11 projects
- Use `py -3.10` for this MediaPipe project

## Recommended Workflow

1. Install Python 3.10
2. Create a virtual environment for this project
3. Install packages in the virtual environment
4. Always activate the virtual environment before working on this project

This keeps your Python installations clean and organized!

## Need Help?

If you encounter any issues:
1. Make sure you downloaded Python 3.10.11 (not 3.11)
2. Verify "Add to PATH" was checked during installation
3. Restart your terminal/Command Prompt after installation
4. Try using the Python Launcher: `py -3.10`
5. Consider using a virtual environment for isolation

## After Successful Installation

Once Python 3.10 is installed and packages are working:

1. Run: `python test_installation.py`
2. You should see all green checkmarks ✓
3. Run: `python gesture_recognition_tracking.py`
4. Choose option 2 to test with webcam
5. Try making "ROCK", "SCISSORS", "PALM" gestures!

Good luck! 🎉
