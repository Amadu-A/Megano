"""Cart admin."""


from django.contrib import admin
from .models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    """Order admin"""
    pass


class CartItemAdmin(admin.ModelAdmin):
    """Order item admin"""
    pass


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
