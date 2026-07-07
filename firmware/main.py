import gc
import time
import network

WIFI_SSID = 'Ploy_2.4G'
WIFI_PASSWORD = 'ploy1234'

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

arm = Arm()
app = Microdot()

@app.get('/health')
async def health(request):
    return {'status': 'ok'}

@app.route('/ws')
@with_websocket
async def ws(request, ws):
    print('client connected')
    try:
        while True:
            data = await ws.receive()
            if data is None:
                break
            command = json.loads(data)
            print('got:', command)
            if command['cmd'] == 'move':
                arm.move(command['channel'], command['angle'])
            elif command['cmd'] == 'wait':
                await asyncio.sleep(command['second'])
    except Exception as e:
        print('error:', e)
    print('client disconnected')

try:
    app.run(host='0.0.0.0', port=8080)
except OSError:
    import machine
    machine.reset()
