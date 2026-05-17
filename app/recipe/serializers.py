"""Serializer for recipe API."""


from rest_framework import serializers

from core.models import Recipe, Tag, Ingredients


class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializers for uploading images."""
    class Meta:
        model = Recipe
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects."""
    class Meta:
        model = Ingredients
        fields = ['id', 'name']
        read_only_fields = ['id']


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag model."""
    class Meta:
        model = Tag
        fields = ['name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializers for Recipe model."""

    #  Link tags to recipe API.
    tag = TagSerializer(many=True, required=False)
    #  make tags as optional part of recipe.

    #  Link ingredients to recipe API.
    ingredient = IngredientSerializer(many=True, required=False)
    #  make ingredient as optional part of recipe.

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link',
                  'tag', 'ingredient', 'image', 'recipe_procedure']
        read_only_fields = ['id']

    @staticmethod
    def validate_recipe_procedure(value):
        """Validate recipe procedure."""
        if not isinstance(value, list):
            raise serializers.ValidationError("Instructions must be a list of steps.")
        for item in value:
            if 'text' not in item or 'title' not in item:
                raise serializers.ValidationError("Each step must have 'text'.")
        return value


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail."""
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']

    def _get_or_create_tags(self, tags, ingredients, recipe):
        """Handle getting or creating tags. """
        auth_user = self.context['request'].user
        for tag in tags:
            tag_exists = Tag.objects.filter(name=tag['name'], user=auth_user)
            if tag_exists.exists():
                recipe.tag.add(tag_exists[0])
            else:
                tag_obj, created = Tag.objects.get_or_create(
                    user=auth_user,
                    **tag
                )
                recipe.tag.add(tag_obj)
        for ingredient in ingredients:
            ingredient_exists = Ingredients.objects.filter(
                name=ingredient['name'],
                user=auth_user
            )
            if ingredient_exists.exists():
                recipe.ingredient.add(ingredient_exists[0])
            else:
                ingredient_obj, created = Ingredients.objects.get_or_create(
                    user=auth_user,
                    **ingredient
                )
                recipe.ingredient.add(ingredient_obj)

    def create(self, validated_data):
        """Create a recipe."""
        tags = validated_data.pop('tag', [])
        ingredients = validated_data.pop('ingredient', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        """Update a recipe to attach tag to recipe."""
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredient', None)
        if tags is not None:
            instance.tag.clear()
            self._get_or_create_tags(tags, ingredients, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
