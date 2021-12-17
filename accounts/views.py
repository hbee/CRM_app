from django.shortcuts import render
from .models import *

def homeView(request):


    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()
    total_customers = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status='Pending').count()
    context = {
        'orders' : orders,
        'customers' : customers,
        'total_orders' : total_orders,
        'total_customers' : total_customers,
        'delivered' : delivered,
        'pending' : pending,
    }
    return render(request, 'accounts/home_dashboard.html', context)

def productsView(request):
    products = Product.objects.all()
    context = {
        'products' : products,
    }
    return render(request, 'accounts/products.html', context)

def customerView(request, pk):
    customer = Customer.objects.get(pk=pk)
    orders = customer.order_set.all()
    orders_count = orders.count()
    context = {
        'customer' : customer,
        'orders' : orders,
        'orders_count' : orders_count,
    }
    return render(request, 'accounts/customer.html', context)
