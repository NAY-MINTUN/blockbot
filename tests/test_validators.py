import unittest

from fastapi.testclient import TestClient

from backend.main import app
from backend.validator import check


class ValidatorTests(unittest.TestCase):
    def test_accepts_safe_angle(self):
        self.assertEqual(check(0, 90), (True, 'ok'))

    def test_rejects_angle_outside_joint_limit(self):
        ok, message = check(1, 64)
        self.assertFalse(ok)
        self.assertIn('65', message)

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


if __name__ == '__main__':
    unittest.main()
