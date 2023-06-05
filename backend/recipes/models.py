from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
        blank=False,
    )
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Единица измерения',
        blank=False,
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'Ингредиент',
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Тэги рецептов"""
    name = models.CharField(
        max_length=200,
        verbose_name='Тэг',
        unique=True,
        blank=False,
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True,
        blank=False,
    )
    slug = models.CharField(
        max_length=200,
        verbose_name='Слаг тэга',
        unique=True,
        blank=False,
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'Тэг',
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Рецепт"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/',
    )
    text = models.TextField(
        max_length=200,
        verbose_name='Описание',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        default=1,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        related_name='recipes',
        through='recipes.AmountIngredient',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        related_name='recipes',
    )
    pub_date = models.DateField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Рецепт',
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class AmountIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='recipes',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        related_name='ingredients',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество',
    )

    def __str__(self):
        return (f'{self.ingredient.name} - {self.amount} {self.ingredient.measurement_unit}')


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_favorites',
        on_delete=models.CASCADE,
        verbose_name='Рецепты',
    )
    user = models.ForeignKey(
        User,
        related_name='user_favorites',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]

    def __str__(self):
        return f'Favorite: Пользователь {self.user.username}, рецепт {self.recipe.name}'


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_shopping_cart',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        related_name='user_shopping_cart',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'ShoppingCart: Пользователь {self.user.username}, рецепт {self.recipe.name}'
