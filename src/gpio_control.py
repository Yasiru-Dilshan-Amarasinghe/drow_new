"""
Raspberry Pi GPIO and PWM Control Module
Handles PWM signals for alerting when drowsiness is detected
"""

try:
    import RPi.GPIO as GPIO
    import time
    RASPBERRY_PI = True
except ImportError:
    RASPBERRY_PI = False
    print("Warning: RPi.GPIO not available. Running in simulation mode.")

class PWMController:
    """
    Control PWM signals on Raspberry Pi GPIO pins.
    Used for triggering alerts (buzzer, LED, etc.) when drowsiness is detected.
    """
    
    def __init__(self, gpio_pin=17, frequency=1000, enable_pi=True):
        """
        Initialize PWM controller.
        
        Args:
            gpio_pin: GPIO pin number for PWM output (default: 17)
            frequency: PWM frequency in Hz (default: 1000)
            enable_pi: Enable Raspberry Pi GPIO (set False for testing)
        """
        self.gpio_pin = gpio_pin
        self.frequency = frequency
        self.pwm = None
        self.is_running = False
        self.enable_pi = enable_pi and RASPBERRY_PI
        
        if self.enable_pi:
            self._init_gpio()
    
    def _init_gpio(self):
        """Initialize GPIO and PWM."""
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(self.gpio_pin, GPIO.OUT)
            self.pwm = GPIO.PWM(self.gpio_pin, self.frequency)
            print(f"✅ PWM initialized on GPIO pin {self.gpio_pin} at {self.frequency}Hz")
        except Exception as e:
            print(f"⚠️ Failed to initialize GPIO: {e}")
            self.enable_pi = False
    
    def start_alert(self, duty_cycle=50):
        """
        Start PWM alert signal (for buzzer/LED).
        
        Args:
            duty_cycle: PWM duty cycle 0-100 (default: 50%)
        """
        if not self.enable_pi or self.pwm is None:
            print(f"🔔 [SIMULATION] PWM Alert - Duty Cycle: {duty_cycle}%")
            return
        
        try:
            if not self.is_running:
                self.pwm.start(duty_cycle)
                self.is_running = True
                print(f"🚨 PWM Alert Started - Duty Cycle: {duty_cycle}%")
        except Exception as e:
            print(f"⚠️ Error starting PWM: {e}")
    
    def stop_alert(self):
        """Stop PWM alert signal."""
        if not self.enable_pi or self.pwm is None:
            print("🔔 [SIMULATION] PWM Alert - Stopped")
            return
        
        try:
            if self.is_running:
                self.pwm.stop()
                self.is_running = False
                print("✅ PWM Alert Stopped")
        except Exception as e:
            print(f"⚠️ Error stopping PWM: {e}")
    
    def set_duty_cycle(self, duty_cycle):
        """
        Change PWM duty cycle (0-100).
        
        Args:
            duty_cycle: Duty cycle percentage (0-100)
        """
        if duty_cycle < 0 or duty_cycle > 100:
            print("⚠️ Duty cycle must be between 0 and 100")
            return
        
        if not self.enable_pi or self.pwm is None:
            print(f"🔔 [SIMULATION] PWM Duty Cycle Set: {duty_cycle}%")
            return
        
        try:
            if self.is_running:
                self.pwm.ChangeDutyCycle(duty_cycle)
                print(f"⚙️ PWM Duty Cycle Changed: {duty_cycle}%")
        except Exception as e:
            print(f"⚠️ Error changing duty cycle: {e}")
    
    def pulse_alert(self, duration=0.5, pulses=3):
        """
        Send pulsing PWM alert signal.
        
        Args:
            duration: Duration of each pulse in seconds
            pulses: Number of pulses
        """
        for i in range(pulses):
            self.start_alert(75)
            time.sleep(duration)
            self.stop_alert()
            if i < pulses - 1:
                time.sleep(0.2)
        print(f"✅ Sent {pulses} pulse alerts")
    
    def cleanup(self):
        """Clean up GPIO resources."""
        if self.enable_pi:
            try:
                if self.pwm is not None and self.is_running:
                    self.pwm.stop()
                GPIO.cleanup(self.gpio_pin)
                print("✅ GPIO cleaned up")
            except Exception as e:
                print(f"⚠️ Error during cleanup: {e}")

class LEDController:
    """
    Control LED on Raspberry Pi GPIO pin.
    Used for visual alert when drowsiness is detected.
    """
    
    def __init__(self, gpio_pin=27, enable_pi=True):
        """
        Initialize LED controller.
        
        Args:
            gpio_pin: GPIO pin number for LED (default: 27)
            enable_pi: Enable Raspberry Pi GPIO
        """
        self.gpio_pin = gpio_pin
        self.is_on = False
        self.enable_pi = enable_pi and RASPBERRY_PI
        
        if self.enable_pi:
            self._init_gpio()
    
    def _init_gpio(self):
        """Initialize GPIO for LED."""
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(self.gpio_pin, GPIO.OUT)
            GPIO.output(self.gpio_pin, GPIO.LOW)
            print(f"✅ LED initialized on GPIO pin {self.gpio_pin}")
        except Exception as e:
            print(f"⚠️ Failed to initialize LED: {e}")
            self.enable_pi = False
    
    def on(self):
        """Turn LED on."""
        if not self.enable_pi:
            print("💡 [SIMULATION] LED - ON")
            return
        
        try:
            GPIO.output(self.gpio_pin, GPIO.HIGH)
            self.is_on = True
            print("💡 LED turned ON")
        except Exception as e:
            print(f"⚠️ Error turning LED on: {e}")
    
    def off(self):
        """Turn LED off."""
        if not self.enable_pi:
            print("💡 [SIMULATION] LED - OFF")
            return
        
        try:
            GPIO.output(self.gpio_pin, GPIO.LOW)
            self.is_on = False
            print("💡 LED turned OFF")
        except Exception as e:
            print(f"⚠️ Error turning LED off: {e}")
    
    def blink(self, count=3, interval=0.5):
        """
        Blink LED.
        
        Args:
            count: Number of blinks
            interval: On/off duration in seconds
        """
        for _ in range(count):
            self.on()
            time.sleep(interval)
            self.off()
            time.sleep(interval)
        print(f"✅ LED blinked {count} times")
    
    def cleanup(self):
        """Clean up GPIO resources."""
        if self.enable_pi:
            try:
                self.off()
                GPIO.cleanup(self.gpio_pin)
                print("✅ LED GPIO cleaned up")
            except Exception as e:
                print(f"⚠️ Error during cleanup: {e}")
