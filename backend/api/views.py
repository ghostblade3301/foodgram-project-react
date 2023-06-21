from recipes.models import Recipe, Tag
# from users.models import User
from .serializers import RecipeSerializer  # , UserSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    @action(methods=['get'], detail=True)
    def tag(self, request, pk=None):
        tag = Tag.objects.get(pk=pk)
        return Response({'tag': tag.name})

    @action(methods=['get'], detail=False)
    def tags(self, request):
        tags = Tag.objects.all()
        return Response({'tags': [tag.name for tag in tags]})

