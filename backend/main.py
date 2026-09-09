import asyncio
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

    browser_send_lock = asyncio.Lock()
    tasks = []

    async def send_browser(message):
        async with browser_send_lock:
            await browser.send_json(message)

    async def browser_to_arm():
        while True:
            command = await browser.receive_json()
            if not isinstance(command, dict):
                await send_browser({'ok': False, 'error': 'Command must be an object.'})
                continue

            if command.get('cmd') != 'move':
                await send_browser({'ok': False, 'error': 'Unknown command.'})
                continue

            ok, message = check(command.get('channel'), command.get('angle'))
            if not ok:
                await send_browser({'ok': False, 'error': message})
                continue

            await arm_conn.send(json.dumps(command))
            log.append({'type': 'sent', 'command': command})
            await send_browser({'ok': True})

    async def arm_to_browser():
        while True:
            data = await arm_conn.recv()
            message = json.loads(data)
            if message.get('type') == 'positions':
                await send_browser(message)

    try:
        tasks = [
            asyncio.create_task(browser_to_arm()),
            asyncio.create_task(arm_to_browser()),
        ]
        done, _pending = await asyncio.wait(
            tasks, return_when=asyncio.FIRST_COMPLETED
        )
        for task in done:
            if task.cancelled():
                continue
            error = task.exception()
            if error:
                raise error
    except WebSocketDisconnect:
        pass
    except Exception:
        try:
            await send_browser({
                'ok': False,
                'error': 'The robot connection was lost.'
            })
        except Exception:
            pass
    finally:
        for task in tasks:
            task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        try:
            await arm_conn.close()
        except Exception:
            pass


app.mount('/', StaticFiles(directory=FRONTEND_DIR, html=True), name='frontend')
