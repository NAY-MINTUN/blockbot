# BlockBot

BlockBot is an educational robot-arm system controlled through a browser-based
Blockly editor or two physical joysticks. The ESP32 receives JSON commands over
WebSocket and drives four servos through a PCA9685 board. Safety limits are
enforced in both the FastAPI relay and the ESP32 firmware.

The robot hardware and FastAPI relay operate on the same trusted Wi-Fi network.
For a supervised public demonstration, the relay can be temporarily exposed
through a secure HTTPS/WebSocket tunnel such as ngrok. The public endpoint must
be stopped after the demonstration because application-level authentication is
not implemented yet.

## Project Status

**Currently Implemented:**
- ESP32 firmware with WebSocket server (Microdot)
- 4-servo arm control with safety limits enforced per servo
- FastAPI relay backend for validated command relay
- Blockly-based visual programming editor
- Local browser program auto-save
- Non-blocking control from two physical analog joysticks
- Automatic joystick centre calibration at startup
- Live commanded-angle display in the browser and Thonny console
- Temporary public demonstrations through an HTTPS/WebSocket tunnel

**In Development:**
- On-screen touch joystick interface
- Named program save/load functionality

---

## Hardware

| Part | Quantity | Purpose |
|------|----------|---------|
| ESP32 | 1 | Runs the firmware and WiFi WebSocket server |
| PCA9685 | 1 | I2C servo driver board |
| MG996R servo | 1 | Base (turntable rotation) |
| MG90S servo | 3 | In/Out arm, Up/Down arm, Gripper |
| KY-023 analog joystick module | 2 | Physical joystick control (optional) |
| 5V power supply | 1 | Dedicated power for servos |

---

## Power Setup

- The ESP32 runs on USB power from your computer.
- The 4 servos run on a **separate 5V power supply**. Never power servos from the ESP32 — they draw too much current and will reset it.
- All grounds must be connected together: ESP32 GND, PCA9685 GND, and power supply GND.

---

## Wiring

### ESP32 ↔ PCA9685 (I2C)

| ESP32 Pin | PCA9685 Pin |
|-----------|-------------|
| 3.3V      | VCC         |
| GND       | GND         |
| GPIO 21   | SDA         |
| GPIO 22   | SCL         |

### Servos → PCA9685

| PCA9685 Channel | Servo Type | Joint             |
|-----------------|-----------|-------------------|
| CH0             | MG996R    | Base (Turntable)  |
| CH1             | MG90S     | In/Out Arm        |
| CH2             | MG90S     | Up/Down Arm       |
| CH3             | MG90S     | Gripper           |

### Joysticks → ESP32 (Optional)

| GPIO Pin | Joystick Pin | Controls        |
|----------|-------------|-----------------|
| 32       | JY1 VRx     | Base rotation   |
| 33       | JY1 VRy     | In/Out arm      |
| 34       | JY2 VRx     | Up/Down arm     |
| 35       | JY2 VRy     | Gripper         |

Connect all joystick VCC pins to 3.3V and all GND pins to GND.

---

## Servo Safety Limits

These limits were determined by physical testing and are enforced by the firmware. No command can move a servo past these angles.

| Channel | Joint            | Servo  | Min Angle | Max Angle |
|---------|------------------|--------|-----------|-----------|
| 0       | Base             | MG996R | 0°        | 180°      |
| 1       | In/Out Arm       | MG90S  | 40°       | 125°      |
| 2       | Up/Down Arm      | MG90S  | 30°       | 130°      |
| 3       | Gripper          | MG90S  | 90°       | 150°      |

---

## Firmware Installation

### Prerequisites
- MicroPython v1.28 (or later) flashed onto the ESP32
- Thonny IDE with MicroPython (ESP32) interpreter configured

### Steps

1. **Create the private WiFi config** from the example:
   ```python
   # firmware/config.py
   WIFI_SSID = 'Your_Network'
   WIFI_PASSWORD = 'Your_Password'
   ```
   `firmware/config.py` is ignored by Git. Upload it to the ESP32 with the
   other firmware files.

2. **Upload these files to the ESP32** via Thonny:
   - `pca9685.py` (PCA9685 I2C driver)
   - `servo.py` (Arm class with safety limits)
   - `joystick.py` (non-blocking physical joystick control)
   - `main.py` (WebSocket server)
   - `microdot/` (Microdot web framework and WebSocket support)

3. **Reset the ESP32** by pressing the EN button. The IP address will print in Thonny's shell.

---

## WebSocket Server

The ESP32 runs a WebSocket server at:
```
ws://[ESP32_IP]:8080/ws
```

Replace `[ESP32_IP]` with the IP address printed when the ESP32 boots.

### Command Format

All commands are sent as JSON over the WebSocket connection.

#### Move a Servo

```json
{"cmd": "move", "channel": 0, "angle": 90}
```

| Field     | Type   | Description |
|-----------|--------|-------------|
| `cmd`     | string | `"move"` |
| `channel` | number | Servo channel (0–3) |
| `angle`   | number | Target angle in degrees (automatically clamped to safe range) |

#### Wait

```json
{"cmd": "wait", "second": 1}
```

| Field    | Type   | Description |
|----------|--------|-------------|
| `cmd`    | string | `"wait"` |
| `second` | number | Duration in seconds |

### Example Command Sequence

Send each JSON object as a separate WebSocket message:

```json
{"cmd": "move", "channel": 0, "angle": 0}
{"cmd": "wait", "second": 1}
{"cmd": "move", "channel": 1, "angle": 90}
{"cmd": "move", "channel": 2, "angle": 75}
{"cmd": "wait", "second": 2}
{"cmd": "move", "channel": 0, "angle": 180}
```

---

## System Architecture

BlockBot uses a three-tier network architecture with a second, local input path
for the physical joysticks:

```
[Browser / Blockly]
        │ WebSocket
        ▼
[FastAPI validation relay]
        │ WebSocket over local Wi-Fi
        ▼
[ESP32 / Microdot] ◀── [Two physical joysticks]
        │ I2C
        ▼
[PCA9685 servo driver]
        │ PWM
        ▼
[Four servos]
```

The backend relay validates all commands before forwarding them to the ESP32, providing an extra layer of safety and logging.

---

## Running the Backend Relay

The Blockly interface requires the backend relay. A developer can connect a
separate WebSocket client directly to the ESP32 for testing, but doing so skips
the backend validation layer.

### Prerequisites
- Python 3.8+
- FastAPI and websockets (installed from `requirements.txt`)

### Steps

1. **Install dependencies** from the project root:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Start the app**, setting `ARM_WS` to the ESP32 address printed in Thonny:
   ```bash
   ARM_WS=ws://192.168.1.XXX:8080/ws \
   uvicorn backend.main:app --host 127.0.0.1 --port 8000
   ```
   The UI and backend will run together at `http://localhost:8000`.

3. **Verify connectivity**:
   ```bash
   curl http://localhost:8000/health
   ```

4. **Run the automated checks**:
   ```bash
   python -m unittest discover -s tests -v
   ```

---

## Testing and Control

### Block Editor (Blockly-based, replaces the old test.html console)

The frontend is now a Blockly-based visual editor (`index.html` / `blocks.js` / `app.js`). It connects to the backend relay over WebSocket and provides:
- Drag-and-drop blocks: `when Run clicked`, `move [joint] to [angle] degrees`, `wait [seconds] seconds`
- Standard Logic, Loops, Math, Variables, and Functions block categories
- A connection status indicator
- Program auto-save/load via browser local storage

Note: this editor is part of the prototype and is intended for supervised local
testing.

#### Steps

1. Start the BlockBot app (see "Running the Backend Relay" above).
2. Open `http://localhost:8000` in your browser.
3. Drag blocks into the workspace and press **Run**. Commands run in order and
   are validated before being sent to the ESP32.

### Direct WebSocket Testing

You can also connect directly to the ESP32 WebSocket without the backend:

```python
import asyncio
import json
import websockets

async def test():
    uri = "ws://[ESP32_IP]:8080/ws"
    async with websockets.connect(uri) as ws:
        # Move base to 90 degrees
        await ws.send(json.dumps({"cmd": "move", "channel": 0, "angle": 90}))
        # Wait 1 second
        await ws.send(json.dumps({"cmd": "wait", "second": 1}))

asyncio.run(test())
```

### Live Joystick Control

Physical joystick control starts automatically with `firmware/main.py` and runs
alongside WebSocket control. Keep both joysticks released while the ESP32 boots
so their centre positions can be calibrated. Use `firmware/joystick_test.py`
only when testing the joysticks without Wi-Fi or browser control.

At startup, the firmware moves every joint to the midpoint of its safe range.
Keep people and objects clear of the arm before applying power.

| Axis | GPIO | Joint | Channel |
|------|------|-------|---------|
| JY1 VRx | 32 | Base rotation | 0 |
| JY1 VRy | 33 | In/Out arm | 1 |
| JY2 VRx | 34 | Up/Down arm | 2 |
| JY2 VRy | 35 | Gripper | 3 |

The integrated controller samples every 50 ms, ignores small readings around
the calibrated centre, and moves by up to 3 degrees per sample. Direction,
dead-zone, speed, and timing settings are defined near the top of
`firmware/joystick.py`.

While a joystick or Blockly program moves the arm, the ESP32 publishes the four
latest commanded angles to connected browsers. These are software command
positions, not measurements from physical position sensors. The firmware also
prints the positions in the Thonny console while joystick movement is active.

---

## Firmware Files

| File | Purpose |
|------|---------|
| `main.py` | WebSocket server, entry point |
| `servo.py` | `Arm` class — moves servos and enforces safety limits |
| `pca9685.py` | Low-level I2C driver for the PCA9685 servo board |
| `joystick.py` | Non-blocking two-joystick controller |
| `joystick_test.py` | Live joystick control utility |
| `helpers.py` | MicroPython compatibility helpers |
| `microdot/` | Embedded Microdot web framework and WebSocket support |

---

## Backend Files

| File | Purpose |
|------|---------|
| `main.py` | FastAPI relay server with WebSocket handling |
| `validator.py` | Command validation — checks channel and angle bounds |

---

## Troubleshooting

### ESP32 Firmware

**Problem: "Cannot connect to ESP32"**
- Verify the ESP32 is on the same WiFi network as your computer.
- Check the IP address in Thonny's shell — it should print when the ESP32 boots.
- Ensure WiFi credentials in `firmware/config.py` are correct.

**Problem: "Servos not responding"**
- Check the I2C wiring between ESP32 and PCA9685.
- Verify GPIO 21 (SDA) and GPIO 22 (SCL) are correct in `servo.py`.
- Ensure the 5V power supply is connected and delivering power to the PCA9685.

**Problem: "Servo moves jerkily or overshoots"**
- The ESP32 may have crashed. Press the EN (reset) button on the board.
- If a servo is at a mechanical stop, the firmware won't exceed its safe limits. Check the angle limits in `servo.py`.

### Backend Relay

**Problem: "Cannot reach the robot" message in the block editor**
- Verify the `ARM_WS` environment variable points to your ESP32's IP and port.
- Ensure the ESP32 WebSocket server is running.
- Check that your computer and ESP32 are on the same WiFi network.

**Problem: "Arm connection lost" during command**
- The ESP32 WebSocket connection may have dropped. Reload the block editor.
- Check the ESP32 power supply — servos drawing too much current can cause resets.

### Block Editor

**Problem: "Connection refused" / status indicator stays red**
- Verify the app is running (`uvicorn backend.main:app --reload`).
- If connecting from an iPad, open the backend machine's LAN IP instead of `localhost`.

---

## Development Notes

- **PCA9685 pulse counts**: 110–500 at 50 Hz (configured in `servo.py`).
- **Servo frequency**: 50 Hz (standard for hobby servos).
- **Each joint has a different safe range** because of physical constraints. These were found by testing and are stored in `LIMITS` in both `servo.py` (firmware) and `validator.py` (backend).
- **The firmware enforces limits** to prevent damage even if invalid commands are sent.
- **WiFi is initialized before importing Microdot** to avoid heap fragmentation (see comment in `main.py`).

---

## Operational Safety

- Always use a separate regulated 5 V supply for the servos.
- Connect the ESP32, PCA9685, and servo power-supply grounds together.
- Keep the arm clear when it powers on because startup homing causes movement.
- Test newly calibrated limits at low speed before a public demonstration.
- Do not hold a joystick while a Blockly program is running; both controls are
  active and the most recent command determines the joint position.
- Supervise the robot whenever servo power is connected.
- Stop any public tunnel immediately after the demonstration.

## Current Limitations

- There is no emergency-stop button yet.
- There is no controller lock between Blockly and physical joystick input.
- Public WebSocket connections do not yet require an application token.
- The ESP32 waits for Wi-Fi before joystick control starts.
- Browser programs are stored only in that browser's local storage.

---

## What Comes Next

- **On-screen touch controls**: Touch-based joysticks and buttons for mobile/tablet.
- **Named programs**: Save, rename, and load multiple programs.
- **Emergency stop**: Cancel a running program and stop motion safely.
- **Mobile app**: Native iOS/Android interface.
