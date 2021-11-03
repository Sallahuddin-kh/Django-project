from django.urls import path
from . import views

urlpatterns = [
    path('', views.CustomerListView.as_view(), name='customer'),
    path('product', views.ProductListView.as_view(), name = 'product'),
]