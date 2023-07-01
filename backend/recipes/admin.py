from django.contrib import admin

from .forms import RecipeForm
from .models import (Favorite, Ingredient, Recipe,
                     ShoppingCart, Tag, AmountIngredient)


class AmountIngredientInline(admin.TabularInline):
    model = AmountIngredient
    extra = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit'
    )
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug'
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'name',
        'text',
        'cooking_time',
    )
    form = RecipeForm
    list_filter = ('author__email', 'tags', 'name')
    search_fields = ('author__email', 'name',)
    inlines = [AmountIngredientInline]

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe'
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe'
    )
