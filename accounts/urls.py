from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeView, name='home'),
    path('products/', views.productsView, name='products'),
    path('customer/<int:pk>/', views.customerView, name='customer'),

    path('customer_form/', views.AddCustomerView, name='AddCustomer'),
    path('update_order/<int:pk>/', views.UpdateOrder, name='UpdateOrder'),
    path('delete_order/<int:pk>/', views.DeleteOrder, name='DeleteOrder'),
    path('delete_customer/<int:pk>/', views.CustomerDelete.as_view(), name='DeleteCustomer'),


]