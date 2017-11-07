import unittest
from app.models import User

class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password = 'nishisb89409578')
        self.assertIsNotNone(u.password_hash)

    def test_no_password_getter(self):
        u = User(password = 'nishisb89409578')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verication(self):
        u = User(password = 'nishisb89409578')
        self.assertTrue(u.verify_password('nishisb89409578'))
        self.assertFalse(u.verify_password('23333333'))

    def test_password_salts_are_random(self):
        u = User(password = 'nishisb89409578')
        u2 = User(password = 'nishisb89409578')
        self.assertTrue(u.password_hash != u2.password_hash)