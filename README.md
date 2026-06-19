# Driver Drowsiness Detection System

A real-time driver drowsiness detection system using Python and OpenCV. This project detects driver fatigue by monitoring eye closure patterns and alerts the driver when drowsiness is detected.

**Now with Raspberry Pi 4 support and PWM signal output!** 🚀

## Features

- **Real-time Face Detection**: Detects driver's face using Haar Cascade classifiers
- **Eye Detection**: Identifies eyes in detected face regions
- **Drowsiness Monitoring**: Tracks eye closure duration to detect drowsiness
- **Audio & Hardware Alerts**: 
  - System audio alerts (beep)
  - PWM signal output for hardware buzzers (Raspberry Pi)
  - LED indicator control (Raspberry Pi)
- **Performance Metrics**: Displays real-time statistics including:
  - Eye Aspect Ratio (EAR)
  - Drowsiness events count
  - Percentage of frame time with closed eyes
- **Logging**: Comprehensive logging of system events and alerts

## Project Structure

```
driver-drowsiness-detection/
├── main.py                    # Main application (Desktop)
├── main_rpi.py                # Raspberry Pi version with PWM control
├── requirements.txt           # Desktop dependencies
├── requirements-rpi.txt       # Raspberry Pi dependencies
├── RPI_SETUP.md              # Raspberry Pi hardware setup guide
├── README.md                  # This file
├── config/
│   ├── config.py             # Desktop configuration
│   └── rpi_config.py         # Raspberry Pi configuration
├── src/
│   ├── eye_detector.py       # Eye and face detection module
│   ├── drowsiness_detector.py # Core drowsiness detection logic
│   ├── gpio_control.py       # Raspberry Pi GPIO & PWM control
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

### Desktop Mode

Run the application on your computer:
```bash
python main.py
```

### Raspberry Pi Mode (with PWM & GPIO)

Run the application with hardware GPIO and PWM control:
```bash
python main_rpi.py
```

**Note**: For detailed Raspberry Pi setup with hardware wiring and configuration, see [RPI_SETUP.md](RPI_SETUP.md)

## Quick Start

### Desktop

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Raspberry Pi

```bash
# Install dependencies for Raspberry Pi
pip install -r requirements-rpi.txt

# Run with PWM support
python main_rpi.py
```

## Configuration

Edit `config/config.py` (Desktop) or `config/rpi_config.py` (Raspberry Pi) to customize:

- `EYE_AR_THRESH`: Eye aspect ratio threshold for closed eyes (default: 0.3)
- `EYE_AR_CONSEC_FRAMES`: Consecutive frames for drowsiness detection (default: 30)
- `ALARM_SOUND`: Enable/disable alarm (default: True)
- `CAMERA_INDEX`: Webcam index (default: 0)
- `FRAME_WIDTH/HEIGHT`: Video frame dimensions

### Raspberry Pi PWM Configuration

Additional settings in `config/rpi_config.py`:

```python
PWM_PIN = 17              # GPIO pin for buzzer PWM output
LED_PIN = 27              # GPIO pin for LED indicator
PWM_FREQUENCY = 1000      # 1kHz for typical buzzer
PWM_DUTY_CYCLE = 75       # 0-100% duty cycle
USE_BUZZER = True         # Enable PWM buzzer
USE_LED = True            # Enable LED indicator
```

## PWM Signal Features (Raspberry Pi)

When running on Raspberry Pi, the system outputs:

- **PWM Signal** on GPIO pin 17:
  - Frequency: 1000 Hz (1 kHz)
  - Duty Cycle: 75% (adjustable)
  - Triggers on drowsiness detection
  - Auto-stops when eyes open

- **LED Indicator** on GPIO pin 27:
  - ON: When drowsiness is detected
  - OFF: When alert state clears

### Example Hardware Connections

**Buzzer Alert**: GPIO 17 → PWM buzzer → GND
**LED Status**: GPIO 27 → 220Ω resistor → LED → GND

See [RPI_SETUP.md](RPI_SETUP.md) for complete wiring diagrams and hardware setup instructions.

## How It Works

1. **Face Detection**: Uses Haar Cascade classifier to detect face regions
2. **Eye Detection**: Identifies eyes within detected face regions
3. **Eye Aspect Ratio (EAR)**: Calculates ratio based on eye position
4. **Drowsiness Detection**: 
   - If EAR < threshold for consecutive frames → drowsiness detected
   - Triggers alarm and logs event
5. **Metrics Tracking**: Maintains statistics of drowsiness events
6. **Raspberry Pi Integration** (main_rpi.py):
   - PWM signal output on GPIO pin 17 (buzzer control)
   - LED control on GPIO pin 27 (visual indicator)
   - Automatic GPIO cleanup on shutdown

## GPIO and PWM Control (Raspberry Pi)

### PWMController Class

Manages PWM output for hardware buzzers and alerts:

```python
from src.gpio_control import PWMController

pwm = PWMController(gpio_pin=17, frequency=1000)
pwm.start_alert(duty_cycle=75)      # Start alert with 75% duty
pwm.set_duty_cycle(100)              # Change duty cycle
pwm.pulse_alert(duration=0.5, pulses=3)  # Send 3 pulses
pwm.stop_alert()                    # Stop alert
pwm.cleanup()                       # Clean up GPIO
```

### LEDController Class

Manages LED output for visual indicators:

```python
from src.gpio_control import LEDController

led = LEDController(gpio_pin=27)
led.on()                           # Turn LED on
led.off()                          # Turn LED off
led.blink(count=3, interval=0.5)  # Blink 3 times
led.cleanup()                      # Clean up GPIO
```

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

### No alarm sound (Desktop)
- Check system volume settings
- Verify `ALARM_SOUND` is enabled in config
- Check audio device is working

### PWM not working (Raspberry Pi)
- Check GPIO pin connections and wiring
- Verify `GPIO_ENABLED = True` in main_rpi.py
- Ensure GPIO permissions are set correctly
- Test GPIO pin manually: `python test_gpio.py`

### Slow detection on Raspberry Pi
- Reduce frame resolution in config
- Increase `SKIP_FRAMES` value
- Close unnecessary applications
- Consider lower resolution camera input

## License

This project is provided as-is for educational and research purposes.

## Contact & Support

For issues or questions, please refer to the code documentation and inline comments.

---

**Safety Notice**: This system is a demonstration project. For production use in vehicles, integrate with appropriate vehicle safety systems and follow all regulatory requirements.
