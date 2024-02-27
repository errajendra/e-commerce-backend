from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import (
    CategoryForm, ProductForm, ProductFAQsForm, ProductReviewForm,
)
from .models import (
    Category, Product, ProductFAQ, ProductReview,
)


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully')
            return redirect('list_categories')
    else:
        form = CategoryForm()
    return render(request, 'forms/form.html', {'form': form})


def update_category(request, pk):
    category = Category.objects.get(id=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully')
            return redirect('list_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'forms/form.html',
     {'form': form, 'title': "Update"})


def list_categories(request):
    categories = Category.objects.all()
    return render(request, 'ecommerce\category-list.html', {'categories': categories})


def delete_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    category.delete()
    messages.success(request, 'Category deleted successfully')
    return redirect('list_categories')


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully')
            return redirect('list_products')
    else:
        form = ProductForm()
    return render(request, 'forms/form.html', {'form': form})


def update_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(data=request.POST, files=request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully')
            return redirect('list_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'forms/form.html',
     {'form': form, 'title': "Update"})


def list_products(request):
    products = Product.objects.all()
    return render(request, 'ecommerce\products-list.html', {'products': products})


def delete_product(request, pk):
    product =get_object_or_404( Product, id=pk)
    product.delete()
    messages.success(request, 'Product deleted successfully')
    return redirect('list_products')


def add_productfaq(request):
    if request.method == 'POST':
        form = ProductFAQsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product FAQ added successfully')
            return redirect('list_productfaq')
    else:
        form = ProductFAQsForm()
    return render(request, 'forms/form.html', {'form': form})


def update_productfaq(request, pk):
    productfaq = ProductFAQ.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductFAQsForm(request.POST, instance=productfaq)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product FAQ updated successfully')
            return redirect('list_productfaq')
    else:
        form = ProductFAQsForm(instance=productfaq)
    return render(request, 'forms/form.html',
     {'form': form, 'title': "Update"})


def list_productfaqs(request):
    productfaqs = ProductFAQ.objects.all()
    return render(request, 'list_productfaqs.html', {'productfaqs': productfaqs})


def delete_productfaq(request, pk):
    productfaq = get_object_or_404(ProductFAQ, id=pk)
    productfaq.delete()
    messages.success(request, 'Product FAQ deleted successfully')
    return redirect('list_productfaqs')


def add_productreview(request):
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Review added successfully')
            return redirect('list_productreview')
    else:
        form = ProductReviewForm()
    return render(request, 'forms/form.html', {'form': form})


def update_productreview(request, pk):
    productreview = ProductReview.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductReviewForm(request.POST, instance=productreview)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Review updated successfully')
            return redirect('list_productreview')
    else:
        form = ProductReviewForm(instance=productreview)
    return render(request, 'forms/form.html',
     {'form': form, 'title': "Update"})


def list_productreviews(request):
    productreviews = ProductReview.objects.all()
    return render(request, 'list_productreviews.html', {'productreviews': productreviews})


def delete_productreview(request, pk):
    productreview = get_object_or_404(ProductReview, id=pk)
    productreview.delete()
    messages.success(request, 'Product Review deleted successfully')
    return redirect('list_productreviews')
