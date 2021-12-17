from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeView, name='home'),
    path('products/', views.productsView, name='products'),
    path('customer/<int:pk>/', views.customerView, name='customer'),
]