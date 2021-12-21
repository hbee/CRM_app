from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    email = models.EmailField(max_length=30, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    profile_pic = models.ImageField(default='demo_user.png' ,null=True, blank=True)

    def __str__(self):
        return self.name or self.user.username


class Tag(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
    )

    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    category = models.CharField(max_length=100, null=True, choices=CATEGORY)
    tag = models.ManyToManyField(Tag)
    description = models.TextField(null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=100, null=True, choices=STATUS)
    Date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "Order n° " + str(self.id)