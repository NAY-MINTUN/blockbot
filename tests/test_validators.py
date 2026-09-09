import unittest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from backend.main import app
from backend.validator import check


class ValidatorTests(unittest.TestCase):
    def test_accepts_safe_angle(self):
        self.assertEqual(check(0, 90), (True, 'ok'))

    def test_identifies_joint_below_minimum_limit(self):
        ok, message = check(1, 39)
        self.assertFalse(ok)
        self.assertEqual(
            message,
            'In/Out joint angle 39° is below its minimum limit of 40°.',
        )

    def test_identifies_joint_above_maximum_limit(self):
        ok, message = check(2, 131)
        self.assertFalse(ok)
        self.assertEqual(
            message,
            'Up/Down joint angle 131° exceeds its maximum limit of 130°.',
        )

    def test_rejects_non_numeric_angle(self):
        self.assertEqual(check(2, '90'), (False, 'angle must be a number'))

    def test_rejects_boolean_channel(self):
        self.assertEqual(check(True, 90), (False, 'channel must be an integer'))


class AppTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health(self):
        self.assertEqual(self.client.get('/health').json(), {'status': 'ok'})

    def test_frontend_is_served(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('BlockBot', response.text)

    def test_relay_forwards_position_telemetry(self):
        class FakeArmConnection:
            def __init__(self):
                self.delivered = False

            async def recv(self):
                if not self.delivered:
                    self.delivered = True
                    return '{"type":"positions","angles":[90,82,80,120]}'
                raise RuntimeError('test connection closed')

            async def send(self, _message):
                pass

            async def close(self):
                pass

        connector = AsyncMock(return_value=FakeArmConnection())
        with patch('backend.main.websockets.connect', connector):
            with self.client.websocket_connect('/ws') as websocket:
                self.assertEqual(websocket.receive_json(), {
                    'type': 'positions',
                    'angles': [90, 82, 80, 120],
                })


if __name__ == '__main__':
    unittest.main()
