"""Non-blocking physical joystick control for the BlockBot arm."""

import asyncio
from machine import ADC, Pin

from servo import LIMITS


# JY1 controls the base and in/out arm; JY2 controls up/down and gripper.
AXES = (
    (32, 0, False),  # JY1 VRx -> base
    (33, 1, True),   # JY1 VRy -> in/out arm
    (34, 2, False),  # JY2 VRx -> up/down arm
    (35, 3, False),  # JY2 VRy -> gripper
)

ADC_MAX = 4095
DEAD_ZONE = 350
MAX_SPEED = 3
TICK_MS = 50
CALIBRATION_SAMPLES = 30


def _make_adc(pin_number):
    adc = ADC(Pin(pin_number))
    adc.atten(ADC.ATTN_11DB)
    return adc


class JoystickController:
    def __init__(self, arm):
        self.arm = arm
        self.adcs = [_make_adc(pin) for pin, _channel, _invert in AXES]
        self.centres = [ADC_MAX // 2] * len(AXES)

    async def calibrate(self):
        """Measure the resting point; joysticks must be released at startup."""
        totals = [0] * len(self.adcs)
        print('Release joysticks - calibrating...')
        for _sample in range(CALIBRATION_SAMPLES):
            for index, adc in enumerate(self.adcs):
                totals[index] += adc.read()
            await asyncio.sleep_ms(10)
        self.centres = [
            total // CALIBRATION_SAMPLES
            for total in totals
        ]
        print('Joystick centres:', self.centres)

    def _delta(self, index):
        raw = self.adcs[index].read()
        centre = self.centres[index]
        offset = raw - centre
        magnitude = abs(offset)

        if magnitude <= DEAD_ZONE:
            return 0

        available = (ADC_MAX - centre) if offset > 0 else centre
        span = max(1, available - DEAD_ZONE)
        speed = 1 + ((magnitude - DEAD_ZONE) * (MAX_SPEED - 1) // span)
        speed = min(MAX_SPEED, speed)
        return speed if offset > 0 else -speed

    async def run(self):
        print('Physical joystick control ready.')
        while True:
            for index, (_pin, channel, invert) in enumerate(AXES):
                delta = self._delta(index)
                if invert:
                    delta = -delta
                if not delta:
                    continue

                lo, hi = LIMITS[channel]
                target = max(lo, min(hi, self.arm.angle(channel) + delta))
                if target != self.arm.angle(channel):
                    self.arm.move(channel, target)

            await asyncio.sleep_ms(TICK_MS)
