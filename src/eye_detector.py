import cv2
import numpy as np
from scipy.spatial import distance as dist

class EyeDetector:
    """
    Detect and track eyes in video frames using cascade classifiers.
    """
    
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_eye.xml"
        )
        
    def detect_faces(self, frame):
        """
        Detect faces in the frame.
        
        Args:
            frame: Input frame
            
        Returns:
            List of detected faces (x, y, w, h)
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30)
        )
        return faces
    
    def detect_eyes(self, frame, face):
        """
        Detect eyes within a face region.
        
        Args:
            frame: Input frame
            face: Face region (x, y, w, h)
            
        Returns:
            List of detected eyes (x, y, w, h)
        """
        x, y, w, h = face
        roi_gray = cv2.cvtColor(frame[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)
        
        eyes = self.eye_cascade.detectMultiScale(
            roi_gray, scaleFactor=1.1, minNeighbors=10, minSize=(15, 15)
        )
        
        # Adjust coordinates to original frame
        eyes_adjusted = [(x + ex, y + ey, ew, eh) for ex, ey, ew, eh in eyes]
        return eyes_adjusted

def calculate_eye_aspect_ratio(eye_landmarks):
    """
    Calculate Eye Aspect Ratio (EAR) from eye landmarks.
    EAR = ||p2 - p6|| + ||p3 - p5|| / 2 * ||p1 - p4||
    
    Args:
        eye_landmarks: Array of eye landmark points (typically 6 points)
        
    Returns:
        Eye aspect ratio
    """
    if len(eye_landmarks) < 6:
        return 0
    
    # Compute distances between eye landmarks
    A = dist.euclidean(eye_landmarks[1], eye_landmarks[5])
    B = dist.euclidean(eye_landmarks[2], eye_landmarks[4])
    C = dist.euclidean(eye_landmarks[0], eye_landmarks[3])
    
    # Compute EAR
    ear = (A + B) / (2.0 * C)
    return ear

def get_eye_center(eye_region):
    """
    Calculate the center of the eye region.
    
    Args:
        eye_region: (x, y, w, h) of eye
        
    Returns:
        (center_x, center_y)
    """
    x, y, w, h = eye_region
    center_x = x + w // 2
    center_y = y + h // 2
    return (center_x, center_y)
