from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list_view, name='product'),
    path('product', views.product_list_view, name = 'product'),
    path('customer',views.CustomerListView.as_view(),name = 'customer'),
    path('customer/create', views.insert_customer, name='customer_create'),
    path('customer/login', views.login_customer, name='customer_login'),
    path('customer/logout', views.customer_sign_out, name='customer_logout'),
    path('basket', views.customer_basket, name='customer_basket'),
    path('basket/<uuid:id>', views.add_product_to_basket, name='add_to_basket'),
    path('basket/remove/<int:id>', views.remove_product_from_basket, name='remove_from_basket'),
    path('basket/remove/<uuid:id>', views.remove_product_from_session_basket, name='remove_from_basket_session'),
    path('basket/getsession', views.convert_sessionbasket_to_tablebasket, name='convert_sessionbasket_to_tablebasket'),
    path('basket/increaseamount/<uuid:id>', views.increase_basket_item_quantity, name='increase_basket_item_quantity'),
    path('basket/decreaseamount/<uuid:id>', views.decrease_basket_item_quantity, name='decrease_basket_item_quantity'),
    path('order/place',views.place_order_form,name = 'place_order_form'),
    path('order' , views.show_customer_orders, name = 'show_customer_orders'),
    path('order/details/<int:id>', views.show_order_details,name = 'show_order_details'),
    path('order/cancel/<int:id>' , views.cancel_order , name = 'cancel_order'),
    path('order/filter' , views.filter_order , name = 'filter_order'),
    path('order/filter/reset', views.show_customer_orders, name = 'filter_order_reset')
]
