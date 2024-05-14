from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    CategoryView, ProductView, CartView, BannerView,
    SubCategoryBannerView,
    ProductReviewView,
    OrderCartProduct, OrderListView, TransactionListView,
    OrderPaymentScreenShotUploadView,
    OrderCancelView, ReOrderlView,
    UserAddressView,
    BlogView,
    ReviewView, ReviewListView,
)

router = DefaultRouter()

router.register('banners', BannerView, basename='banners')
router.register('categories', CategoryView, basename='categories')
router.register('sub-categories-banner', SubCategoryBannerView, basename='sub_categories')
router.register('blogs', BlogView, basename='blogs')
router.register('products', ProductView, basename='products')
router.register('cart', CartView, basename='cart')
router.register('product-review', ProductReviewView, basename='product-review')
router.register('order-cart-product', OrderCartProduct, basename='order-from-cart')
router.register('address', UserAddressView, basename='address')
router.register('orders', OrderListView, basename='orders')
router.register('order-payment-screenshot-upload', OrderPaymentScreenShotUploadView,
                basename='order-payment-screenshot-upload')
router.register('cancel-order', OrderCancelView, basename='cancel-order')
router.register('re-order', ReOrderlView, basename='re-order')
router.register('transactions', TransactionListView, basename='transactions')
router.register('review', ReviewView, basename='review')
router.register('reviews', ReviewListView, basename='reviews')

urlpatterns = [
    # router.urls is a list of URL patterns that are automatically created by
    # the router based on your viewset(s).
    path("", include(router.urls)),
]
