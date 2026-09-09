import gc
import time
import network

from config import WIFI_PASSWORD, WIFI_SSID

# Connect WiFi before importing Microdot so the driver
# can allocate its rx buffers while heap is still free.
wlan = network.WLAN(network.STA_IF)
wlan.active(False)
time.sleep_ms(100)
wlan.active(True)
time.sleep_ms(200)
if not wlan.isconnected():
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        pass
print('IP:', wlan.ifconfig()[0])
time.sleep(1)
gc.collect()

# Heavy imports after WiFi buffers are already allocated.
import asyncio
import json
from microdot import Microdot
from microdot.websocket import with_websocket
from servo import Arm
from joystick import JoystickController

arm = Arm()
app = Microdot()
clients = []


async def send_positions(positions=None, client=None):
    positions = positions or arm.positions()
    payload = json.dumps({'type': 'positions', 'angles': positions})
    targets = [client] if client else clients[:]
    stale = []

    for target in targets:
        try:
            await target.send(payload)
        except Exception:
            stale.append(target)

    for target in stale:
        if target in clients:
            clients.remove(target)


joysticks = JoystickController(arm, on_positions=send_positions)

@app.get('/health')
async def health(request):
    return {'status': 'ok'}

@app.route('/ws')
@with_websocket
async def ws(request, ws):
    print('client connected')
    clients.append(ws)
    try:
        await send_positions(client=ws)
        while True:
            data = await ws.receive()
            if data is None:
                break
            command = json.loads(data)
            print('got:', command)
            if command['cmd'] == 'move':
                arm.move(command['channel'], command['angle'])
                await send_positions()
            elif command['cmd'] == 'wait':
                await asyncio.sleep(command['second'])
    except Exception as e:
        print('error:', e)
    finally:
        if ws in clients:
            clients.remove(ws)
    print('client disconnected')

async def main():
    # Establish known, safe software and physical positions before accepting
    # either joystick or WebSocket movement commands.
    arm.home()
    await joysticks.calibrate()
    asyncio.create_task(joysticks.run())
    await app.start_server(host='0.0.0.0', port=8080)


try:
    asyncio.run(main())
except OSError:
    import machine
    machine.reset()
