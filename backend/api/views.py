from djoser.views import UserViewSet
from recipes.models import Recipe, Tag, Ingredient
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.models import User

from .mixins import ListRetrieveMixin
from .pagination import CustomPagination
from .serializers import (
    RecipeSerializer,
    UserSerializer,
    TagSerializer,
    IngredientSerializer
)


class IngredientViewSet(ListRetrieveMixin):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]


class TagViewSet(ListRetrieveMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AllowAny, )
    pagination_class = CustomPagination

    @action(methods=['get'], detail=True)
    def tag(self, request, pk=None):
        tag = Tag.objects.get(pk=pk)
        return Response({'tag': tag.name})

    @action(methods=['get'], detail=False)
    def tags(self, request):
        tags = Tag.objects.all()
        return Response({'tags': [tag.name for tag in tags]})


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
