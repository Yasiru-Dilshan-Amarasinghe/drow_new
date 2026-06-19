# Driver Drowsiness Detection System

A real-time driver drowsiness detection system using Python and OpenCV. This project detects driver fatigue by monitoring eye closure patterns and alerts the driver when drowsiness is detected.

## Features

- **Real-time Face Detection**: Detects driver's face using Haar Cascade classifiers
- **Eye Detection**: Identifies eyes in detected face regions
- **Drowsiness Monitoring**: Tracks eye closure duration to detect drowsiness
- **Audio Alerts**: Triggers alarm when drowsiness is detected
- **Performance Metrics**: Displays real-time statistics including:
  - Eye Aspect Ratio (EAR)
  - Drowsiness events count
  - Percentage of frame time with closed eyes
- **Logging**: Comprehensive logging of system events and alerts

## Project Structure

```
driver-drowsiness-detection/
├── main.py                    # Main application entry point
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── config/
│   └── config.py             # Configuration settings
├── src/
│   ├── eye_detector.py       # Eye and face detection module
│   ├── drowsiness_detector.py # Core drowsiness detection logic
│   └── utils.py              # Utility functions for visualization and logging
└── models/                    # Directory for trained models (if using dlib)
```

## Installation

### Prerequisites
- Python 3.7 or higher
- Webcam/camera device

### Setup

1. Clone or download the project
2. Navigate to project directory:
   ```bash
   cd driver-drowsiness-detection
   ```

3. Create virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Run the main application:
```bash
python main.py
```

The system will:
1. Start capturing video from your webcam
2. Detect face and eyes in real-time
3. Calculate eye aspect ratio
4. Alert when drowsiness is detected
5. Display statistics on screen

### Controls

- **Press 'q'** to exit the application
- **Close window** to stop the system

### Output

The system generates:
- **Real-time video display** with face/eye detection overlays
- **Console alerts** when drowsiness is detected
- **Audio alerts** (beep) when drowsiness threshold is exceeded
- **Log file** (`drowsiness_detection.log`) with all events and statistics

## Configuration

Edit `config/config.py` to customize:

- `EYE_AR_THRESH`: Eye aspect ratio threshold for closed eyes (default: 0.3)
- `EYE_AR_CONSEC_FRAMES`: Consecutive frames for drowsiness detection (default: 30)
- `ALARM_SOUND`: Enable/disable alarm (default: True)
- `CAMERA_INDEX`: Webcam index (default: 0)
- `FRAME_WIDTH/HEIGHT`: Video frame dimensions
- `ENABLE_LOGGING`: Enable/disable logging

## How It Works

1. **Face Detection**: Uses Haar Cascade classifier to detect face regions
2. **Eye Detection**: Identifies eyes within detected face regions
3. **Eye Aspect Ratio (EAR)**: Calculates ratio based on eye position
4. **Drowsiness Detection**: 
   - If EAR < threshold for consecutive frames → drowsiness detected
   - Triggers alarm and logs event
5. **Metrics Tracking**: Maintains statistics of drowsiness events

## Dependencies

- **opencv-python**: Computer vision library for image processing
- **numpy**: Numerical computing library
- **scipy**: Scientific computing library
- **imutils**: Image processing utilities
- **dlib**: Optional, for advanced facial landmark detection
- **Pillow**: Image processing

## Requirements

- Minimum CPU: Intel Core i5 or equivalent
- RAM: 4GB or more
- Stable lighting for optimal face detection
- Working webcam

## Limitations

- Works best in well-lit environments
- Accuracy depends on camera quality and lighting
- May have false positives with glasses or different lighting conditions
- Uses Haar Cascade (consider dlib for production use)

## Future Enhancements

- Integration with vehicle telemetry systems
- Machine learning models for better accuracy
- Multi-face detection for passenger monitoring
- Integration with vehicle safety systems
- Mobile app version
- Cloud-based analytics

## Troubleshooting

### Camera not detected
- Ensure webcam is connected and working
- Check `CAMERA_INDEX` in config (try 0, 1, 2, etc.)
- Grant camera permissions if prompted

### Face not detected
- Ensure good lighting
- Position face directly toward camera
- Remove obstructions

### No alarm sound
- Check system volume settings
- Verify `ALARM_SOUND` is enabled in config
- Check audio device is working

## License

This project is provided as-is for educational and research purposes.

## Contact & Support

For issues or questions, please refer to the code documentation and inline comments.

---

**Safety Notice**: This system is a demonstration project. For production use in vehicles, integrate with appropriate vehicle safety systems and follow all regulatory requirements.
