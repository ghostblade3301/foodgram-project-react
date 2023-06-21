from django.urls import path, include
from .views import RecipeViewSet
from rest_framework import routers
# from api.views import (
#     RecipeAPIList,
#     RecipeAPIUpdate,
#     UserAPIList,
#     RecipeAPIDetailView
#     )


app_name = 'api'

router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet)

# router = DefaultRouter()
# router.register('recipes', RecipeAPIView, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    # path('recipes/', RecipeViewSet.as_view({'get': 'list'})),
    # path('recipes/<int:pk>/', RecipeViewSet.as_view({'put': 'update'})),
    # path('users/', UserAPIList.as_view()),
    # path('recipe_detail/<int:pk>/', RecipeViewSet.as_view()),
]
