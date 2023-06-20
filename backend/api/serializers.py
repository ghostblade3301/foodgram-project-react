from rest_framework import serializers
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
from recipes.models import Recipe
from users.models import User


# class RecipeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Recipe
#         fields = '__all__'


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name')

# class RecipeModel:
#     def __init__(self, name, author, text, cooking_time):
#         self.name = name
#         self.author = author
#         self.text = text
#         self.cooking_time = cooking_time


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
