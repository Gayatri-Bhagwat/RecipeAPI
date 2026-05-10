"""Test cases to test recipe ingredients apis."""
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag, Ingredients, Recipe
from user.tests.test_user_api import create_user


class TestIngredientApis(TestCase):
    """Test cases to test recipe ingredients apis."""
    def setUp(self):
        """Test data."""
        self.client = APIClient()
        self.user_data = {'email':'testIngredientUser@gmail.com', 'password':'Password313!','name':'testIngredientUser',
                          'created_at':timezone.now(),'updated_at':timezone.now()}
        self.user = create_user(**self.user_data)
        self.client.force_login(self.user)
        self.other_user_data = {'email':'testOtherUser@gmail.com', 'password':'OtherPassword313!','name':'testOtherUser',
                                'created_at':timezone.now(),'updated_at':timezone.now()}
        self.other_user = create_user(**self.other_user_data)
        self.client.force_login(self.other_user)
        self.tag = Tag.objects.create(name='testTag', user=self.user,created_at=timezone.now(), updated_at=timezone.now())
        self.ingredient = Ingredients.objects.create(name="testIngredient", user=self.user,
                        created_at=timezone.now(), updated_at=timezone.now())
        self.recipe = Recipe.objects.create(title="testRecipe", description="Recipe with tags and ingredient.",
                      time_minutes=7, price=60, user=self.user, link="test.link-2",
                      created_at=timezone.now(), updated_at=timezone.now())
        self.recipe.tag.add(self.tag)
        self.recipe.ingredient.add(self.ingredient)

        self.other_tag = Tag.objects.create(name="TestOtherTag", user=self.other_user,
                         created_at=timezone.now(), updated_at=timezone.now())
        self.other_ingredient = Ingredients.objects.create(name="TestOtherIngredient", user=self.other_user,
                                 created_at=timezone.now(), updated_at=timezone.now())
        self.other_recipe = Recipe.objects.create(title="testOtherRecipe", user=self.other_user,
                        description="Recipe created with other tags and ingredients", price=100,
                        link="test other - link2", time_minutes=9, created_at=timezone.now(), updated_at=timezone.now())
        self.other_recipe.tag.add(self.other_tag)
        self.other_recipe.ingredient.add(self.other_ingredient)

    def test_ingredient_list_api(self):
        """Test the ingredient list API."""
        url = reverse("recipe:ingredients-list")
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], self.ingredient.id)
        self.assertEqual(response.data[0]['name'], self.ingredient.name)

    def test_tags_list_apis(self):
        """Test the ingredient list API."""
        url = reverse("recipe:tag-list")
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], self.tag.id)
        self.assertEqual(response.data[0]['name'], self.tag.name)

    def test_ingredients_update_api(self):
        """Test the update ingredient api."""
        data = {
            'name':'updated-ingredient-name'
        }
        url = reverse("recipe:ingredients-detail", kwargs={"pk": self.ingredient.id})
        self.client.force_authenticate(self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])

    def test_tags_update_api(self):
        """Test the update ingredient api."""
        data = {
            'name': 'updated-tag-name'
        }
        url = reverse("recipe:tag-detail", kwargs={"pk": self.tag.id})
        self.client.force_authenticate(self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])

    def test_ingredients_delete_api(self):
        """Test ingredient delete api."""
        url = reverse("recipe:ingredients-detail", kwargs={"pk":self.ingredient.id})
        self.client.force_authenticate(self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ingredients.objects.filter(name=self.ingredient.name).exists())

    def test_tags_delete_api(self):
        """Test ingredient delete api."""
        url = reverse("recipe:tag-detail", kwargs={"pk": self.tag.id})
        self.client.force_authenticate(self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ingredients.objects.filter(name=self.tag.name).exists())

    def test_update_and_delete_recipe_throws_error_for_incorrect_tag_id(self):
        """Test update and delete recipe throws error for incorrect tag id"""
        data = {
            'name':'not-existing-tag'
        }
        url = reverse("recipe:tag-detail", kwargs={"pk":4})
        self.client.force_authenticate(self.user)
        response_update = self.client.put(url,data)
        response_delete = self.client.delete(url)
        self.assertEqual(response_update.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_delete.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_delete.json()['detail'],'No Tag matches the given query.')

    def test_whether_tags_created_by_logged_in_user_are_only_returned(self):
        """Test whether tags created by logged-in user are only returned."""
        url = reverse("recipe:tag-list")
        self.client.force_authenticate(self.other_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.other_tag.name, response.data[0]['name'])
        self.assertEqual(self.other_tag.id, response.data[0]['id'])





