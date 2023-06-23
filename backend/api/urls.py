from django.urls import path, include, re_path
from .views import RecipeViewSet, UserViewSet, TagViewSet, IngredientViewSet
from rest_framework import routers
# from api.views import (
#     RecipeAPIList,
#     RecipeAPIUpdate,
#     UserAPIList,
#     RecipeAPIDetailView
#     )


app_name = 'api'

router = routers.DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'users', UserViewSet)
router.register(r'ingredients', IngredientViewSet)


# router = DefaultRouter()
# router.register('recipes', RecipeAPIView, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    re_path(r'auth/', include('djoser.urls.authtoken'))
]
