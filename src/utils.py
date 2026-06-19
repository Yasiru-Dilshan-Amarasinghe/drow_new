import cv2
import logging
from datetime import datetime

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
