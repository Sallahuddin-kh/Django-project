from django.contrib import admin
from .models import Basket, BasketItem, Country, Customer, Product, Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'status' ,'placed_at', 'order_shipping_address','order_price')
    list_filter = ('customer__email', 'placed_at')

admin.site.register(Country)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Basket)
admin.site.register(BasketItem)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)
