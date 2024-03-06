from django.urls import path, include
from .views import *

urlpatterns = [
    # Api
    path('api/', include('ecommerce.api.urls')),
    
    # Category Urls
    path('add-category/', add_category, name='add_category'),
    path('update-category/<int:pk>/', update_category, name='update_category'),
    path('list-categories/', list_categories, name='list_categories'),
    path('delete-category/<int:pk>/', delete_category, name='delete_category'),
    
    # Product Urls
    path('add-product/', add_product, name='add_product'),
    path('update-product/<int:pk>/', update_product, name='update_product'),
    path('list-products/', list_products, name='list_products'),
    path('delete-product/<int:pk>/', delete_product, name='delete_product'),
    
    # Product FAQs Urls
    path('add-productfaq/', add_productfaq, name='add_productfaq'),
    path('update-productfaq/<int:pk>/', update_productfaq, name='update_productfaq'),
    path('list-productfaqs/', list_productfaqs, name='list_productfaqs'),
    path('delete-productfaq/<int:pk>/', delete_productfaq, name='delete_productfaq'),
    
    # Product Reviews  Urls
    path('add-productreview/', add_productreview, name='add_productreview'),
    path('update-productreview/<int:pk>/', update_productreview, name='update_productreview'),
    path('list-productreviews/<int:id>/', list_productreviews, name='list_productreviews'),
    path('delete-productreview/<int:pk>/', delete_productreview, name='delete_productreview'),
    
    # Cart  Urls
    path('list-user-cart/<int:pk>/', user_cart_list, name='list_user_cart'),
    path('delete-cart/<int:pk>/', delete_cart, name='delete_cart'),
    
    # Order Urls
    path('orders/', order_list, name="orders"),
]