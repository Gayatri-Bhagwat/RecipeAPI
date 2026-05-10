"""Test whether filtered data is returned correctly."""
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from core.models import Ingredients, Tag, Recipe
from recipe.tests.test_ingredient_and_tags_apis import TestIngredientApis


class TestRecipeFilters(TestIngredientApis):
    """Test recipe filters api."""

    def setUp(self):
        """Test data to test filters."""
        super().setUp()
        self.ingredient_not_assignedTo_recipe = Ingredients.objects.create(name="Ingredient not assigned to any recipe.",
                                               user=self.user, created_at=timezone.now(), updated_at=timezone.now())
        self.tag_not_assignedTo_recipe = Tag.objects.create(name="Tag not assigned to any recipe.",
                                         user=self.user, created_at=timezone.now(), updated_at=timezone.now())

    def test_ingredient_search_works_as_expected(self):
        """Test whether search ingredient API returns expected data. [ingredient which is not assigned to any recipe and
        is created by logged-in user.]"""
        search = "Ingredient"
        url = reverse("recipe:ingredients-list",query={"search": search} )
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
        self.assertEqual(response.data[0]['name'], self.tag_not_assignedTo_recipe.name)

    def test_whether_tag_assigned_to_specific_recipe_are_returned_for_assigned_only_true(self):
        """Test whether list tag recipe returns tags assigned to some recipe when assigned only is true."""
        assigned_only = 'true'
        url = reverse("recipe:tag-list", query={"assigned_only":assigned_only})
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.tag.name, response.data[0]['name'])
        self.assertEqual(self.recipe.tag.first().name, response.data[0]['name'])

    def test_whether_ingredient_assigned_to_specific_recipe_are_returned_for_assigned_only_true(self):
        """Test whether list tag recipe returns tags assigned to some recipe when assigned only is true."""
        assigned_only = 'true'
        url = reverse("recipe:ingredients-list", query={"assigned_only":assigned_only})
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.ingredient.name, response.data[0]['name'])
        self.assertEqual(self.recipe.ingredient.first().name, response.data[0]['name'])

    def test_whether_assigned_only_and_search_works_as_expected(self):
        """Test whether API works correctly when both the params provided."""
        url = reverse('recipe:tag-list', query={
            'search' : 'Tag',
            'assigned_only': 'false'
        })
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], self.tag_not_assignedTo_recipe.name)
        self.assertFalse(Recipe.objects.filter(tag__id__in=[self.tag_not_assignedTo_recipe.id]).exists())

    def test_whether_recipe_data_is_returned_for_provided_tag_id(self):
        """Test whether correct recipe data is returned for the provided tag id."""
        url = reverse("recipe:recipe-list", query={
            'tag':[1]
        })
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], self.recipe.title)

    def test_whether_recipe_data_is_returned_for_provided_tag_and_ingredient_id(self):
        """Test whether correct recipe data is returned for the provided tag and ingredient id."""
        url = reverse("recipe:recipe-list", query={
            'tag': [1],
            'ingredient':[1]
        })
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], self.recipe.title)

    def test_whether_recipe_data_is_not_returned_for_the_tag_which_is_not_associated_to_anyRecipe(self):
        """Test whether empty recipe data is returned for the provided tag and ingredient id."""
        url = reverse("recipe:recipe-list", query={
            'tag': [2]
        })
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_search_filter_for_recipe_works_as_expected(self):
        """Test whether correct recipe is returned for the search data."""
        search = "test"
        url = reverse("recipe:recipe-list", query={"search":search})
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(self.recipe.title.__contains__(search), True)