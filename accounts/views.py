from django.shortcuts import render

def homeView(request):
    return render(request, 'accounts/home_dashboard.html')

def productsView(request):
    return render(request, 'accounts/products.html')

def customerView(request):
    return render(request, 'accounts/customer.html')
