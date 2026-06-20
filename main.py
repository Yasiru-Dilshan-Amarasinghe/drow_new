"""
Driver Drowsiness Detection System
Real-time drowsiness detection using OpenCV and eye aspect ratio
"""

import cv2
import sys
import logging
import time
from src.eye_detector import EyeDetector, calculate_eye_aspect_ratio, get_eye_center
from src.drowsiness_detector import DrowsinessDetector, trigger_alarm
from src.utils import setup_logging, draw_detections, display_stats, log_event, display_datetime, display_error_status, display_system_info

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
    
    # FPS calculation
    prev_time = time.time()
    fps = 0
    frame_count = 0
    errors = []
    
    try:
        while True:
            ret, frame = cap.read()
            frame_count += 1
            
            # Calculate FPS
            current_time = time.time()
            if current_time - prev_time >= 1:
                fps = frame_count / (current_time - prev_time)
                frame_count = 0
                prev_time = current_time
            
            if not ret:
                logger.warning("Failed to read frame from camera")
                errors = ["Camera frame read failed"]
                break
            
            errors = []  # Clear errors on successful frame read
            
            # Detect faces
            faces = eye_detector.detect_faces(frame)
            
            if len(faces) > 0:
                # Process first detected face
                face = faces[0]
                eyes = eye_detector.detect_eyes(frame, face)
                
                # Calculate eye aspect ratio (simplified for cascade classifiers)
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
                detection_status = "Face Detected"
            else:
                cv2.putText(frame, "No face detected", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
                detection_status = "No Face"
            
            # Display statistics
            frame = display_stats(frame, drowsiness_detector)
            
            # Display date and time
            frame = display_datetime(frame, position=(10, frame.shape[0] - 20))
            
            # Display error status
            frame = display_error_status(frame, errors, position=(10, 150))
            
            # Display system info (FPS, camera status, detection status)
            frame = display_system_info(frame, fps=fps, camera_status="OK", 
                                       detection_status=detection_status)
            
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
