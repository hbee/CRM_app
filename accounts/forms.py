from django import forms
from .models import Order, Customer

class AddOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('customer', 'product', 'status')


class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email']

