from django.conf import settings
settings.configure()
from  rest_framework.test import APIClient
from accounts.models import UserData
from rest_framework import status
from django.test import TestCase
import pytest
client = APIClient()

@pytest.mark.django_db
def test_create_f1driver():
# #     response = client.post('/api/accounts/v1/register/',data={
# #     "email":"e@b.com",
# #     "name":"a",
# #     "password":"123456"
# # })
# #     assert response.status_code == 201
# #     f1driver = UserData.objects.first()
# #     assert f1driver is not None
# #
    client = APIClient()
    url = '/api/accounts/v1/register/'
    payload = {
    "email":"e@b.com",
    "name":"a",
    "password":"123456"
    }
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert UserData.objects.count() == 1




# فایل تست

from django.conf import settings
settings.configure()
from django.test import TestCase
from accounts.models import UserData
import django.contrib.auth.models
class UserDataTest(TestCase):
    def setUp(self):
        self.name = "John Doe"
        self.email = "johndoe@example.com"
        self.password = "testpassword"
        self.user = UserData.objects.create_user(
            name=self.name,
            email=self.email,
            password=self.password
        )

    def test_create_user(self):
        """
        این تست بررسی می‌کند که کاربر جدید به درستی ایجاد می‌شود.
        """
        self.assertEqual(self.user.name, self.name)
        self.assertEqual(self.user.email, self.email)
        self.assertTrue(self.user.check_password(self.password))
        self.assertFalse(self.user.is_admin)
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_edit_user(self):
        """
        این تست بررسی می‌کند که کاربر به درستی ویرایش می‌شود.
        """
        new_name = "Jane Doe"
        new_email = "janedoe@example.com"

        self.user.name = new_name
        self.user.email = new_email
        self.user.save()

        edited_user = UserData.objects.get(id=self.user.id)

        self.assertEqual(edited_user.name, new_name)
        self.assertEqual(edited_user.email, new_email)

    def test_superuser(self):
        """
        این تست بررسی می‌کند که کاربر مدیر سیستم به درستی ایجاد می‌شود.
        """
        superuser = UserData.objects.create_superuser(
            name="Super User",
            email="superuser@example.com",
            password="testpassword"
        )

        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)