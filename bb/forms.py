from django import forms
from .models import PostProduct
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostProductForm(forms.ModelForm):
    class Meta:
        model = PostProduct
        fields = ('title', 'price', 'text', 'image', 'in_stock', 'published',)

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=100, help_text='Enter your username')
    email = forms.EmailField(max_length=150, help_text='Enter your email')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
