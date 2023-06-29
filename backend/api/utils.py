from django.db.models import Sum

from recipes.models import AmountIngredient, ShoppingCart


def create_ingredient_list(user):
    # Получаем список рецептов в корзине пользователя
    shopping_cart = ShoppingCart.objects.filter(user=user)
    recipe_ids = shopping_cart.values_list('recipe', flat=True)

    # Получаем ингредиенты и их количество для рецептов из списка покупок
    ingredients = AmountIngredient.objects.filter(
        recipe__in=recipe_ids
    ).values(
        'ingredient__name',
        'ingredient__measurement_unit'
    ).annotate(amount=Sum('amount'))

    # Создаем заголовок для списка покупок
    shopping_list_final = 'Shopping List\n'

    # Добавляем в список каждый ингредиент с его количеством и
    # единицами измерения
    for item in ingredients:
        ingredient_name = item['ingredient__name']
        measurement_unit = item['ingredient__measurement_unit']
        amount = item['amount']
        shopping_list_final += (
            f'{ingredient_name} '
            f'({measurement_unit}) {amount}\n'
        )
    return shopping_list_final
