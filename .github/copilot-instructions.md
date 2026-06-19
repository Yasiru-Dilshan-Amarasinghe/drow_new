# Driver Drowsiness Detection System - Copilot Instructions

This is a real-time driver drowsiness detection project using Python and OpenCV.

## Project Overview

**Type**: Python OpenCV Computer Vision Application
**Purpose**: Real-time detection of driver drowsiness through eye closure monitoring
**Key Technologies**: OpenCV, Python, NumPy, Haar Cascade Classifiers

## Project Components

- **main.py**: Entry point for the application
- **src/eye_detector.py**: Face and eye detection module
- **src/drowsiness_detector.py**: Core drowsiness detection logic with alarm system
- **src/utils.py**: Visualization and logging utilities
- **config/config.py**: Configuration settings
- **requirements.txt**: Python dependencies

## Key Features

- Real-time face and eye detection
- Eye aspect ratio (EAR) calculation
- Drowsiness event detection and logging
- Audio alerts on drowsiness detection
- Performance metrics display
- Comprehensive event logging

## Running the Project

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

Press 'q' to exit the application.

## Project Status

✅ Project structure created
✅ Core modules implemented
✅ Dependencies configured
✅ Documentation complete
✅ Ready to run

## Next Steps

1. Run `pip install -r requirements.txt` to install dependencies
2. Execute `python main.py` to start the drowsiness detection system
3. Ensure webcam is accessible and properly positioned
4. Monitor console output and log file for events

## Customization

Modify `config/config.py` to adjust:
- Eye closure detection sensitivity
- Alarm settings
- Camera parameters
- Logging options

---
*Project initialized: 2026-06-19*
