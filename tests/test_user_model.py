import unittest
import time
from datetime import datetime
from app import create_app, db
from app.models import User, AnonymousUser, Role, Permission, Follow

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

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

    def test_roles_and_permissions(self):
        u = User(email='guo@example.com', password='dog')
        self.assertTrue(u.can(Permission.WRITE_ARTICLES))
        self.assertFalse(u.can(Permission.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))

    def test_timestamps(self):
        u = User(password='dog')
        db.session.add(u)
        db.session.commit()
        self.assertTrue(
            (datetime.utcnow() - u.member_since).total_seconds() < 3)
        self.assertTrue(
            (datetime.utcnow() - u.last_seen).total_seconds() < 3)

    def test_ping(self):
        u = User(password="cat")
        db.session.add(u)
        db.session.commit()
        time.sleep(2)
        last_seen_before = u.last_seen
        u.ping()
        self.assertTrue(u.last_seen > last_seen_before)

    def test_gravatar(self):
        u = User(email='guo@example.com', password='dog')
        with self.app.test_request_context('/'):
            gravatar = u.gravatar()
            gravatar_256 = u.gravatar(size=256)
            gravatar_pg = u.gravatar(rating='pg')
            gravatar_retro = u.gravatar(default='retro')
        with self.app.test_request_context('/', base_url='https://example.com'):
            gravatar_ssl = u.gravatar()
        self.assertTrue('http://www.gravatar.com/avatar/' +
                        '835c9208ed8a2f46dd3ccdd49693cbf8'in gravatar)
        self.assertTrue('s=256'in gravatar_256)
        self.assertTrue('r=pg'in gravatar_pg)
        self.assertTrue('d=retro'in gravatar_retro)
        self.assertTrue('https://secure.gravatar.com/avatar/' +
                        '835c9208ed8a2f46dd3ccdd49693cbf8' in gravatar_ssl)

    def test_follows(self):
        u1 = User(email='guo@example.com', password='cat')
        u2 = User(email='qu@example.com', password='dog')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertFalse(u1.is_followed_by(u2))
        timestamp_before = datetime.utcnow()
        u1.follow(u2)
        db.session.add(u1)
        db.session.commit()
        timestamp_after = datetime.utcnow()
        self.assertTrue(u1.is_following(u2))
        self.assertFalse(u1.is_followed_by(u2))
        self.assertTrue(u2.is_followed_by(u1))
        self.assertTrue(u1.followed.count() == 2)
        self.assertTrue(u2.followers.count() == 2)
        f = u1.followed.all()[-1]
        self.assertTrue(f.followed == u2)
        self.assertTrue(timestamp_before <= f.timestamp <= timestamp_after)
        f = u2.followers.all()[-1]
        self.assertTrue(f.follower == u1)
        u1.unfollow(u2)
        db.session.add(u1)
        db.session.commit()
        self.assertTrue(u1.followed.count() == 1)
        self.assertTrue(u2.followers.count() == 1)
        self.assertTrue(Follow.query.count() == 2)
        u2.follow(u1)
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        db.session.delete(u2)
        db.session.commit()
        self.assertTrue((Follow.query.count() == 1))