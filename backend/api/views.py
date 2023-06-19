from django.forms import model_to_dict
from recipes.models import Recipe
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RecipeSerializer


# class RecipeAPIView(generics.ListAPIView):
#     queryset = Recipe.objects.all()
#     serializer_class = RecipeSerializer


# class UserAPIView(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class RecipeAPIView(APIView):
    def get(self, request):
        w = Recipe.objects.all()
        return Response({'recipes': RecipeSerializer(w, many=True).data})

    def post(self, request):
        serializer = RecipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipe_new = Recipe.objects.create(
            name=request.data['name'],
            text=request.data['text'],
            cooking_time=request.data['cooking_time'],
            author_id=request.data['author_id']
        )
        return Response({'post': RecipeSerializer(recipe_new).data})
