"""
Driver Drowsiness Detection System
Real-time drowsiness detection using OpenCV and eye aspect ratio
"""

import cv2
import sys
import logging
from src.eye_detector import EyeDetector, calculate_eye_aspect_ratio, get_eye_center
from src.drowsiness_detector import DrowsinessDetector, trigger_alarm
from src.utils import setup_logging, draw_detections, display_stats, log_event

# Configuration
EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 30
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

def main():
    """Main function to run the drowsiness detection system."""
    
    # Setup logging
    logger = setup_logging("drowsiness_detection.log")
    logger.info("=== Driver Drowsiness Detection System Started ===")
    
    # Initialize detectors
    eye_detector = EyeDetector()
    drowsiness_detector = DrowsinessDetector(
        eye_ar_thresh=EYE_AR_THRESH,
        eye_ar_consec_frames=EYE_AR_CONSEC_FRAMES,
        alarm_enabled=True
    )
    
    # Initialize video capture
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    if not cap.isOpened():
        logger.error("Failed to open camera")
        print("Error: Could not open camera")
        return
    
    logger.info("Camera initialized successfully")
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                logger.warning("Failed to read frame from camera")
                break
            
            # Detect faces
            faces = eye_detector.detect_faces(frame)
            
            if len(faces) > 0:
                # Process first detected face
                face = faces[0]
                eyes = eye_detector.detect_eyes(frame, face)
                
                # Calculate eye aspect ratio (simplified for cascade classifiers)
                # In real-world, use dlib landmarks for better accuracy
                eye_aspect_ratio = len(eyes) / 2 if len(eyes) > 0 else 1.0
                
                # If no eyes detected, assume closed
                if len(eyes) == 0:
                    eye_aspect_ratio = 0.2
                
                # Update drowsiness detector
                is_drowsy, counter, alarm_on = drowsiness_detector.update(eye_aspect_ratio)
                
                # Trigger alarm if needed
                if alarm_on and is_drowsy:
                    try:
                        trigger_alarm()
                        log_event(logger, "ALARM_TRIGGERED", 
                                f"Drowsiness detected at {counter} frames")
                    except Exception as e:
                        logger.warning(f"Could not trigger alarm: {e}")
                
                # Draw detections
                frame = draw_detections(frame, faces, eyes, is_drowsy, eye_aspect_ratio)
            else:
                cv2.putText(frame, "No face detected", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
            
            # Display statistics
            frame = display_stats(frame, drowsiness_detector)
            
            # Display frame
            cv2.imshow("Driver Drowsiness Detection", frame)
            
            # Press 'q' to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                logger.info("System stopped by user")
                break
    
    except KeyboardInterrupt:
        logger.info("System interrupted by user")
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    
    finally:
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        
        # Log final statistics
        metrics = drowsiness_detector.get_drowsiness_metrics()
        logger.info(f"Final Statistics - Total Events: {metrics['total_events']}, "
                   f"Average EAR: {metrics['avg_ear']:.2f}, "
                   f"Closed Percentage: {metrics['closed_percentage']:.1f}%")
        logger.info("=== Driver Drowsiness Detection System Stopped ===")

if __name__ == "__main__":
    main()
