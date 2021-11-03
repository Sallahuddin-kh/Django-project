from django.shortcuts import render
from .models import Customer, Product
from django.views import generic

class CustomerListView(generic.ListView):
    model = Customer

class ProductListView(generic.ListView):
    model = Product
