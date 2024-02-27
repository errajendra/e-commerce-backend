from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    CategoryView, ProductView,
)

router = DefaultRouter()

router.register('categories', CategoryView, basename='categories')
router.register('products', ProductView, basename='products')

urlpatterns = [
    # router.urls is a list of URL patterns that are automatically created by
    # the router based on your viewset(s).
    path("", include(router.urls)),
]
