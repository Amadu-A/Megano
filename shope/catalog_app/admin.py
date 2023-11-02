from django.contrib import admin

from .models import (Product,
                     Category,
                     Image,
                     Slider,
                     Banner,
                     DiscountProduct,
                     DiscountProductGroup,
                     CartSale,
                     CharacteristicType,
                     CharacteristicValue,
                     CompareProduct,
                     CharacteristicProduct,
                     ProductViewed,
                     Rewiew,
                     )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Image._meta.fields]


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Slider._meta.fields]


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Banner._meta.fields]


@admin.register(DiscountProduct)
class DiscountProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DiscountProduct._meta.fields]


@admin.register(DiscountProductGroup)
class DiscountProductGroupAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DiscountProductGroup._meta.fields]
    exclude = ('value',)


@admin.register(CartSale)
class CartSaleAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CartSale._meta.fields]


@admin.register(ProductViewed)
class ProductViewedAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductViewed._meta.fields]


@admin.register(CompareProduct)
class CompareProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CompareProduct._meta.fields]


###############################################################
# ХАРАКТЕРИСТИКИ ПРОДУКТОВ
###############################################################
class CharacteristicTypeAdmin(admin.ModelAdmin):
    """CharacteristicType admin"""
    pass


class ChatacteristicValueAdmin(admin.ModelAdmin):
    """ChatacteristicValue admin"""
    pass


class CharacteristicProductAdmin(admin.ModelAdmin):
    """ChatacteristicProduct admin"""
    pass


admin.site.register(CharacteristicProduct, CharacteristicProductAdmin)
admin.site.register(CharacteristicType, CharacteristicTypeAdmin)
admin.site.register(CharacteristicValue, ChatacteristicValueAdmin)

###############################################################
#  ОТЗЫВ
###############################################################


class RewiewAdmin(admin.ModelAdmin):
    """Rewiew admin"""
    pass


admin.site.register(Rewiew, RewiewAdmin)
