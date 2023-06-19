from rest_framework import serializers
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
# from recipes.models import Recipe
# from users.models import User


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


class RecipeSerializer(serializers.Serializer):
    name = serializers.CharField()
    text = serializers.CharField()
    cooking_time = serializers.IntegerField()
    author = serializers.CharField()

# def encode():
#     model = RecipeModel('Жареная картошка', 1, 'Картошку порезать дольками и поджарить на сковороде', 15)
#     model_sr = RecipeSerializer(model)
#     print(model_sr.data, type(model_sr), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json, type(model_sr))


# def decode():
#     stream = io.BytesIO(b'{"name":"Grechka", "author":1, "text":"grechku pomyt i varit v kasrtryule", "cooking_time":15}')
#     data = JSONParser().parse(stream)
#     serializer = RecipeSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)
