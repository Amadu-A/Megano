"""Order admin."""


from django.contrib import admin
from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    """Order admin"""
    pass


class OrderItemAdmin(admin.ModelAdmin):
    """Order item admin"""
    pass


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
