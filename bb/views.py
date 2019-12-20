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
    products = PostProduct.objects.filter(last_update_date__lte=timezone.now()).exclude(published = False).order_by('last_update_date')
    return render(request, 'products/products_list.html', {'products' : products})

def product_detail(request, translit_title):
    product = get_object_or_404(PostProduct, translit_title=translit_title)
    return render(request, 'products/product_detail.html', {'product' : product})

def new_product(request):
    if request.method == "POST":
        form = PostProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            translit_title = product.translit_title
            return redirect('product_detail', translit_title)
    else:
        form = PostProductForm()
    return render(request, 'products/new_product.html', {'form': form})

def product_edit(request, translit_title):
    product = get_object_or_404(PostProduct, translit_title=translit_title)
    if request.method == "POST":
        form = PostProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('product_detail', translit_title=translit_title)
    else:
        form = PostProductForm(instance=product)
    return render(request, 'products/new_product.html', {'form': form})

def products_draft_list(request):
    products = PostProduct.objects.filter(published=False).order_by('last_update_date')
    return render(request, 'products/products_draft_list.html', {'products': products})

def product_publish(request, translit_title):
    product = get_object_or_404(PostProduct, translit_title=translit_title)
    product.publish()
    return redirect('product_detail', translit_title)

def product_remove(request, translit_title):
    product = get_object_or_404(PostProduct, translit_title=translit_title)
    product.delete()
    return redirect('products_list')

# Create your views here.
"""
Создание представлений
"""
