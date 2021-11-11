from django.shortcuts import render
from .models import Customer, Product, Country
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib import messages
import datetime

class CustomerListView(generic.ListView):
    model = Customer

def product_list_view(request):
    products = Product.objects.all()
    context = {'product_list':products}
    return render(request, 'theretailerapp/product_list.html', context)

def insert_customer(request):
    country  = Country.objects.all()
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        shipping_address = request.POST.get("shipping_address")
        billing_address = request.POST.get("billing_address")
        ph_number = request.POST.get("ph_number")
        email = request.POST.get("email")
        if Customer.objects.filter(email = email).exists():
            messages.error(request,'Email Already exists')
            return render(request,'theretailerapp/customer_signup_form.html', {'countries':country},)
        selected_country  = request.POST.get("country")
        selected_country_obj = Country.objects.get(country_name = selected_country)
        created_at = datetime.date.today()
        created_at_str = created_at.strftime('%Y-%m-%d')
        try:
            customer_instance = Customer(first_name=first_name,
            last_name=last_name,
            shipping_address=shipping_address,
            billing_address=billing_address,
            ph_number=ph_number,email=email,
            created_at=created_at_str,
            updated_at=created_at_str,
            )
            customer_instance.counrty = selected_country_obj
            customer_instance.save()
        except Exception as e:
            print(e)
            messages.error(request,'System was not able to register try later')
        messages.success(request, 'Customer Accounted Created Succesfully.')
        return HttpResponseRedirect('/product')
    return render(request,'theretailerapp/customer_signup_form.html', {'countries':country},)

def login_customer(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        if Customer.objects.filter(email = email).exists():
            customer =  Customer.objects.get(email = email)
            request.session['does_exist'] = 'true'
            request.session['email'] = customer.email
            request.session['first_name'] = customer.first_name
            return HttpResponseRedirect('/product')
        else:
            messages.error(request,'User Does not exist')
    return render(request,'theretailerapp/customer_signin_form.html')

def customer_sign_out(request):
    request.session.flush()
    messages.success(request, 'Signed Out Successfully')
    return HttpResponseRedirect('/product')
    