from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import PostProduct
from .forms import PostProductForm

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

def new_product(request):
    if request.method == "POST":
        form = PostProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.first_appearance_date = timezone.now()
            product.save()
            translit_title = product.translit_title
            return redirect('product_detail', translit_title)
    else:
        form = PostProductForm()
    return render(request, 'products/new_product.html', {'form': form})

def product_edit(request, translit_title):
    post = get_object_or_404(PostProduct, translit_title=translit_title)
    if request.method == "POST":
        form = PostProductForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.first_appearance_date = timezone.now()
            post.save()
            return redirect('product_detail', translit_title=translit_title)
    else:
        form = PostProductForm(instance=post)
    return render(request, 'products/new_product.html', {'form': form})

# Create your views here.
"""
Создание представлений
"""
