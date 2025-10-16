import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Gesture recognition function
def recognize_gesture(hand_landmarks):
    """
    Recognize hand gesture based on finger positions
    Returns: "ROCK", "SCISSORS", "PALM", or "UNKNOWN"
    """
    # Extract key points (wrist and fingertips)
    wrist = hand_landmarks.landmark[0]
    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]
    middle_tip = hand_landmarks.landmark[12]
    ring_tip = hand_landmarks.landmark[16]
    pinky_tip = hand_landmarks.landmark[20]
    
    # Calculate distances from each fingertip to wrist
    def calculate_distance(point1, point2):
        return np.sqrt((point1.x - point2.x)**2 + 
                      (point1.y - point2.y)**2 + 
                      (point1.z - point2.z)**2)
    
    # Calculate distances
    thumb_dist = calculate_distance(thumb_tip, wrist)
    index_dist = calculate_distance(index_tip, wrist)
    middle_dist = calculate_distance(middle_tip, wrist)
    ring_dist = calculate_distance(ring_tip, wrist)
    pinky_dist = calculate_distance(pinky_tip, wrist)
    
    # Calculate average distance
    avg_distance = (thumb_dist + index_dist + middle_dist + ring_dist + pinky_dist) / 5
    
    # Set threshold to determine if finger is extended
    # A finger is extended if its distance is greater than the average
    threshold = avg_distance * 0.9
    
    # Check which fingers are extended
    # For better ROCK detection, we also check finger knuckles
    index_mcp = hand_landmarks.landmark[5]  # Index finger knuckle
    middle_mcp = hand_landmarks.landmark[9]  # Middle finger knuckle
    
    # Calculate distances from fingertips to their respective knuckles
    index_tip_to_mcp = calculate_distance(index_tip, index_mcp)
    middle_tip_to_mcp = calculate_distance(middle_tip, middle_mcp)
    
    # A finger is extended if:
    # 1. Distance from tip to wrist is greater than threshold
    # 2. Distance from tip to knuckle is large (finger is straight)
    fingers_extended = []
    fingers_extended.append(thumb_dist > threshold)  # Thumb
    fingers_extended.append(index_dist > threshold and index_tip_to_mcp > 0.05)  # Index
    fingers_extended.append(middle_dist > threshold and middle_tip_to_mcp > 0.05)  # Middle
    fingers_extended.append(ring_dist > threshold)  # Ring
    fingers_extended.append(pinky_dist > threshold)  # Pinky
    
    # Count extended fingers
    extended_count = sum(fingers_extended)
    
    # Gesture classification with improved ROCK detection
    if extended_count <= 1:
        # 0 or 1 finger extended = ROCK (closed fist or fist with thumb)
        return "ROCK"
    elif extended_count == 2:
        # Check if it's specifically index and middle fingers (SCISSORS)
        if fingers_extended[1] and fingers_extended[2]:
            return "SCISSORS"
        else:
            return "UNKNOWN"
    elif extended_count >= 4:
        # 4 or 5 fingers extended = PALM (open hand)
        return "PALM"
    else:
        return "UNKNOWN"


def process_video(input_path, output_path=None):
    """
    Process video file for hand gesture recognition
    """
    # Open video file
    cap = cv2.VideoCapture(input_path)
    
    if not cap.isOpened():
        print(f"Error: Cannot open video file {input_path}")
        return
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Initialize video writer if output path is provided
    out = None
    if output_path:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Buffer for gesture stabilization
    gesture_buffer = []
    buffer_size = 5
    
    print("Processing video... Press 'q' to quit.")
    
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame with MediaPipe
        results = hands.process(rgb_frame)
        
        # Draw hand landmarks and recognize gestures
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
                )
                
                # Recognize gesture
                gesture = recognize_gesture(hand_landmarks)
                
                # Add to buffer for stabilization
                gesture_buffer.append(gesture)
                if len(gesture_buffer) > buffer_size:
                    gesture_buffer.pop(0)
                
                # Get most common gesture from buffer
                if gesture_buffer:
                    stable_gesture = max(set(gesture_buffer), key=gesture_buffer.count)
                else:
                    stable_gesture = gesture
                
                # Display gesture on frame
                cv2.putText(frame, f"Gesture: {stable_gesture}", 
                           (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                           1.5, (0, 255, 255), 3)
                
                # Display frame number
                cv2.putText(frame, f"Frame: {frame_count}", 
                           (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.7, (255, 255, 255), 2)
        
        # Write frame to output video
        if out:
            out.write(frame)
        
        # Display the frame
        cv2.imshow('Hand Gesture Recognition', frame)
        
        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release resources
    cap.release()
    if out:
        out.release()
    cv2.destroyAllWindows()
    
    print(f"Processing complete! Total frames: {frame_count}")
    if output_path:
        print(f"Output saved to: {output_path}")


def process_webcam():
    """
    Process webcam feed for real-time hand gesture recognition
    """
    # Open webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Cannot access webcam")
        return
    
    # Buffer for gesture stabilization
    gesture_buffer = []
    buffer_size = 5
    
    print("Starting webcam... Press 'q' to quit.")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame with MediaPipe
        results = hands.process(rgb_frame)
        
        # Draw hand landmarks and recognize gestures
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
                )
                
                # Recognize gesture
                gesture = recognize_gesture(hand_landmarks)
                
                # Add to buffer for stabilization
                gesture_buffer.append(gesture)
                if len(gesture_buffer) > buffer_size:
                    gesture_buffer.pop(0)
                
                # Get most common gesture from buffer
                if gesture_buffer:
                    stable_gesture = max(set(gesture_buffer), key=gesture_buffer.count)
                else:
                    stable_gesture = gesture
                
                # Display gesture on frame
                cv2.putText(frame, f"Gesture: {stable_gesture}", 
                           (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                           1.5, (0, 255, 255), 3)
        else:
            cv2.putText(frame, "No hand detected", 
                       (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                       1.0, (0, 0, 255), 2)
        
        # Display instructions
        cv2.putText(frame, "Press 'q' to quit", 
                   (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.7, (255, 255, 255), 2)
        
        # Display the frame
        cv2.imshow('Hand Gesture Recognition - Webcam', frame)
        
        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print("=" * 60)
    print("Hand Gesture Recognition and Tracking System")
    print("=" * 60)
    print("\nSelect mode:")
    print("1. Process video file")
    print("2. Real-time webcam")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ")
    
    if choice == "1":
        input_path = input("Enter input video path (e.g., hand.mp4): ")
        save_output = input("Save output video? (y/n): ").lower()
        
        if save_output == 'y':
            output_path = input("Enter output video path (e.g., output.mp4): ")
            process_video(input_path, output_path)
        else:
            process_video(input_path)
    
    elif choice == "2":
        process_webcam()
    
    elif choice == "3":
        print("Exiting...")
    
    else:
        print("Invalid choice!")
    
    # Cleanup
    hands.close()
