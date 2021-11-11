from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list_view, name='product'),
    path('product', views.product_list_view, name = 'product'),
    path('customer',views.CustomerListView.as_view(),name = 'customer'),
    path('customer/create', views.insert_customer, name='customer_create'),
    path('customer/login', views.login_customer, name='customer_login'),
    path('customer/logout', views.customer_sign_out, name='customer_logout'),
]
