import unittest
import time
from app import create_app, db
from app.models import User

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

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

    def test_valid_confirmation_token(self):
        u = User(password = 'nishisb89409578')
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    def test_invalid_confirmation_token(self):
        u1 = User(password = 'nishisb89409578')
        u2 = User(password = 'cat')
        db.session.add(u1)
        db.session.add(u1)
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    def test_expired_confirmation_token(self):
        u = User(password = 'nishisb89409578')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(u.confirm(token))

    def test_valid_reset_token(self):
        u = User(password='nishisb89409578')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertTrue(u.reset_password(token, 'dog'))
        self.assertTrue(u.verify_password('dog'))

    def test_invalid_token(self):
        u1 = User(password='nishisb89409578')
        u2 = User(password='dog')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_reset_token()
        self.assertFalse(u2.reset_password(token, 'cat'))
        self.assertTrue(u2.verify_password('dog'))

    def test_valid_email_change_token(self):
        u = User(email='guo@example.com', password='nishisb89409578')
        db.session.add(u)
        db.session.commit()
        token = u.generate_email_change_token('qu@example.com')
        self.assertTrue(u.change_email(token))
        self.assertTrue(u.email == 'qu@example.com')

    def test_invalid_email_change_token(self):
        u1 = User(email='guo@example.com', password='dog')
        u2 = User(email='qu@example.com', password='cat')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_email_change_token('ziliang@example.com')
        self.assertFalse(u2.change_email(token))
        self.assertTrue(u2.email == 'qu@example.com')

    def test_duplicate_email_change_token(self):
        u1 = User(email='guo@example.com', password='dog')
        u2 = User(email='qu@example.com', password='cat')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u2.generate_email_change_token('guo@example.com')
        self.assertFalse(u2.change_email(token))
        self.assertTrue(u2.email == 'qu@example.com')