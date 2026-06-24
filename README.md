# BlockBot

BlockBot is an educational robot arm for kids. The idea is simple — open a block editor on an iPad, or a computer, snap blocks together like Lego, press Run, and a real robot arm moves. No typing, no installing anything.

When fully built, kids will be able to write real programs using blocks — move a joint, wait, repeat, if/else, variables, and their own functions. The arm takes commands over WiFi via WebSocket. They can also drive it live using on-screen touch joysticks on the iPad or two physical joysticks. Everything goes through the same safety limits so the arm can never hurt itself.


---

## Hardware

- 1x ESP32 (runs the firmware and WiFi server)
- 1x PCA9685 (servo driver board, talks to ESP32 over I2C)
- 1x MG996R servo (Base)
- 3x MG90S servo (In/Out arm, Up/Down arm, Gripper)
- 2x KY-023 joystick module (physical joystick control)
- 1x 5V power supply (dedicated to servos)

---

## Power Setup

The ESP32 runs on USB power.
The 4 servos run on a **separate 5V supply
Never power servos from the ESP32 — they draw too much current and will crash it.
All grounds must be joined — ESP32 GND, PCA 9685all connected together.

---

## Wiring

**ESP32 → PCA9685 (I2C)**

| ESP32   | PCA9685 |
|---------|---------|
| 3.3V    | VCC     |
| GND     | GND     |
| GPIO 21 | SDA     |
| GPIO 22 | SCL     |

**Servos → PCA9685**

| Channel | PCA9685 |        Servo        |
|---------|---------|---------------------|
| 0       | CH0     | MG996R (Base)       |
| 1       | CH1     | MG90S  (In/Out Arm) |
| 2       | CH2     | MG90S  (Up/Down Arm)|
| 3       | CH3     | MG90S  (Gripper)    |

**Joysticks → ESP32**

| GPIO | Joystick |   Controls  |
|------|----------|-------------|
| 34   | J1 VRx   | Base        |
| 35   | J1 VRy   | In/Out Arm  |
| 32   | J2 VRx   | Up/Down Arm |
| 33   | J2 VRy   | Gripper     |

All joystick VCC → 3.3V. All joystick GND → GND.

---

## Servo Channels and Safe Limits

These limits were found by physically testing the arm with joystick control. Going outside these angles hits the mechanical stop or strains the servo. The firmware enforces these limits — no command can ever send a servo past them.

| Channel | Joint     | Servo  | Min  | Max  | Notes                          |
|---------|-----------|--------|------|----------|
| 0       | Turntable | MG996R | 0°   | 180° | Full range is safe             |
| 1       | In/Out    | MG90S  | 65°  | 12       |
| 2       | Up/Down   | MG90S  | 30°  | 120° |                                |
| 3       | Gripper   | MG90S  | 90°  | 15       |

---

## Firmware

All files are in `firmware/`. Written in M

| File               | What it does         |
|--------------------|---------------------------------------------------|
| `pca9685.py`       | Low-level I2C drive  |
| `servo.py`         | Arm class — moves servos, enforces safe limits    |
| `main.py`          | WebSocket server —   |
| `test_limits.py`   | Sweep and step tools used to find servo limits    |
| `joystick_test.py` | Live joystick contrn |

### Installing the Firmware

1. Flash MicroPython v1.28 onto the ESP32
2. Open Thonny and set interpreter to **MicroPython (ESP32)**
3. Upload `pca9685.py`, `servo.py`, and `m
4. Edit `main.py` and set your WiFi credentials:

```python
WIFI_SSID = 'Your_Network'
WIFI_PASSWORD = 'Your_Password'

5. Press the physical EN button — you'll see the IP address in Thonny's shell

---
WiFi & WebSocket

Once booted, the ESP32 hosts a WebSocket s

ws://[ESP32_IP]:8080

Commands

All commands are JSON sent as text over We

Move a servo:
{"cmd": "move", "channel": 0, "angle": 90}
- channel — 0 to 3
- angle — degrees, automatically clamped to the safe range for that channel

Wait:
{"cmd": "wait", "second": 1}
- second — duration in seconds

Example Sequence

{"cmd": "move", "channel": 0, "angle": 0}
{"cmd": "wait", "second": 1}
{"cmd": "move", "channel": 1, "angle": 90}
{"cmd": "move", "channel": 2, "angle": 75}
{"cmd": "wait", "second": 2}
{"cmd": "move", "channel": 0, "angle": 180

---
Testing from the Browser

A test page is included at test.html.

1. Start a local server on your Mac:
python3 -m http.server 3000

2. Open http://localhost:3000/test.html in
3. Click Connect — the log should show Connected
4. Set a channel and angle, then click Sen

▎ Make sure your Mac and ESP32 are on the

---
How to Run (Joystick Mode)

1. Plug the ESP32 into your computer via USB
2. Open Thonny and set interpreter to MicroPython
3. Open firmware/joystick_test.py
4. Press Run (F5)

Push the joystick gently for slow movementStop when done — Thonny shell will print the final angle of each joint.

---
What I Learned So Far

- Servos must have their own power supply
- Every servo has a different safe range — you have to find it by physical testing
- The shoulder joystick direction was reve code
- Starting each joint at the middle of its range on boot prevents sudden jerks
- After a crash, the ESP32 may need a physun button) to clear socket state

---
What Comes Next

- Scratch-style block editor on iPad
- On-screen touch joysticks
- Block programming — move, wait, repeat, if/else, variables, functions
- Live physical joystick control via WiFi
- Auto-reconnect and connection status display
- Save and load programs on the iPad