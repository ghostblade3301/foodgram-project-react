from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (AmountIngredient, Favorite, Ingredient, Recipe,
                            ShoppingCart, Tag)
from rest_framework import exceptions, serializers
from users.models import Follow

User = get_user_model()


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ShortIngredientSerializerForRecipe(serializers.ModelSerializer):
    amount = serializers.IntegerField()
    id = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class UserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id',
            'username', 'first_name',
            'last_name', 'is_subscribed'
        )

    # Метод для получения значения поля is_subscribed
    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, author=obj.id).exists()


class UserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'email',
            'username', 'first_name',
            'last_name', 'password'
        )


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


# Сериализатор для получения ингредиента в рецепте
class GetIngredientInRecipeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()

    class Meta:
        model = AmountIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')

    # Методы для получения значений полей
    def get_name(self, obj):
        return obj.ingredient.name

    def get_id(self, obj):
        return obj.ingredient.id

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit

    def get_amount(self, obj):
        return obj.amount


class SubscriptionSerializer(serializers.ModelSerializer):
    recipes = ShortRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    # Методы для получения значений полей
    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def get_is_subscribed(self, obj):
        return True

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes',
                  "recipes", 'recipes_count')


# Сериализатор для получения рецепта
class GetRecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    # Методы для получения значений полей
    def get_ingredients(self, obj):
        recipe = obj
        ingredients = AmountIngredient.objects.filter(recipe=recipe)
        serializer = GetIngredientInRecipeSerializer(ingredients, many=True)
        return serializer.data

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return (ShoppingCart.objects.filter(user=request.user,
                                            recipe=obj.id).exists())

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return (Favorite.objects.filter(user=request.user,
                                        recipe=obj.id).exists())


# Сериализатор для создания и обновления рецепта
class PostRecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = ShortIngredientSerializerForRecipe(many=True)
    image = Base64ImageField()
    cooking_time = serializers.IntegerField()
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )

    # Валидация полей
    def validate_tags(self, tags):
        # Проверка наличия хотя бы одного тега
        if not tags:
            raise exceptions.ValidationError('There must be at least one tag.')
        return tags

    def validate_ingredients(self, ingredients):
        # Проверка наличия хотя бы одного ингредиента
        if not ingredients:
            raise exceptions.ValidationError(
                'There must be at least one ingredient.')
        # Проверка на наличие дубликатов ингредиентов
        ingredients_id_list = [ingredient['id'] for ingredient in ingredients]
        for ingredient_id in ingredients_id_list:
            if ingredients_id_list.count(ingredient_id) > 1:
                raise exceptions.ValidationError(
                    'A recipe cannot have two identical ingredients.')
        return ingredients

    def validate_cooking_time(self, cooking_time):
        # Проверка минимального времени приготовления
        if cooking_time <= 0:
            raise exceptions.ValidationError(
                'The minimum cooking time is 1 minute.')
        return cooking_time

    # Создание и обновление рецепта
    def create(self, validated_data):
        # Получение автора рецепта из контекста запроса
        author = self.context.get('request').user
        # Извлечение тегов и ингредиентов из валидированных данных
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        # Создание объекта рецепта и присвоение тегов
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)
        # Создание связей между рецептом и ингредиентами
        recipe_ingredients = []

        for ingredient in ingredients:
            amount = ingredient['amount']
            ingredient_instance = ingredient['id']
            ingredient = get_object_or_404(Ingredient, pk=ingredient_instance)

            recipe_ingredients.append(
                AmountIngredient(
                    recipe=recipe,
                    ingredient=ingredient,
                    amount=amount
                )
            )
        AmountIngredient.objects.bulk_create(recipe_ingredients)
        return recipe

    def update(self, instance, validated_data):
        # Обновление тегов рецепта при их наличии
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.set(tags)
        # Обновление ингредиентов рецепта при их наличии
        ingredients = validated_data.pop('ingredients', None)
        if ingredients is not None:
            instance.ingredients.clear()

            for ingredient in ingredients:
                amount = ingredient['amount']
                ingredient_instance = ingredient['id']
                ingredient = (get_object_or_404(Ingredient,
                                                pk=ingredient_instance))

                AmountIngredient.objects.update_or_create(
                    recipe=instance,
                    ingredient=ingredient,
                    amount=amount
                )
        # Вызов стандартного метода обновления для остальных полей
        return super().update(instance, validated_data)

    # Представление данных в виде объекта GetRecipeSerializer
    def to_representation(self, instance):
        serializer = GetRecipeSerializer(
            instance
        )
        return serializer.data

    class Meta:
        model = Recipe
        exclude = ('pub_date',)
