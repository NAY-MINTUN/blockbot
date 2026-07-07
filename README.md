# BlockBot

BlockBot is an ESP32-based robot arm controlled via WiFi. Commands are sent as JSON over WebSocket to move servos, with built-in safety limits that prevent the arm from damaging itself. The current implementation includes a WebSocket server on the ESP32, a FastAPI relay backend for command validation, and a browser-based test console for manual control.

## Project Status

**Currently Implemented:**
- ESP32 firmware with WebSocket server (Microdot)
- 4-servo arm control with safety limits enforced per servo
- FastAPI relay backend for validated command relay
- Browser test console with servo control sliders, presets, and sequence builder
- Live joystick control via physical analog joysticks

**In Development:**
- Block-based visual programming editor
- On-screen touch joystick interface
- Program save/load functionality

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
| 34       | J1 VRx      | Base rotation   |
| 35       | J1 VRy      | In/Out arm      |
| 32       | J2 VRx      | Up/Down arm     |
| 33       | J2 VRy      | Gripper         |

Connect all joystick VCC pins to 3.3V and all GND pins to GND.

---

## Servo Safety Limits

These limits were determined by physical testing and are enforced by the firmware. No command can move a servo past these angles.

| Channel | Joint            | Servo  | Min Angle | Max Angle |
|---------|------------------|--------|-----------|-----------|
| 0       | Base             | MG996R | 0°        | 180°      |
| 1       | In/Out Arm       | MG90S  | 65°       | 125°      |
| 2       | Up/Down Arm      | MG90S  | 30°       | 120°      |
| 3       | Gripper          | MG90S  | 90°       | 150°      |

---

## Firmware Installation

### Prerequisites
- MicroPython v1.28 (or later) flashed onto the ESP32
- Thonny IDE with MicroPython (ESP32) interpreter configured

### Steps

1. **Configure WiFi credentials** in `firmware/main.py`:
   ```python
   WIFI_SSID = 'Your_Network'
   WIFI_PASSWORD = 'Your_Password'
   ```

2. **Upload these files to the ESP32** via Thonny:
   - `pca9685.py` (PCA9685 I2C driver)
   - `servo.py` (Arm class with safety limits)
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

BlockBot uses a 3-tier architecture:

```
[Browser]
    ↓ WebSocket
[Backend (FastAPI)]
    ↓ WebSocket
[ESP32 Firmware (Microdot)]
    ↓ I2C
[PCA9685 Servo Driver]
    ↓
[Servos]
```

The backend relay validates all commands before forwarding them to the ESP32, providing an extra layer of safety and logging.

---

## Running the Backend Relay

The backend is optional. You can connect directly to the ESP32 WebSocket if you prefer, but the backend provides command validation and logging.

### Prerequisites
- Python 3.8+
- FastAPI, Uvicorn, websockets (see `requirements.txt`)

### Steps

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Update the ARM_WS address** in `backend/main.py` to match your ESP32's IP:
   ```python
   ARM_WS = 'ws://192.168.1.XXX:8080/ws'
   ```

3. **Start the backend**:
   ```bash
   fastapi dev backend/main.py
   ```
   The backend will run at `ws://localhost:8000/ws`.

4. **Verify connectivity**:
   ```bash
   curl http://localhost:8000/health
   ```

---

## Testing and Control

### Browser Test Console

A comprehensive test page is included at `test.html`. It connects to the backend relay and provides:
- Servo control sliders (0°–180°, with safe limits highlighted)
- Preset positions (Home, Reach, Park)
- Sequence builder (queue commands and run them in order)
- Message log showing all sent/received commands

#### Steps

1. Start the backend relay (see "Running the Backend Relay" above).

2. Serve the test page locally:
   ```bash
   python3 -m http.server 3000
   ```

3. Open `http://localhost:3000/test.html` in your browser.

4. Enter `localhost:8000` and click **Connect**.

5. Use the sliders to control the servos. Commands are validated by the backend before being sent to the ESP32.

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

If you have physical joysticks wired to the ESP32:

1. Open `firmware/joystick_test.py` in Thonny.
2. Press **Run** (F5).
3. Push the joysticks to move the arm. Press **Ctrl-C** to stop.

---

## Firmware Files

| File | Purpose |
|------|---------|
| `main.py` | WebSocket server, entry point |
| `servo.py` | `Arm` class — moves servos and enforces safety limits |
| `pca9685.py` | Low-level I2C driver for the PCA9685 servo board |
| `joystick_test.py` | Live joystick control utility |
| `test_limits.py` | Calibration tool for finding safe angle limits |
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
- Ensure WiFi credentials in `firmware/main.py` are correct.

**Problem: "Servos not responding"**
- Check the I2C wiring between ESP32 and PCA9685.
- Verify GPIO 21 (SDA) and GPIO 22 (SCL) are correct in `servo.py`.
- Ensure the 5V power supply is connected and delivering power to the PCA9685.

**Problem: "Servo moves jerkily or overshoots"**
- The ESP32 may have crashed. Press the EN (reset) button on the board.
- If a servo is at a mechanical stop, the firmware won't exceed its safe limits. Check the angle limits in `servo.py`.

### Backend Relay

**Problem: "Cannot reach arm" error in test console**
- Verify `ARM_WS` in `backend/main.py` points to your ESP32's IP and port.
- Ensure the ESP32 WebSocket server is running.
- Check that your computer and ESP32 are on the same WiFi network.

**Problem: "Arm connection lost" during command**
- The ESP32 WebSocket connection may have dropped. Try reconnecting from the test console.
- Check the ESP32 power supply — servos drawing too much current can cause resets.

### Browser Test Console

**Problem: "Connection refused" when connecting**
- Verify the backend is running (`fastapi dev backend/main.py`).
- Check that you've entered the correct backend address (e.g., `localhost:8000`).
- If connecting from a different machine, use the machine's IP instead of `localhost`.

---

## Development Notes

- **Servo pulse width range**: 110–500 microseconds (configured in `servo.py`).
- **Servo frequency**: 50 Hz (standard for hobby servos).
- **Each joint has a different safe range** because of physical constraints. These were found by testing and are stored in `LIMITS` in both `servo.py` (firmware) and `validator.py` (backend).
- **The firmware enforces limits** to prevent damage even if invalid commands are sent.
- **WiFi is initialized before importing Microdot** to avoid heap fragmentation (see comment in `main.py`).

---

## What Comes Next

- **Block-based visual editor**: Scratch-style blocks for move, wait, repeat, if/else, variables, and functions.
- **On-screen touch controls**: Touch-based joysticks and buttons for mobile/tablet.
- **Program persistence**: Save and load programs on the device.
- **Auto-reconnect**: Automatic reconnection if WiFi or WebSocket drops.
- **Mobile app**: Native iOS/Android interface.
