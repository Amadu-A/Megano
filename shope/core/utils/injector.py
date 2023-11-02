import inject

from interface.banner_interface import IBanner
from interface.cart_sale_interface import ICartSale
from interface.category_interface import ICategory
from interface.compare_product_interface import ICompareProduct
from interface.discount_interface import IDiscountBaseModel
from interface.discount_product_group_interface import IDiscountProductGroup
from interface.discount_product_interface import IDiscountProduct
from interface.order_interface import IOrder
from interface.price_interface import IPrice

from interface.product_interface import IProduct
from interface.product_viewed_interface import IProductViewed
from interface.slider_interface import ISlider
from repositories.banner_repositories import BannerRepository
from repositories.cart_sale_repositories import CartSaleRepository
from repositories.category_repositories import CategoryRepository
from repositories.compare_product_repositories import CompareProductRepository
from repositories.discount_product_group_repositories import DiscountProductGroupRepository
from repositories.discount_product_repositories import DiscountProductRepository
from repositories.discount_repositories import DiscountBaseModelRepository
from interface.auth_interface import IAuth

from repositories.order_repositories import OrderRepository
from repositories.auth_repositories import AuthRepository
from repositories.price_repositories import PriceRepository
from repositories.product_repositories import ProductRepository
from repositories.product_viewed_repositories import ProductViewedRepository

from repositories.profile_repositories import ProfileRepository
from interface.profile_interface import IProfile

from repositories.characterisic_repositories import CharacteristicRepository
from interface.characteristic_interface import ICharacteristicProduct

from interface.catalog_filter_interface import ICatalogFilter
from repositories.catalog_filter_repositories import CatalogFilterRepository

from repositories.order_item_repositories import OrderItemRepository
from interface.order_item_interface import IOrderItem
from repositories.slider_repositories import SliderRepository

from repositories.cart_repositories import CartRepository
from interface.cart_interface import ICart
from interface.cartitem_interface import ICartItem
from repositories.cartitem_repositories import CartItemRepository

from interface.seller_interface import ISeller
from repositories.seller_repositories import SellerRepository

from interface.review_interface import IReview
from repositories.reivew_repositories import ReviewRepository

BINDS = (
    (IOrder, OrderRepository),
    (IDiscountBaseModel, DiscountBaseModelRepository),
    (IAuth, AuthRepository),
    (IDiscountProduct, DiscountProductRepository),
    (IDiscountProductGroup, DiscountProductGroupRepository),
    (ICartSale, CartSaleRepository),
    (IProfile, ProfileRepository),
    (IProduct, ProductRepository),
    (ICharacteristicProduct, CharacteristicRepository),
    (ICategory, CategoryRepository),
    (ICatalogFilter, CatalogFilterRepository),
    (IProductViewed, ProductViewedRepository),
    (ISlider, SliderRepository),
    (IBanner, BannerRepository),
    (IOrderItem, OrderItemRepository),
    (ICart, CartRepository),
    (ICartItem, CartItemRepository),
    (ISeller, SellerRepository),
    (IReview, ReviewRepository),
    (ICompareProduct, CompareProductRepository),
    (IPrice, PriceRepository),
)


def config(binder):
    """Конфигуратор для inject."""
    for interface, implementation in BINDS:
        binder.bind(interface, implementation())


def configure_inject():
    """Конфигурирует зависимости для проекта."""
    inject.configure_once(config)
