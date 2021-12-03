from django.shortcuts import render
from .models import  Customer, Product, Country, Basket, BasketItem, Order, OrderItem
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib import messages
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class CustomerListView(generic.ListView):
    model = Customer

def get_customer_object_from_session(request):
    customer_email= request.session['email']
    return Customer.objects.get(email = customer_email)

def product_list_view(request):
    product_list = Product.objects.filter(is_active = True)
    page = request.GET.get('page', 1)
    paginator = Paginator(product_list, 5)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
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
    del request.session['email']
    del request.session['first_name']
    messages.success(request, 'Signed Out Successfully')
    return HttpResponseRedirect('/product')

def add_product_to_basket(request,product_id):
    product_obj = Product.objects.get(id = product_id)
    available_quantity = product_obj.available_quantity
    if available_quantity <= 0:
        msg = product_obj.product_name + ' Out of stock. Product not added to basket'
        messages.error(request, msg)
        return HttpResponseRedirect('/product')
    if 'email' in request.session:
        customer_obj = get_customer_object_from_session(request)
        if not Basket.objects.filter(customer = customer_obj).exists():
            print("Creating new basket")  
            basket_instance = Basket(customer = customer_obj) 
            basket_instance.save()
        basket = Basket.objects.filter(customer = customer_obj).get()
        if BasketItem.objects.filter(basket=basket).filter(product = product_obj):
            basket_item = BasketItem.objects.filter(basket=basket).filter(product = product_obj).get()
            BasketItem.objects.filter(basket=basket).filter(product = product_obj).update(quantity = basket_item.quantity + 1)
        else:
            basket_item = BasketItem(basket = basket,product = product_obj,quantity = 1)
            basket_item.save()
        Product.objects.filter(id = product_id).update(available_quantity = available_quantity - 1)
        msg = product_obj.product_name + ' Added to basket successfully'
        messages.success(request, msg)
        return HttpResponseRedirect('/product')
    else:
        cart = request.session.get('cart')
        product_id_str  = str(product_id)
        if cart:
            quantity = cart.get(product_id_str)
            if quantity:
                cart[product_id_str] = quantity + 1
            else:
                cart[product_id_str] = 1
        else:
            cart = {}
            cart[product_id_str] = 1
        Product.objects.filter(id = product_id).update(available_quantity = available_quantity - 1)
        request.session['cart'] = cart
        msg = product_obj.product_name + ' Added to basket successfully'
        messages.success(request, msg)
        return HttpResponseRedirect('/product')

def customer_basket(request):
    cart = request.session.get('cart')
    if 'email' in request.session:
        basket_message = False
        if cart:
            basket_message = True
        customer_obj = get_customer_object_from_session(request)
        if Basket.objects.filter(customer = customer_obj).exists():
            basket = Basket.objects.filter(customer = customer_obj).get()
            basket_items = BasketItem.objects.filter(basket = basket)
            return render(request,'theretailerapp/basket_list.html',{'items':basket_items , 'basket_message' : basket_message})
        return render(request,'theretailerapp/basket_list.html',{'basket_message' : basket_message})
    else:
        if cart:
            keys = list(cart.keys())
            products = Product.objects.filter(id__in = keys)
            return render(request,'theretailerapp/basket_list.html',{'items':products})
        return render(request,'theretailerapp/basket_list.html')

def remove_product_from_basket(request,basketitem_id):
    if 'email' in request.session:
        basket_item= BasketItem.objects.filter(id=basketitem_id).get()
        product_name = basket_item.product.product_name
        product_id = basket_item.product.id
        product_quantity = basket_item.quantity
        available_quantity = Product.objects.filter(id = product_id).get().available_quantity
        Product.objects.filter(id = product_id).update(available_quantity = available_quantity +product_quantity)
        msg = product_name + ' removed from basket successfully'
        BasketItem.objects.filter(id=basketitem_id).delete()
        messages.success(request, msg)
        return HttpResponseRedirect('/basket')
    else:
        return HttpResponseRedirect('/customer/login')

def remove_product_from_session_basket(request,product_id):
    product_obj = Product.objects.get(id = product_id)
    available_quantity = product_obj.available_quantity
    cart = request.session.get('cart')
    product_id_str  = str(product_id)
    if cart:
        quantity = cart.get(product_id_str)
        cart.pop(product_id_str)
        Product.objects.filter(id = product_id).update(available_quantity = available_quantity + quantity)
    request.session['cart'] = cart
    return HttpResponseRedirect('/basket')

def convert_sessionbasket_to_tablebasket(request):
    if 'email' in request.session:
        customer_obj = get_customer_object_from_session(request)
        if not Basket.objects.filter(customer = customer_obj).exists():
            print("Creating new basket")  
            basket_instance = Basket(customer = customer_obj) 
            basket_instance.save()
        basket = Basket.objects.filter(customer = customer_obj).get()
        cart = request.session.get('cart')
        if cart:
            keys = list(cart.keys())
            for key in keys:
                product_obj = Product.objects.get(id = key)
                if BasketItem.objects.filter(basket = basket).filter(product = product_obj).exists():
                    basket_item = BasketItem.objects.filter(basket = basket).filter(product = product_obj).get()
                    quantity = basket_item.quantity + cart[key]
                    BasketItem.objects.filter(basket = basket).filter(product = product_obj).update(quantity = quantity)
                else:
                    basket_item = BasketItem(basket = basket,product = product_obj,quantity = cart[key])
                    basket_item.save()
            del request.session['cart']
    return HttpResponseRedirect('/basket')

def calculate_basket_total_price(basket_items):
    total_price = 0
    for item in basket_items:
        for i in range(item.quantity):
            total_price = total_price + item.product.price
    return total_price

def place_order_form(request):
    if 'email' in request.session:
        customer_obj = get_customer_object_from_session(request)
        basket = Basket.objects.filter(customer = customer_obj).get()
        basket_items = BasketItem.objects.filter(basket = basket)
        default_shipping_address = customer_obj.shipping_address
        total_price = calculate_basket_total_price(basket_items)
        if request.method == 'GET':
            return render(request,'theretailerapp/order_confirmation.html',{'items':basket_items,
                                                                            'shipping_address':default_shipping_address,
                                                                            'total_price':total_price})
        elif request.method == 'POST':
            order_address = request.POST.get("shipping_address")
            placed_at = datetime.datetime.now()
            placed_at_str = placed_at.strftime('%Y-%m-%d %H:%M:%S')
            order_instance = Order(customer = customer_obj,
                                    created_at = placed_at_str,
                                    updated_at = placed_at_str,
                                    order_shipping_address = order_address,
                                    order_price = total_price,
                                    status = 'pending')
            order_instance.save()
            for item in basket_items:
                product = item.product
                for i in range(item.quantity):
                    order_item_instance = OrderItem(product=product, order = order_instance)
                    order_item_instance.save()
                item.delete()
            basket.delete()
            messages.success(request, "Order Placed")
            return HttpResponseRedirect('/basket')
    else:
        return HttpResponseRedirect('/customer/login')

def show_customer_orders(request):
    if 'email' in request.session:
        customer_obj = get_customer_object_from_session(request)
        order_list = Order.objects.filter(customer = customer_obj)
        start_date ='' 
        end_date = ''
        page = request.GET.get('page', 1)
        paginator = Paginator(order_list, 5)
        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)
        return render(request,'theretailerapp/order_list.html', {'order_list' :  orders,
                                                                'start_date':start_date,
                                                                'end_date':end_date})
    else:
        return HttpResponseRedirect('/customer/login')

def show_order_details(request,order_id):
    if 'email' in request.session:
        order_items = OrderItem.objects.filter(order = order_id)
        order = Order.objects.get(id = order_id)
        return render(request,'theretailerapp/order_details.html', {'product_list' :  order_items, 'order': order})
    else:
        return HttpResponseRedirect('/customer/login')

def cancel_order(request,order_id):
    if 'email' in request.session:
        updated_at = datetime.datetime.now()
        updated_at_str = updated_at.strftime('%Y-%m-%d %H:%M:%S')
        Order.objects.filter(id = order_id).update(status = 'cancelled', updated_at = updated_at_str)
        order = Order.objects.filter(id = order_id).get()
        order_items = OrderItem.objects.filter(order = order)
        for item in order_items:
            available_quantity = Product.objects.filter(id = item.product.id).get().available_quantity
            Product.objects.filter(id = item.product.id).update(available_quantity = available_quantity + 1)
        messages.warning(request,'Order Cancelled')
        return HttpResponseRedirect('/order')
    else:
        return HttpResponseRedirect('/customer/login')

def filter_orders(request):
    if 'email' in request.session:
        from_date = request.GET.get('from_filter_date')
        to_date = request.GET.get('to_filter_date')
        status = request.GET.get('status')
        customer_obj = get_customer_object_from_session(request)
        order_list = Order.objects.filter(customer = customer_obj)
        if(from_date != '' and to_date != ''):
            order_list = order_list.filter(created_at__range=[from_date, to_date])
        if status != 'None':
            order_list = order_list.filter(status = status)
        page = request.GET.get('page', 1)
        paginator = Paginator(order_list, 5)
        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)
        return render(request,'theretailerapp/order_list_filter.html', {'order_list' :  orders,
                                                                'start_date':from_date,
                                                                'end_date':to_date,
                                                                'status' : status})
    else:
        return HttpResponseRedirect('/customer/login')

def increase_basket_item_quantity(request,product_id):
    add_product_to_basket(request,product_id)
    return HttpResponseRedirect('/basket')

def decrease_basket_item_quantity(request,product_id):
    product_obj = Product.objects.get(id = product_id)
    if 'email' in request.session:
        customer_obj = get_customer_object_from_session(request)
        basket = Basket.objects.filter(customer = customer_obj).get()
        basket_item = BasketItem.objects.filter(basket = basket).filter(product = product_obj).get()
        quantity = basket_item.quantity - 1
        if quantity == 0:
            basket_item.delete()
        else:
            BasketItem.objects.filter(basket = basket).filter(product = product_obj).update(quantity = quantity)
    else:
        cart = request.session.get('cart')
        product_id_str  = str(product_id)
        if cart:
            quantity = cart.get(product_id_str)
            if quantity > 1:
                cart[product_id_str] = quantity - 1
            else:
                cart.pop(product_id_str)
        request.session['cart'] = cart
    Product.objects.filter(id = product_id).update(available_quantity = product_obj.available_quantity + 1)
    return HttpResponseRedirect('/basket')
