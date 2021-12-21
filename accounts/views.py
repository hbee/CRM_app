from django.shortcuts import render, redirect
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from .models import *
from .forms import AddOrderForm, AddCustomerForm, CreateUserForm
from .filters import OrderFilter
from .decorators import is_user_authenticated, allowed_users

@is_user_authenticated
def RegisterView(request):
    form = CreateUserForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='client')
            user.groups.add(group)
            username = form.cleaned_data.get('username')
            customer_email = form.cleaned_data.get('email')
            Customer.objects.create(user=user, email=customer_email, name=username) #this creates a customer object for the user just created
            #tho it is better to use django signals if you want to create an instance of a model everytime an object of another model is created
            messages.success(request, "Account was created successfully for " + username)
            return redirect('login')

    context = {
        'form' : form,
    }
    return render(request, 'accounts/register.html', context)

@is_user_authenticated
def LoginView(request):
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

@login_required(login_url='login')
def LogoutView(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def homeView(request):
    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
    if group == 'admin':
        form = AddOrderForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                form.save()

        form = AddOrderForm()
        orders = Order.objects.all()
        last_5_orders = Order.objects.all().order_by('-Date_created')[:5]
        customers = Customer.objects.all()
        total_orders = orders.count()
        total_customers = orders.count()
        delivered = orders.filter(status="Delivered").count()
        pending = orders.filter(status='Pending').count()
        context = {
            'orders': last_5_orders,
            'customers': customers,
            'total_orders': total_orders,
            'total_customers': total_customers,
            'delivered': delivered,
            'pending': pending,
            'form': form,
        }
        return render(request, 'accounts/home_dashboard.html', context)
    else:
        return redirect('client')


@login_required(login_url='login')
@allowed_users(allowed=['admin'])
def productsView(request):
    products = Product.objects.all()
    context = {
        'products' : products,
    }
    return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
@allowed_users(allowed=['admin'])
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
@allowed_users(allowed=['admin'])
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
@allowed_users(allowed=['admin'])
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
@allowed_users(allowed=['admin'])
def DeleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('home')

    context = {
        'order': order,
    }
    return render(request, 'accounts/delete.html', context)

@login_required(login_url='login')
@allowed_users(allowed=['client'])
def ClientHomeView(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status="delivered").count()
    pending = orders.filter(status="pending").count()
    context = {
        'orders' : orders,
        'total_orders' : total_orders,
        'delivered' : delivered,
        'pending' : pending,
    }
    return render(request, 'accounts/client.html', context)


@login_required(login_url='login')
@allowed_users(allowed=['client'])
def AccountSettingsView(request):
    customer = request.user.customer
    form = AddCustomerForm(instance=customer)
    if request.method == 'POST':
        form = AddCustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/account_settings.html', context)