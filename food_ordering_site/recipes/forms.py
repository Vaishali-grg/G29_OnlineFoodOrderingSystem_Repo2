from django import forms
from .models import Recipe,Category

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 'category', 'image_url']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image_url'] 