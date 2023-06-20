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
        serializer.save()
        return Response({'post': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Method PUT not allowed'})

        try:
            instance = Recipe.objects.get(pk=pk)
        except:
            return Response({'error': 'Object does not exists'})

        serializer = RecipeSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post': serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Method PUT not allowed'})
        try:
            instance = Recipe.objects.get(pk=pk)
            instance.delete()
        except:
            return Response({'error': "Object does not exists"})
        return Response({'recipe': 'post ' + str(pk) + ' deleted'})
