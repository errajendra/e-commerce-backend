from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .exceptions import *


# Auther: Rajendra
"""
    Category Listing Viewsets
"""
class CategoryView(ModelViewSet):
    http_method_names = ('get',)
    serializer_class = CategoryListSerializer
    queryset = Category.objects.select_related().all()
    pagination_class = None
    


"""
    Product Listing and Detail Viewset
"""
class ProductView(ModelViewSet):
    http_method_names = ('get',)
    serializer_class = ProductListSerializer
    
    def get_queryset(self):
        qs = Product.objects.select_related().all()
        
        # Filter by Category
        if self.request.query_params.get('category'):
            qs = qs.filter(category__id=self.request.query_params.get('category'))
            
        # Search by Name, Tag  or Description
        if self.request.query_params.get('search'):
            qs = qs.filter(
                Q(name__icontains = self.request.query_params.get('search')) |
                Q(sub_name__icontains = self.request.query_params.get('search')) |
                Q(description__icontains = self.request.query_params.get('search')) |
                Q(category__name__icontains = self.request.query_params.get('search'))
            )
        
        # Sorting by Price
        sort_by = self.request.query_params.get('sort')
        if sort_by:
            return qs.order_by(sort_by)
        return qs
    
    
    """
        Override Product Detail View to include related data
        Serializer is used here instead of all Detail
        because we need full control over fields in the response
    """
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ProductDetailSerializer
        return super().retrieve(request, *args, **kwargs)



""" 
    Cart Item View Set.
"""
class CartView(ModelViewSet):
    http_method_names = ('get', 'post', 'delete', 'put')
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        return Cart.objects.select_related().filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        data = super().list(request, *args, **kwargs)
        context = {
            "total_price": sum([item['product']['price']*item['quantity'] for item in data.data]),
            "list": data.data
        }
        return Response(context)



"""
Product Reviews Viewset
"""
class ProductReviewView(ModelViewSet):
    http_method_names = ('post',)
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductReviewSerializer
    
    def get_queryset(self):
        return ProductReview.objects.select_related().filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        data = super().create(request, *args, **kwargs)
        return Response(data.data)



"""
Order Items of Cart Viewset
"""
class OrderCartProduct(ModelViewSet):
    http_method_names = ('post',)
    permission_classes = (IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        user = request.user
        cart_items = user.cart.select_related().all()
        
        if not cart_items:
            raise CartIsEmpaty()
        
        total_price = 0
        
        for cart in cart_items:
            price = cart.quantity * cart.product.price
            total_price += price
        
        order = Order.objects.create(
            user = user,
            total_price = total_price
        )
        order.save()
        order_products_qs = []
        for cart in cart_items:
            order_products_qs.append(
                OrderProduct(
                    order = order,
                    product = cart.product,
                    quantity = cart.quantity,
                    price = cart.quantity * cart.product.price
                )
            )
        OrderProduct.objects.bulk_create(order_products_qs)
        cart_items.delete()
        return Response(
            status=status.HTTP_201_CREATED,
            data = {
                "order": OrderSerializer(order).data
            }
        )



"""
Order List Viewset
"""
class OrderList(ModelViewSet):
    http_method_names = ('get',)
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        return self.request.user.orders.all()
