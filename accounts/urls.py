from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeView, name='home'),
    path('products/', views.productsView, name='products'),
    path('customer/', views.customerView, name='customer'),
]