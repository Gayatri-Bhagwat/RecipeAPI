"""
Database models
"""

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
import uuid
import os

from django.utils import timezone


def recipe_image_file_path(instance, filename):
    """Generate path for new recipe image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'recipe', filename)


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extrafield):
        """create, saves and returns a new user"""
        if not email:
            raise ValueError("user must have an email address")
        user = self.model(email=self.normalize_email(email), **extrafield)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extrafield):
        """create a superuser"""

        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    headline = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    objects = UserManager()
    USERNAME_FIELD = "email"


class Recipe(models.Model):
    """Recipe Object."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=5)
    likes = models.IntegerField(default=0)
    servings = models.IntegerField(default=2)
    link = models.CharField(max_length=255, blank=True)
    tag = models.ManyToManyField('Tag')
    ingredient = models.ManyToManyField('Ingredients')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    recipe_procedure = models.JSONField(null=True, blank=True, default=list)

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tag Object. (for filtering recipes)"""
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    """Ingredients Object."""
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        """To define the models exact name."""
        verbose_name_plural = "Ingredients"


class RefreshToken(models.Model):
    """Refresh Token Object."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='refresh_token'
    )
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_revoked = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def is_valid(self):
        return not self.is_revoked and not self.is_expired()
