BlockBot

# BlockBot

BlockBot is an educational robot arm for kids. The idea is simple — open a block editor on an iPad, snap blocks together like Lego, press Run, and a real robot arm moves. No typing, no installing anything.

When fully built, kids will be able to write real programs using blocks — move a joint, wait, repeat, if/else, variables, and their own functions. The arm will take commands over WiFi. They can also drive it live using on-screen touch joysticks on the iPad or two physical joysticks. Everything goes through the same safety limits so the arm can never hurt itself.

This file documents everything built so far and will be updated as each part gets added.

---

## Hardware

- 1x ESP32 (runs the firmware, will handle WiFi)
- 1x PCA9685 (servo driver board, talks to ESP32 over I2C)
- 1x MG996R servo (base — metal gear, more torque)
- 3x MG90S servo (shoulder, elbow, wrist)
- 2x KY-023 joystick module (physical joystick control)
- 1x 5V power supply (dedicated to servos)

---

## Power Setup

The ESP32 runs on USB power.
The 4 servos run on a **separate 5V supply** connected to PCA9685 V+.
Never power servos from the ESP32 — they draw too much current and will crash it.
All grounds must be joined — ESP32 GND, PCA9685 GND, and 5V supply GND all connected together.

---

## Wiring

**ESP32 → PCA9685 (I2C)**

| ESP32   | PCA9685 |
|---------|---------|
| 3.3V    | VCC     |
| GND     | GND     |
| GPIO 21 | SDA     |
| GPIO 22 | SCL     |

————start here——

**Joysticks → ESP32**

| GPIO | Joystick | Controls |
|------|----------|----------|
| 34   | J1 VRx   | Base     |
| 35   | J1 VRy   | Shoulder |
| 32   | J2 VRx   | Elbow    |
| 33   | J2 VRy   | Wrist    |

All joystick VCC → 3.3V. All joystick GND → GND.

---

## Servo Channels and Safe Limits

These limits were found by physically testing the arm with joystick control. Going outside these angles hits the mechanical stop or strains the servo. The firmware enforces these limits — no command can ever send a servo past them.

| Channel | Joint    | Servo  | Min | Max  | Notes                          |
|---------|----------|--------|-----|------|--------------------------------|
| 0       | Turntable| MG996R | 0°  | 180° | full range is safe             |
| 1       | In/Out   | MG90S  | 25° | 125° | joystick axis inverted in code |
| 2       | Up/Down  | MG90S  | 50° | 140° |                                |
| 3       | Gripper  | MG90S  | 93° | 150° |                                |

---

## Firmware

All files are in `firmware/`. Written in MicroPython.

| File               | What it does                                      |
|--------------------|---------------------------------------------------|
| `pca9685.py`       | Low level I2C driver for the PCA9685 chip         |
| `servo.py`         | Arm class — moves servos, enforces safe limits    |
| `main.py`          | Runs on boot                                      |
| `test_limits.py`   | Sweep and step tools used to find servo limits    |
| `joystick_test.py` | Live joystick control for testing and calibration |

---

## How to Run

1. Plug the ESP32 into your computer via USB
2. Open Thonny and set interpreter to **MicroPython (ESP32)**
3. Open `firmware/joystick_test.py`
4. Press **Run (F5)**

Push the joystick gently for slow movement, push fully for fast. Press Stop when done — Thonny shell will print the final angle of each joint.

---

## What I Learned So Far

- Servos must have their own power supply separate from the ESP32
- Every servo has a different safe range — you have to find it by physical testing
- The shoulder joystick direction was reversed and had to be flipped in code
- Starting each joint at the middle of its range on boot prevents sudden jerks

---

## What Comes Next

- WiFi communication between ESP32 and iPad
- WebSocket server on ESP32 to receive movement commands
- Scratch-style block editor on iPad
- On-screen touch joysticks
- Block programming — move, wait, repeat, if/else, variables, functions
- Auto-reconnect and connection status display
- Save and load programs on the iPad