from django.shortcuts import render
from recipes.models import (Favorite,
                            Ingredient,
                            Recipe,
                            AmountIngredient,
                            ShoppingCart,
                            Tag,
                            )
from rest_framework import generics
from .serializers import RecipeSerializer


class RecipeAPIView(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
