from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import (
    Category, Product,
    ProductFAQ, ProductReview,
    Banner,
)


"""
Category Forms
"""
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }



""" 
Product Form
- Includes a form field for the category that this product belongs to.
"""
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        # exclude = ('benefits', 'how_to_use')
        
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'sub_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'availability': forms.Select(attrs={'class': 'form-control'}),
            "benefits": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="default"
            ),
            "cons": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="default"
            ),
            "how_to_use": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="default"
            )
        }
        


"""
Product FAQs Form
"""
class ProductFAQsForm(forms.ModelForm):
    class Meta:
        model = ProductFAQ
        fields = "__all__"

        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'class': 'form-control'}),
        }



"""
Product Review Form
"""
class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = "__all__"

        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'class': 'form-control'}),
        }



"""
Home Page Banner Form
"""
class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = "__all__"

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }
