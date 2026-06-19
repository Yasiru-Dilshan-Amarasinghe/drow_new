import cv2
import numpy as np
from collections import deque
from datetime import datetime

class DrowsinessDetector:
    """
    Main drowsiness detection module.
    Tracks eye closure duration and alerts when drowsiness is detected.
    """
    
    def __init__(self, eye_ar_thresh=0.3, eye_ar_consec_frames=30, alarm_enabled=True, pwm_controller=None):
        """
        Initialize the drowsiness detector.
        
        Args:
            eye_ar_thresh: Eye aspect ratio threshold for closed eyes
            eye_ar_consec_frames: Consecutive frames threshold for drowsiness
            alarm_enabled: Enable/disable alarm
            pwm_controller: Optional PWMController instance for GPIO control
        """
        self.EYE_AR_THRESH = eye_ar_thresh
        self.EYE_AR_CONSEC_FRAMES = eye_ar_consec_frames
        self.alarm_enabled = alarm_enabled
        self.pwm_controller = pwm_controller
        
        self.COUNTER = 0  # Consecutive frames with eyes closed
        self.ALARM_ON = False
        self.drowsiness_count = 0
        self.last_alert_time = None
        self.frame_history = deque(maxlen=100)
        
    def update(self, eye_aspect_ratio):
        """
        Update detector state based on current eye aspect ratio.
        
        Args:
            eye_aspect_ratio: Current EAR value
            
        Returns:
            tuple: (is_drowsy, counter, alarm_status)
        """
        self.frame_history.append({
            'timestamp': datetime.now(),
            'ear': eye_aspect_ratio,
            'closed': eye_aspect_ratio < self.EYE_AR_THRESH
        })
        
        # Update counter for consecutive frames with eyes closed
        if eye_aspect_ratio < self.EYE_AR_THRESH:
            self.COUNTER += 1
        else:
            self.COUNTER = 0
        
        # Check if drowsiness threshold is exceeded
        is_drowsy = False
        if self.COUNTER >= self.EYE_AR_CONSEC_FRAMES:
            is_drowsy = True
            self.ALARM_ON = True
            self.drowsiness_count += 1
            self.last_alert_time = datetime.now()
            
            # Trigger PWM signal if controller is available
            if self.pwm_controller and not self.pwm_controller.is_running:
                self.pwm_controller.start_alert(duty_cycle=75)
        else:
            self.ALARM_ON = False
            # Stop PWM signal if drowsiness no longer detected
            if self.pwm_controller and self.pwm_controller.is_running:
                self.pwm_controller.stop_alert()
        
        return is_drowsy, self.COUNTER, self.ALARM_ON
    
    def get_drowsiness_metrics(self):
        """
        Get drowsiness metrics from history.
        
        Returns:
            dict: Contains drowsiness statistics
        """
        if not self.frame_history:
            return {
                'total_events': 0,
                'avg_ear': 0,
                'closed_frames_count': 0,
                'closed_percentage': 0
            }
        
        ears = [frame['ear'] for frame in self.frame_history]
        closed_frames = sum(1 for frame in self.frame_history if frame['closed'])
        
        return {
            'total_events': self.drowsiness_count,
            'avg_ear': np.mean(ears),
            'closed_frames_count': closed_frames,
            'closed_percentage': (closed_frames / len(self.frame_history)) * 100
        }
    
    def reset(self):
        """Reset the detector state."""
        self.COUNTER = 0
        self.ALARM_ON = False
        self.drowsiness_count = 0
        self.last_alert_time = None
        self.frame_history.clear()
        
        # Stop PWM if running
        if self.pwm_controller and self.pwm_controller.is_running:
            self.pwm_controller.stop_alert()
    
    def cleanup(self):
        """Clean up resources."""
        if self.pwm_controller:
            self.pwm_controller.cleanup()

def trigger_alarm():
    """
    Trigger alarm when drowsiness is detected.
    Uses system beep on Windows, Linux, and macOS.
    """
    import sys
    if sys.platform == "win32":
        import winsound
        winsound.Beep(1000, 500)  # Frequency: 1000 Hz, Duration: 500 ms
    else:
        # For Linux/Mac
        import os
        os.system('afplay /System/Library/Sounds/Alarm.aiff' if sys.platform == 'darwin' 
                  else 'paplay /usr/share/sounds/freedesktop/stereo/alarm.oga')
