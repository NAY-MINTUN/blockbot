import asyncio
import json
import os
import hashlib
import secrets
import sqlite3
import re
import socket
import math
from collections import deque
from pathlib import Path

import websockets
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi import Body
from fastapi.staticfiles import StaticFiles

from backend.validator import check


FRONTEND_DIR = Path(__file__).resolve().parent.parent / 'frontend'
log: deque[dict] = deque(maxlen=100)

app = FastAPI(title='BlockBot')

DB_PATH = Path(os.getenv('BLOCKBOT_DB', Path(__file__).resolve().parent / 'blockbot.sqlite3'))

def db():
    connection = sqlite3.connect(DB_PATH)
    connection.execute('CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, salt BLOB NOT NULL, password_hash BLOB NOT NULL)')
    connection.execute('CREATE TABLE IF NOT EXISTS sessions (token TEXT PRIMARY KEY, email TEXT NOT NULL REFERENCES users(email), created_at TEXT DEFAULT CURRENT_TIMESTAMP)')
    connection.execute('CREATE TABLE IF NOT EXISTS user_state (email TEXT PRIMARY KEY REFERENCES users(email), state TEXT NOT NULL DEFAULT \'{}\')')
    return connection

def session_email(token):
    if not token:
        return None
    with db() as connection:
        row = connection.execute('SELECT email FROM sessions WHERE token=?', (token,)).fetchone()
    return row[0] if row else None

@app.get('/api/state')
async def get_state(token: str):
    email = session_email(token)
    if not email:
        raise HTTPException(401, 'Please sign in again.')
    with db() as connection:
        row = connection.execute('SELECT state FROM user_state WHERE email=?', (email,)).fetchone()
    return json.loads(row[0]) if row else {'devices': [], 'program': None}

@app.put('/api/state')
async def put_state(payload: dict = Body(...), token: str = ''):
    email = session_email(token)
    if not email:
        raise HTTPException(401, 'Please sign in again.')
    state = {'devices': payload.get('devices', []), 'program': payload.get('program')}
    encoded = json.dumps(state)
    if len(encoded) > 1_000_000:
        raise HTTPException(413, 'Saved workspace is too large.')
    with db() as connection:
        connection.execute('INSERT INTO user_state(email,state) VALUES(?,?) ON CONFLICT(email) DO UPDATE SET state=excluded.state', (email, encoded))
    return {'ok': True}

@app.get('/api/devices/discover')
async def discover_devices(token: str):
    if not session_email(token):
        raise HTTPException(401, 'Please sign in again.')
    try:
        from zeroconf import ServiceBrowser, Zeroconf
    except ImportError:
        try:
            address = socket.gethostbyname('blockbot-arm.local')
            return {'devices': [{'name': 'BlockBot arm', 'address': f'ws://{address}:8080/ws', 'type': 'robot-arm'}], 'available': True}
        except OSError:
            return {'devices': [], 'available': False}
    found = []
    class Listener:
        def add_service(self, zc, service_type, name):
            info = zc.get_service_info(service_type, name)
            if info and info.port:
                address = info.parsed_addresses()[0] if info.parsed_addresses() else None
                if address:
                    found.append({'name': name.removesuffix('._blockbot._tcp.local.'), 'address': f'ws://{address}:{info.port}/ws', 'type': 'robot-arm'})
        def update_service(self, zc, service_type, name):
            self.add_service(zc, service_type, name)
        def remove_service(self, zc, service_type, name):
            pass
    zc = Zeroconf()
    browser = ServiceBrowser(zc, '_blockbot._tcp.local.', Listener())
    await asyncio.sleep(2.5)
    browser.cancel()
    zc.close()
    if not found:
        try:
            address = socket.gethostbyname('blockbot-arm.local')
            found.append({'name': 'BlockBot arm', 'address': f'ws://{address}:8080/ws', 'type': 'robot-arm'})
        except OSError:
            pass
    return {'devices': found, 'available': True}

@app.post('/api/auth/signup')
async def signup(payload: dict = Body(...)):
    email = str(payload.get('email', '')).strip().lower()
    password = payload.get('password', '')
    if not re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+', email):
        raise HTTPException(400, 'Enter a valid email address.')
    if not isinstance(password, str) or len(password) < 8:
        raise HTTPException(400, 'Password must be at least 8 characters.')
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    token = secrets.token_urlsafe(32)
    with db() as connection:
        try:
            connection.execute('INSERT INTO users(email,salt,password_hash) VALUES(?,?,?)', (email, salt, digest))
        except sqlite3.IntegrityError:
            raise HTTPException(409, 'An account with this email already exists.')
        connection.execute('INSERT INTO sessions(token,email) VALUES(?,?)', (token, email))
    return {'token': token, 'email': email}

@app.post('/api/auth/login')
async def login(payload: dict = Body(...)):
    email = str(payload.get('email', '')).strip().lower()
    password = payload.get('password', '')
    with db() as connection:
        row = connection.execute('SELECT salt,password_hash FROM users WHERE email=?', (email,)).fetchone()
        if not row or not isinstance(password, str):
            raise HTTPException(401, 'Email or password is incorrect.')
        digest = hashlib.scrypt(password.encode(), salt=row[0], n=2**14, r=8, p=1)
        if not secrets.compare_digest(digest, row[1]):
            raise HTTPException(401, 'Email or password is incorrect.')
        token = secrets.token_urlsafe(32)
        connection.execute('INSERT INTO sessions(token,email) VALUES(?,?)', (token, email))
    return {'token': token, 'email': email}

@app.post('/api/auth/logout')
async def logout(payload: dict = Body(...)):
    token = payload.get('token', '')
    with db() as connection:
        connection.execute('DELETE FROM sessions WHERE token=?', (token,))
    return {'ok': True}


@app.get('/health')
async def health():
    return {'status': 'ok'}


@app.websocket('/ws')
async def relay(browser: WebSocket):
    from urllib.parse import urlparse
    requested_arm = browser.query_params.get('device')
    arm_url = requested_arm or ''
    parsed = urlparse(arm_url)
    if parsed.scheme not in ('ws', 'wss') or not parsed.hostname:
        await browser.close(code=1008)
        return
    await browser.accept()

    email = session_email(browser.query_params.get('token'))
    if not email:
        await browser.close(code=1008)
        return
    try:
        limits = json.loads(browser.query_params.get('limits', 'null'))
    except ValueError:
        limits = None
    if not isinstance(limits, list) or len(limits) != 4:
        await browser.send_json({'ok': False, 'error': 'Set all robot joint limits before connecting.'})
        await browser.close(code=1008)
        return
    for channel, item in enumerate(limits):
        if (not isinstance(item, dict) or isinstance(item.get('min'), bool)
                or isinstance(item.get('max'), bool)
                or not isinstance(item.get('min'), (int, float))
                or not isinstance(item.get('max'), (int, float))
                or not math.isfinite(item['min']) or not math.isfinite(item['max'])
                or item['min'] < 0 or item['max'] > 180
                or item['min'] >= item['max']):
            await browser.send_json({'ok': False, 'error': 'Enter a minimum and maximum for every joint.'})
            await browser.close(code=1008)
            return

    try:
        arm_conn = await websockets.connect(arm_url, open_timeout=5)
        await arm_conn.send(json.dumps({'cmd':'configure_limits','limits':limits}))
    except Exception:
        try:
            await browser.send_json({
                'ok': False,
                'error': 'Cannot reach the robot. Check its power and Wi-Fi connection.'
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

            if command.get('cmd') in ('estop', 'reset_estop'):
                await arm_conn.send(json.dumps(command))
                log.append({'type': 'sent', 'command': command})
                await send_browser({'ok': True})
                continue

            if command.get('cmd') != 'move':
                await send_browser({'ok': False, 'error': 'Unknown command.'})
                continue

            custom_limits = browser.query_params.get('limits')
            limits = None
            if custom_limits:
                try:
                    import json as _json
                    limits = _json.loads(custom_limits)
                except (ValueError, TypeError):
                    limits = None
            ok, message = check(command.get('channel'), command.get('angle'), limits)
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
