import gc
import time
import network
import machine

try:
    from config import WIFI_PASSWORD, WIFI_SSID
except ImportError:
    WIFI_SSID = None
    WIFI_PASSWORD = None

# Connect WiFi before importing Microdot so the driver
# can allocate its rx buffers while heap is still free.
wlan = network.WLAN(network.STA_IF)
wlan.active(False)
time.sleep_ms(100)
wlan.active(True)
time.sleep_ms(200)
setup_mode = not WIFI_SSID
if not setup_mode and not wlan.isconnected():
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    timeout = time.ticks_add(time.ticks_ms(), 20000)
    while not wlan.isconnected() and time.ticks_diff(timeout, time.ticks_ms()) > 0:
        time.sleep_ms(250)
    setup_mode = not wlan.isconnected()
if setup_mode:
    setup_ap = network.WLAN(network.AP_IF)
    setup_ap.active(True)
    try:
        setup_ap.config(essid='BlockBot-Setup', password='blockbot')
    except Exception:
        setup_ap.config(essid='BlockBot-Setup')
    print('Setup Wi-Fi: BlockBot-Setup (password: blockbot), open http://192.168.4.1')
else:
    try:
        wlan.config(hostname='blockbot-arm')
    except Exception:
        pass
    print('IP:', wlan.ifconfig()[0])
    time.sleep(1)
gc.collect()

# Heavy imports after WiFi buffers are already allocated.
import asyncio
import json
from microdot import Microdot, Response
from microdot.websocket import with_websocket
from servo import Arm
from joystick import JoystickController

arm = Arm()
app = Microdot()
clients = []
emergency_stopped = False


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

@app.get('/')
async def setup_page(request):
    if not setup_mode:
        return {'name': 'BlockBot arm', 'setup': False}
    page = '''<!doctype html><meta name="viewport" content="width=device-width"><title>Set up BlockBot</title>
    <style>body{font:18px system-ui;max-width:480px;margin:40px auto;padding:18px;color:#172033}h1{color:#007ee9}label{display:block;margin:18px 0}input{box-sizing:border-box;width:100%;padding:12px;margin-top:6px}button{background:#007ee9;color:white;border:0;border-radius:10px;padding:13px 20px;font-size:17px}</style>
    <h1>Connect your BlockBot arm</h1><p>Enter your home Wi-Fi details. The arm will restart and join that network.</p>
    <form method="post" action="/setup"><label>Wi-Fi name<input name="ssid" required></label><label>Wi-Fi password<input name="password" type="password"></label><button>Connect</button></form>'''
    return Response(page, headers={'Content-Type': 'text/html; charset=utf-8'})

def form_value(body, key):
    def decode(value):
        raw = bytearray()
        index = 0
        while index < len(value):
            if value[index] == '+' :
                raw.append(32)
            elif value[index] == '%' and index + 2 < len(value):
                raw.append(int(value[index + 1:index + 3], 16))
                index += 2
            else:
                raw.append(ord(value[index]))
            index += 1
        return raw.decode('utf-8')

    for part in body.decode('ascii').split('&'):
        pair = part.split('=', 1)
        if len(pair) == 2 and pair[0] == key:
            return decode(pair[1])
    return ''

@app.post('/setup')
async def save_setup(request):
    if not setup_mode:
        return 'Setup is already complete.'
    ssid = form_value(request.body, 'ssid')
    password = form_value(request.body, 'password')
    if not ssid:
        return 'A Wi-Fi name is required.', 400
    with open('config.py', 'w') as config_file:
        config_file.write('WIFI_SSID = ' + repr(ssid) + '\nWIFI_PASSWORD = ' + repr(password) + '\n')
    async def restart():
        await asyncio.sleep(1)
        machine.reset()
    asyncio.create_task(restart())
    return 'Wi-Fi saved. The arm is restarting; reconnect your device to your home Wi-Fi.'

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

            global emergency_stopped

            if command.get('cmd') == 'configure_limits':
                try:
                    arm.configure_limits(command.get('limits'))
                    await send_positions()
                except Exception as error:
                    print('invalid joint limits:', error)
                continue

            if command['cmd'] == 'estop':
                emergency_stopped = True
                print('EMERGENCY STOP ACTIVATED')
                await send_positions()
                continue

            if command['cmd'] == 'reset_estop':
                emergency_stopped = False
                print('Emergency stop reset')
                continue

            if emergency_stopped:
                print('Ignoring command: emergency stop is active')
                continue
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
    await joysticks.calibrate()
    if not setup_mode:
        try:
            from mdns_client import Client
            from mdns_client.responder import Responder
            mdns = Client(wlan.ifconfig()[0])
            responder = Responder(mdns, own_ip=lambda: wlan.ifconfig()[0], host='blockbot-arm')
            responder.advertise('_blockbot', '_tcp', port=8080)
            print('Advertising BlockBot robot arm on the local network.')
        except ImportError:
            print('Service discovery is disabled; BlockBot hostname discovery is still available.')
    # Physical controls are local to the ESP32 and do not depend on Wi-Fi.
    # Arm starts with built-in safe ranges; a browser can replace them later.
    asyncio.create_task(joysticks.run())
    await app.start_server(host='0.0.0.0', port=8080)


try:
    asyncio.run(main())
except OSError:
    import machine
    machine.reset()
