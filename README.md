# Hand Gesture Recognition and Tracking System

This project implements a hand gesture recognition and tracking system using MediaPipe Hands, based on the EE4213 Human Computer Interaction tutorial.

## Features

- **Real-time hand detection and tracking** using MediaPipe Hands
- **21 key point detection** for accurate hand pose estimation
- **Gesture recognition** for three gestures:
  - 🪨 **ROCK** - Closed fist
  - ✌️ **SCISSORS** - Index and middle fingers extended
  - ✋ **PALM** - All fingers extended
- **Gesture stabilization** using buffer mechanism to reduce jitter
- **Two modes**:
  - Video file processing with optional output saving
  - Real-time webcam processing

## System Architecture

The system follows the complete hand gesture recognition pipeline:

1. **Data Acquisition** - Capture video from file or webcam
2. **Hand Detection** - Locate hands in the frame using MediaPipe
3. **Key Point Detection** - Extract 21 hand landmarks
4. **Gesture Recognition** - Classify gestures based on finger positions
5. **Tracking** - Stabilize results using temporal buffering

## Requirements

- **Python 3.10** (IMPORTANT: MediaPipe has compatibility issues with Python 3.11 on Windows)
- Webcam (for real-time mode)
- Windows/Linux/macOS

> ⚠️ **Important**: If you have Python 3.11, please see `PYTHON_DOWNGRADE_GUIDE.md` for instructions on installing Python 3.10.

## Installation

### Quick Start (Python 3.10 users)

1. **Clone or download this project**

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

### If You Have Python 3.11

MediaPipe doesn't work with Python 3.11 on Windows. You have two options:

**Option 1: Install Python 3.10 (Recommended)**
- See detailed guide: `PYTHON_DOWNGRADE_GUIDE.md`
- Download Python 3.10.11 from python.org
- Install packages with Python 3.10

**Option 2: Use Python Launcher**
```bash
py -3.10 -m pip install -r requirements.txt
py -3.10 gesture_recognition_tracking.py
```

### Manual Installation

```bash
pip install opencv-python
pip install mediapipe
pip install numpy
```

## Usage

### Method 1: Interactive Mode

Run the script and follow the prompts:

```bash
python gesture_recognition_tracking.py
```

You'll see a menu:
```
Select mode:
1. Process video file
2. Real-time webcam
3. Exit
```

### Method 2: Direct Function Calls

You can also import and use the functions directly in your own code:

```python
from gesture_recognition_tracking import process_video, process_webcam

# Process a video file
process_video("input.mp4", "output.mp4")

# Or use webcam
process_webcam()
```

## How It Works

### Gesture Recognition Algorithm

The system recognizes gestures by:

1. **Extracting key points**: Wrist and 5 fingertips (thumb, index, middle, ring, pinky)
2. **Calculating distances**: Distance from each fingertip to the wrist
3. **Determining finger state**: Compare distances against a threshold to determine if fingers are extended
4. **Classifying gesture**:
   - **ROCK**: 0-1 fingers extended
   - **SCISSORS**: 2 fingers extended (index + middle)
   - **PALM**: 4-5 fingers extended
   - **UNKNOWN**: Other configurations

### Stabilization Mechanism

To reduce jitter and flickering:
- Uses a buffer of the last 5 gesture predictions
- Displays the most common gesture in the buffer
- Provides smooth, stable gesture recognition

## Controls

- **Press 'q'** to quit the application
- The webcam feed is **mirrored** for natural interaction

## Project Structure

```
Hand_Track/
├── gesture_recognition_tracking.py  # Main script
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
└── (your video files)              # Place your test videos here
```

## Recording Your Own Test Video

For the class assignment, you need to record your own gesture video:

1. **Use your phone or webcam** to record a video showing:
   - ROCK gesture (closed fist)
   - SCISSORS gesture (index + middle fingers)
   - PALM gesture (open hand)

2. **Save the video** as MP4 format

3. **Place it in the project folder**

4. **Run the script** and select option 1 to process your video

## Troubleshooting

### Common Issues

1. **"No module named 'cv2'"**
   - Solution: `pip install opencv-python`

2. **"No module named 'mediapipe'"**
   - Solution: `pip install mediapipe`

3. **Version conflicts**
   - Solution: Create a virtual environment:
     ```bash
     python -m venv venv
     # Windows:
     venv\Scripts\activate
     # Linux/Mac:
     source venv/bin/activate
     pip install -r requirements.txt
     ```

4. **Webcam not working**
   - Check if another application is using the webcam
   - Try changing camera index in code: `cv2.VideoCapture(1)` instead of `0`

5. **Video file not opening**
   - Ensure the file path is correct
   - Use forward slashes or raw strings: `r"C:\path\to\video.mp4"`
   - Verify the video format is supported (MP4, AVI, MOV)

## Technical Details

### MediaPipe Hand Landmarks

The system detects 21 landmarks per hand:
- 0: Wrist
- 1-4: Thumb (CMC, MCP, IP, TIP)
- 5-8: Index finger (MCP, PIP, DIP, TIP)
- 9-12: Middle finger (MCP, PIP, DIP, TIP)
- 13-16: Ring finger (MCP, PIP, DIP, TIP)
- 17-20: Pinky (MCP, PIP, DIP, TIP)

### Parameters

You can adjust these in the code:

```python
# MediaPipe Hands parameters
hands = mp_hands.Hands(
    static_image_mode=False,      # False for video
    max_num_hands=2,               # Detect up to 2 hands
    min_detection_confidence=0.5,  # Detection threshold
    min_tracking_confidence=0.5    # Tracking threshold
)

# Gesture stabilization
buffer_size = 5  # Number of frames to average
```

## Assignment Submission

For **Optional Class Assignment #5**:

1. ✅ Configure the environment and run successfully
2. ✅ Record your own gesture MP4 file
3. ✅ Process the video and get recognition results
4. 📸 Take a screenshot showing successful hand gesture recognition
5. 📤 Upload the screenshot to Canvas

**Tip**: Make sure the screenshot clearly shows:
- The video window with hand landmarks drawn
- The recognized gesture label
- Your hand performing one of the three gestures

## References

- MediaPipe Hands: https://google.github.io/mediapipe/solutions/hands.html
- Tutorial PDF: "EE4213: Human Computer Interaction - Hand gestures recognition and tracking"
- Zhang, F., "MediaPipe Hands: On-device Real-time Hand Tracking", arXiv:2006.10214, 2020

## License

This project is for educational purposes as part of the EE4213 course.

## Author

Based on the tutorial by Tiantian XIE (ttxie3-c@my.cityu.edu.hk)
