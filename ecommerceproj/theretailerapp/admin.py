from django.contrib import admin
from .models import Basket, BasketItem, Country, Customer, Product, ApprovalStatus, Order, OrderItem

admin.site.register(Country)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Basket)
admin.site.register(BasketItem)
admin.site.register(ApprovalStatus)
admin.site.register(Order)
admin.site.register(OrderItem)
