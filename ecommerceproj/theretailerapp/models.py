from django.db import models
import uuid
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from datetime import datetime

class Country(models.Model):
    country_name = models.CharField(max_length=200, help_text='Enter a Country name')

    def __str__(self):
        return self.country_name

class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular customer across whole shop')
    first_name = models.CharField(max_length=20, help_text='Enter first name')
    last_name = models.CharField(max_length=20, help_text='Enter last name')
    shipping_address = models.CharField(max_length=200, help_text='Shipping Address')
    billing_address = models.CharField(max_length=200, help_text='Billing Address')
    password = models.CharField(max_length=50)
    ph_number = PhoneNumberField()
    email = models.EmailField(unique=True,max_length = 254)
    counrty = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True)
    created_at = models.DateField(null=True, blank=True)
    updated_at = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.first_name

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular product across whole shop')
    product_name = models.CharField(max_length=50, help_text='Enter first name')
    description = models.CharField(max_length=1000,help_text='Description of the product')
    price = models.FloatField()
    available_quantity = models.PositiveIntegerField()
    created_at = models.DateField(null=True, blank=True)
    updated_at = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default = True)
    def __str__(self):
        return self.product_name

class Basket(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)

class BasketItem(models.Model):
    basket = models.ForeignKey(Basket,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 1)

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('pending')
        DELIVERED = 'delivered', _('delivered')
        CANCELLED = 'cancelled', _('cancelled')
        APPROVED = 'approved', _('approved')

    status = models.CharField(max_length = 20, choices = Status.choices, default= Status.PENDING)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    created_at = models.DateTimeField(null=True, blank=True)
    order_shipping_address = models.CharField(max_length=200, help_text='Shipping Address')
    order_price = models.FloatField()
    updated_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        updated_at = datetime.now()
        updated_at_str = updated_at.strftime('%Y-%m-%d %H:%M:%S')
        super().save(*args, **kwargs)
        self.updated_at = updated_at_str
        
class OrderItem(models.Model):
     product = models.ForeignKey(Product,on_delete=models.CASCADE)
     order = models.ForeignKey(Order, on_delete=models.CASCADE)
