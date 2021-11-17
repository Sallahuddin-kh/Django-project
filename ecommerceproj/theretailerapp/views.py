from django.shortcuts import render
from .models import Customer, Product, Country, Basket, BasketItem
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
    if 'email' in request.session:
        messages.warning(request,'Customer Already logged In. Sign Out to proceed')
        return HttpResponseRedirect('/product')
    country  = Country.objects.all()
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        shipping_address = request.POST.get("shipping_address")
        billing_address = request.POST.get("billing_address")
        ph_number = request.POST.get("ph_number")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password != confirm_password:
            messages.error(request,'Password and Confirm password do not match')
            return render(request,'theretailerapp/customer_signup_form.html', {'countries':country},)
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
            password = password,
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
    if 'email' in request.session:
        messages.warning(request,'Customer Already logged In')
        return HttpResponseRedirect('/product')
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        if Customer.objects.filter(email = email).exists():
            customer =  Customer.objects.get(email = email)
            if customer.password == password:
                request.session['email'] = customer.email
                request.session['first_name'] = customer.first_name
                return HttpResponseRedirect('/product')
            else:
                messages.error(request,'Incorrect password')
        else:
            messages.error(request,'Incorrect email')
    return render(request,'theretailerapp/customer_signin_form.html')

def customer_sign_out(request):
    request.session.flush()
    messages.success(request, 'Signed Out Successfully')
    return HttpResponseRedirect('/product')

def add_product_to_basket(request,id):
    if 'email' in request.session:
        customer_email= request.session['email']
        customer_obj = Customer.objects.get(email = customer_email)
        product_obj = Product.objects.get(id = id)
        if product_obj.available_quantity <= 0:
            msg = product_obj.product_name + ' Out of stock. Product not added to basket'
            messages.error(request, msg)
            return HttpResponseRedirect('/product')
        if not Basket.objects.filter(customer = customer_obj).exists():
            print("Creating new basket")  
            basket_instance = Basket(customer = customer_obj) 
            basket_instance.save()
        basket = Basket.objects.filter(customer = customer_obj).get()
        basket_item = BasketItem(basket = basket,product = product_obj,quantity = 1)
        basket_item.save()
        msg = product_obj.product_name + ' Added to basket successfully'
        messages.success(request, msg)
        return HttpResponseRedirect('/product')
    else:
        return HttpResponseRedirect('/customer/login')

def customer_basket(request):
    if 'email' in request.session:
        customer_email= request.session['email']
        customer_obj = Customer.objects.get(email = customer_email)
        if Basket.objects.filter(customer = customer_obj).exists():
            basket = Basket.objects.filter(customer = customer_obj).get()
            basket_items = BasketItem.objects.filter(basket = basket)
            return render(request,'theretailerapp/basket_list.html',{'items':basket_items})
        return render(request,'theretailerapp/basket_list.html')
    else:
        return HttpResponseRedirect('/customer/login')

def remove_product_from_basket(request,id):
    if 'email' in request.session:
        product_name = BasketItem.objects.filter(id=id).get().product.product_name
        msg = product_name + ' removed from basket successfully'
        BasketItem.objects.filter(id=id).delete()
        messages.success(request, msg)
        return HttpResponseRedirect('/basket')
    else:
        return HttpResponseRedirect('/customer/login')
