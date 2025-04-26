# yourapp/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# yourapp/forms.py
from django import forms
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']






from django import forms
from .models import Outlet, Menu

class OutletForm(forms.ModelForm):
    class Meta:
        model = Outlet
        fields = ['name','location','image_url']

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'description', 'price','image_url','preparation_time']



from django import forms
from .models import MenuItemRating

class MenuItemRatingForm(forms.ModelForm):
    class Meta:
        model = MenuItemRating
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'min': 1, 'max': 5, 'class': 'form-control', 'placeholder': 'Rate 1-5'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control', 'placeholder': 'Leave a comment (optional)', 'rows': 3
            }),
        }