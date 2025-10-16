# Usage Examples and Tips

## Example 1: Quick Webcam Test

The fastest way to test the system:

```bash
python gesture_recognition_tracking.py
```

When prompted, select option `2` for webcam mode.

**What to expect:**
- A window will open showing your webcam feed
- Green dots and lines will appear on your hand (21 landmarks)
- The gesture name will appear at the top of the screen
- Press 'q' to quit

**Try these gestures:**
- 🪨 **ROCK**: Make a fist
- ✌️ **SCISSORS**: Extend only index and middle fingers
- ✋ **PALM**: Open your hand with all fingers extended

## Example 2: Process a Video File

If you have a pre-recorded video:

```bash
python gesture_recognition_tracking.py
```

Select option `1`, then:
- Enter your video filename: `my_gestures.mp4`
- Choose whether to save output: `y` or `n`
- If yes, enter output filename: `output.mp4`

**Example session:**
```
Select mode:
1. Process video file
2. Real-time webcam
3. Exit

Enter your choice (1-3): 1
Enter input video path (e.g., hand.mp4): test_video.mp4
Save output video? (y/n): y
Enter output video path (e.g., output.mp4): result.mp4
Processing video... Press 'q' to quit.
```

## Example 3: Using as a Python Module

You can import the functions in your own scripts:

```python
from gesture_recognition_tracking import process_video, process_webcam, recognize_gesture

# Process a video file
process_video("input.mp4", "output.mp4")

# Or use webcam
process_webcam()
```

## Example 4: Custom Gesture Detection

Modify the `recognize_gesture()` function to add new gestures:

```python
def recognize_gesture(hand_landmarks):
    # ... existing code ...
    
    # Add custom gesture: "PEACE" (index + middle fingers, thumb extended)
    if extended_count == 3 and fingers_extended[0] and fingers_extended[1] and fingers_extended[2]:
        return "PEACE"
    
    # Add custom gesture: "THUMBS_UP" (only thumb extended)
    if extended_count == 1 and fingers_extended[0]:
        return "THUMBS_UP"
    
    # ... rest of the code ...
```

## Example 5: Adjusting Detection Sensitivity

Modify the MediaPipe parameters for different scenarios:

```python
# For better accuracy (slower)
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,  # Higher = more strict
    min_tracking_confidence=0.7
)

# For faster processing (less accurate)
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,  # Track only one hand
    min_detection_confidence=0.3,  # Lower = more lenient
    min_tracking_confidence=0.3
)
```

## Example 6: Recording Your Own Test Video

### Using Windows Camera App:
1. Open Camera app (Windows key + type "Camera")
2. Click the video button
3. Record yourself making gestures
4. Save the video
5. Move it to the project folder

### Using Phone:
1. Record video with your phone camera
2. Transfer to computer via USB or cloud
3. Place in project folder
4. Ensure it's in MP4 format

### Tips for good recordings:
- ✓ Good lighting
- ✓ Plain background
- ✓ Hand clearly visible
- ✓ Hold each gesture for 2-3 seconds
- ✓ Keep hand in center of frame

## Example 7: Batch Processing Multiple Videos

Create a script to process multiple videos:

```python
from gesture_recognition_tracking import process_video
import os

# List of video files
videos = ["video1.mp4", "video2.mp4", "video3.mp4"]

for video in videos:
    if os.path.exists(video):
        output = f"output_{video}"
        print(f"Processing {video}...")
        process_video(video, output)
        print(f"Saved to {output}")
    else:
        print(f"File not found: {video}")
```

## Example 8: Debugging - Print Hand Landmarks

To see the raw landmark data:

```python
# Add this inside the main loop after hand detection
if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
        # Print wrist position
        wrist = hand_landmarks.landmark[0]
        print(f"Wrist: x={wrist.x:.3f}, y={wrist.y:.3f}, z={wrist.z:.3f}")
        
        # Print all fingertip positions
        tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
        for tip_id in tips:
            tip = hand_landmarks.landmark[tip_id]
            print(f"Tip {tip_id}: x={tip.x:.3f}, y={tip.y:.3f}")
```

## Example 9: Save Screenshots

Capture screenshots when specific gestures are detected:

```python
import cv2
from datetime import datetime

# Inside the processing loop
if stable_gesture == "PALM":
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"palm_gesture_{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    print(f"Screenshot saved: {filename}")
```

## Example 10: Performance Monitoring

Add FPS counter to monitor performance:

```python
import time

fps_start_time = time.time()
fps_counter = 0

# In the main loop
fps_counter += 1
if (time.time() - fps_start_time) > 1:
    fps = fps_counter / (time.time() - fps_start_time)
    print(f"FPS: {fps:.2f}")
    fps_counter = 0
    fps_start_time = time.time()
    
    # Display on frame
    cv2.putText(frame, f"FPS: {fps:.1f}", 
               (width - 150, 30), cv2.FONT_HERSHEY_SIMPLEX, 
               0.7, (0, 255, 0), 2)
```

## Common Use Cases

### For the Assignment:
1. Test installation: `python test_installation.py`
2. Record your video showing all three gestures
3. Process it: `python gesture_recognition_tracking.py` → option 1
4. Take screenshot of successful recognition
5. Submit to Canvas

### For Development:
1. Use webcam mode for quick testing
2. Adjust parameters based on your environment
3. Add custom gestures as needed
4. Test with different lighting conditions

### For Presentation:
1. Process video with output saving
2. Use the output video in your presentation
3. Show real-time demo with webcam if available

## Tips for Best Results

**Lighting:**
- Use bright, even lighting
- Avoid backlighting (light behind you)
- Natural daylight works best

**Hand Position:**
- Keep hand centered in frame
- Maintain consistent distance from camera
- Avoid rapid movements

**Gestures:**
- Hold each gesture steady for 1-2 seconds
- Make clear, distinct gestures
- Ensure all fingers are visible

**Camera:**
- Use a stable camera position
- Higher resolution is better
- Clean camera lens

## Troubleshooting Examples

**Problem: Gestures not recognized**
```python
# Solution: Lower the threshold
threshold = avg_distance * 0.6  # Instead of 0.8
```

**Problem: Too much jitter**
```python
# Solution: Increase buffer size
buffer_size = 10  # Instead of 5
```

**Problem: Slow performance**
```python
# Solution: Reduce resolution
frame = cv2.resize(frame, (640, 480))
```

**Problem: Hand not detected**
```python
# Solution: Lower detection confidence
min_detection_confidence=0.3  # Instead of 0.5
```

## Next Steps

After mastering the basics:
1. Add more gesture types
2. Integrate with other applications
3. Create gesture-controlled games
4. Build a presentation controller
5. Develop accessibility tools

Happy coding! 🚀
