from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import PostProduct

def home(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Отрисовка HTML-шаблона home.html с данными внутри переменной контекста context
    return render(request, 'home.html', context = {})

def products_list(request):
    products = PostProduct.objects.filter(first_appearance_date__lte=timezone.now()).order_by('first_appearance_date')
    return render(request, 'products/products_list.html', {'products' : products})

def product_detail(request, translit_title):
    product = get_object_or_404(PostProduct, translit_title=translit_title)
    return render(request, 'products/product_detail.html', {'product' : product})

# Create your views here.
"""
Создание представлений
"""
