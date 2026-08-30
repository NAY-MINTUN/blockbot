# Running the BlockBot Prototype on a Laptop + Tablet/iPad

BlockBot is intended to run locally for supervised classroom testing. The
laptop, tablet, and ESP32 must all be connected to the same trusted Wi-Fi
network.

## 1. Find your laptop's LAN IP address

```bash
# Mac
ipconfig getifaddr en0
# or, more generally:
ifconfig | grep "inet "
```

You'll get something like `192.168.1.50`. Both the laptop and the iPad need
to be on the **same WiFi network** as each other and as the ESP32.

## 2. Start the complete prototype

From the project root, activate the virtual environment and start the app with
the ESP32 address printed in Thonny:

```bash
source .venv/bin/activate
ARM_WS=ws://192.168.1.198:8080/ws uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

`0.0.0.0` means "listen on every network interface" — so both `127.0.0.1`
(laptop) and `192.168.1.50` (from the iPad's perspective) can reach it.

The FastAPI app serves both the Blockly interface and WebSocket relay, so no
second frontend server is required.

## 3. Open it from the iPad/tablet

In Safari, go to:
```
http://192.168.1.50:8000
```
(your laptop's IP + the BlockBot port)

The status indicator should show **Robot connected**. Begin with small, safe
movements while supervising the arm.

## Checklist

- [ ] Laptop and iPad are on the same WiFi network
- [ ] ESP32 is also on that same WiFi network
- [ ] BlockBot started with `--host 0.0.0.0 --port 8000`
- [ ] `ARM_WS` points to the ESP32's current address
- [ ] Status indicator turns green when opened from the iPad
- [ ] Robot movements are supervised and remain within tested limits
