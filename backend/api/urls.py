from django.urls import path
from .views import RecipeAPIView  # , UserAPIView


app_name = 'api'

# router = DefaultRouter()
# router.register('recipes', RecipeAPIView, basename='recipes')

urlpatterns = [
    path('recipes/', RecipeAPIView.as_view()),
# path('users/', UserAPIView.as_view()),
]
