# Raspberry Pi 4 Driver Drowsiness Detection System

Complete setup and hardware integration guide for running the drowsiness detection system on Raspberry Pi 4 with PWM signal output.

## Hardware Requirements

### Components Needed
- **Raspberry Pi 4** (4GB or 8GB RAM recommended)
- **Raspberry Pi Camera Module v2** or **USB Webcam**
- **Active Buzzer Module** (5V, 3-pin) OR Passive Buzzer with transistor
- **LED** (5mm, any color) + **220Ω Resistor**
- **Jumper wires** and **Breadboard** (optional but recommended)
- **Power supply** (5V, 3A USB-C)
- **MicroSD card** (32GB+ recommended) with Raspberry Pi OS installed

### Wiring Diagram

```
Raspberry Pi GPIO Pins (BCM numbering):

GPIO 17 (Pin 11) ──── PWM Output ──── Buzzer+/Active Buzzer Signal
GPIO 27 (Pin 13) ──── LED+ ──── 220Ω Resistor ──── LED ──── Ground
GND (Pin 6, 9, 14, 20, 25, 30, 34, 39) ──── Common Ground

Pin Layout Reference:
    3.3V  [1] [2]  5V
SDA [3] [4]  5V
SCL [5] [6]  GND
     [7] [8]  UART TX
     [9] [10] UART RX
GPIO 17 [11] [12] GPIO 18
GPIO 27 [13] [14] GND
GPIO 22 [15] [16] GPIO 23
    3.3V [17] [18] GPIO 24
MOSI [19] [20] GND
MISO [21] [22] GPIO 25
SCLK [23] [24] CE0
     [25] [26] CE1
```

### Active Buzzer Wiring
```
Active Buzzer (recommended for simplicity):
- Red/+ wire → GPIO 17 (PWM Pin)
- Black/- wire → GND
- Connect via 1kΩ resistor for protection
```

### Passive Buzzer Wiring (with transistor)
```
For better control with passive buzzer:
GPIO 17 → 1kΩ Resistor → Base (B) of 2N2222 Transistor
Collector (C) → Passive Buzzer+
Emitter (E) → GND
Buzzer- → 5V (through current limiting resistor)
```

### LED Wiring
```
GPIO 27 → 220Ω Resistor → LED Anode (+)
LED Cathode (-) → GND
```

## Software Setup

### 1. Raspberry Pi OS Installation

1. Download Raspberry Pi Imager from https://www.raspberrypi.com/software/
2. Install Raspberry Pi OS Lite (headless) or Desktop version
3. Enable camera and SSH in raspi-config:
   ```bash
   sudo raspi-config
   # Interface Options → Camera → Enable
   # Interface Options → SSH → Enable
   # Save and reboot
   ```

### 2. Install Python and Dependencies

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade

# Install Python and pip
sudo apt-get install python3 python3-pip python3-venv

# Install build tools (for RPi.GPIO compilation)
sudo apt-get install build-essential python3-dev

# Install OpenCV dependencies
sudo apt-get install libatlas-base-dev libjasper-dev libhdf5-dev libharfbuzz0b libwebp6
sudo apt-get install libharfbuzz0b libjasper-dev libqblas0 libqt4-test libqtcore4 libqtgui4
```

### 3. Clone and Setup Project

```bash
# Navigate to desired directory
cd ~

# Clone project from GitHub
git clone https://github.com/Yasiru-Dilshan-Amarasinghe/drow_new.git
cd drow_new

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies for Raspberry Pi
pip install -r requirements-rpi.txt
```

### 4. Configure GPIO

Give Python GPIO access without sudo:
```bash
# Add user to gpio group
sudo usermod -a -G gpio $USER

# Install libgpiod for better GPIO control
sudo apt-get install libgpiod2 python3-libgpiod
```

## Running the System

### Desktop Mode (for testing without Raspberry Pi)
```bash
python main.py
```

### Raspberry Pi Mode (with PWM/GPIO)
```bash
python main_rpi.py
```

## Configuration

Edit `config/rpi_config.py` to customize:

```python
# GPIO Pin Configuration
PWM_PIN = 17          # GPIO pin for buzzer (change if using different pin)
LED_PIN = 27          # GPIO pin for LED (change if using different pin)

# PWM Settings
PWM_FREQUENCY = 1000  # 1kHz for typical buzzer (adjust for your buzzer)
PWM_DUTY_CYCLE = 75   # 75% duty cycle (0-100)

# Drowsiness Detection
EYE_AR_THRESH = 0.3           # Sensitivity (lower = more sensitive)
EYE_AR_CONSEC_FRAMES = 30     # Frames before alerting (adjust for frame rate)

# Features
USE_BUZZER = True             # Enable PWM buzzer output
USE_LED = True                # Enable LED indicator
ENABLE_AUDIO_ALARM = False    # Disable system alarm (use hardware instead)
```

## Testing GPIO and PWM

```bash
# Test PWM output
python3 << 'EOF'
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
pwm = GPIO.PWM(17, 1000)
pwm.start(75)
time.sleep(2)
pwm.stop()
GPIO.cleanup()
EOF

# Test LED output
python3 << 'EOF'
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.HIGH)
time.sleep(1)
GPIO.output(27, GPIO.LOW)
GPIO.cleanup()
EOF
```

## Troubleshooting

### Camera not detected
```bash
# Check camera
vcgencmd get_camera
# Should output: supported=1 detected=1

# Try different camera index (0, 1, 2, etc.)
# Edit main_rpi.py: CAMERA_INDEX = 0
```

### GPIO Permission Denied
```bash
# Add to sudoers (allows GPIO access without sudo)
sudo visudo
# Add line: %gpio ALL=(ALL) NOPASSWD: /usr/bin/python3
```

### PWM not working
```bash
# Check if GPIO 17 is available
cat /proc/device-tree/model
gpioinfo

# Try different PWM pin if available:
# GPIO 12 (Pin 32) - Hardware PWM
# GPIO 13 (Pin 33) - Hardware PWM
```

### Slow detection on Raspberry Pi
- Reduce frame resolution in config
- Increase SKIP_FRAMES value
- Disable LED/PWM if not needed
- Close other applications

## Advanced Usage

### Multiple Alerts

Edit `src/drowsiness_detector.py` to add multiple PWM outputs:

```python
# Multi-alert example
self.pwm_controller.pulse_alert(duration=0.3, pulses=3)
```

### Custom Alert Logic

Create custom alert combinations:

```python
# In main_rpi.py
if is_drowsy:
    pwm_controller.start_alert(duty_cycle=100)  # Full power buzzer
    led_controller.blink(count=5)                 # Blink LED 5 times
```

### Data Logging

The system logs all events to `drowsiness_detection.log`:

```bash
# View real-time logs
tail -f drowsiness_detection.log

# Count drowsiness events
grep "DROWSINESS_ALERT" drowsiness_detection.log | wc -l
```

## Performance Optimization

For optimal performance on Raspberry Pi 4:

1. **Reduce frame processing**
   ```python
   SKIP_FRAMES = 2  # Process every 2nd frame
   FRAME_WIDTH = 480
   FRAME_HEIGHT = 360
   ```

2. **Use Lite Desktop or Headless**
   - Raspberry Pi OS Lite uses less memory
   - Disable unnecessary services: `sudo systemctl disable service_name`

3. **Overclock (optional, advanced)**
   ```bash
   sudo raspi-config
   # Overclocking → Modest overclocking
   ```

## Running as System Service

Create a systemd service to auto-start on boot:

```bash
# Create service file
sudo nano /etc/systemd/system/drowsiness-detection.service
```

Add content:
```ini
[Unit]
Description=Driver Drowsiness Detection System
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/drow_new
ExecStart=/home/pi/drow_new/venv/bin/python3 /home/pi/drow_new/main_rpi.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable drowsiness-detection.service
sudo systemctl start drowsiness-detection.service
sudo systemctl status drowsiness-detection.service
```

## Power Consumption

Typical power usage on Raspberry Pi 4:
- Idle: ~0.5A (2.5W)
- With Camera + Processing: ~1.2-1.5A (6-7.5W)
- With Buzzer Alert: ~1.8-2.0A (9-10W)

Recommended power supply: 5V 3A USB-C

## Safety Notes

⚠️ **Important**: 
- Always use appropriate current-limiting resistors
- Check GPIO voltage ratings (3.3V logic level)
- Do not connect 5V directly to GPIO pins
- Use proper heat dissipation if overclocking
- Test all connections before powering on camera

## License

This project is provided as-is for educational and research purposes.

---

**Last Updated**: 2026-06-19
