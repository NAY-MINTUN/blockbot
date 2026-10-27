from machine import I2C, Pin
from pca9685 import PCA9685

SDA_PIN = 21
SCL_PIN = 22
SERVO_HZ = 50
MIN_PULSE = 110
MAX_PULSE = 500

# Local joystick limits used until the browser supplies configured limits.

DEFAULT_LIMITS = [
    {'min': 0, 'max': 180},
    {'min': 40, 'max': 125},
    {'min': 30, 'max': 130},
    {'min': 90, 'max': 150},
]

class Arm:
    def __init__(self):
        i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=400000)
        self.driver = PCA9685(i2c)
        self.driver.freq(SERVO_HZ)
        self.limits = None
        self.angles = [None, None, None, None]
        self.configure_limits(DEFAULT_LIMITS)

    def configure_limits(self, limits):
        if not isinstance(limits, list) or len(limits) != 4:
            raise ValueError('four joint ranges are required')
        checked = []
        for item in limits:
            low, high = item.get('min'), item.get('max')
            if (isinstance(low, bool) or isinstance(high, bool)
                    or not isinstance(low, (int, float)) or not isinstance(high, (int, float))
                    or low != low or high != high
                    or low < 0 or high > 180 or low >= high):
                raise ValueError('joint ranges must be valid degrees from 0 to 180')
            checked.append((low, high))
        self.limits = checked
        for channel, (low, high) in enumerate(checked):
            self.move(channel, (low + high) / 2)

    def move(self, channel, angle):
        if self.limits is None:
            raise ValueError('configure user joint limits before moving')
        if not isinstance(channel, int) or channel < 0 or channel >= len(self.limits):
            raise ValueError('unknown joint')
        lo, hi = self.limits[channel]
        angle = max(lo, min(hi, angle))
        pulse = MIN_PULSE + int((MAX_PULSE - MIN_PULSE) * angle / 180)
        self.driver.channel(channel, pulse)
        self.angles[channel] = angle
        return angle

    def angle(self, channel):
        return self.angles[channel]

    def positions(self):
        return self.angles[:]
