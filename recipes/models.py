from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Единица измерения',
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
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
    )
    slug = models.CharField(
        verbose_name='Слаг тэга',
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
        verbose_name='Автор',
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipe_images/',
    )
    text = models.TextField(
        max_length=200,
        verbose_name='Описание',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        default=0,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        related_name='recipes',
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
