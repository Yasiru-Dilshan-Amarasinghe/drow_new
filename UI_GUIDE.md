# Professional PyQt6 UI Guide

## Driver Drowsiness Detection - Industry-Level Interface

This document provides a comprehensive guide to the professional PyQt6-based graphical user interface for the Driver Drowsiness Detection System.

## Features

### 🎨 Professional Interface
- **Modern Dark Theme**: Industry-standard styling with dark background
- **Responsive Design**: Adaptable layout that works on various screen sizes
- **Real-time Video Display**: Live camera feed with detection overlays
- **Intuitive Controls**: Easy-to-use buttons and settings panels

### 📊 Multiple Tabs
1. **Controls Tab**: Start/Stop detection, view status and key metrics
2. **Settings Tab**: Configure camera, detection thresholds, and alert preferences
3. **Statistics Tab**: View session statistics and drowsiness level progress
4. **System Info Tab**: Application information and current status

### 📈 Real-time Metrics
- **Eye Aspect Ratio (EAR)**: Current eye closure metric
- **FPS Counter**: Live frames per second display
- **Event Tracking**: Total drowsiness events count
- **Drowsiness Level**: Visual progress bar (0-100%)
- **Session Duration**: Time since start
- **Statistics**: Average EAR, eyes closed percentage

### 🔧 Configurable Settings
- **EAR Threshold**: Adjust sensitivity (0.1 - 1.0)
- **Consecutive Frames**: Set detection threshold (5 - 100 frames)
- **Alert Options**: Toggle audio and visual alerts
- **Camera Selection**: Choose camera source

## Installation

### Prerequisites
- Python 3.8+
- Virtual environment activated

### Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- PyQt6 (6.6.1) - GUI framework
- PyQt6-Charts (6.6.0) - Charting capabilities
- OpenCV, NumPy, and other core dependencies

## Running the UI Application

### Basic Usage
```bash
python ui_main.py
```

### Full Installation and Run
```bash
# Create virtual environment (if not exists)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the UI application
python ui_main.py
```

## Interface Overview

### Main Window (1400 × 900 pixels)

```
┌─────────────────────────────────────────────────────────┐
│   Professional Driver Drowsiness Detection System       │
├──────────────────────────────┬──────────────────────────┤
│                              │ ┌─ Controls ─────────────┤
│                              │ │ ▶ START   ⏹ STOP     │
│     Live Video Feed          │ │ Status: ● RUNNING    │
│     (640×480)                │ │ FPS: 28.5             │
│                              │ │ Alert: ✓ No Drowsiness│
│                              │ │ EAR: 0.45             │
│                              │ │ Events: 2             │
│                              │ │ Time: 15:30:45        │
│                              │ │ [Settings] [Stats]    │
│                              │ │ [System Info]         │
└──────────────────────────────┴──────────────────────────┘
│ Status: Ready                                            │
└─────────────────────────────────────────────────────────┘
```

## Tab Details

### 1. Controls Tab
- **START Button**: Begin drowsiness detection
- **STOP Button**: End detection session
- **Status Indicator**: Shows RUNNING (green) or STOPPED (red)
- **FPS Display**: Real-time frame rate
- **Alert Status**: Visual indicator of drowsiness state
- **Key Metrics**: EAR, event count, current time

### 2. Settings Tab
- **Camera Settings**: Select camera source
- **EAR Threshold**: Fine-tune detection sensitivity
- **Consecutive Frames**: Set alarm trigger threshold
- **Audio Alert**: Enable/disable audio alerts
- **Visual Alert**: Enable/disable visual alerts

### 3. Statistics Tab
- **Total Events**: Count of drowsiness detections
- **Average EAR**: Mean eye aspect ratio
- **Eyes Closed %**: Percentage of frames with closed eyes
- **Session Duration**: Total detection time
- **Drowsiness Level**: Progress bar (visual drowsiness indicator)

### 4. System Info Tab
- **Application**: Name and version
- **Status**: Current system status
- **Last Update**: Timestamp of last event
- **About Section**: Description and technology stack

## Color Scheme

### Professional Theme Colors
- **Primary Background**: Light Gray (#ecf0f1)
- **Text Color**: Dark Blue (#2c3e50)
- **Border Color**: Light Gray (#bdc3c7)
- **Active Tab**: Blue (#3498db)
- **Success/OK**: Green (#27ae60)
- **Alert/Error**: Red (#e74c3c)
- **Video Background**: Black

## Key UI Components

### Buttons
- **START Button** (Green): Click to begin detection
- **STOP Button** (Red): Click to end detection
- Color changes on hover for visual feedback
- Disabled state when not applicable

### Status Indicators
- **Dot Indicator** (● Green/Red): Shows running/stopped status
- **Alert Status**: Changes color based on drowsiness detection
- **Progress Bar**: Visual drowsiness level (0-100%)

### Real-time Updates
- **FPS Display**: Updates every frame
- **EAR Value**: Real-time eye closure metric
- **Time Labels**: Current time and timestamp
- **Statistics**: Update every 500ms

## Threading Model

The application uses a separate thread for video capture to prevent UI freezing:

```
Main UI Thread (Qt Event Loop)
└── VideoCapture Thread
    ├── Captures frames
    ├── Emits signals
    └── Updates UI safely
```

Benefits:
- **Responsive UI**: No freezing during video processing
- **Smooth Display**: 60+ FPS possible
- **Real-time Updates**: Instant metric changes

## Configuration Options

### In-Application Settings

#### EAR Threshold
- **Range**: 0.1 - 1.0
- **Default**: 0.3
- **Lower Value**: More sensitive to drowsiness
- **Higher Value**: Less sensitive, fewer false alarms

#### Consecutive Frames
- **Range**: 5 - 100
- **Default**: 30 (approximately 1 second at 30 FPS)
- **Lower Value**: Faster alert response
- **Higher Value**: Ignores brief eye closures

### Code Configuration

Edit `ui_main.py` for advanced settings:

```python
# Default values
EYE_AR_THRESH = 0.3                # Eye aspect ratio threshold
EYE_AR_CONSEC_FRAMES = 30          # Consecutive frames for drowsiness
FRAME_WIDTH = 640                  # Video frame width
FRAME_HEIGHT = 480                 # Video frame height
```

## Advanced Features

### Statistics Tracking
- Maintains history of EAR values
- Calculates session-wide averages
- Tracks drowsiness events chronologically
- Displays percentage of frames with closed eyes

### Error Handling
- Graceful camera failure handling
- Error messages in status bar
- Automatic stop on critical errors
- Detailed logging to file

### Professional Styling
- Consistent font sizes and weights
- Color-coded status indicators
- Hover effects on buttons
- Smooth transitions and animations

## Troubleshooting

### UI Won't Start
```
Error: "No module named PyQt6"
Solution: pip install PyQt6 PyQt6-Charts
```

### Video Not Displaying
```
Error: Camera shows black
Solution: Check camera permissions and camera index in settings
```

### Performance Issues
```
Solution: 
- Close other applications
- Reduce screen resolution
- Disable unnecessary visual elements
```

## Requirements

### System Requirements
- **OS**: Windows 10+, Linux, macOS
- **Python**: 3.8+
- **RAM**: 2GB+ (4GB recommended)
- **Processor**: Dual-core or better
- **Camera**: USB webcam or built-in camera

### Library Versions
```
PyQt6==6.6.1
PyQt6-Charts==6.6.0
opencv-python==4.8.1.78
numpy==1.24.3
scipy==1.11.1
Pillow==10.0.0
```

## Development & Customization

### Adding Custom Widgets
```python
# In create_controls_tab() or similar:
custom_widget = QCustomWidget()
layout.addWidget(custom_widget)
```

### Modifying Colors
Edit the `apply_theme()` method:
```python
def apply_theme(self):
    theme = """
    QMainWindow { background-color: #your_color; }
    ...
    """
    self.setStyleSheet(theme)
```

### Adding New Tabs
```python
def create_custom_tab(self):
    widget = QWidget()
    layout = QVBoxLayout()
    # Add widgets here
    widget.setLayout(layout)
    return widget

# In setup_ui():
tabs.addTab(self.create_custom_tab(), "Custom Tab")
```

## Performance Optimization

### Frame Processing
- Video capture runs in separate thread
- UI updates at 500ms intervals (not every frame)
- Efficient OpenCV operations

### Memory Management
- Automatic cleanup on close
- Thread-safe frame handling
- Proper resource deallocation

## License

This professional UI is part of the Driver Drowsiness Detection System project.

## Support

For issues, feature requests, or customization help:
1. Check the RPI_SETUP.md for Raspberry Pi setup
2. Review the main README.md
3. Check log files in drowsiness_detection.log

---

**Version**: 1.0  
**Last Updated**: 2026-06-20
