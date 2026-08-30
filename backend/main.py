import json
import os
from collections import deque
from pathlib import Path

import websockets
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles

from backend.validator import check


ARM_WS = os.getenv('ARM_WS', 'ws://192.168.1.198:8080/ws')
FRONTEND_DIR = Path(__file__).resolve().parent.parent / 'frontend'
log: deque[dict] = deque(maxlen=100)

app = FastAPI(title='BlockBot')


@app.get('/health')
async def health():
    return {'status': 'ok'}


@app.websocket('/ws')
async def relay(browser: WebSocket):
    await browser.accept()

    try:
        arm_conn = await websockets.connect(ARM_WS, open_timeout=5)
    except Exception:
        try:
            await browser.send_json({
                'ok': False,
                'error': 'Cannot reach the robot. Check its power, Wi-Fi, and ARM_WS address.'
            })
            await browser.close()
        except Exception:
            pass
        return

    try:
        while True:
            command = await browser.receive_json()
            if not isinstance(command, dict):
                await browser.send_json({'ok': False, 'error': 'Command must be an object.'})
                continue

            if command.get('cmd') != 'move':
                await browser.send_json({'ok': False, 'error': 'Unknown command.'})
                continue

            ok, message = check(command.get('channel'), command.get('angle'))
            if not ok:
                await browser.send_json({'ok': False, 'error': message})
                continue

            try:
                await arm_conn.send(json.dumps(command))
                log.append({'type': 'sent', 'command': command})
                await browser.send_json({'ok': True})
            except Exception:
                try:
                    await browser.send_json({'ok': False, 'error': 'The robot connection was lost.'})
                except Exception:
                    pass
                break

    except WebSocketDisconnect:
        pass
    finally:
        try:
            await arm_conn.close()
        except Exception:
            pass


app.mount('/', StaticFiles(directory=FRONTEND_DIR, html=True), name='frontend')
