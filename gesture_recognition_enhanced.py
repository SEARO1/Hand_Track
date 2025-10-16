import cv2
import mediapipe as mp
import numpy as np
import time
from collections import deque
import argparse

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

class GestureRecognizer:
    """Enhanced gesture recognition with multiple gesture support and improved accuracy"""
    
    def __init__(self, buffer_size=7):
        self.hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.6
        )
        self.gesture_buffer = deque(maxlen=buffer_size)
        self.fps_buffer = deque(maxlen=30)
        
    def calculate_distance(self, p1, p2):
        """Calculate Euclidean distance between two points"""
        return np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2)
    
    def is_finger_extended(self, landmarks, finger_tip_idx, finger_pip_idx, finger_mcp_idx, wrist_idx=0):
        """
        Determine if a finger is extended based on joint positions
        Uses both distance and angle-based detection for better accuracy
        """
        tip = landmarks[finger_tip_idx]
        pip = landmarks[finger_pip_idx]
        mcp = landmarks[finger_mcp_idx]
        wrist = landmarks[wrist_idx]
        
        # Distance-based check: tip should be farther from wrist than PIP joint
        tip_to_wrist = self.calculate_distance(tip, wrist)
        pip_to_wrist = self.calculate_distance(pip, wrist)
        
        # Straightness check: tip should be far from MCP
        tip_to_mcp = self.calculate_distance(tip, mcp)
        
        return tip_to_wrist > pip_to_wrist * 0.95 and tip_to_mcp > 0.05
    
    def is_thumb_extended(self, landmarks):
        """Special check for thumb extension (different anatomy)"""
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        thumb_mcp = landmarks[2]
        index_mcp = landmarks[5]
        
        # Thumb is extended if tip is far from palm (index MCP)
        thumb_to_index = self.calculate_distance(thumb_tip, index_mcp)
        ip_to_index = self.calculate_distance(thumb_ip, index_mcp)
        
        return thumb_to_index > ip_to_index * 1.1
    
    def recognize_gesture(self, landmarks):
        """
        Recognize hand gestures with improved accuracy
        Supports: ROCK, SCISSORS, PAPER, PEACE, THUMBS_UP, POINTING, OK, MIDDLE_FINGER
        """
        # Check each finger extension status
        thumb_extended = self.is_thumb_extended(landmarks)
        index_extended = self.is_finger_extended(landmarks, 8, 6, 5)
        middle_extended = self.is_finger_extended(landmarks, 12, 10, 9)
        ring_extended = self.is_finger_extended(landmarks, 16, 14, 13)
        pinky_extended = self.is_finger_extended(landmarks, 20, 18, 17)
        
        # Count extended fingers
        fingers = [thumb_extended, index_extended, middle_extended, ring_extended, pinky_extended]
        extended_count = sum(fingers)
        
        # Gesture classification with priority order
        
        # MIDDLE_FINGER: Only middle finger extended
        if middle_extended and not index_extended and not ring_extended and not pinky_extended:
            return "MIDDLE_FINGER"
        
        # POINTING: Only index finger extended
        if index_extended and not middle_extended and not ring_extended and not pinky_extended:
            return "POINTING"
        
        # PEACE/SCISSORS: Index and middle fingers extended
        if index_extended and middle_extended and not ring_extended and not pinky_extended:
            return "PEACE"
        
        # THUMBS_UP: Only thumb extended
        if thumb_extended and not index_extended and not middle_extended and not ring_extended and not pinky_extended:
            return "THUMBS_UP"
        
        # OK sign: Thumb and index forming circle (approximation)
        if thumb_extended and index_extended and not middle_extended and not ring_extended and not pinky_extended:
            thumb_tip = landmarks[4]
            index_tip = landmarks[8]
            if self.calculate_distance(thumb_tip, index_tip) < 0.05:
                return "OK"
        
        # ROCK: Closed fist (0-1 fingers extended)
        if extended_count <= 1:
            return "ROCK"
        
        # PAPER: Open hand (4-5 fingers extended)
        if extended_count >= 4:
            return "PAPER"
        
        # THREE: Three fingers extended
        if extended_count == 3:
            return "THREE"
        
        return "UNKNOWN"
    
    def get_stable_gesture(self, current_gesture):
        """Apply temporal smoothing to reduce jitter"""
        self.gesture_buffer.append(current_gesture)
        
        if len(self.gesture_buffer) < 3:
            return current_gesture
        
        # Get most common gesture in buffer
        gesture_counts = {}
        for gesture in self.gesture_buffer:
            gesture_counts[gesture] = gesture_counts.get(gesture, 0) + 1
        
        most_common = max(gesture_counts, key=gesture_counts.get)
        
        # Only return if it appears in majority of buffer
        if gesture_counts[most_common] > len(self.gesture_buffer) // 2:
            return most_common
        
        return current_gesture
    
    def get_gesture_color(self, gesture):
        """Return color for each gesture type"""
        colors = {
            "ROCK": (0, 0, 255),        # Red
            "PAPER": (0, 255, 0),       # Green
            "PEACE": (255, 255, 0),     # Cyan
            "POINTING": (255, 165, 0),  # Orange
            "THUMBS_UP": (0, 255, 255), # Yellow
            "MIDDLE_FINGER": (255, 0, 255),  # Magenta
            "OK": (255, 192, 203),      # Pink
            "THREE": (147, 20, 255),    # Purple
            "UNKNOWN": (128, 128, 128), # Gray
            "NO_HAND": (100, 100, 100)  # Dark Gray
        }
        return colors.get(gesture, (255, 255, 255))
    
    def update_fps(self, fps):
        """Update FPS buffer for averaging"""
        self.fps_buffer.append(fps)
    
    def get_average_fps(self):
        """Get average FPS from buffer"""
        if len(self.fps_buffer) == 0:
            return 0
        return sum(self.fps_buffer) / len(self.fps_buffer)
    
    def release(self):
        """Release MediaPipe resources"""
        self.hands.close()


class CameraManager:
    """Robust camera initialization with fallback options"""
    
    @staticmethod
    def open_camera_with_fallback(camera_index=0):
        """Try to open camera with multiple backends"""
        candidates = []
        
        # Try different backends
        backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]
        
        for backend in backends:
            for idx in [camera_index, 0, 1]:
                candidates.append((idx, backend))
        
        for idx, backend in candidates:
            try:
                cap = cv2.VideoCapture(idx, backend)
                if cap.isOpened():
                    ret, _ = cap.read()
                    if ret:
                        print(f"[INFO] Camera opened: index={idx}, backend={backend}")
                        return cap
                    cap.release()
            except:
                continue
        
        return None


class GestureRecognitionApp:
    """Main application for gesture recognition"""
    
    def __init__(self, source=0, save_output=None, show_fps=True, show_landmarks=True):
        self.source = source
        self.save_output = save_output
        self.show_fps = show_fps
        self.show_landmarks = show_landmarks
        self.recognizer = GestureRecognizer(buffer_size=7)
        
    def process_frame(self, frame, frame_time):
        """Process a single frame for gesture recognition"""
        # Flip for mirror effect (only for webcam)
        if isinstance(self.source, int):
            frame = cv2.flip(frame, 1)
        
        # Convert to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process with MediaPipe
        results = self.recognizer.hands.process(rgb_frame)
        
        current_gesture = "NO_HAND"
        hand_count = 0
        
        # Process detected hands
        if results.multi_hand_landmarks:
            hand_count = len(results.multi_hand_landmarks)
            
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                # Draw landmarks
                if self.show_landmarks:
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )
                
                # Recognize gesture
                gesture = self.recognizer.recognize_gesture(hand_landmarks.landmark)
                stable_gesture = self.recognizer.get_stable_gesture(gesture)
                
                if idx == 0:  # Use first hand for main gesture display
                    current_gesture = stable_gesture
                
                # Draw gesture label near hand
                if hand_landmarks.landmark:
                    h, w, _ = frame.shape
                    wrist = hand_landmarks.landmark[0]
                    x, y = int(wrist.x * w), int(wrist.y * h)
                    
                    color = self.recognizer.get_gesture_color(stable_gesture)
                    cv2.putText(frame, stable_gesture, (x - 50, y - 30),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # Draw main gesture display
        color = self.recognizer.get_gesture_color(current_gesture)
        cv2.putText(frame, f"Gesture: {current_gesture}", (20, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)
        
        # Draw hand count
        cv2.putText(frame, f"Hands: {hand_count}", (20, 110),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Draw FPS
        if self.show_fps and frame_time > 0:
            fps = 1.0 / frame_time
            self.recognizer.update_fps(fps)
            avg_fps = self.recognizer.get_average_fps()
            cv2.putText(frame, f"FPS: {avg_fps:.1f}", (20, frame.shape[0] - 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Draw instructions
        cv2.putText(frame, "Press 'q' to quit | 's' to screenshot", 
                   (20, frame.shape[0] - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        return frame
    
    def run_webcam(self):
        """Run real-time webcam gesture recognition"""
        cap = CameraManager.open_camera_with_fallback(self.source)
        
        if cap is None:
            print("[ERROR] Could not open camera")
            return
        
        # Setup video writer if needed
        out = None
        if self.save_output:
            fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(self.save_output, fourcc, fps, (width, height))
            print(f"[INFO] Recording to {self.save_output}")
        
        print("\n" + "="*60)
        print("GESTURE RECOGNITION - WEBCAM MODE")
        print("="*60)
        print("\nSupported Gestures:")
        print("  🪨 ROCK - Closed fist")
        print("  ✌️ PEACE - Index and middle fingers")
        print("  ✋ PAPER - Open hand (all fingers)")
        print("  👆 POINTING - Index finger only")
        print("  👍 THUMBS_UP - Thumb only")
        print("  🖕 MIDDLE_FINGER - Middle finger only")
        print("  👌 OK - Thumb and index circle")
        print("  3️⃣ THREE - Three fingers extended")
        print("\nControls:")
        print("  'q' - Quit")
        print("  's' - Save screenshot")
        print("="*60 + "\n")
        
        screenshot_count = 0
        prev_time = time.time()
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Calculate frame time
            current_time = time.time()
            frame_time = current_time - prev_time
            prev_time = current_time
            
            # Process frame
            processed_frame = self.process_frame(frame, frame_time)
            
            # Write to output if recording
            if out:
                out.write(processed_frame)
            
            # Display
            cv2.imshow('Enhanced Gesture Recognition', processed_frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                screenshot_count += 1
                filename = f"screenshot_{screenshot_count}.png"
                cv2.imwrite(filename, processed_frame)
                print(f"[INFO] Screenshot saved: {filename}")
        
        # Cleanup
        cap.release()
        if out:
            out.release()
        cv2.destroyAllWindows()
        self.recognizer.release()
        print("\n[INFO] Application closed")
    
    def run_video(self):
        """Process video file"""
        cap = cv2.VideoCapture(self.source)
        
        if not cap.isOpened():
            print(f"[ERROR] Could not open video: {self.source}")
            return
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"\n[INFO] Video: {self.source}")
        print(f"[INFO] Resolution: {width}x{height}, FPS: {fps}, Frames: {total_frames}")
        
        # Setup video writer if needed
        out = None
        if self.save_output:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(self.save_output, fourcc, fps, (width, height))
            print(f"[INFO] Output: {self.save_output}")
        
        frame_count = 0
        prev_time = time.time()
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Calculate frame time
            current_time = time.time()
            frame_time = current_time - prev_time
            prev_time = current_time
            
            # Process frame
            processed_frame = self.process_frame(frame, frame_time)
            
            # Add frame counter
            cv2.putText(processed_frame, f"Frame: {frame_count}/{total_frames}",
                       (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Write to output
            if out:
                out.write(processed_frame)
            
            # Display
            cv2.imshow('Enhanced Gesture Recognition - Video', processed_frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                filename = f"screenshot_frame_{frame_count}.png"
                cv2.imwrite(filename, processed_frame)
                print(f"[INFO] Screenshot saved: {filename}")
        
        # Cleanup
        cap.release()
        if out:
            out.release()
        cv2.destroyAllWindows()
        self.recognizer.release()
        
        print(f"\n[INFO] Processed {frame_count} frames")
        if self.save_output:
            print(f"[INFO] Output saved: {self.save_output}")


def main():
    """Main entry point with argument parsing"""
    parser = argparse.ArgumentParser(description='Enhanced Hand Gesture Recognition System')
    parser.add_argument('--source', type=str, default='0',
                       help='Video source: 0 for webcam, or path to video file')
    parser.add_argument('--output', type=str, default=None,
                       help='Output video file path (optional)')
    parser.add_argument('--no-fps', action='store_true',
                       help='Hide FPS counter')
    parser.add_argument('--no-landmarks', action='store_true',
                       help='Hide hand landmarks')
    
    args = parser.parse_args()
    
    # Determine source type
    try:
        source = int(args.source)
    except ValueError:
        source = args.source
    
    # Create and run application
    app = GestureRecognitionApp(
        source=source,
        save_output=args.output,
        show_fps=not args.no_fps,
        show_landmarks=not args.no_landmarks
    )
    
    if isinstance(source, int):
        app.run_webcam()
    else:
        app.run_video()


if __name__ == "__main__":
    # Interactive mode if no arguments provided
    import sys
    
    if len(sys.argv) == 1:
        print("\n" + "="*60)
        print("ENHANCED HAND GESTURE RECOGNITION SYSTEM")
        print("="*60)
        print("\nSelect mode:")
        print("1. Webcam (real-time)")
        print("2. Video file")
        print("3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            save = input("Record output? (y/n): ").strip().lower()
            output = "output_webcam.mp4" if save == 'y' else None
            app = GestureRecognitionApp(source=0, save_output=output)
            app.run_webcam()
        
        elif choice == "2":
            video_path = input("Enter video path: ").strip()
            save = input("Save processed video? (y/n): ").strip().lower()
            output = input("Output path: ").strip() if save == 'y' else None
            app = GestureRecognitionApp(source=video_path, save_output=output)
            app.run_video()
        
        elif choice == "3":
            print("Exiting...")
        else:
            print("Invalid choice!")
    else:
        main()
