from django.contrib import admin
from .models import Basket, BasketItem, Country, Customer, Product

admin.site.register(Country)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Basket)
admin.site.register(BasketItem)