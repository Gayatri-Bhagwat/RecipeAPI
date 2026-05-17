"""Tests for user api"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED
from rest_framework.test import APIClient
from rest_framework import status
import json

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:login")
UPDATE_USER_URL = reverse("user:update")


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserAPITest(TestCase):
    """Test public user api test"""

    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'email': 'test2@example.com',
            'password': 'testhost313!',
            'name': 'test_user2'
        }
        self.user = create_user(**self.payload)

    def test_create_user_success(self):
        """Test creating user successful"""
        payload = {
            "email": "test@example.com",
            "password": "test@1234",
            "name": "test_user",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password, payload["password"])
        self.assertNotIn("password", res.data)

    def test_user_withEmail_exists(self):
        """Test user with email already exists"""
        payload = {
            "email": "test@example.com",
            "password": "test@1234",
            "name": "test_user",
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test password too short"""
        payload = {
            "email": "test@example.com",
            "password": "test",
            "name": "test_user",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload["email"]
        ).exists()
        self.assertFalse(user_exists)

    def test_token_retrieved_successfully(self):
        """Test token retrival is successful"""
        value = self.client.post(TOKEN_URL, self.payload)
        print(value)
        self.assertEqual(value.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(
            json.loads(value.content.decode('utf-8'))['token']
        )

    def test_token_not_retrieved(self):
        """Test token retrival is not successful"""
        payload = {
            'email': 'testnotuser@gmail.com',
            'password': 'testnotuser313!',
            'name': 'not_registered_user'
        }
        message = 'Unable to authenticate with provided credentials'
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(
            res.content.decode('utf-8'))['non_field_errors'][0],
            message
        )

    def test_user_is_updated_successfully(self):
        """Test whether user is updated successfully"""
        data = {
            'name': 'testdemouser2',
            'password': 'testpassword313!',
        }
        self.client.force_authenticate(self.user)
        res = self.client.patch(UPDATE_USER_URL, data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, data['name'])

    def test_post_endpoint_not_allowed_for_update_user(self):
        """Test post endpoint is not allowed to update user"""
        self.client.force_authenticate(self.user)
        res = self.client.post(UPDATE_USER_URL, {
            'name': 'abcd',
            'password': 'gettestuser231'
        })
        self.assertEqual(res.status_code, HTTP_405_METHOD_NOT_ALLOWED)
