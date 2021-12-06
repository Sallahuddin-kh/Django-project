from django.contrib import admin
from .models import Basket, BasketItem, Country, Customer, Product, Order, OrderItem


class ProductTabularInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductTabularInline]
    list_display = ('customer', 'status', 'created_at', 'updated_at', 'order_shipping_address', 'order_price', 'order_products')
    list_filter = ('customer__email', 'created_at')
    fields = ('customer', 'status', 'created_at', 'updated_at', 'order_shipping_address', 'order_price')

    def order_products(self, order_obj):
        items = OrderItem.objects.filter(order = order_obj)
        products = []
        for item in items:
            products.append(item.product.product_name)
        return products

admin.site.register(Country)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Basket)
admin.site.register(BasketItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
