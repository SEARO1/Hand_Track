"""
Test script to verify all required packages are installed correctly
"""

import sys

def test_imports():
    """Test if all required packages can be imported"""
    print("=" * 60)
    print("Testing Package Installation")
    print("=" * 60)
    print()
    
    # Test OpenCV
    try:
        import cv2
        print("✓ OpenCV installed successfully")
        print(f"  Version: {cv2.__version__}")
    except ImportError as e:
        print("✗ OpenCV not found")
        print(f"  Error: {e}")
        print("  Install with: pip install opencv-python")
        return False
    
    # Test MediaPipe
    try:
        import mediapipe as mp
        print("✓ MediaPipe installed successfully")
        print(f"  Version: {mp.__version__}")
    except ImportError as e:
        print("✗ MediaPipe not found")
        print(f"  Error: {e}")
        print("  Install with: pip install mediapipe")
        return False
    
    # Test NumPy
    try:
        import numpy as np
        print("✓ NumPy installed successfully")
        print(f"  Version: {np.__version__}")
    except ImportError as e:
        print("✗ NumPy not found")
        print(f"  Error: {e}")
        print("  Install with: pip install numpy")
        return False
    
    print()
    return True


def test_webcam():
    """Test if webcam is accessible"""
    print("=" * 60)
    print("Testing Webcam Access")
    print("=" * 60)
    print()
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            print("✓ Webcam is accessible")
            ret, frame = cap.read()
            if ret:
                print(f"  Resolution: {frame.shape[1]}x{frame.shape[0]}")
            cap.release()
            return True
        else:
            print("✗ Cannot access webcam")
            print("  Make sure no other application is using the camera")
            return False
    except Exception as e:
        print(f"✗ Error accessing webcam: {e}")
        return False


def test_mediapipe_hands():
    """Test if MediaPipe Hands can be initialized"""
    print()
    print("=" * 60)
    print("Testing MediaPipe Hands")
    print("=" * 60)
    print()
    
    try:
        import mediapipe as mp
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        print("✓ MediaPipe Hands initialized successfully")
        hands.close()
        return True
    except Exception as e:
        print(f"✗ Error initializing MediaPipe Hands: {e}")
        return False


def test_python_version():
    """Check Python version"""
    print("=" * 60)
    print("System Information")
    print("=" * 60)
    print()
    
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✓ Python version is compatible (3.8+)")
        return True
    else:
        print("✗ Python version is too old (need 3.8+)")
        print("  Please upgrade Python")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Hand Gesture Recognition - Installation Test")
    print("=" * 60)
    print()
    
    results = []
    
    # Test Python version
    results.append(("Python Version", test_python_version()))
    print()
    
    # Test package imports
    results.append(("Package Installation", test_imports()))
    
    # Test webcam
    results.append(("Webcam Access", test_webcam()))
    
    # Test MediaPipe Hands
    results.append(("MediaPipe Hands", test_mediapipe_hands()))
    
    # Summary
    print()
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    print()
    
    all_passed = True
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")
        if not result:
            all_passed = False
    
    print()
    print("=" * 60)
    
    if all_passed:
        print("🎉 All tests passed! You're ready to run the program.")
        print()
        print("Next steps:")
        print("1. Run: python gesture_recognition_tracking.py")
        print("2. Select option 2 for webcam mode")
        print("3. Try making ROCK, SCISSORS, and PALM gestures")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print()
        print("Common solutions:")
        print("- Install missing packages: pip install -r requirements.txt")
        print("- Close other applications using the webcam")
        print("- Upgrade Python to version 3.8 or higher")
    
    print("=" * 60)
    print()
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
