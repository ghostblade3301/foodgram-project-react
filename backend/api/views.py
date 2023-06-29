from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import exceptions, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.filters import FilterForIngredients, FilterForRecipes
from recipes.models import (Favorite, Ingredient, Recipe,
                            ShoppingCart, Tag)
from users.models import Follow

from .mixins import ListRetrieveMixin
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .utils import create_ingredient_list
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
        queryset = User.objects.filter(followings__user=user)
        # Разбиение результатов на страницы
        pages = self.paginate_queryset(queryset)
        serializer = self.serializer_class(
            pages, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=('post', 'delete'),
        serializer_class=SubscriptionSerializer
    )
    def subscribe(self, request, id=None):
        user = request.user
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
            raise exceptions.ValidationError(
                'Нельзя подписаться на самого себя')
        # Если подписка уже существует
        if follow_search.exists():
            # Выводим ошибку
            raise exceptions.ValidationError(
                'Вы уже подписались на этого пользователя')
        # Создание подписки
        Follow.objects.create(user=user, author=author)
        serializer = self.get_serializer(author)
        # Возвращение ответа с сериализованными данными
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_subscription(self, user, author, follow_search):
        # Если подписка не существует
        if not follow_search.exists():
            raise exceptions.ValidationError(
                'Вы еще не подписаны на этого пользователя')
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

    # Определяем, какой сериализатор использовать в зависимости от действия
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            # Сериализатор для просмотра списка и конкретного рецепта
            return GetRecipeSerializer
        # Сериализатор для создания и изменения рецепта
        return PostRecipeSerializer

    # Добавляем действие "favorite" для добавления рецепта в избранное
    @action(detail=True, methods=('POST', 'DELETE'),
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            error_message = 'Рецепт уже в избранном'
            return self.create_method(Favorite, pk, request, error_message)

        elif request.method == 'DELETE':
            error_message = 'Рецепт не в избранном'
            return self.delete_method(Favorite, pk, request, error_message)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Добавляем действие "shopping_cart" для добавления рецепта в корзину
    @action(detail=True, methods=('POST', 'DELETE'),
            permission_classes=[IsAuthenticated])
    # Определяем post или delete
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            error_message = 'Рецепт уже в корзине'
            return self.create_method(ShoppingCart, pk, request, error_message)
        elif request.method == 'DELETE':
            error_message = 'Рецепта нет в корзине'
            return self.delete_method(ShoppingCart, pk, request, error_message)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Добавляем действие "download_shopping_cart" для скачивания списка покупок
    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        shopping_list_final = create_ingredient_list(request.user)
        filename = 'shopping_list.txt'
        response = HttpResponse(
            shopping_list_final[:-1],
            content_type='text/plain',
        )
        response['Content-Disposition'] = ('attachment; filename={0}'
                                           .format(filename))
        return response
