"""Views for user api"""
import os

import django
from django.contrib.auth import authenticate

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

import app.authentication
from core.models import RefreshToken
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import AllowAny

from user.utils.generate_token import generate_auth_token

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.app.settings')
django.setup()


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    permission_classes = [AllowAny]
    authentication_classes = [app.authentication.CustomAuthenticate]
    serializer_class = UserSerializer


class TokenUserView(ObtainAuthToken):
    """Login a user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):

        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=email, password=password)
        if not user:
            return Response({'error': 'Invalid credentials.'}, status=401)

        access_token, refresh_token = generate_auth_token(user)

        return Response({
            'access_token': access_token.key,  # ✅ DRF Token uses .key
            'refresh_token': refresh_token.token,
        })


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = [app.authentication.CustomAuthenticate]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class RefreshTokenView(APIView):
    """View set for refreshing an access token"""
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        refresh_token_value = request.data.get('refresh_token')

        if not refresh_token_value:
            return Response(
                {'error': 'refresh_token is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh_token = RefreshToken.objects.select_related('user').get(
                token=refresh_token_value
            )
        except RefreshToken.DoesNotExist:
            return Response(
                {'error': 'Invalid refresh token.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not refresh_token.is_valid():
            return Response(
                {'error': 'Refresh token expired or revoked. Please log in again.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        Token.objects.filter(user=refresh_token.user).delete()

        new_access_token, new_refresh_token = generate_auth_token(refresh_token.user)

        refresh_token.is_revoked = True
        refresh_token.save()

        return Response({
            'access_token': new_access_token.key,
            'refresh_token': new_refresh_token.token,
            'expires_in': '15 minutes',
        }, status=status.HTTP_200_OK)
