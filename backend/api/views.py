from django.shortcuts import render
from recipes.models import (Favorite,
                            Ingredient,
                            Recipe,
                            AmountIngredient,
                            ShoppingCart,
                            Tag,
                            )
from users.models import User
from rest_framework import generics
from .serializers import RecipeSerializer, UserSerializer


class RecipeAPIView(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class UserAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    count = User.objects.count()
    serializer_class = UserSerializer
