"""Core admin."""


from django.contrib import admin
from .models import Seller, Price, CacheSetup


class SellerAdmin(admin.ModelAdmin):
    """Seller admin"""
    pass


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Price._meta.fields]

    def get_queryset(self, request):
        queryset = super(PriceAdmin, self).get_queryset(request=request)
        if request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(seller__user=request.user)


admin.site.register(Seller, SellerAdmin)


class CacheSetupAdmin(admin.ModelAdmin):
    """CacheSetup  admin"""
    pass


admin.site.register(CacheSetup, CacheSetupAdmin)
