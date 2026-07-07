import json
import websockets
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from validator import check

ARM_WS = 'ws://192.168.1.198:8080/ws'
log: list[dict] = []

app = FastAPI()

@app.get('/health')
async def health():
    return {'status': 'ok'}

@app.get('/logs')
async def logs():
    return log

@app.websocket('/ws')
async def relay(browser: WebSocket):
    await browser.accept()

    # Try to connect to the arm first — tell the browser if it's unreachable
    try:
        arm_conn = await websockets.connect(ARM_WS)
    except Exception as e:
        await browser.send_json({'ok': False, 'error': f'Cannot reach arm: {e}'})
        await browser.close()
        return

    try:
        while True:
            command = await browser.receive_json()

            if command.get('cmd') == 'move':
                ok, message = check(command['channel'], command['angle'])
                if not ok:
                    await browser.send_json({'ok': False, 'error': message})
                    continue

            try:
                await arm_conn.send(json.dumps(command))
                log.append({'type': 'sent', 'command': command})
                await browser.send_json({'ok': True})
            except Exception as e:
                await browser.send_json({'ok': False, 'error': f'Arm connection lost: {e}'})
                break

    except WebSocketDisconnect:
        pass
    finally:
        await arm_conn.close()
