# BlockBot

BlockBot lets you control a robot arm with a block editor or physical joysticks.
The app runs in a web browser. An ESP32 connects to the arm and talks to the app
through a local Python server.

## What BlockBot can do

- Create an account or sign in.
- Add, connect, and delete devices.
- Show robot controls when a robot arm is selected.
- Let you set the minimum and maximum angle for each joint.
- Save devices and programs to your account on this computer.
- Control the arm with Blockly blocks or two physical joysticks.
- Stop a running program with the **STOP** button.
- Use the physical joysticks even when the ESP32 is not connected to home Wi-Fi.

Accounts and saved data belong to this local BlockBot installation. There is no
email verification or password reset.

## Parts

| Part | What it does |
|------|--------------|
| ESP32 | Runs the robot firmware and connects to Wi-Fi |
| PCA9685 board | Controls the servos |
| 1 MG996R servo | Turns the base |
| 3 MG90S servos | Move the arm and gripper |
| 2 KY-023 joysticks | Optional physical controls |
| Separate 5 V power supply | Powers the servos |

## Wiring

### ESP32 to PCA9685

| ESP32 | PCA9685 |
|-------|---------|
| 3.3 V | VCC |
| GND | GND |
| GPIO 21 | SDA |
| GPIO 22 | SCL |

### Servos to PCA9685

| PCA9685 channel | Servo | Joint |
|-----------------|-------|-------|
| CH0 | MG996R | Base |
| CH1 | MG90S | In / Out |
| CH2 | MG90S | Up / Down |
| CH3 | MG90S | Gripper |

### Optional joysticks

| ESP32 pin | Joystick output | Joint |
|-----------|-----------------|-------|
| GPIO 32 | JY1 VRx | Base |
| GPIO 33 | JY1 VRy | In / Out |
| GPIO 34 | JY2 VRx | Up / Down |
| GPIO 35 | JY2 VRy | Gripper |

Connect joystick VCC to 3.3 V and GND to GND. Connect all grounds together:
ESP32, PCA9685, and the servo power supply.

**Do not power the servos from the ESP32.** Use a separate, regulated 5 V supply
for the servos.

## Set up the ESP32

### Before you start

- Flash MicroPython onto the ESP32.
- Install Thonny and set its interpreter to MicroPython (ESP32).
- Upload these files and folders from `firmware/` to the ESP32:
  - `main.py`
  - `servo.py`
  - `pca9685.py`
  - `joystick.py`
  - `helpers.py`
  - the full `microdot/` folder

### Upload from VS Code with MicroPico

The project targets a classic ESP32 module. MicroPico lists ESP32-WROOM support
as experimental; its main workflow is designed for Raspberry Pi Pico boards.
If you use it with this ESP32, results may vary.

1. In VS Code, open the `firmware/` folder as the workspace.
2. Connect the ESP32 using a USB data cable. Install MicroPico from the VS Code
   Extensions view, then run **MicroPico: Switch Board** from the Command
   Palette (`Cmd+Shift+P` on macOS) and select the ESP32 serial port.
3. Run MicroPico's project upload command or use its upload button. Upload the
   entire `firmware/` workspace so `main.py`, the other Python files, and the
   complete `microdot/` folder are copied to the board.
4. Include `config.py` if you want the ESP32 to join your saved Wi-Fi network.
   It contains your Wi-Fi password; do not publish or commit it to a shared
   repository.
5. Reset the ESP32 and watch MicroPico's terminal for startup output.

Press **Cmd+S** to save edits on your Mac; uploading is a separate step that
copies the saved files to the ESP32. MicroPico's support for ESP32 is
experimental, so if upload fails, use another MicroPython-compatible serial
file transfer tool or Thonny to copy the same files.

### Connect it to Wi-Fi

1. Restart the ESP32.
2. On your computer or phone, join Wi-Fi named `BlockBot-Setup`. The password
   is `blockbot`.
3. Open `http://192.168.4.1:8080`.
4. Enter your home Wi-Fi name and password.
5. The ESP32 restarts and joins your home Wi-Fi. Thonny prints its new IP address.

## Run BlockBot

Open a terminal in the project folder and run:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Open [http://localhost:8000](http://localhost:8000) in your browser. Create an
account or sign in. Keep the terminal open while using BlockBot. To stop the
server, press **Ctrl+C** in that terminal.

## Add and set up the arm

1. In BlockBot, open **Devices** and choose **Find devices**.
2. If the arm does not appear, add it manually. Use the address printed by
   Thonny in this format: `ws://ESP32-IP:8080/ws`. For example,
   `ws://192.168.1.198:8080/ws`.
3. Set a minimum and maximum angle for each joint in **Devices**. The app needs
   all four ranges before it can connect.
4. Keep the arm clear before connecting. When the ESP32 receives the ranges, it
   moves each joint to the middle of its range.
5. Wait for the app to show that the robot is connected. Then build a program
   with blocks and press **Run**.

Choose ranges only after checking how far each joint can safely move. Values
must be between 0° and 180°. The app and ESP32 check commands against the ranges
you enter.

## Joystick control

Joystick control starts when the ESP32 starts and works without a Wi-Fi
connection or browser. Keep both joysticks released while it boots so it can
find their centre positions. Until the browser connects, the ESP32 uses its
built-in joint ranges (Base 0–180°, In/Out 40–125°, Up/Down 30–130°, Gripper
90–150°). A connected browser replaces these with the limits configured in the
app. Joysticks and Blockly can both control the arm. Keep hands and objects
clear while either one is moving it.

| Joystick axis | ESP32 pin | Joint |
|---------------|-----------|-------|
| JY1 VRx | GPIO 32 | Base |
| JY1 VRy | GPIO 33 | In / Out |
| JY2 VRx | GPIO 34 | Up / Down |
| JY2 VRy | GPIO 35 | Gripper |

## Troubleshooting

### The app cannot find the ESP32

- Check that the computer and ESP32 use the same Wi-Fi network.
- Read the ESP32 IP address in Thonny and add the WebSocket address manually:
  `ws://ESP32-IP:8080/ws`.
- Check that the router allows devices on Wi-Fi to talk to each other.
- Make sure the ESP32 is powered on and its firmware is running.

### The app says the robot is offline

- Check the saved device address. `127.0.0.1` points to the computer running the
  app, not to the ESP32.
- Check the Wi-Fi connection and the IP address printed by Thonny.
- Make sure all four joint ranges are filled in.

### The servos do not move

- Check the PCA9685 I2C wiring: SDA to GPIO 21 and SCL to GPIO 22.
- Check the separate 5 V servo supply and the shared ground connections.
- Check that the ranges you entered allow the requested movement.

## Project files

| Path | Purpose |
|------|---------|
| `frontend/` | Browser app and Blockly editor |
| `backend/main.py` | Web app and WebSocket relay |
| `backend/validator.py` | Checks robot commands |
| `firmware/main.py` | ESP32 Wi-Fi and WebSocket server |
| `firmware/servo.py` | Servo control and joint ranges |
| `firmware/joystick.py` | Physical joystick control |
| `firmware/pca9685.py` | PCA9685 driver |
