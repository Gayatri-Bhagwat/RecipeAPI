"""Test whether filtered data is returned correctly."""
from django.test import TestCase

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredients, Tag, Recipe
from user.tests.test_user_api import create_user


class TestRecipeFilters(TestCase):
    """Test recipe filters api."""

    def setUp(self):
        """Test data."""
        self.client = APIClient()
        self.user_data = {
            'email': 'testFilterUser@gmail.com',
            'password': 'Password313!',
            'name': 'testFilterUser',
            'created_at': timezone.now(),
            'updated_at': timezone.now()
        }
        self.user = create_user(**self.user_data)
        self.client.force_login(self.user)
        self.other_user_data = {
            'email': 'testFilterOtherUser@gmail.com',
            'password': 'OtherPassword313!',
            'name': 'testFilterOtherUser',
            'created_at': timezone.now(),
            'updated_at': timezone.now()
        }
        self.other_user = create_user(**self.other_user_data)
        self.client.force_login(self.other_user)
        self.tag = Tag.objects.create(
            name='testTag', user=self.user, created_at=timezone.now(), updated_at=timezone.now()
        )
        self.ingredient = Ingredients.objects.create(
            name="testIngredient", user=self.user, created_at=timezone.now(), updated_at=timezone.now()
        )
        self.recipe = Recipe.objects.create(
            title="testRecipe", description="Recipe with tags and ingredient.", time_minutes=7, price=60,
            user=self.user, link="test.link-2", created_at=timezone.now(), updated_at=timezone.now()
        )
        self.recipe.tag.add(self.tag)
        self.recipe.ingredient.add(self.ingredient)

        self.other_tag = Tag.objects.create(
            name="TestOtherTag", user=self.other_user, created_at=timezone.now(), updated_at=timezone.now()
        )
        self.other_ingredient = Ingredients.objects.create(
            name="TestOtherIngredient", user=self.other_user, created_at=timezone.now(), updated_at=timezone.now()
        )
        self.other_recipe = Recipe.objects.create(
            title="testOtherRecipe", user=self.other_user, description="Recipe created with other tags and ingredients",
            price=100, link="test other - link2", time_minutes=9, created_at=timezone.now(), updated_at=timezone.now()
        )
        self.other_recipe.tag.add(self.other_tag)
        self.other_recipe.ingredient.add(self.other_ingredient)
        self.ingredient_not_assignedTo_recipe = Ingredients.objects.create(
            name="Ingredient not assigned to any recipe.", user=self.user, created_at=timezone.now(),
            updated_at=timezone.now())
        self.tag_not_assignedTo_recipe = Tag.objects.create(
            name="Tag not assigned to any recipe.", user=self.user, created_at=timezone.now(), updated_at=timezone.now()
        )

    def test_ingredient_search_works_as_expected(self):
        """Test whether search ingredient API returns expected data. [ingredient which is not assigned to any recipe and
        is created by logged-in user.]"""
        search = "Ingredient"
        url = reverse("recipe:ingredients-list", query={"search": search})
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], self.ingredient_not_assignedTo_recipe.name)

    def test_tag_search_works_as_expected(self):
        """Test whether search tag API returns expected data. [tag which is not assigned to any recipe and
        is created by logged-in user.]"""
        search = "Tag"
        url = reverse("recipe:tag-list", query={"search": search})
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['name'], self.tag_not_assignedTo_recipe.name)

    def test_whether_tag_assigned_to_specific_recipe_are_returned_for_assigned_only_true(self):
        """Test whether list tag recipe returns tags assigned to some recipe when assigned only is true."""
        assigned_only = 'true'
        url = reverse("recipe:tag-list", query={"assigned_only": assigned_only})
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.tag.name, response.json()[0]['name'])
        self.assertEqual(self.recipe.tag.first().name, response.json()[0]['name'])

    def test_whether_ingredient_assigned_to_specific_recipe_are_returned_for_assigned_only_true(self):
        """Test whether list tag recipe returns tags assigned to some recipe when assigned only is true."""
        assigned_only = 'true'
        url = reverse("recipe:ingredients-list", query={"assigned_only": assigned_only})
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.ingredient.name, response.json()[0]['name'])
        self.assertEqual(self.recipe.ingredient.first().name, response.json()[0]['name'])

    def test_whether_assigned_only_and_search_works_as_expected(self):
        """Test whether API works correctly when both the params provided."""
        url = reverse('recipe:tag-list', query={
            'search': 'Tag',
            'assigned_only': 'false'
        })
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['name'], self.tag_not_assignedTo_recipe.name)
        self.assertFalse(Recipe.objects.filter(tag__id__in=[self.tag_not_assignedTo_recipe.id]).exists())

    def test_whether_recipe_data_is_not_returned_for_the_tag_which_is_not_associated_to_anyRecipe(self):
        """Test whether empty recipe data is returned for the provided tag and ingredient id."""
        url = reverse("recipe:recipe-list", query={
            'tag': [2]
        })
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

    def test_search_filter_for_recipe_works_as_expected(self):
        """Test whether correct recipe is returned for the search data."""
        search = "test"
        url = reverse("recipe:recipe-list", query={"search": search})
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(self.recipe.title.__contains__(search), True)
