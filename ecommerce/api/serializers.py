from rest_framework import serializers
from ..models import (
    Category, Product, ProductFAQ, ProductReview,
)
from user.api.serializers import UserInfoSerializer


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')



class ProductFAQsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFAQ
        fields = ('id', 'question', 'answer')


class ProductReviewListSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)
    class Meta:
        model = ProductReview
        fields = ('id', 'user', 'rating', 'review')



class ProductListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer(read_only=True)
    class Meta:
        model = Product
        fields = (
            'id', 'category', 'name', 'sub_name', 'price', 'image1'
        )
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['list_price'] = instance.list_price
        data['rating'] = instance.rating
        return data



class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer(read_only=True)

    class Meta:
        model = Product
        exclude = (
            'discount_price', 'created_at', 'updated_at', 'status'
        )
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['list_price'] = instance.list_price
        data['rating'] = instance.rating
        data['faqs'] = ProductFAQsListSerializer(instance.faqs.all(), many=True).data
        data['reviews'] = ProductReviewListSerializer(instance.reviews.all(), many=True).data
        return data
