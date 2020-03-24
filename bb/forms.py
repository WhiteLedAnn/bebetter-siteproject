from django import forms
from .models import PostProduct
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match!")
    
    def clean_email(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).exclude(username=username).count():          
            raise forms.ValidationError("This email is already in use! Try another email.")
        return email
         
    def clean_username(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")        
        if username and User.objects.filter(username=username).exclude(email=email).count():
            raise forms.ValidationError("This username has already been taken!")
        return username
