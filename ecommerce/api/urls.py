from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    CategoryView, ProductView, CartView,
    ProductReviewView,
    OrderCartProduct, OrderList,
)

router = DefaultRouter()

router.register('categories', CategoryView, basename='categories')
router.register('products', ProductView, basename='products')
router.register('cart', CartView, basename='cart')
router.register('product-review', ProductReviewView, basename='product-review')
router.register('order-cart-product', OrderCartProduct, basename='order-from-cart')
router.register('orders', OrderList, basename='orders')

urlpatterns = [
    # router.urls is a list of URL patterns that are automatically created by
    # the router based on your viewset(s).
    path("", include(router.urls)),
]
