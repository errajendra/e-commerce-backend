from rest_framework import serializers
from django.db.models import Avg
from ..models import (
    Category, Product, ProductFAQ, ProductReview,
    Cart, Order, OrderProduct, Transaction,
)
from user.api.serializers import UserInfoSerializer


# Rajendra
"""
    Category Listing Serializer
"""
class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')



"""
    Product FAQs Listing Serializer 
    used in Product Details Serialiser (api)
"""
class ProductFAQsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFAQ
        fields = ('id', 'question', 'answer')



"""
    The ProductReviewSerializer class is a subclass of serializers.ModelSerializer.
    It is used to serialize and deserialize instances of the ProductReview model.
    Take review from user.
"""
class ProductReviewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'product', 'rating', 'review', 'created_at']



"""
    Product Reviews Average Rating Serializer
    Used to get the average rating of a product review.
    It is called by the ProductDetailsViewSet when getting details for a product.
"""
class ProductReviewListSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)
    class Meta:
        model = ProductReview
        fields = ('id', 'user', 'rating', 'review', 'updated_at')



"""
    Product Listing Serializer
"""
class ProductListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer(read_only=True)
    class Meta:
        model = Product
        fields = (
            'id', 'category', 'name', 'sub_name',
            'price', 'is_featured', 'image1'
        )
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['list_price'] = instance.list_price
        data['rating'] = instance.rating    # Returning Avg Rating of Product
        return data



"""
    Product Detail Serializer,
    includes  all information from ProductListSerializer plus more detailed info.
    Called by ProductDetailsViewSet in views.py
"""
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
        
        # Reviews Details
        reviews = instance.reviews.all()
        if reviews:
            ratings_couces = reversed(list(ProductReview.PRODUCT_RATING_CHOICES))
            rating_detail = []
            for rate in ratings_couces:
                review_rates = reviews.filter(rating=rate[0])
                rating_avg = review_rates.aggregate(Avg('rating'))['rating__avg']
                if not rating_avg:
                    rating_detail.append({
                        "value": rate[1],
                        "vote_percentage": 0
                    })
                else:
                    rating_detail.append({
                        "value": rate[1],
                        "vote_percentage": f"{round(review_rates.count() * 100 / reviews.count(), 2)} %"
                    })
        else:
            rating_detail = []
                
        data['reviews'] = {
            "count": reviews.count(),
            "ratings": rating_detail,
            "list": ProductReviewListSerializer(
                reviews.exclude(review=""), many=True).data
        } 
        
        # Related Products
        data['related_products'] = ProductListSerializer(
            Product.objects.filter(
                category=instance.category,
            ).exclude(id=instance.id).order_by('is_featured')[:4],
            many=True
        ).data
        return data



"""
    A serializer for the Cart model.
"""
class CartSerializer(serializers.ModelSerializer):
   
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(
            status = True,
            availability = "IN STOCK",
        ))
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'quantity']

    def create(self, validated_data):
        """
        Create and return a new Cart instance, given the validated data.
        """
        user = validated_data['user']
        product = validated_data['product']
        quantity = validated_data['quantity']

        try:
            existing_cart_item = Cart.objects.get(user=user, product=product)
            existing_cart_item.quantity += quantity
            existing_cart_item.save()
            return existing_cart_item
        except Cart.DoesNotExist:
            return Cart.objects.create(**validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['product'] = ProductListSerializer(
            instance=instance.product,
            context={'request':self.context['request']}).data
        return data



class OrderItemsSerialiser(serializers.ModelSerializer):
    """ Serializer for order items in an order"""
    product = ProductListSerializer(read_only=True)
    class Meta:
        model = OrderProduct
        fields = "__all__"



class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'total_price', 'status', 
            'created_at', 'updated_at'
        ]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['products'] = OrderItemsSerialiser(
            instance.order_products.all(),
            many = True
        ).data
        return data
        


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'id', 'user', 'order', 'amount', 'status',
            'created_at', 'updated_at')