# Quick Fix Guide - Package Installation Issues

## Problem: MediaPipe Import Error

If you see this error:
```
ImportError: cannot import name 'model_ckpt_util' from 'mediapipe.python._framework_bindings'
```

## Solution: Install Compatible Version

Follow these steps exactly:

### Step 1: Uninstall Current MediaPipe
```bash
pip uninstall mediapipe -y
```

### Step 2: Install Compatible Version
```bash
pip install mediapipe==0.10.9
```

### Step 3: Install Other Packages
```bash
pip install opencv-python numpy
```

### Step 4: Verify Installation
```bash
python test_installation.py
```

## Complete Fresh Installation

If you want to start fresh:

```bash
# Uninstall all packages
pip uninstall opencv-python mediapipe numpy -y

# Install from requirements.txt
pip install -r requirements.txt
```

## Alternative: Install Packages One by One

```bash
pip install opencv-python
pip install mediapipe==0.10.9
pip install numpy
```

## Verify Everything Works

Run this command to test:
```bash
python -c "import cv2; import mediapipe as mp; import numpy as np; print('Success! All packages installed')"
```

You should see: `Success! All packages installed`

## Common Issues and Solutions

### Issue 1: "pip is not recognized"
**Solution:**
```bash
python -m pip install mediapipe==0.10.9
```

### Issue 2: Permission Denied
**Windows:** Run Command Prompt as Administrator
**Mac/Linux:**
```bash
pip install --user mediapipe==0.10.9
```

### Issue 3: Multiple Python Versions
Use specific Python version:
```bash
python3 -m pip install mediapipe==0.10.9
```

### Issue 4: Slow Download
Use a mirror:
```bash
pip install mediapipe==0.10.9 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## After Installation

Once packages are installed, run:
```bash
python gesture_recognition_tracking.py
```

Select option 2 for webcam test to verify everything works!

## Still Having Issues?

1. Check Python version: `python --version` (need 3.8+)
2. Update pip: `python -m pip install --upgrade pip`
3. Create virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Mac/Linux
   pip install -r requirements.txt
   ```

## Working Configuration

These versions are tested and working:
- Python: 3.11.9
- opencv-python: 4.8.0 or higher
- mediapipe: 0.10.9 (IMPORTANT: Must be this version)
- numpy: 1.24.0 or higher
