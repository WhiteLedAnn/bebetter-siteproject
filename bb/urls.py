from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [  
    path('', views.products_list, name='products_list'),
    path(r'<translit_title>', views.product_detail, name='product_detail'),
    path('new/', views.new_product, name='new_product'),
    path(r'<translit_title>/edit/', views.product_edit, name='product_edit'),
    path('drafts/', views.products_draft_list, name='products_draft_list'),
    path(r'<translit_title>/publish/', views.product_publish, name='product_publish'),
    path(r'<translit_title>/remove/', views.product_remove, name='product_remove'),
]
# =.= code by (ab)
"""pip install django-uuslug"""
