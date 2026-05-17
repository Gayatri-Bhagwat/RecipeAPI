"""Views for user api"""
import os

import django

from rest_framework import generics, authentication, permissions
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.app.settings')
django.setup()


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class TokenUserView(ObtainAuthToken):
    """Login a user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user
