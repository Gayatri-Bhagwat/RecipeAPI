# tests/test_refresh_token.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient
from rest_framework import status

from core.models import RefreshToken
from user.utils.generate_token import generate_auth_token

User = get_user_model()

REFRESH_TOKEN_URL = reverse("user:refresh")


class RefreshTokenTestCase(TestCase):
    """Refresh token test case."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@gmail.com',
            password='testpass123'
        )
        self.access_token, self.refresh_token = generate_auth_token(self.user)

    def test_tokens_are_generated(self):
        """Both access and refresh tokens must be created."""
        self.assertIsNotNone(self.access_token)
        self.assertIsNotNone(self.refresh_token)

    def test_token_lengths_are_equal(self):
        """Access token and refresh token must be same length (40 chars)."""
        self.assertEqual(len(self.access_token.key), 40)
        self.assertEqual(len(self.refresh_token.token), 40)

    def test_refresh_token_is_not_revoked_on_creation(self):
        """Newly created refresh token should not be revoked."""
        self.assertFalse(self.refresh_token.is_revoked)

    def test_refresh_token_expiry_is_7_days(self):
        """Refresh token should expire in ~7 days."""
        expected_expiry = timezone.now() + timedelta(days=7)
        diff = abs((self.refresh_token.expires_at - expected_expiry).total_seconds())
        self.assertLess(diff, 5)  # within 5 seconds tolerance

    def test_generate_auth_token_rotates_on_duplicate(self):
        """Calling generate_auth_token again should rotate, not duplicate."""
        new_access, new_refresh = generate_auth_token(self.user)
        self.assertEqual(RefreshToken.objects.filter(user=self.user).count(), 1)
        self.assertNotEqual(new_refresh.token, self.refresh_token.token)

    def test_refresh_token_success(self):
        """Valid refresh token should return new access and refresh tokens."""
        response = self.client.post(REFRESH_TOKEN_URL, {
            'refresh_token': self.refresh_token.token
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.json())
        self.assertIn('refresh_token', response.json())

    def test_refresh_token_missing(self):
        """Request without refresh_token should return 400."""
        response = self.client.post(REFRESH_TOKEN_URL, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_token_invalid(self):
        """Invalid refresh token string should return 401."""
        response = self.client.post(REFRESH_TOKEN_URL, {
            'refresh_token': 'invalidtoken123'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_rotates_after_use(self):
        """Old refresh token should be invalid after being used once."""
        old_token = self.refresh_token.token

        # Use the refresh token
        self.client.post(REFRESH_TOKEN_URL, {'refresh_token': old_token})

        # Try using the same token again
        response = self.client.post(REFRESH_TOKEN_URL, {
            'refresh_token': old_token
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_new_access_token_is_different(self):
        """After refresh, new access token must differ from old one."""
        old_access = self.access_token.key
        response = self.client.post(REFRESH_TOKEN_URL, {
            'refresh_token': self.refresh_token.token
        })
        self.assertNotEqual(response.json()['access_token'], old_access)

    def test_expired_refresh_token_returns_401(self):
        """Expired refresh token should return 401."""
        self.refresh_token.expires_at = timezone.now() - timedelta(seconds=1)
        self.refresh_token.save()

        response = self.client.post(REFRESH_TOKEN_URL, {
            'refresh_token': self.refresh_token.token
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_is_expired_method_true(self):
        """is_expired() should return True for past expiry."""
        self.refresh_token.expires_at = timezone.now() - timedelta(days=1)
        self.refresh_token.save()
        self.assertTrue(self.refresh_token.is_expired())

    def test_is_expired_method_false(self):
        """is_expired() should return False for future expiry."""
        self.assertFalse(self.refresh_token.is_expired())

    def test_revoked_refresh_token_returns_401(self):
        """Revoked refresh token should return 401."""
        self.refresh_token.is_revoked = True
        self.refresh_token.save()

        response = self.client.post(REFRESH_TOKEN_URL, {
            'refresh_token': self.refresh_token.token
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_is_valid_false_when_revoked(self):
        """is_valid() should return False when revoked."""
        self.refresh_token.is_revoked = True
        self.refresh_token.save()
        self.assertFalse(self.refresh_token.is_valid())

    def test_is_valid_false_when_expired(self):
        """is_valid() should return False when expired."""
        self.refresh_token.expires_at = timezone.now() - timedelta(days=1)
        self.refresh_token.save()
        self.assertFalse(self.refresh_token.is_valid())

    def test_is_valid_true_when_active(self):
        """is_valid() should return True for active token."""
        self.assertTrue(self.refresh_token.is_valid())

    def test_refresh_token_expiring_within_7_days(self):
        """Token expiring within 7 days should trigger rotation."""
        self.refresh_token.expires_at = timezone.now() + timedelta(days=3)
        self.refresh_token.save()

        response = self.client.post(REFRESH_TOKEN_URL, {
            'refresh_token': self.refresh_token.token
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # New refresh token should be issued
        self.assertNotEqual(response.json()['refresh_token'], self.refresh_token.token)

    def test_expired_access_token_returns_401(self):
        """Expired access token on a protected endpoint should return 401."""
        # Backdating the token creation by 20 minutes
        self.access_token.created = timezone.now() - timedelta(minutes=20)
        self.access_token.save()

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.access_token.key}')
        response = self.client.get(reverse('recipe:tag-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_valid_access_token_returns_200(self):
        """Valid access token should pass authentication."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.access_token.key}')
        response = self.client.get(reverse('recipe:tag-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
