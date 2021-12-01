from django.shortcuts import render
from .models import  Customer, Product, Country, Basket, BasketItem, Order, OrderItem
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib import messages
import datetime

class CustomerListView(generic.ListView):
    model = Customer

def product_list_view(request):
    products = Product.objects.filter(is_active = True)
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
    # try:
    #     del request.session['cart']
    # except:
    #     pass
    messages.success(request, 'Signed Out Successfully')
    return HttpResponseRedirect('/product')

def add_product_to_basket(request,id):
    product_obj = Product.objects.get(id = id)
    available_quantity = product_obj.available_quantity
    if 'email' in request.session:
        customer_email= request.session['email']
        customer_obj = Customer.objects.get(email = customer_email)
        if available_quantity <= 0:
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
        Product.objects.filter(id = id).update(available_quantity = available_quantity - 1)
        msg = product_obj.product_name + ' Added to basket successfully'
        messages.success(request, msg)
        return HttpResponseRedirect('/product')
    else:
        # return HttpResponseRedirect('/customer/login')
        cart = request.session.get('cart')
        id_s  = str(id)
        if cart:
            quantity = cart.get(id_s)
            if quantity:
                cart[id_s] = quantity + 1
            else:
                cart[id_s] = 1
        else:
            cart = {}
            cart[id_s] = 1
        Product.objects.filter(id = id).update(available_quantity = available_quantity - 1)
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
        customer_email= request.session['email']
        customer_obj = Customer.objects.get(email = customer_email)
        if Basket.objects.filter(customer = customer_obj).exists():
            basket = Basket.objects.filter(customer = customer_obj).get()
            basket_items = BasketItem.objects.filter(basket = basket)
            return render(request,'theretailerapp/basket_list.html',{'items':basket_items , 'basket_message' : basket_message})
        return render(request,'theretailerapp/basket_list.html')
    else:
        if cart:
            keys = list(cart.keys())
            products = Product.objects.filter(id__in = keys)
            print(type(products))
            return render(request,'theretailerapp/basket_list.html',{'items':products})
        return render(request,'theretailerapp/basket_list.html')

def remove_product_from_basket(request,id):
    if 'email' in request.session:
        product_name = BasketItem.objects.filter(id=id).get().product.product_name
        product_id = BasketItem.objects.filter(id=id).get().product.id
        available_quantity = Product.objects.filter(id = product_id).get().available_quantity
        Product.objects.filter(id = product_id).update(available_quantity = available_quantity +1)
        msg = product_name + ' removed from basket successfully'
        BasketItem.objects.filter(id=id).delete()
        messages.success(request, msg)
        return HttpResponseRedirect('/basket')
    else:
        return HttpResponseRedirect('/customer/login')

def remove_product_from_session_basket(request,id):
    product_obj = Product.objects.get(id = id)
    available_quantity = product_obj.available_quantity
    cart = request.session.get('cart')
    id_s  = str(id)
    if cart:
        quantity = cart.get(id_s)
        if quantity == 1:
            cart.pop(id_s)
        else:
            cart[id_s] = quantity -1
    Product.objects.filter(id = id).update(available_quantity = available_quantity +1)
    request.session['cart'] = cart
    return HttpResponseRedirect('/basket')

def convert_sessionbasket_to_tablebasket(request):
    if 'email' in request.session:
        customer_email= request.session['email']
        customer_obj = Customer.objects.get(email = customer_email)
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
                for i in range(cart[key]):
                    basket_item = BasketItem(basket = basket,product = product_obj,quantity = 1)
                    basket_item.save()
            del request.session['cart']
    return HttpResponseRedirect('/basket')


def place_order_form(request):
    if 'email' in request.session:
        customer_email= request.session['email']
        customer_obj = Customer.objects.get(email = customer_email)
        basket = Basket.objects.filter(customer = customer_obj).get()
        basket_items = BasketItem.objects.filter(basket = basket)
        default_shipping_address = customer_obj.shipping_address
        total_price = 0
        for item in basket_items:
            total_price = total_price + item.product.price
        if request.method == 'GET':
            return render(request,'theretailerapp/order_confirmation.html',
            {'items':basket_items,
            'shipping_address':default_shipping_address,
            'total_price':total_price})
        else:
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
        customer_email= request.session['email']
        customer_obj = Customer.objects.get(email = customer_email)
        order = Order.objects.filter(customer = customer_obj)
        start_date ='' 
        end_date = ''
        return render(request,'theretailerapp/order_list.html', {'order_list' :  order,
                                                                'start_date':start_date,
                                                                'end_date':end_date})
    else:
        return HttpResponseRedirect('/customer/login')

def show_order_details(request,id):
    if 'email' in request.session:
        order_items = OrderItem.objects.filter(order = id)
        order = Order.objects.get(id = id)
        return render(request,'theretailerapp/order_details.html', {'product_list' :  order_items, 'order': order})
    else:
        return HttpResponseRedirect('/customer/login')

def cancel_order(request,id):
    if 'email' in request.session:
        updated_at = datetime.datetime.now()
        updated_at_str = updated_at.strftime('%Y-%m-%d %H:%M:%S')
        Order.objects.filter(id = id).update(status = 'cancelled', updated_at = updated_at_str)
        order = Order.objects.filter(id = id).get()
        order_items = OrderItem.objects.filter(order = order)
        for item in order_items:
            available_quantity = Product.objects.filter(id = item.product.id).get().available_quantity
            Product.objects.filter(id = item.product.id).update(available_quantity = available_quantity + 1)
        messages.warning(request,'Order Cancelled')
        return HttpResponseRedirect('/order')
    else:
        return HttpResponseRedirect('/customer/login')

def filter_order(request):
    if 'email' in request.session:
        from_date = request.GET.get('from_filter_date')
        to_date = request.GET.get('to_filter_date')
        status = request.GET.get('status')
        customer_email= request.session['email']
        customer_obj = Customer.objects.get(email = customer_email)
        order = Order.objects.filter(customer = customer_obj)
        if(from_date != '' and to_date != ''):
            order = order.filter(created_at__range=[from_date, to_date])
        if status != 'None':
            order = order.filter(status = status)
        return render(request,'theretailerapp/order_list.html', {'order_list' :  order,
                                                                'start_date':from_date,
                                                                'end_date':to_date})
    else:
        return HttpResponseRedirect('/customer/login')

def reset_filter_order(request):
    if 'email' in request.session:
        customer_email= request.session['email']
        customer_obj = Customer.objects.get(email = customer_email)
        order = Order.objects.filter(customer = customer_obj)
        return render(request,'theretailerapp/order_list.html', {'order_list' :  order})
    else:
        return HttpResponseRedirect('/customer/login')

