from django import forms
from .models import PostProduct

class PostProductForm(forms.ModelForm):
    class Meta:
        model = PostProduct
        fields = ('title', 'price', 'text', 'image', 'in_stock', 'published',)
