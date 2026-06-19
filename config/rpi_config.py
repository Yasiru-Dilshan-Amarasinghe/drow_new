# Raspberry Pi Configuration for Driver Drowsiness Detection System

# GPIO Configuration
GPIO_ENABLED = True  # Enable GPIO control on Raspberry Pi
PWM_PIN = 17  # GPIO pin for PWM buzzer (BCM numbering)
LED_PIN = 27  # GPIO pin for status LED (BCM numbering)

# PWM Configuration
PWM_FREQUENCY = 1000  # PWM frequency in Hz (1000 Hz = 1kHz for buzzer)
PWM_DUTY_CYCLE = 75  # Default duty cycle (0-100)
PWM_ALERT_DURATION = 0.5  # Duration of each pulse in seconds

# Eye Detection Settings
EYE_AR_THRESH = 0.3  # Threshold below which eyes are considered closed
EYE_AR_CONSEC_FRAMES = 30  # Consecutive frames for drowsiness detection

# Camera Configuration
CAMERA_INDEX = 0  # Webcam/CSI camera index
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 30

# Alert Settings
USE_BUZZER = True  # Enable/disable buzzer PWM output
USE_LED = True  # Enable/disable LED indicator
ENABLE_AUDIO_ALARM = False  # Disable system audio alarm (use hardware buzzer instead)

# Logging
LOG_FILE = "drowsiness_detection.log"
ENABLE_LOGGING = True

# Performance
DISPLAY_FPS = True
SKIP_FRAMES = 1  # Process every nth frame (lower = faster, higher = faster processing)
