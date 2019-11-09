from django.shortcuts import render

def home(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Отрисовка HTML-шаблона home.html с данными внутри переменной контекста context
    return render(request, 'home.html', context = {})

def products_list(request):
    return render(request, 'products/products_list.html', {})

# Create your views here.
