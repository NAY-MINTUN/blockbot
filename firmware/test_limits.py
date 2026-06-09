"""
Servo limit finder for BlockBot arm.

Channels assumed (adjust JOINTS to match your wiring):
  0 - Base     (MG996R)
  1 - Shoulder (MG90S)
  2 - Elbow    (MG90S)
  3 - Wrist    (MG90S)

Run from Thonny or:
  mpremote run firmware/test_limits.py

--- Workflow ---
1. Run sweep(ch) to see the full range your servo physically accepts.
2. Note the angle where the servo hits its mechanical stop or starts grinding.
3. Update MIN_ANGLE / MAX_ANGLE per channel in JOINTS below.
4. Run confirm(ch) to verify your chosen limits look right.
"""

import time
from servo import Arm

# ── Per-joint config ────────────────────────────────────────────────
# Adjust min/max after observing physical limits with sweep().
JOINTS = {
    0: {"name": "Base (MG996R)",    "min":  0, "max": 180},
    1: {"name": "Shoulder (MG90S)", "min": 65, "max": 125},
    2: {"name": "Elbow (MG90S)",    "min": 50, "max": 120},
    3: {"name": "Wrist (MG90S)",    "min": 90, "max": 150},
}
# ────────────────────────────────────────────────────────────────────

arm = Arm()


def move(ch, angle):
    """Move channel ch to angle (clamped to servo.py's 0–180 range)."""
    arm.move(ch, angle)
    print(f"  ch{ch} → {angle}°")


def center(ch=None):
    """Center one servo (or all if ch is None)."""
    targets = [ch] if ch is not None else list(JOINTS)
    for c in targets:
        move(c, 90)
    time.sleep_ms(500)


def sweep(ch, step=5, delay_ms=300):
    """
    Sweep ch from its configured min to max and back.
    Watch for grinding or stalling — that marks the real limit.
    Press Ctrl-C to stop early.
    """
    j = JOINTS[ch]
    lo, hi = j["min"], j["max"]
    print(f"\n--- Sweeping {j['name']} (ch{ch}) {lo}° → {hi}° ---")
    print("Watch for grinding / stall — those are your true limits.")
    try:
        for angle in range(lo, hi + 1, step):
            move(ch, angle)
            time.sleep_ms(delay_ms)
        time.sleep_ms(500)
        for angle in range(hi, lo - 1, -step):
            move(ch, angle)
            time.sleep_ms(delay_ms)
    except KeyboardInterrupt:
        print("  Stopped early.")
    print(f"--- Sweep done ---\n")


def step_test(ch, step=10):
    """
    Interactive step test: press Enter to move forward one step,
    type '-' + Enter to go back, 'q' to quit.
    Use this to find the exact limit angle.
    """
    j = JOINTS[ch]
    angle = 90
    move(ch, angle)
    print(f"\n--- Step test {j['name']} (ch{ch}), step={step}° ---")
    print("Enter  → +step   |  '-' → -step   |  'q' → quit")
    while True:
        try:
            raw = input(f"  [{angle}°] > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break
        if raw == "q":
            break
        elif raw == "-":
            angle = max(0, angle - step)
        else:
            angle = min(180, angle + step)
        move(ch, angle)
    print(f"  Final angle: {angle}°  — update JOINTS[{ch}] limits if needed.\n")


def confirm(ch):
    """Move ch to its configured min, center, then max to verify limits."""
    j = JOINTS[ch]
    print(f"\n--- Confirming limits for {j['name']} (ch{ch}) ---")
    print(f"  Moving to MIN ({j['min']}°)…")
    move(ch, j["min"]); time.sleep(1)
    print(f"  Moving to CENTER (90°)…")
    move(ch, 90);        time.sleep(1)
    print(f"  Moving to MAX ({j['max']}°)…")
    move(ch, j["max"]); time.sleep(1)
    move(ch, 90)
    print("--- Done ---\n")


def help():
    print("""
BlockBot servo limit tools
──────────────────────────
sweep(ch)          — slow sweep min→max→min, watch for grinding
step_test(ch)      — interactive +/- stepping to find exact limit
confirm(ch)        — move to min / center / max to verify JOINTS config
center(ch=None)    — center one servo or all
move(ch, angle)    — move to a specific angle

Examples:
  sweep(0)         # test base (MG996R)
  step_test(1)     # find shoulder limit interactively
  confirm(2)       # verify elbow limits after editing JOINTS
  center()         # center everything
""")


# On import, print quick help and center all servos.
print("\nBlockBot limit tester loaded. Centering all servos…")
center()
help()
