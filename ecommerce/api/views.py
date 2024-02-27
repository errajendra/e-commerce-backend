from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from .serializers import *


class CategoryView(ModelViewSet):
    http_method_names = ('get',)
    serializer_class = CategoryListSerializer
    queryset = Category.objects.all()
    pagination_class = None
    


class ProductView(ModelViewSet):
    http_method_names = ('get',)
    serializer_class = ProductListSerializer
    
    def get_queryset(self):
        qs = Product.objects.all()
        
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
