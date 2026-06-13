from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from user.utils.generate_token import ACCESS_TOKEN_LIFETIME


class CustomAuthenticate(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.select_related('user').get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        if not token.user.is_active:
            raise AuthenticationFailed('User is inactive.')

        token_age = timezone.now() - token.created
        if token_age > ACCESS_TOKEN_LIFETIME:
            raise AuthenticationFailed('Token has expired. Please refresh.')

        return token.user, token
