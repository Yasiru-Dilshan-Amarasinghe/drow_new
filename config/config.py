# Configuration settings for Driver Drowsiness Detection System

# Eye aspect ratio thresholds
EYE_AR_THRESH = 0.3  # Threshold below which eyes are considered closed
EYE_AR_CONSEC_FRAMES = 30  # Number of consecutive frames for drowsiness detection

# Alarm settings
ALARM_SOUND = True  # Enable/disable alarm sound
ALERT_THRESHOLD = 1  # Number of drowsiness instances before alerting

# Camera settings
CAMERA_INDEX = 0  # Webcam index (0 for default)
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 30

# Display settings
DISPLAY_LEVEL_INFO = True
SHOW_FACE_DETECTION = True
SHOW_EYE_DETECTION = True

# Model paths (cascade classifiers)
CASCADE_PATH_FACE = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
CASCADE_PATH_EYES = cv2.data.haarcascades + "haarcascade_eye.xml"

# Logging
LOG_FILE = "drowsiness_detection.log"
ENABLE_LOGGING = True
