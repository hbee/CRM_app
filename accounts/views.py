from django.shortcuts import render, redirect
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from .models import *
from .forms import AddOrderForm, AddCustomerForm

def homeView(request):
    error = None
    form = AddOrderForm(request.POST or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
            else:
                error = 'Customer couldn\'nt be added'
        except:
            error = 'Something went wrong'

    form = AddOrderForm()
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
        'form' : form,
        'error': error,
    }
    return render(request, 'accounts/home_dashboard.html', context)

def productsView(request):
    products = Product.objects.all()
    context = {
        'products' : products,
    }
    return render(request, 'accounts/products.html', context)

def customerView(request, pk):
    form = AddOrderForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
    customer = Customer.objects.get(pk=pk)
    orders = customer.order_set.all()
    orders_count = orders.count()
    context = {
        'form' : form,
        'customer' : customer,
        'orders' : orders,
        'orders_count' : orders_count,
    }
    return render(request, 'accounts/customer.html', context)

def AddCustomerView(request):
    form = AddCustomerForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form' : form}
    return render(request, 'accounts/customer_form.html', context)

class CustomerDelete(DeleteView):
    model = Customer
    template_name = 'accounts/customer_delete.html'
    success_url = reverse_lazy('home')


def UpdateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = AddOrderForm(instance=order)
    if request.method == 'POST':
        form = AddOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form' : form,
    }
    return render(request, 'accounts/order.html', context)

def DeleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('home')

    context = {
        'order': order,
    }
    return render(request, 'accounts/delete.html', context)