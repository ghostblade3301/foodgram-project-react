from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        ingredients = cleaned_data.get('ingredients')
        if not ingredients:
            raise forms.ValidationError('Рецепт должен содержать хотя бы один ингредиент')
        return cleaned_data