from django.shortcuts import render
from .models import Customer, Product, Country
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib import messages
import datetime

class CustomerListView(generic.ListView):
    model = Customer

class ProductListView(generic.ListView):
    model = Product

def insert_customer(request):
    country  = Country.objects.all()
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        shipping_address = request.POST.get("shipping_address")
        billing_address = request.POST.get("billing_address")
        ph_number = request.POST.get("ph_number")
        email = request.POST.get("email")
        selected_country  = request.POST.get("country")
        selected_country_obj = Country.objects.get(country_name = selected_country)
        created_at = request.POST.get("created_at")
        date_time_obj = datetime.datetime.strptime(created_at, '%Y-%m-%d')
        created_at_str = date_time_obj.strftime('%Y-%m-%d')
        updated_at = request.POST.get("updated_at")
        date_time_obj = datetime.datetime.strptime(updated_at, '%Y-%m-%d')
        updated_at_str = date_time_obj.strftime('%Y-%m-%d')
        if(created_at>updated_at):
            messages.warning(request, 'Updated Date larger than Creation Date')
        else:
            customer_instance = Customer(first_name=first_name,
            last_name=last_name,
            shipping_address=shipping_address,
            billing_address=billing_address,
            ph_number=ph_number,email=email,
            created_at=created_at_str,
            updated_at=updated_at_str,
            )
            customer_instance.counrty = selected_country_obj
            customer_instance.save()
            HttpResponseRedirect('/')
    return render(request,'theretailerapp/customer_signup_form.html', {'countries':country},)
