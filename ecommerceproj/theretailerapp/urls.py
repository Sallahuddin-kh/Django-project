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
    path('basket/<uuid:id>', views.add_product_to_basket, name="add_to_basket"),
    path('basket/remove/<int:id>', views.remove_product_from_basket, name="remove_from_basket"),
    path('order/<int:id>',views.place_order,name = 'place_order')
]
