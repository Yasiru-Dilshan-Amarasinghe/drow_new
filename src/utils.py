import cv2
import logging
from datetime import datetime
import sys

def setup_logging(log_file="drowsiness_detection.log"):
    """
    Setup logging configuration.
    
    Args:
        log_file: Path to log file
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def display_datetime(frame, position=None):
    """
    Display current date and time on the frame.
    
    Args:
        frame: Input frame
        position: (x, y) position for text (default: bottom left)
        
    Returns:
        Frame with datetime overlay
    """
    if position is None:
        position = (10, frame.shape[0] - 20)
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, f"Time: {current_time}", position,
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    return frame

def display_error_status(frame, error_list, position=(10, 150)):
    """
    Display error and status information on the frame.
    
    Args:
        frame: Input frame
        error_list: List of error messages or status info
        position: (x, y) starting position for text
        
    Returns:
        Frame with error status overlay
    """
    y_offset = position[1]
    
    if error_list:
        # Display errors in red
        for error in error_list:
            cv2.putText(frame, f"ERROR: {error}", (position[0], y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            y_offset += 25
    else:
        # Display system status in green
        cv2.putText(frame, "STATUS: OK", (position[0], y_offset),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    return frame

def display_system_info(frame, fps=0, camera_status="OK", detection_status="OK"):
    """
    Display system information on frame.
    
    Args:
        frame: Input frame
        fps: Current frames per second
        camera_status: Camera status string
        detection_status: Detection status string
        
    Returns:
        Frame with system info overlay
    """
    # FPS counter (top right)
    cv2.putText(frame, f"FPS: {fps:.1f}", (frame.shape[1] - 150, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Camera status
    camera_color = (0, 255, 0) if camera_status == "OK" else (0, 0, 255)
    cv2.putText(frame, f"Camera: {camera_status}", (frame.shape[1] - 150, 60),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, camera_color, 1)
    
    # Detection status
    detection_color = (0, 255, 0) if detection_status == "OK" else (255, 165, 0)
    cv2.putText(frame, f"Detection: {detection_status}", (frame.shape[1] - 150, 85),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, detection_color, 1)
    
    return frame

def draw_detections(frame, faces, eyes, drowsy=False, ear=0):
    """
    Draw detection results on the frame.
    
    Args:
        frame: Input frame
        faces: List of detected faces
        eyes: List of detected eyes
        drowsy: Boolean indicating drowsiness state
        ear: Eye aspect ratio value
        
    Returns:
        Annotated frame
    """
    # Draw face rectangles
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, "Face", (x, y - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Draw eye rectangles
    for (x, y, w, h) in eyes:
        color = (0, 0, 255) if drowsy else (0, 255, 0)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
    
    # Display EAR value
    cv2.putText(frame, f"EAR: {ear:.2f}", (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Display drowsiness status
    if drowsy:
        cv2.putText(frame, "DROWSINESS DETECTED!", (10, 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]),
                     (0, 0, 255), 3)
    else:
        cv2.putText(frame, "ALERT", (10, 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    return frame

def display_stats(frame, detector):
    """
    Display drowsiness statistics on frame.
    
    Args:
        frame: Input frame
        detector: DrowsinessDetector instance
        
    Returns:
        Annotated frame
    """
    metrics = detector.get_drowsiness_metrics()
    
    y_offset = 120
    cv2.putText(frame, f"Events: {metrics['total_events']}", (10, y_offset),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    cv2.putText(frame, f"Avg EAR: {metrics['avg_ear']:.2f}", (10, y_offset + 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    cv2.putText(frame, f"Closed %: {metrics['closed_percentage']:.1f}%", (10, y_offset + 60),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    return frame

def get_timestamp():
    """
    Get current timestamp string.
    
    Returns:
        Formatted timestamp string
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_event(logger, event_type, data=None):
    """
    Log an event with optional data.
    
    Args:
        logger: Logger instance
        event_type: Type of event
        data: Additional event data
    """
    message = f"[{event_type}] {get_timestamp()}"
    if data:
        message += f" - {data}"
    logger.info(message)
