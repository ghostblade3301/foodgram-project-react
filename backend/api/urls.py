from django.urls import include, path, re_path
from rest_framework import routers

from .views import IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)
router.register('users', UserViewSet)
router.register('ingredients', IngredientViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    re_path('auth/', include('djoser.urls.authtoken'))
]
