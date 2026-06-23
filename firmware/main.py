import gc
import time
import network
import asyncio
import json
import hashlib
import binascii
from servo import Arm

WIFI_SSID = 'Ploy_2.4G'
WIFI_PASSWORD = 'ploy1234'

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

arm = Arm()

async def handle(reader, writer):
    # Read HTTP upgrade request
    request = b''
    while b'\r\n\r\n' not in request:
        chunk = await reader.read(256)
        if not chunk:
            writer.close()
            return
        request += chunk

    # Find Sec-WebSocket-Key
    key = None
    for line in request.split(b'\r\n'):
        if line.lower().startswith(b'sec-websocket-key:'):
            key = line.split(b': ', 1)[1].strip()
            break

    if key is None:
        writer.close()
        return

    # Compute accept key
    d = hashlib.sha1(key)
    d.update(b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11')
    accept = binascii.b2a_base64(d.digest())[:-1]

    # Send 101 Switching Protocols
    writer.write(
        b'HTTP/1.1 101 Switching Protocols\r\n'
        b'Upgrade: websocket\r\n'
        b'Connection: Upgrade\r\n'
        b'Sec-WebSocket-Accept: ' + accept + b'\r\n\r\n'
    )
    await writer.drain()
    print('client connected')

    # Handle WebSocket frames
    while True:
        try:
            header = await reader.readexactly(2)
            opcode = header[0] & 0x0f
            has_mask = header[1] & 0x80
            length = header[1] & 0x7f

            if length == 126:
                length = int.from_bytes(await reader.readexactly(2), 'big')
            elif length == 127:
                length = int.from_bytes(await reader.readexactly(8), 'big')

            mask = await reader.readexactly(4) if has_mask else None
            payload = await reader.readexactly(length)

            if mask:
                payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))

            if opcode == 8:  # close
                break
            elif opcode == 1:  # text
                command = json.loads(payload.decode())
                print('got:', command)
                if command['cmd'] == 'move':
                    arm.move(command['channel'], command['angle'])
                elif command['cmd'] == 'wait':
                    await asyncio.sleep(command['second'])
        except Exception as e:
            print('error:', e)
            break

    writer.close()
    print('client disconnected')

async def main():
    server = await asyncio.start_server(handle, '0.0.0.0', 8080)
    print('server started')
    while True:
        await asyncio.sleep(60)

try:
    asyncio.run(main())
except OSError:
    import machine
    machine.reset()
