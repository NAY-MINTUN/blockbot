"""
Joystick limit tester for BlockBot arm.

Wiring (change pin numbers below to match yours):
  J1 VRx → GPIO 34   (Base,     ch0 MG996R)
  J1 VRy → GPIO 35   (Shoulder, ch1 MG90S)
  J2 VRx → GPIO 32   (Elbow,    ch2 MG90S)
  J2 VRy → GPIO 33   (Wrist,    ch3 MG90S)
  All GND → GND,  All VCC → 3.3 V

Run: mpremote run firmware/joystick_test.py
Stop: Ctrl-C  (servos hold last position)
"""

from machine import ADC, Pin
import time
from servo import Arm

# ── Pin config ───────────────────────────────────────────────────────
J1_X = 34   # Base
J1_Y = 35   # Shoulder
J2_X = 32   # Elbow
J2_Y = 33   # Wrist
# ────────────────────────────────────────────────────────────────────

# ── Tuning ───────────────────────────────────────────────────────────
DEAD_ZONE   = 300    # ADC counts either side of centre (4096/2) to ignore
MAX_SPEED   = 3      # degrees per tick at full deflection
TICK_MS     = 50     # loop period in ms  (50 ms → 20 updates/sec)
PRINT_EVERY = 10     # print status every N ticks
# ────────────────────────────────────────────────────────────────────

# Per-channel safe limits — must match servo.py LIMITS
LIMITS = {
    0: (  0, 180),
    1: ( 25, 125),
    2: ( 50, 140),
    3: ( 93, 150),
}

NAMES  = {0: "Base", 1: "Shoulder", 2: "Elbow", 3: "Wrist"}
INVERT = {0: False, 1: True, 2: False, 3: False}


def make_adc(pin):
    a = ADC(Pin(pin))
    a.atten(ADC.ATTN_11DB)   # full 0–3.3 V range
    return a


def read_delta(adc):
    """Return a signed speed (-MAX_SPEED..+MAX_SPEED) from an ADC axis."""
    raw = adc.read()           # 0–4095
    centre = 2048
    offset = raw - centre
    if abs(offset) < DEAD_ZONE:
        return 0
    # Scale dead-zone-edge → full deflection to 1..MAX_SPEED
    sign = 1 if offset > 0 else -1
    scaled = (abs(offset) - DEAD_ZONE) / (centre - DEAD_ZONE)
    return sign * max(1, int(scaled * MAX_SPEED))


arm  = Arm()
adcs = [make_adc(J1_X), make_adc(J1_Y), make_adc(J2_X), make_adc(J2_Y)]

# Start each joint at the middle of its safe range
angles = [
    (LIMITS[ch][0] + LIMITS[ch][1]) // 2
    for ch in range(4)
]
for ch, a in enumerate(angles):
    arm.move(ch, a)

print("\nJoystick limit tester running — Ctrl-C to stop.")
print(f"{'Ch':<4} {'Name':<10} {'Min':>5} {'Max':>5} {'Current':>8}")
for ch in range(4):
    lo, hi = LIMITS[ch]
    print(f"{ch:<4} {NAMES[ch]:<10} {lo:>5} {hi:>5} {angles[ch]:>8}")
print()

tick = 0
try:
    while True:
        changed = False
        for ch, adc in enumerate(adcs):
            delta = read_delta(adc)
            if INVERT[ch]:
                delta = -delta
            if delta:
                lo, hi = LIMITS[ch]
                new_angle = max(lo, min(hi, angles[ch] + delta))
                if new_angle != angles[ch]:
                    angles[ch] = new_angle
                    arm.move(ch, new_angle)
                    changed = True

        tick += 1
        if tick % PRINT_EVERY == 0 or changed:
            status = "  ".join(
                f"{NAMES[ch]}:{angles[ch]:>3}°" for ch in range(4)
            )
            print(status)

        time.sleep_ms(TICK_MS)

except KeyboardInterrupt:
    print("\nStopped. Final angles:")
    for ch in range(4):
        lo, hi = LIMITS[ch]
        print(f"  ch{ch} {NAMES[ch]:<10}: {angles[ch]}°  (safe range {lo}–{hi}°)")
