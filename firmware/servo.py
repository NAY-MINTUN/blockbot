from machine import I2C, Pin
from pca9685 import PCA9685

SDA_PIN = 21
SCL_PIN = 22
SERVO_HZ = 50
MIN_PULSE = 110
MAX_PULSE = 500

# Per-channel safe limits (min_angle, max_angle).
# S1=ch0 (MG996R base), S2–S4=ch1–3 (MG90S).
LIMITS = {
    0: (  0, 180),
    1: ( 65, 125),
    2: ( 30, 120),
    3: ( 90, 150),
}

class Arm:
    def __init__(self):
        i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=400000)
        self.driver = PCA9685(i2c)
        self.driver.freq(SERVO_HZ)

    def move(self, channel, angle):
        lo, hi = LIMITS.get(channel, (0, 180))
        angle = max(lo, min(hi, angle))
        pulse = MIN_PULSE + int((MAX_PULSE - MIN_PULSE) * angle / 180)
        self.driver.channel(channel, pulse)
        