from api.filters import FilterForIngredients, FilterForRecipes
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from rest_framework import exceptions, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from users.models import Follow

from .mixins import ListRetrieveMixin
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (GetRecipeSerializer, IngredientSerializer,
                          PostRecipeSerializer, ShortRecipeSerializer,
                          SubscriptionSerializer, TagSerializer,
                          UserSerializer)

User = get_user_model()


class IngredientViewSet(ListRetrieveMixin):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    filterset_class = FilterForIngredients


class TagViewSet(ListRetrieveMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated],
        serializer_class=SubscriptionSerializer
    )
    def subscriptions(self, request):
        user = request.user
        # Получение всех подписок пользователя
        favorites = user.followers.all()
        # Получение ID авторов подписок
        users_id = [favorite.author.id for favorite in favorites]
        # Получение всех пользователей по ID
        users = User.objects.filter(id__in=users_id)
        # Пагинация пользователей
        paginated_queryset = self.paginate_queryset(users)
        serializer = self.serializer_class(paginated_queryset, many=True)
        # Возвращение ответа с пагинацией
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=('post', 'delete'),
        serializer_class=SubscriptionSerializer
    )
    def subscribe(self, request, id=None):
        # Текущий пользователь
        user = request.user
        # Автор на которого подписываются
        author = get_object_or_404(User, pk=id)
        # Поиск подписки пользователя на автора
        follow_search = Follow.objects.filter(user=user, author=author)

        if request.method == 'POST':
            return self.create_subscription(user, author, follow_search)

        if request.method == 'DELETE':
            return self.delete_subscription(user, author, follow_search)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create_subscription(self, user, author, follow_search):
        # Если пользователь пытается подписаться на самого себя
        if user == author:
            raise exceptions.ValidationError('Cannot subscribe to yourself')
        # Если подписка уже существует
        if follow_search.exists():
            # Выводим ошибку
            raise exceptions.ValidationError(
                'You are already subscribed to this user.')
        # Создание подписки
        Follow.objects.create(user=user, author=author)
        serializer = self.get_serializer(author)
        # Возвращение ответа с сериализованными данными
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_subscription(self, user, author, follow_search):
        # Если подписка не существует
        if not follow_search.exists():
            raise exceptions.ValidationError(
                'You are not subscribed to this user yet.')
        # Удаление подписки
        Follow.objects.filter(user=user, author=author).delete()
        # Возвращение ответа без содержания (204 No Content)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteShoppingCart:
    @staticmethod
    def create_method(model, recipe_pk, request, error_message):
        # Текущий пользователь
        user = request.user
        # Рецепт, который добавляется в избранное
        recipe = get_object_or_404(Recipe, pk=recipe_pk)
        # Если рецепт уже находится в избранном у пользователя
        if model.objects.filter(recipe=recipe, user=user).exists():
            raise exceptions.ValidationError(error_message)
        # Добавление рецепта в избранное
        model.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(instance=recipe,
                                           context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_method(model, recipe_pk, request, error_message):
        user = request.user
        # Рецепт, который удаляется из избранного
        recipe = get_object_or_404(Recipe, pk=recipe_pk)
        # Если рецепт не находится в избранном у пользователя
        if not model.objects.filter(user=user, recipe=recipe).exists():
            raise exceptions.ValidationError(error_message)
        # Удаление рецепта из избранного
        model.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(ModelViewSet, FavoriteShoppingCart):
    queryset = Recipe.objects.all()
    pagination_class = CustomPagination
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = FilterForRecipes

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            # Сериализатор для просмотра списка и конкретного рецепта
            return GetRecipeSerializer
        # Сериализатор для создания и изменения рецепта
        return PostRecipeSerializer

    @action(detail=True, methods=('POST', 'DELETE'),
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            error_message = 'Recipe is already in favorites.'
            return self.create_method(Favorite, pk, request, error_message)

        elif request.method == 'DELETE':
            error_message = 'Recipe is not in favorites.'
            return self.delete_method(Favorite, pk, request, error_message)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=('POST', 'DELETE'),
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            error_message = 'Recipe is already in shopping cart.'
            return self.create_method(ShoppingCart, pk, request, error_message)
        elif request.method == 'DELETE':
            error_message = 'Recipe is not in shopping cart.'
            return self.delete_method(ShoppingCart, pk, request, error_message)
        return Response(status=status.HTTP_400_BAD_REQUEST)
