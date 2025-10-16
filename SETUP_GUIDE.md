# Quick Setup Guide

## Step-by-Step Installation

### 1. Check Python Installation

Open Command Prompt (Windows) or Terminal (Mac/Linux) and check Python version:

```bash
python --version
```

You should see Python 3.8 or higher. If not, download from [python.org](https://www.python.org/downloads/).

### 2. Navigate to Project Directory

```bash
cd c:\Users\SEARO\Desktop\Hand_Track
```

### 3. Install Dependencies

**Option A: Using requirements.txt (Recommended)**
```bash
pip install -r requirements.txt
```

**Option B: Manual Installation**
```bash
pip install opencv-python==4.8.1.78
pip install mediapipe==0.10.8
pip install numpy==1.24.3
```

### 4. Verify Installation

Create a test file `test_installation.py`:

```python
import cv2
import mediapipe as mp
import numpy as np

print("✓ OpenCV version:", cv2.__version__)
print("✓ MediaPipe version:", mp.__version__)
print("✓ NumPy version:", np.__version__)
print("\nAll packages installed successfully!")
```

Run it:
```bash
python test_installation.py
```

## Quick Start

### Test with Webcam (Easiest)

```bash
python gesture_recognition_tracking.py
```

Then select option `2` for real-time webcam mode.

### Test with Video File

1. Record a short video (10-30 seconds) showing ROCK, SCISSORS, and PALM gestures
2. Save it as `test.mp4` in the project folder
3. Run:
   ```bash
   python gesture_recognition_tracking.py
   ```
4. Select option `1` and enter `test.mp4` when prompted

## Common Setup Issues

### Issue 1: "pip is not recognized"

**Solution**: Add Python to PATH or use:
```bash
python -m pip install -r requirements.txt
```

### Issue 2: Permission Denied

**Windows**: Run Command Prompt as Administrator

**Mac/Linux**: Use sudo:
```bash
sudo pip install -r requirements.txt
```

### Issue 3: Multiple Python Versions

Use specific Python version:
```bash
python3 -m pip install -r requirements.txt
python3 gesture_recognition_tracking.py
```

### Issue 4: Package Conflicts

Create a virtual environment:

**Windows**:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Mac/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Testing Your Setup

### Test 1: Import Test
```python
python -c "import cv2, mediapipe, numpy; print('Success!')"
```

### Test 2: Webcam Test
```python
python -c "import cv2; cap = cv2.VideoCapture(0); print('Webcam OK' if cap.isOpened() else 'Webcam Error'); cap.release()"
```

### Test 3: MediaPipe Test
```python
python -c "import mediapipe as mp; hands = mp.solutions.hands.Hands(); print('MediaPipe OK')"
```

## For the Assignment

1. ✅ Complete installation (Steps 1-3)
2. ✅ Verify with test script (Step 4)
3. 📹 Record your gesture video
4. ▶️ Run the program and process your video
5. 📸 Take screenshot of successful recognition
6. 📤 Submit to Canvas

## Need Help?

- Check the main README.md for detailed documentation
- Review the Troubleshooting section
- Ensure all dependencies are correctly installed
- Verify your Python version is 3.8+

## Quick Reference Commands

```bash
# Install packages
pip install -r requirements.txt

# Run program
python gesture_recognition_tracking.py

# Test installation
python test_installation.py

# Check Python version
python --version

# Check pip version
pip --version
```

Good luck with your assignment! 🎓
