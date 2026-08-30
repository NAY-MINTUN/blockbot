# Deploying BlockBot

BlockBot controls hardware on a private Wi-Fi network. The recommended
production setup is therefore a small always-on computer (a Raspberry Pi,
mini PC, or laptop) on the same network as the ESP32. It runs one BlockBot
service that serves both the web interface and the WebSocket relay.

Do not expose the ESP32 or the current BlockBot backend directly to the public
internet. The control socket does not yet have user authentication.

## 1. Prepare the firmware

Create the private Wi-Fi config file:

```bash
cp firmware/config.example.py firmware/config.py
```

Edit `firmware/config.py` with the Wi-Fi name and password, then upload
`config.py` together with the other firmware files in Thonny. The file is
ignored by Git, so the password will not be included in future commits.

Reset the ESP32 and write down the IP address printed in Thonny, for example
`192.168.1.198`.

## 2. Test the production service locally

From the project root, create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Start BlockBot with the address printed by the ESP32:

```bash
ARM_WS=ws://192.168.1.198:8080/ws uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000` on the computer. On a tablet connected to the
same Wi-Fi, open `http://LAPTOP_IP:8000`.

On macOS, find the laptop address with:

```bash
ipconfig getifaddr en0
```

The top-right status should say **Robot connected**. Test with small, safe
movements before building a longer program.

## 3. Run it continuously with Docker

Install Docker on the computer that will stay beside the robot, then run:

```bash
docker build -t blockbot .
docker run -d --name blockbot --restart unless-stopped \
  -p 8000:8000 \
  -e ARM_WS=ws://192.168.1.198:8080/ws \
  blockbot
```

Useful operating commands:

```bash
docker logs -f blockbot
docker restart blockbot
docker stop blockbot
```

If the ESP32 gets a different IP later, reserve its address in the router or
recreate the container with the new `ARM_WS` value.

## 4. Push the code to GitHub

Before pushing, rotate any Wi-Fi password that was previously committed. Then
review exactly what will be published:

```bash
git status
git diff --check
git diff
```

Stage the production changes explicitly so unrelated local files are not
published accidentally, then commit and push:

```bash
git add .gitignore .dockerignore Dockerfile DEPLOYMENT.md README.md \
  backend/main.py backend/validator.py \
  firmware/main.py firmware/config.example.py \
  frontend/app.js frontend/blockbot-logo.svg frontend/blocks.js frontend/favicon.svg \
  frontend/index.html frontend/style.css \
  tests/test_validators.py
git commit -m "Improve BlockBot UI and production setup"
git push origin main
```

If GitHub says the remote contains newer work, do not force-push. Run
`git pull --rebase origin main`, resolve any conflicts, test again, and push.

## Public internet access

A cloud host cannot normally connect to `192.168.x.x`; that address exists
only inside the robot's local network. A public deployment therefore needs an
additional authenticated outbound bridge or a private VPN. That bridge is not
implemented in this repository yet.

For now, keep the controller on a trusted LAN. Do not port-forward ports 8000
or 8080. Before public access is added, implement authentication, TLS, origin
checks, rate limits, and an emergency-stop command.

## Production checklist

- ESP32, host computer, and tablet are on the same trusted Wi-Fi.
- `firmware/config.py` exists on the ESP32 and is not tracked by Git.
- The ESP32 has a reserved IP address.
- `ARM_WS` points to that IP.
- `http://HOST_IP:8000/health` returns `{"status":"ok"}`.
- The UI reports **Robot connected**.
- Servo limits have been tested physically.
- The host automatically restarts the service after reboot.
- Ports 8000 and 8080 are not exposed to the public internet.
