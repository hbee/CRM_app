from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.homeView, name='home'),
    path('products/', views.productsView, name='products'),
    path('customer/<int:pk>/', views.customerView, name='customer'),

    path('customer_form/', views.AddCustomerView, name='AddCustomer'),
    path('update_order/<int:pk>/', views.UpdateOrder, name='UpdateOrder'),
    path('delete_order/<int:pk>/', views.DeleteOrder, name='DeleteOrder'),
    path('delete_customer/<int:pk>/', views.CustomerDelete.as_view(), name='DeleteCustomer'),

    path('register/', views.RegisterView, name='register'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),

    path('client/', views.ClientHomeView, name='client'),
    path('settings/', views.AccountSettingsView, name='settings'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_complete'),
]