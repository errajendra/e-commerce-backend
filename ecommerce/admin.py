from django.contrib import admin
from .models import *



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'category', 
        'name',  
        'sub_name',
        'description',
        'price', 
        'discount_price', 
        'stock',  
        'is_featured',
        'availability', 
        'status', 
        'created_at'
    )
    list_filter = (
        'category', 'availability', 'is_featured', 'status', 'created_at')
    search_fields = ('name', 'sub_name', 'description')
    


@admin.register(ProductFAQ)
class ProductFAQsAdmmin(admin.ModelAdmin):
    list_display = ('product', 'question', 'answer', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    list_editable = ('status', )
    search_fields = (
        'product__name', 'product__sub_name', 'product__description', 'question',)



@admin.register(ProductReview)
class ProductReviewAdmmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'review', 'status')
    list_filter = ('status', 'rating',)
    list_editable = ('status', 'rating',)
    search_fields = (
        'product__name', 'product__sub_name', 'product__description', 
        'user__name', 'user__email', 'user__mobile_number')
