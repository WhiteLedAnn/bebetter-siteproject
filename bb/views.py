from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.utils import timezone
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic.edit import FormView
from django.template.loader import render_to_string
from django.db import IntegrityError
from .models import PostProduct
from .forms import PostProductForm
from .forms import SignUpForm
from .tokens import account_activation_token


class registration(FormView): # не используется
    form_class = UserCreationForm #форма для регистрации из коробки
    success_url = "/account/cabinet/"
    template_name = "registration/registration.html"
    def form_valid(self, form):
        form.save()
        return super(registration, self).form_valid(form)# передает выше
    def form_invalid(self, form):
        return super(registration, self).form_invalid(form)

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

@login_required
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

@login_required
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

@login_required
def products_draft_list(request):
    products = PostProduct.objects.filter(published=False).order_by('last_update_date')
    return render(request, 'products/products_draft_list.html', {'products': products})

@login_required
def product_publish(request, translit_title):
    product = get_object_or_404(PostProduct, translit_title=translit_title)
    product.publish()
    return redirect('product_detail', translit_title)

@login_required
def product_remove(request, translit_title):
    product = get_object_or_404(PostProduct, translit_title=translit_title)
    product.delete()
    return redirect('products_list')

def cabinet(request):
    """
    Функция отображения для кабинета пользовательницы.
    """
    # Отрисовка HTML-шаблона cabinet.html с данными внутри переменной контекста context
    return render(request, 'cabinet/cabinet.html', context = {})

def registration_view(request):
    if request.method  == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.username = form.cleaned_data.get('username')
            user.profile.email = form.cleaned_data.get('email')
            user.is_active = False # не может залогиниться пока не подтвердит ссылку
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            message = render_to_string('registration/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('activation_sent')
    else:
        form = SignUpForm()
        return render(request, 'registration/registration.html', {'form': form})

def activation_sent_view(request):
    return render(request, 'registration/activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token): 
        user.is_active = True
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'registration/activation_invalid.html')

# Create your views here.
"""
Создание представлений
"""
