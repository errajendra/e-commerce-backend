from django.contrib import admin
from .models import *



@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'name', 'email', 'mobile_number',
        'house_number','street', 'city', 'state',
        'zip_code', 'country', 'is_default')
    search_fields = (
        'name', 'email', 'mobile_number',
        'street', 'city', 'state', 'zip_code', 'country',
        'user__name', 'user__mobile_number', 'user__email')
    list_filter = ('is_default',)


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



@admin.register(Cart)
class cartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')
    list_filter = ('quantity', 'created_at')
    search_fields = (
        'product__name', 'product__sub_name', 'product__description', 
        'user__name', 'user__email', 'user__mobile_number')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'total_price', 'status',
        'delivery_address', 'delivery_zip_code',
        'created_at', 'updated_at'
    ]
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = (
        'user__name', 'user__mobile_number', 'user__email',)



@admin.register(OrderProduct)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'order', 'product', 'quantity', 'price',
        'created_at', 'updated_at'
    ]
    list_filter = ('created_at', 'updated_at')
    search_fields = ('order__user__name', 'order__user__mobile_number', 'order__user__email')



@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order', 'amount', 'status', 'mode', 'tracking_id',)
    list_filter = ('status', 'mode',)
    search_fields = (
        'user__name', 'user__mobile_number', 'user__email', 
        'order__id', 'tracking_id',)



@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title',)
