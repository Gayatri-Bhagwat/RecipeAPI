"""Class for testing recipe admin section and recipe API section."""
import json

from django.contrib.admin import AdminSite
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from core.admin import RecipeAdmin
from core.models import Recipe, Tag, Ingredients
from recipe.serializers import RecipeSerializer
from user.tests.test_user_api import create_user


class TestRecipeAdminSection(TestCase):
    """Class for testing recipe admin section."""
    def setUp(self):
        self.user_data = {
            'email': 'recipeTest@gmail.com',
            'password': 'RecipeTest123',
            'name': 'RecipeTestUser',
            'created_at': timezone.now(),
            'updated_at': timezone.now()
        }
        self.user = create_user(**self.user_data)
        self.user_two_data = {
            'email': 'recipeTest2@gmail.com',
            'password': 'RecipeTest2123!',
            'name': 'RecipeTestUser2',
            'created_at': timezone.now(),
            'updated_at': timezone.now()
        }
        self.user_two = create_user(**self.user_two_data)
        self.recipe = Recipe.objects.create(
            user=self.user, title="Recipe1", description="A refreshing drink", time_minutes=4, link="Link-1",
            price=25, created_at=timezone.now(), updated_at=timezone.now()
        )
        self.recipe2 = Recipe.objects.create(
            user=self.user_two, title="Recipe2", description="A refreshing drink made with coffee, suger, milk",
            time_minutes=4, link="Link-2", price=50, created_at=timezone.now(), updated_at=timezone.now()
        )
        self.client = APIClient()
        self.client.force_login(self.user)
        self.admin = AdminSite()
        self.create_recipe = reverse('recipe:recipe-list')
        self.recipe_admin = RecipeAdmin(Recipe, self.admin)

    def test_admin_section_contains_required_number_of_records(self):
        """Test admin section contains required number of records."""
        url = reverse('admin:core_recipe_changelist')
        response = self.client.get(url)
        view_list = self.recipe_admin.get_changelist_instance(response.wsgi_request)
        queryset = view_list.get_queryset(response.wsgi_request)
        self.assertEqual(queryset.count(), 1)

    def test_admin_section_contains_required_number_of_fields_in_list_display(self):
        """Test whether admin section has required fields for recipe models."""
        expected_fields = ['id', 'user', 'title', 'description', 'link', 'recipe_procedure', 'created_at', 'updated_at']
        actual_fields = self.recipe_admin.list_display
        self.assertEqual(list(actual_fields), expected_fields)

    def test_admin_section_contains_required_filters_in_list_display(self):
        """Test whether admin section has required filters for recipe models."""
        expected_filters = ['title', 'price']
        actual_filters = self.recipe_admin.list_filter
        self.assertEqual(list(actual_filters), expected_filters)

    def test_whether_view_form_displays_title_of_recipe(self):
        """Test whether admin view form displays title of the recipe. """
        self.assertEqual(str(self.recipe), self.recipe.title)

    def test_list_api_returns_recipe_list(self):
        """Test whether list api returns recipe list."""
        url = reverse('recipe:recipe-list')
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        recipe_serializer = RecipeSerializer(Recipe.objects.filter(user=self.user), many=True)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, recipe_serializer.data)

    def test_list_api_returns_none_for_unauthenticated_user(self):
        """Test whether list api returns None for unauthenticated user."""
        url = reverse('recipe:recipe-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_recipe_details_api_returns_expected_data(self):
        """Test whether recipe details api returns expected data."""
        url = reverse('recipe:recipe-detail', kwargs={'pk': self.recipe.id})
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], self.recipe.description)

    def test_recipe_details_api_returns_none_for_unauthenticated_user(self):
        """Test whether recipe details api returns None for unauthenticated user."""
        url = reverse('recipe:recipe-detail', kwargs={'pk': self.recipe.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_no_recipe_returns_for_unmatched_query(self):
        """Test whether no recipe returns when invalid id is provided."""
        url = reverse('recipe:recipe-detail', kwargs={'pk': 7})
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'].title(), 'No Recipe Matches The Given Query.')

    def test_create_recipe_api(self):
        """Test whether create recipe api creates new recipe."""
        data = {
            'title': 'New Recipe',
            'time_minutes': 20,
            'price': 35,
            'description': 'Good Option for Lunch/Dinner'
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(self.create_recipe, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        actual_response = response.json()
        self.assertEqual(actual_response['title'], data['title'])
        self.assertEqual(actual_response['time_minutes'], data['time_minutes'])

    def test_create_recipe_without_providing_mandatory_fields_throws_error(self):
        """Test whether create recipe API throws an error if mandatory fields are not provided."""
        data = {
            'time_minutes': 20,
            'price': 35,
            'description': 'Good Option for Lunch/Dinner'
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(self.create_recipe, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        actual_response = response.json()
        self.assertEqual(actual_response['title'], ["This field is required."])

    def test_recipe_is_updated(self):
        """Test whether the recipe is updated with the required fields."""
        data = {
            'title': 'Update Recipe',
            'price': self.recipe.price,
            'description': 'Good Option for Lunch/Dinner',
            'time_minutes': self.recipe.time_minutes,
        }
        self.client.force_authenticate(self.user)
        update_recipe = reverse("recipe:recipe-detail", kwargs={'pk': self.recipe.id})
        response = self.client.put(update_recipe, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], 'Update Recipe')
        self.assertEqual(response.json()['id'], self.recipe.id)

    def test_recipe_is_deleted(self):
        """Test whether the recipe is deleted with the required fields."""
        delete_recipe = reverse("recipe:recipe-detail", kwargs={'pk': self.recipe.id})
        self.client.force_authenticate(self.user)
        response = self.client.delete(delete_recipe)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=self.recipe.id).exists())

    def test_update_and_delete_recipe_throws_error_for_incorrect_recipe_id(self):
        """Test whether delete recipe throws error when incorrect recipe id."""
        delete_recipe = reverse("recipe:recipe-detail", kwargs={'pk': 4})
        update_recipe = reverse("recipe:recipe-detail", kwargs={'pk': 4})
        self.client.force_authenticate(self.user)
        response_delete = self.client.delete(delete_recipe)
        response_update = self.client.put(update_recipe)
        self.assertEqual(response_delete.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_delete.json()['detail'], 'No Recipe matches the given query.')
        self.assertEqual(response_update.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_update.json()['detail'], 'No Recipe matches the given query.')

    def test_whether_recipe_is_successfully_created_with_tags_and_ingredients(self):
        """Test whether image is successfully uploaded along with recipe"""
        data = {
            'title': 'New Recipe with tags',
            'time_minutes': 20,
            'price': 35,
            'description': 'Good Option for Lunch/Dinner',
            'tag': [{'name': 'new recipe tag'}],
            'ingredient': [{'name': 'masala'}, {'name': 'salt'}, {'name': 'oil'}]
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(self.create_recipe, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['title'], 'New Recipe with tags')
        self.assertTrue(Tag.objects.filter(name='new recipe tag').exists())
        self.assertTrue(Ingredients.objects.filter(name='masala').exists())
        created_recipe = Recipe.objects.filter(title=data['title']).first()
        self.assertEqual(created_recipe.tag.first().name, data['tag'][0]['name'])

    def test_recipe_procedure_is_added_to_recipe_object(self):
        """Test whether recipe procedure is added to the new recipe & recipe object is created successfully."""
        data = {
            'title': 'New recipe with detailed steps.',
            'time_minutes': 10,
            'price': 10,
            'description': 'Recipe with detailed steps..',
            'tag': [{'name': 'Spicy'}],
            'ingredient': [{'name': 'masala'}, {'name': 'salt'}, {'name': 'oil'}],
            'recipe_procedure': [
                {
                    "step": 1,
                    "title": "cutting",
                    "text": "Cut necessary veggies.",
                    "timer": 5,
                },
                {
                    "step": 2,
                    "title": "mixing",
                    "text": "mix necessary veggies & spices.",
                    "timer": 5,
                },
            ]
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(self.create_recipe, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.json()['recipe_procedure']), 2)
