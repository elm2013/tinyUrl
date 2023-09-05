from django.test import TestCase
from django.utils import timezone
from shortuuid import ShortUUID

from urls.models import URL
from accounts.models import UserData

class URLModelTestCase(TestCase):
    def setUp(self):
        self.user = UserData.objects.create_user(
            email='test@example.com',
            password='password',
            name='Test User'
        )
        self.url = URL.objects.create(
            original_url='http://example.com',
            expiration_date=timezone.now() + timezone.timedelta(days=7)
        )
        self.url.user.add(self.user)

    def test_url_is_expired(self):
        expired_url = URL.objects.create(
            original_url='http://example.com',
            expiration_date=timezone.now() - timezone.timedelta(days=1)
        )
        self.assertTrue(expired_url.is_expired())

    def test_url_save(self):
        self.assertIsNotNone(self.url.tiny_url)
        self.assertEqual(len(self.url.tiny_url), 8)

        self.assertEqual(self.url.user.count(), 1)
        self.assertEqual(self.url.user.first(), self.user)

class UserDataModelTestCase(TestCase):
    def setUp(self):
        self.user = UserData.objects.create_user(
            email='test@example.com',
            password='password',
            name='Test User'
        )

    def test_user_creation(self):
        self.assertEqual(UserData.objects.count(), 1)
        self.assertEqual(UserData.objects.first(), self.user)

        self.assertTrue(self.user.check_password('password'))
        self.assertFalse(self.user.check_password('incorrect_password'))

        self.assertEqual(str(self.user), 'Test User')