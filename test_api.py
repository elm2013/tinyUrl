from django.test import TestCase

# Create your tests here.

import pytest
from  rest_framework.test import APIClient
from accounts.models import UserData
from rest_framework import status
client = APIClient()

# @pytest.mark.django_db
# def test_create_f1driver():
# #     response = client.post('/api/accounts/v1/register/',data={
# #     "email":"e@b.com",
# #     "name":"a",
# #     "password":"123456"
# # })
# #     assert response.status_code == 201
# #     f1driver = UserData.objects.first()
# #     assert f1driver is not None
#
#     client = APIClient()
#     url = '/api/accounts/v1/register/'
#     payload = {
#     "email":"e@b.com",
#     "name":"a",
#     "password":"123456"
#     }
#     response = client.post(url, payload)
#     assert response.status_code == status.HTTP_201_CREATED
#     assert UserData.objects.count() == 1
#
# def test_greater():
#    num = 100
#    assert num > 100
#
# def test_greater_equal():
#    num = 100
#    assert num >= 100
#
# def test_less():
#    num = 100
#    assert num < 200