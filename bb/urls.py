from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.products_list, name='products_list'),
    path(r'<translit_title>', views.product_detail, name='product_detail'),
]
# =.= code by (ab)
"""pip install django-uuslug"""
