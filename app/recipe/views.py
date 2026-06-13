"""Views for recipe API's"""

from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework import viewsets, status, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

import app.authentication
from core.models import Recipe, Tag, Ingredients
from recipe.serializers import RecipeSerializer, TagSerializer, IngredientSerializer, \
    RecipeImageSerializer, RecipeDetailSerializer


@extend_schema_view(
    list=extend_schema(
        description="List of all Tags/Ingredients based on the filter you applied.",
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.BOOL,
                description="Add 'True' if you want the tags/ingredients assigned "
                            "to some specific recipe.\n"
            ),
            OpenApiParameter(
                'search',
                OpenApiTypes.STR,
                description="Search term to filter recipes.\n"
            )
        ]
    )
)
class BaseRecipeAttrViewSet(
    mixins.ListModelMixin, mixins.DestroyModelMixin,
    mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    """Common view-set for tags and ingredients"""
    authentication_classes = [app.authentication.CustomAuthenticate]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return filtered queryset for authenticated user."""
        assigned_only = bool(
            self.request.query_params.get('assigned_only') == 'true'
        )
        search = self.request.query_params.get('search')
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)
        else:
            queryset = queryset.filter(recipe__isnull=True)

        if search:
            queryset = queryset.filter(name__icontains=search)

        if not search and not assigned_only:
            queryset = self.queryset
        return queryset.filter(user=self.request.user).order_by('-name').distinct()


@extend_schema_view(
    list=extend_schema(
        description="List of all Recipes based on the filter you applied.",
        parameters=[
            OpenApiParameter(
                'tag',
                OpenApiTypes.STR,
                description='Comma separated list of IDs to filter.\n',
            ),
            OpenApiParameter(
                'ingredient',
                OpenApiTypes.STR,
                description='Comma separated list of IDs to filter.\n',
            ),
            OpenApiParameter(
                'search',
                OpenApiTypes.STR,
                description='Search for specific Recipe title to Get Recipe Data.\n',
            ),
            OpenApiParameter(
                'prep_time',
                OpenApiTypes.STR,
                description='Get the list of All recipes with preparation '
                            'time less than or equal to given preparation time\n',
            )
        ]
    ),
)
class RecipeViewSet(viewsets.ModelViewSet):
    """Views for recipe API's"""
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [app.authentication.CustomAuthenticate]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def _params_to_ints(qs):
        """Convert the list of string to integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Return queryset for recipe view."""
        tags = self.request.query_params.get('tag', None)
        ingredients = self.request.query_params.get('ingredient', None)
        search = self.request.query_params.get("search", None)
        prep_time = self.request.query_params.get("prep_time", None)
        sort_by = self.request.query_params.get("sort_by", None)
        queryset = self.queryset
        tag_ids = []
        ingredient_ids = []
        if not tags and not ingredients:
            queryset = self.queryset
        else:
            if tags:
                tag_ids = self._params_to_ints(tags)
            if ingredients:
                ingredient_ids = self._params_to_ints(ingredients)
            if tags and ingredients:
                queryset = queryset.filter(
                    tag__id__in=tag_ids, ingredient__id__in=ingredient_ids
                )
            elif tags:
                queryset = queryset.filter(tag__id__in=tag_ids)
            else:
                queryset = queryset.filter(ingredient__id__in=ingredient_ids)
        if search:
            queryset = queryset.filter(title__icontains=search)
        if prep_time:
            queryset = self._filter_prep_time(prep_time, queryset)
        if sort_by:
            queryset = self._sort_queryset(sort_by, queryset)
        return queryset.filter(user=self.request.user).distinct()

    @staticmethod
    def _sort_queryset(sort_by, queryset):
        if sort_by == "asc":
            queryset = queryset.order_by("created_at")
        elif sort_by == "desc":
            queryset = queryset.order_by("-created_at")
        else:
            raise ValidationError(
                detail='sort_by must be "asc" or "desc"',
                code='invalid_sort_parameter'
            )
        return queryset

    @staticmethod
    def _filter_prep_time(prep_time, queryset):
        if prep_time == 'all':
            return queryset
        elif prep_time == "30":
            return queryset.filter(time_minutes__lte=prep_time)
        elif prep_time == "60":
            return queryset.filter(time_minutes__gte=30, time_minutes__lte=60)
        elif prep_time == "90":
            return queryset.filter(time_minutes__gte=90)
        return queryset

    def get_serializer_class(self):
        """Return  serializer class for recipe view."""
        if self.action == 'list':
            return RecipeSerializer
        elif self.action == 'upload_image':
            return RecipeImageSerializer

        return RecipeDetailSerializer

    def perform_create(self, serializer):
        """Create a new recipe instance."""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to recipe"""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(BaseRecipeAttrViewSet):
    """Views for Tag API"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [app.authentication.CustomAuthenticate]
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Views for Ingredient API"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [app.authentication.CustomAuthenticate]
    serializer_class = IngredientSerializer
    queryset = Ingredients.objects.all()
