"""Class to handle token generation. """
import secrets
from django.utils import timezone
from datetime import timedelta
from rest_framework.authtoken.models import Token

from core.models import RefreshToken

ACCESS_TOKEN_LIFETIME  = timedelta(seconds=30)
REFRESH_TOKEN_LIFETIME = timedelta(days=7)


def generate_auth_token(user):
    """Creates a new access + refresh token pair for the user."""
    Token.objects.filter(user=user).delete()
    access_token = Token.objects.create(user=user)

    # ✅ update_or_create handles rotation — is_revoked reset to False
    refresh_token, _ = RefreshToken.objects.update_or_create(
        user=user,
        defaults={
            'token': secrets.token_hex(20),
            'expires_at': timezone.now() + REFRESH_TOKEN_LIFETIME,
            'is_revoked': False,  # ✅ always reset to False
        }
    )

    return access_token, refresh_token
