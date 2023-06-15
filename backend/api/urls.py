from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import RecipeAPIView


app_name = 'api'

# router = DefaultRouter()
# router.register('recipes', RecipeAPIView, basename='recipes')

urlpatterns = [
    path('', RecipeAPIView.as_view()),
]
