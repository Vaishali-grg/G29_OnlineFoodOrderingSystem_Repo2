from django import forms
from .models import StoreMaterialType, StoreMaterial

class StoreMaterialTypeForm(forms.ModelForm):
    class Meta:
        model = StoreMaterialType
        fields = ['name', 'description', 'image_url']

class StoreMaterialForm(forms.ModelForm):
    class Meta:
        model = StoreMaterial
        fields = ['name', 'price', 'quantity', 'description', 'image_url']
