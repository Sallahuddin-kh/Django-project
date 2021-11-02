from django.db import models
import uuid
from django.urls import reverse
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField

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
    ph_number = PhoneNumberField()
    email = models.EmailField(max_length = 254)
    counrty = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True)
    created_at = models.DateField(null=True, blank=True)
    updated_at = models.DateField(null=True, blank=True)

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular product across whole shop')
    product_name = models.CharField(max_length=50, help_text='Enter first name')
    description = models.CharField(max_length=1000,help_text='Description of the product')
    price = models.FloatField()
    available_quantity = models.PositiveIntegerField()
    created_at = models.DateField(null=True, blank=True)
    updated_at = models.DateField(null=True, blank=True)
