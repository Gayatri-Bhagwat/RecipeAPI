"""
Django Admin Customization
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models
from core.models import Ingredients, Recipe, Tag


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ["id"]
    list_display = ['id',"email", "name", "headline"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },

        ),
        (_("Profile TagLine"), {"fields":("headline",)}),
        (_("Important dates"), {"fields": ("last_login",)}),
    )

    readonly_fields = ["last_login"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "headline"
                ),
            },
        ),
    )

@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Admin for recipe model."""
    list_display = ('id', 'user','title','description','link','recipe_procedure','created_at','updated_at')
    list_filter = ('title','price')
    search_fields = ['title','price','description']
    readonly_fields = ('created_at','updated_at')

    def get_queryset(self, request):
        """Return recipe data created by logged-in user."""
        return Recipe.objects.filter(user=request.user)

@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin for Tags model"""
    list_display = ['id', 'name', 'recipe_title','created_at','updated_at']
    list_filter = ['name']
    search_fields = ['name']
    readonly_fields = ('created_at','updated_at')

    @staticmethod
    def recipe_title(obj):
        """Return recipe_title linked to ingredients."""
        recipe_queryset = Recipe.objects.filter(tag = obj)
        return [recipe.title for recipe in recipe_queryset]

@admin.register(models.Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    """Admin for Ingredients model"""
    list_display = ['id', 'name','recipe_title','created_at','updated_at']
    list_filter = ['name']
    search_fields = ['name']
    readonly_fields = ('created_at','updated_at')

    @staticmethod
    def recipe_title(obj):
        """Return recipe_title linked to ingredients."""
        recipe_queryset = Recipe.objects.filter(ingredient = obj)
        return [recipe.title for recipe in recipe_queryset]



