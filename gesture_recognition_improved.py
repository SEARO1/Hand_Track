"""
Enhanced Hand Gesture Recognition System
Supports: ROCK, SCISSORS, PAPER gestures
Features: Video/Webcam processing, gesture confidence, FPS tracking, improved accuracy
"""

import cv2
import mediapipe as mp
import numpy as np
import argparse
import time
from collections import deque, Counter

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


class GestureRecognizer:
    """Enhanced gesture recognition with confidence scoring"""
    
    def __init__(self, confidence_threshold=0.7):
        self.confidence_threshold = confidence_threshold
        self.gesture_history = deque(maxlen=30)
        
    def calculate_distance(self, p1, p2):
        """Calculate 3D Euclidean distance between two points"""
        return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)
    
    def is_finger_extended(self, landmarks, finger_tip_idx, finger_pip_idx, finger_mcp_idx):
        """
        Check if a finger is extended by comparing tip position to joints
        More accurate than just distance from wrist
        """
        tip = landmarks[finger_tip_idx]
        pip = landmarks[finger_pip_idx]  # Proximal interphalangeal joint
        mcp = landmarks[finger_mcp_idx]  # Metacarpophalangeal joint
        
        # Calculate distances
        tip_to_pip = self.calculate_distance(tip, pip)
        pip_to_mcp = self.calculate_distance(pip, mcp)
        tip_to_mcp = self.calculate_distance(tip, mcp)
        
        # Finger is extended if tip is far from MCP and the finger is relatively straight
        # (tip-to-mcp distance is close to sum of individual segments)
        is_extended = tip_to_mcp > (tip_to_pip + pip_to_mcp) * 0.85
        
        return is_extended
    
    def is_thumb_extended(self, landmarks):
        """Special check for thumb extension (different anatomy)"""
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        thumb_mcp = landmarks[2]
        index_mcp = landmarks[5]
        
        # Thumb is extended if it's far from index finger base
        thumb_to_index = self.calculate_distance(thumb_tip, index_mcp)
        thumb_length = self.calculate_distance(thumb_tip, thumb_mcp)
        
        return thumb_to_index > thumb_length * 0.8
    
    def recognize_gesture(self, landmarks):
        """
        Recognize hand gesture with confidence score
        Returns: (gesture_name, confidence)
        """
        # Check each finger
        thumb_extended = self.is_thumb_extended(landmarks)
        index_extended = self.is_finger_extended(landmarks, 8, 6, 5)
        middle_extended = self.is_finger_extended(landmarks, 12, 10, 9)
        ring_extended = self.is_finger_extended(landmarks, 16, 14, 13)
        pinky_extended = self.is_finger_extended(landmarks, 20, 18, 17)
        
        # Count extended fingers (excluding thumb for main count)
        fingers = [index_extended, middle_extended, ring_extended, pinky_extended]
        extended_count = sum(fingers)
        
        # Gesture classification with confidence
        gesture = "UNKNOWN"
        confidence = 0.0
        
        # ROCK: All fingers closed (fist)
        if extended_count == 0 and not thumb_extended:
            gesture = "ROCK"
            confidence = 0.95
        elif extended_count == 0:  # Fist with thumb out
            gesture = "ROCK"
            confidence = 0.85
        
        # SCISSORS: Only index and middle fingers extended
        elif extended_count == 2 and index_extended and middle_extended:
            if not ring_extended and not pinky_extended:
                gesture = "SCISSORS"
                confidence = 0.95
            else:
                gesture = "SCISSORS"
                confidence = 0.75
        
        # PAPER: All or most fingers extended (open hand)
        elif extended_count >= 4:
            gesture = "PAPER"
            confidence = 0.95
        elif extended_count == 3 and thumb_extended:
            gesture = "PAPER"
            confidence = 0.85
        
        # Ambiguous cases
        elif extended_count == 1:
            gesture = "UNKNOWN"
            confidence = 0.5
        elif extended_count == 3:
            gesture = "UNKNOWN"
            confidence = 0.6
        
        return gesture, confidence
    
    def get_stable_gesture(self, current_gesture, current_confidence):
        """
        Use temporal smoothing to get stable gesture
        Returns most common gesture from recent history
        """
        if current_confidence >= self.confidence_threshold:
            self.gesture_history.append(current_gesture)
        
        if len(self.gesture_history) == 0:
            return "NO HAND", 0.0
        
        # Get most common gesture from history
        gesture_counts = Counter(self.gesture_history)
        most_common = gesture_counts.most_common(1)[0]
        stable_gesture = most_common[0]
        stability = most_common[1] / len(self.gesture_history)
        
        return stable_gesture, stability


class VideoProcessor:
    """Process video files or webcam feed for gesture recognition"""
    
    def __init__(self, source=0, output_path=None, show_fps=True, show_landmarks=True):
        self.source = source
        self.output_path = output_path
        self.show_fps = show_fps
        self.show_landmarks = show_landmarks
        
        # Initialize MediaPipe Hands
        self.hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        
        # Initialize gesture recognizer
        self.recognizer = GestureRecognizer(confidence_threshold=0.7)
        
        # FPS calculation
        self.fps_history = deque(maxlen=30)
        self.prev_time = time.time()
        
        # Gesture colors
        self.gesture_colors = {
            "ROCK": (0, 0, 255),      # Red
            "SCISSORS": (0, 255, 255), # Yellow
            "PAPER": (0, 255, 0),      # Green
            "UNKNOWN": (128, 128, 128),# Gray
            "NO HAND": (200, 200, 200) # Light gray
        }
    
    def calculate_fps(self):
        """Calculate current FPS"""
        current_time = time.time()
        fps = 1 / (current_time - self.prev_time)
        self.prev_time = current_time
        self.fps_history.append(fps)
        return np.mean(self.fps_history)
    
    def draw_info_panel(self, frame, gesture, confidence, stability, fps):
        """Draw information panel on frame"""
        height, width = frame.shape[:2]
        
        # Semi-transparent background for info panel
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (400, 180), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        # Gesture name (large)
        color = self.gesture_colors.get(gesture, (255, 255, 255))
        cv2.putText(frame, gesture, (20, 60),
                   cv2.FONT_HERSHEY_BOLD, 2.0, color, 4)
        
        # Confidence bar
        bar_width = int(300 * confidence)
        cv2.rectangle(frame, (20, 80), (320, 100), (50, 50, 50), -1)
        cv2.rectangle(frame, (20, 80), (20 + bar_width, 100), color, -1)
        cv2.putText(frame, f"Confidence: {confidence:.0%}", (20, 120),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Stability indicator
        stability_width = int(300 * stability)
        cv2.rectangle(frame, (20, 130), (320, 150), (50, 50, 50), -1)
        cv2.rectangle(frame, (20, 130), (20 + stability_width, 150), (255, 200, 0), -1)
        cv2.putText(frame, f"Stability: {stability:.0%}", (20, 170),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # FPS counter
        if self.show_fps:
            cv2.putText(frame, f"FPS: {fps:.1f}", (width - 150, 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # Instructions
        cv2.putText(frame, "Press 'Q' to quit | 'S' to screenshot", 
                   (10, height - 15),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    def process(self):
        """Main processing loop"""
        # Open video source
        cap = cv2.VideoCapture(self.source)
        
        if not cap.isOpened():
            print(f"Error: Cannot open video source: {self.source}")
            return
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS)) if self.source != 0 else 30
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"Video source: {self.source}")
        print(f"Resolution: {width}x{height} @ {fps} FPS")
        
        # Initialize video writer if output path is provided
        out = None
        if self.output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(self.output_path, fourcc, fps, (width, height))
            print(f"Recording to: {self.output_path}")
        
        print("\nGesture Guide:")
        print("  ROCK     - Closed fist (all fingers bent)")
        print("  SCISSORS - Index and middle fingers extended")
        print("  PAPER    - Open hand (all fingers extended)")
        print("\nProcessing... Press 'Q' to quit, 'S' to save screenshot\n")
        
        frame_count = 0
        screenshot_count = 0
        
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                if self.source == 0:
                    print("Error: Cannot read from webcam")
                    break
                else:
                    print("Video finished!")
                    break
            
            frame_count += 1
            
            # Flip frame for webcam (mirror effect)
            if self.source == 0:
                frame = cv2.flip(frame, 1)
            
            # Convert to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process with MediaPipe
            results = self.hands.process(rgb_frame)
            
            # Default values
            gesture = "NO HAND"
            confidence = 0.0
            stability = 0.0
            
            # Process hand landmarks
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks
                    if self.show_landmarks:
                        mp_drawing.draw_landmarks(
                            frame,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style()
                        )
                    
                    # Recognize gesture
                    raw_gesture, raw_confidence = self.recognizer.recognize_gesture(
                        hand_landmarks.landmark
                    )
                    
                    # Get stable gesture
                    gesture, stability = self.recognizer.get_stable_gesture(
                        raw_gesture, raw_confidence
                    )
                    confidence = raw_confidence
            
            # Calculate FPS
            current_fps = self.calculate_fps()
            
            # Draw information panel
            self.draw_info_panel(frame, gesture, confidence, stability, current_fps)
            
            # Write to output video
            if out:
                out.write(frame)
            
            # Display frame
            window_name = 'Enhanced Gesture Recognition'
            cv2.imshow(window_name, frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == ord('Q'):
                print("\nQuitting...")
                break
            elif key == ord('s') or key == ord('S'):
                screenshot_count += 1
                screenshot_name = f"screenshot_{screenshot_count}.png"
                cv2.imwrite(screenshot_name, frame)
                print(f"Screenshot saved: {screenshot_name}")
        
        # Cleanup
        print(f"\nProcessed {frame_count} frames")
        cap.release()
        if out:
            out.release()
            print(f"Output saved to: {self.output_path}")
        cv2.destroyAllWindows()
        self.hands.close()


def main():
    """Main entry point with argument parsing"""
    parser = argparse.ArgumentParser(
        description='Enhanced Hand Gesture Recognition System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process webcam
  python gesture_recognition_improved.py
  
  # Process video file
  python gesture_recognition_improved.py --input hand.mp4
  
  # Process video and save output
  python gesture_recognition_improved.py --input hand.mp4 --output result.mp4
  
  # Hide landmarks for cleaner view
  python gesture_recognition_improved.py --no-landmarks
        """
    )
    
    parser.add_argument('--input', '-i', type=str, default=None,
                       help='Input video file path (default: webcam)')
    parser.add_argument('--output', '-o', type=str, default=None,
                       help='Output video file path (optional)')
    parser.add_argument('--no-fps', action='store_true',
                       help='Hide FPS counter')
    parser.add_argument('--no-landmarks', action='store_true',
                       help='Hide hand landmarks')
    
    args = parser.parse_args()
    
    # Determine video source
    source = args.input if args.input else 0
    
    # Create processor
    processor = VideoProcessor(
        source=source,
        output_path=args.output,
        show_fps=not args.no_fps,
        show_landmarks=not args.no_landmarks
    )
    
    # Run processing
    try:
        processor.process()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
