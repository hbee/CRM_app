from django.shortcuts import render, redirect
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import AddOrderForm, AddCustomerForm, CreateUserForm
from .filters import OrderFilter


def RegisterView(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, "Account was created successfully for " + username)
                return redirect('login')

        context = {
            'form' : form,
        }
        return render(request, 'accounts/register.html', context)


def LoginView(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect')

        return render(request, 'accounts/login.html')


def LogoutView(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
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
    last_5_orders = Order.objects.all().order_by('-Date_created')[:5]
    customers = Customer.objects.all()
    total_orders = orders.count()
    total_customers = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status='Pending').count()
    context = {
        'orders' : last_5_orders,
        'customers' : customers,
        'total_orders' : total_orders,
        'total_customers' : total_customers,
        'delivered' : delivered,
        'pending' : pending,
        'form' : form,
        'error': error,
    }
    return render(request, 'accounts/home_dashboard.html', context)


@login_required(login_url='login')
def productsView(request):
    products = Product.objects.all()
    context = {
        'products' : products,
    }
    return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
def customerView(request, pk):
    form = AddOrderForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
    customer = Customer.objects.get(pk=pk)
    orders = customer.order_set.all()
    orders_count = orders.count()
    orderFilter = OrderFilter(request.GET, queryset=orders)
    orders = orderFilter.qs
    context = {
        'form' : form,
        'customer' : customer,
        'orders' : orders,
        'orders_count' : orders_count,
        'orderFilter' : orderFilter,
    }
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
def AddCustomerView(request):
    form = AddCustomerForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form' : form}
    return render(request, 'accounts/customer_form.html', context)



class CustomerDelete(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = 'accounts/customer_delete.html'
    success_url = reverse_lazy('home')
    login_url = 'accounts/login.html'


@login_required(login_url='login')
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


@login_required(login_url='login')
def DeleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('home')

    context = {
        'order': order,
    }
    return render(request, 'accounts/delete.html', context)