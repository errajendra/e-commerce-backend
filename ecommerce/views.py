from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import (
    CategoryForm, ProductForm, ProductFAQsForm, ProductReviewForm,
    BannerForm, BlogForm,
)
from .models import (
    Category, Product, ProductFAQ, ProductReview, Cart,
    Order, Transaction,
    Banner,
    Blog,
)
from user.models import CustomUser as User


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


"""
Product Views
"""
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


"""
Product FAQs Views
"""
def add_productfaq(request):
    if request.method == 'POST':
        form = ProductFAQsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product FAQ added successfully')
            return redirect('list_productfaqs')
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
            return redirect('list_productfaqs')
    else:
        form = ProductFAQsForm(instance=productfaq)
    return render(request, 'forms/form.html',
     {'form': form, 'title': "Update"})


def list_productfaqs(request):
    products = Product.objects.select_related().all()
    context = {
        'title': "Products FAQs",
        'products': products
    }
    return render(request, 'ecommerce/products-faqs-list.html', context)


def delete_productfaq(request, pk):
    productfaq = get_object_or_404(ProductFAQ, id=pk)
    productfaq.delete()
    messages.success(request, 'Product FAQ deleted successfully')
    return redirect('list_productfaqs')


"""
Product Reviews
"""
def add_productreview(request):
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Review added successfully')
            return redirect('list_productreviews', id=request.POST['product'])
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
            return redirect('list_productreviews', id=productreview.product.id)
    else:
        form = ProductReviewForm(instance=productreview)
    return render(request, 'forms/form.html',
     {'form': form, 'title': "Update Review"})


def list_productreviews(request, id):
    product = Product.objects.select_related().get(id=id)
    return render(
        request, 'ecommerce/product-reviews.html', {'product': product})


def delete_productreview(request, pk):
    productreview = get_object_or_404(ProductReview, id=pk)
    productreview.delete()
    messages.success(request, 'Product Review deleted successfully')
    return redirect('list_productreviews', id=productreview.product.id)




"""
Banner Views
"""
def add_banner(request):
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('list_banners')
    else:
        form = BannerForm()
    return render(request, 'forms/form.html', {'form': form})


def update_banner(request, pk):
    banner = Banner.objects.get(id=pk)
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES or None, instance=banner)
        if form.is_valid():
            form.save()
            return redirect('list_banners')
    else:
        form = BannerForm(instance=banner)
    return render(request, 'forms/form.html',
     {'form': form, 'title': "Update Banner"})


def list_banners(request):
    banner = Banner.objects.all()
    return render(
        request, 'ecommerce/banners.html', {
            'title': 'Banners',
            'banners': banner})


def delete_banner(request, pk):
    banner = get_object_or_404(Banner, id=pk)
    banner.delete()
    return redirect('list_banners')





"""
Banner Views
"""
def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('list_blogs')
    else:
        form = BlogForm()
    return render(request, 'forms/form.html', {'form': form})


def update_blog(request, pk):
    blog = Blog.objects.get(id=pk)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES or None, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('list_blogs')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'forms/form.html',
     {'form': form, 'title': "Update Blog"})


def list_blogs(request):
    blog = Blog.objects.all()
    return render(
        request, 'ecommerce/blogs.html', {
            'title': 'Blogs',
            'blogs': blog})


def delete_blog(request, pk):
    blog = get_object_or_404(Blog, id=pk)
    blog.delete()
    return redirect('list_blogs')




""" Cart Views """
def user_cart_list(request, pk):
    """ All Cart Items of Perticular User. """
    user = get_object_or_404(User, id=pk)
    context = {
        'title': f"{user.name} - Cart Items",
        'carts': Cart.objects.select_related().filter(user=user)
    }
    return render(request, 'cart/user-cart.html', context)


def delete_cart(request, pk):
    """ Delete cart item. """
    cart = get_object_or_404(Cart, id=pk)
    user = cart.user
    cart.delete()
    messages.success(request, 'Cart Item deleted successfully')
    return redirect(user_cart_list(request, user.id))



""" 
Order Views
"""
def order_list(request, user_id=None):
    """ All Orders. """
    if user_id:
        user = get_object_or_404(User, id=user_id)
        title = f"Orders of - {user.name}"
        orders = Order.objects.select_related().filter(user=user)
    else:
        title = "Orders"
        orders = Order.objects.select_related().all()
    context = {
        'title': title,
        'orders': orders
    }
    return render(request, 'order/list.html', context)



""" 
Transaction list views
"""
def transaction_list(request, user_id=None):
    """ All transactions. """
    if user_id:
        user = get_object_or_404(User, id=user_id)
        title = f"Transactions of - {user.name}"
        transactions = Transaction.objects.select_related().filter(user=user)
    else:
        title = "Transactions"
        transactions = Transaction.objects.select_related().all()
    context = {
        'title': title,
        'transactions': transactions
    }
    return render(request, 'transaction/list.html', context)
