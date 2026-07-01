"""Views for user api"""
import os

import django
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

import app.authentication
from core.models import RefreshToken, User
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
            'user_name': user.name,
            'headline': user.headline
        })


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = [app.authentication.CustomAuthenticate]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


@extend_schema(
    description="API endpoint to refresh expired token.",
    request={
        "application/json": {
            'type': 'object',
            'properties': {
                'refresh_token': {'type': 'string', 'description': 'Refresh token.'},
            },
            'required': ['current_password', 'change_password'],
        }
    },
    responses={
        200: OpenApiResponse(description='Refresh token updated successfully.'),
        401: {
            OpenApiResponse(description='Refresh token expired or revoked.'),
            OpenApiResponse(description='Invalid refresh token.'),
        },
        400: OpenApiResponse(description="Refresh token is required"),

    }
)
class RefreshTokenView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        refresh_token_value = request.data.get('refresh_token')

        if not refresh_token_value:
            return Response({'error': 'refresh_token is required.'}, status=400)

        try:
            refresh_token = RefreshToken.objects.get(token=refresh_token_value)
        except RefreshToken.DoesNotExist:
            return Response({'error': 'Invalid refresh token.'}, status=401)

        if not refresh_token.is_valid():
            return Response({'error': 'Refresh token expired or revoked.'}, status=401)

        new_access_token, new_refresh_token = generate_auth_token(refresh_token.user)

        return Response({
            'access_token': new_access_token.key,
            'refresh_token': new_refresh_token.token,
        }, status=200)


@extend_schema(
    description="API endpoint to reset a user's password.",
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'current_password': {'type': 'string', 'description': 'Current password.'},
                'change_password': {'type': 'string', 'description': 'New password.'},
            },
            'required': ['current_password', 'change_password'],
        }
    },
    responses={
        200: OpenApiResponse(description='Password updated successfully.'),
        400: OpenApiResponse(description='Current password is incorrect.'),
        404: OpenApiResponse(description='No account found with this email.'),
    }
)
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        email = kwargs.get('email')
        if not email:
            return Response({'error': 'Email is required.'}, status=400)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'error': 'No account found with this email.'}, status=404)
        provided_current_password = self.request.data.get('current_password')
        provided_password = self.request.data.get('change_password')
        if not user.check_password(provided_current_password):
            return Response({'error': 'Current password is incorrect.'}, status=400)

        user.set_password(provided_password)
        user.save(update_fields=['password'])

        Token.objects.filter(user=user).delete()

        return Response({'message': 'Password updated successfully.'}, status=200)


@extend_schema(
    description="API endpoint to logout user.",
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'refresh_token': {'type': 'string', 'description': 'Refresh token.'},
            },
            'required': ['refresh_token'],
        }
    },
    responses={
        205: OpenApiResponse(description='Logged out successfully.'),
        400: {
            OpenApiResponse(description='Invalid or expired refresh token.'),
            OpenApiResponse(description='Refresh token is required'),
        }
    }
)
class LogOutView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @staticmethod
    def post(request, *args, **kwargs):
        """Log out user"""
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'refresh_token is required.'}, status=400)

        try:
            token = RefreshToken.objects.get(token=refresh_token)
            token.delete()
            return Response({'message': 'Logged out successfully.'}, status=205)
        except RefreshToken.DoesNotExist:
            return Response({'error': 'Invalid or expired refresh token.'}, status=400)
        except Exception as e:
            return Response({'error': f'An unexpected error occurred {e}'}, status=500)
