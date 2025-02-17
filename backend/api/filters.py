from django_filters import rest_framework

from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag


class FilterForRecipes(rest_framework.FilterSet):
    is_favorited = rest_framework.BooleanFilter(
        method='is_favorited_method',
    )
    is_in_shopping_cart = rest_framework.BooleanFilter(
        method='is_in_shopping_cart_method',
    )
    author = rest_framework.NumberFilter(
        field_name='author',
        lookup_expr='exact'
    )
    tags = rest_framework.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    def is_favorited_method(self, queryset, name, value):
        if self.request.user.is_anonymous:
            return Recipe.objects.none()

        favorites = (Favorite.objects.filter(user=self.request.user).
                     values_list('recipe_id', flat=True))
        if value:
            return queryset.filter(id__in=favorites)
        return queryset.exclude(id__in=favorites)

    def is_in_shopping_cart_method(self, queryset, name, value):
        if self.request.user.is_anonymous:
            return Recipe.objects.none()
        shopping_cart = (ShoppingCart.objects.filter(user=self.request.user).
                         values_list('recipe_id', flat=True))
        if value:
            return queryset.filter(id__in=shopping_cart)
        return queryset.exclude(id__in=shopping_cart)

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')


class FilterForIngredients(rest_framework.FilterSet):
    name = rest_framework.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)
