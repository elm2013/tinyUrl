from django.conf import settings
settings.configure()
import pytest
from django.utils import timezone
from shortuuid import ShortUUID

from urls.models import URL
from accounts.models import UserData

@pytest.fixture
def user():
    return UserData.objects.create_user(
        email='test@example.com',
        password='password',
        name='Test User'
    )

@pytest.fixture
def url(user):
    return URL.objects.create(
        original_url='http://example.com',
        expiration_date=timezone.now() + timezone.timedelta(days=7)
    )

def test_url_is_expired(url):
    expired_url = URL.objects.create(
        original_url='http://example.com',
        expiration_date=timezone.now() - timezone.timedelta(days=1)
    )
    assert expired_url.is_expired()

def test_url_save(url):
    assert url.tiny_url is not None
    assert len(url.tiny_url) == 8

    assert url.user.count() == 1
    assert url.user.first() == user

def test_user_creation(user):
    assert UserData.objects.count() == 1
    assert UserData.objects.first() == user

    assert user.check_password('password')
    assert not user.check_password('incorrect_password')

    assert str(user) == 'Test User'