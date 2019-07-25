from django.contrib import admin
from mainapp.models import ProductCategory, Product
from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]

    list_filter = ["user", "status"]

    class Meta:
        model = Order


class OrderItemAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OrderItem._meta.fields]

    list_filter = ["order_id"]

    class Meta:
        model = OrderItem

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)