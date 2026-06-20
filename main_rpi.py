"""
Driver Drowsiness Detection System - Raspberry Pi Version
Real-time drowsiness detection using OpenCV and eye aspect ratio
With PWM signal output for hardware alerts (buzzer, LED, etc.)
"""

import cv2
import sys
import logging
import time
from src.eye_detector import EyeDetector, calculate_eye_aspect_ratio, get_eye_center
from src.drowsiness_detector import DrowsinessDetector, trigger_alarm
from src.utils import setup_logging, draw_detections, display_stats, log_event, display_datetime, display_error_status, display_system_info
from src.gpio_control import PWMController, LEDController

# Configuration
EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 30
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Raspberry Pi Configuration
GPIO_ENABLED = True  # Set to False to run on desktop without GPIO
PWM_PIN = 17  # GPIO pin for buzzer
LED_PIN = 27  # GPIO pin for LED
PWM_FREQUENCY = 1000  # 1kHz for buzzer

def main():
    """Main function to run the drowsiness detection system with PWM control."""
    
    # Setup logging
    logger = setup_logging("drowsiness_detection.log")
    logger.info("=== Driver Drowsiness Detection System Started (RPi Mode) ===")
    
    # Initialize GPIO controllers
    pwm_controller = None
    led_controller = None
    
    if GPIO_ENABLED:
        try:
            pwm_controller = PWMController(gpio_pin=PWM_PIN, frequency=PWM_FREQUENCY, enable_pi=True)
            led_controller = LEDController(gpio_pin=LED_PIN, enable_pi=True)
            logger.info("GPIO controllers initialized")
        except Exception as e:
            logger.warning(f"Could not initialize GPIO: {e}")
    
    # Initialize detectors
    eye_detector = EyeDetector()
    drowsiness_detector = DrowsinessDetector(
        eye_ar_thresh=EYE_AR_THRESH,
        eye_ar_consec_frames=EYE_AR_CONSEC_FRAMES,
        alarm_enabled=False,  # Disable system alarm in favor of PWM
        pwm_controller=pwm_controller
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
    camera_status = "OK"
    
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
                camera_status = "FAILED"
                break
            
            errors = []  # Clear errors on successful frame read
            camera_status = "OK"
            
            # Detect faces
            faces = eye_detector.detect_faces(frame)
            
            if len(faces) > 0:
                # Process first detected face
                face = faces[0]
                eyes = eye_detector.detect_eyes(frame, face)
                
                # Calculate eye aspect ratio
                eye_aspect_ratio = len(eyes) / 2 if len(eyes) > 0 else 1.0
                
                # If no eyes detected, assume closed
                if len(eyes) == 0:
                    eye_aspect_ratio = 0.2
                
                # Update drowsiness detector
                is_drowsy, counter, alarm_on = drowsiness_detector.update(eye_aspect_ratio)
                
                # Control LED based on drowsiness state
                if led_controller:
                    if is_drowsy:
                        led_controller.on()
                    else:
                        led_controller.off()
                
                # Trigger system alarm if needed (for non-Pi testing)
                if alarm_on and is_drowsy and not GPIO_ENABLED:
                    try:
                        trigger_alarm()
                    except Exception as e:
                        logger.warning(f"Could not trigger system alarm: {e}")
                
                # Log drowsiness event
                if is_drowsy:
                    log_event(logger, "DROWSINESS_ALERT", 
                            f"Eyes closed for {counter} frames, PWM triggered")
                
                # Draw detections
                frame = draw_detections(frame, faces, eyes, is_drowsy, eye_aspect_ratio)
                detection_status = "Face Detected"
            else:
                cv2.putText(frame, "No face detected", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
                if led_controller:
                    led_controller.off()
                detection_status = "No Face"
            
            # Display statistics
            frame = display_stats(frame, drowsiness_detector)
            
            # Display date and time
            frame = display_datetime(frame, position=(10, frame.shape[0] - 20))
            
            # Display error status
            frame = display_error_status(frame, errors, position=(10, 150))
            
            # Display system info (FPS, camera status, detection status, GPIO status)
            gpio_status = "GPIO ON" if GPIO_ENABLED and pwm_controller else "GPIO OFF"
            frame = display_system_info(frame, fps=fps, camera_status=camera_status, 
                                       detection_status=detection_status)
            
            # Add GPIO status
            gpio_color = (0, 255, 0) if GPIO_ENABLED and pwm_controller else (255, 165, 0)
            cv2.putText(frame, gpio_status, (frame.shape[1] - 150, 110),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, gpio_color, 1)
            
            # Display frame
            cv2.imshow("Driver Drowsiness Detection - Raspberry Pi", frame)
            
            # Press 'q' to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                logger.info("System stopped by user")
                break
    
    except KeyboardInterrupt:
        logger.info("System interrupted by user")
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        errors = [str(e)]
    
    finally:
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        
        # Stop all GPIO signals
        if pwm_controller:
            pwm_controller.stop_alert()
            pwm_controller.cleanup()
        if led_controller:
            led_controller.off()
            led_controller.cleanup()
        
        drowsiness_detector.cleanup()
        
        # Log final statistics
        metrics = drowsiness_detector.get_drowsiness_metrics()
        logger.info(f"Final Statistics - Total Events: {metrics['total_events']}, "
                   f"Average EAR: {metrics['avg_ear']:.2f}, "
                   f"Closed Percentage: {metrics['closed_percentage']:.1f}%")
        logger.info("=== Driver Drowsiness Detection System Stopped ===")

if __name__ == "__main__":
    main()
