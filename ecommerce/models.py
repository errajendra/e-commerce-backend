from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from user.models import BaseModel, CustomUser as User, _



class Banner(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length=50)



class UserAddress(BaseModel):
    """
    A model representing a user's address.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    name = models.CharField('House Number', max_length=50, null=True, blank=True)
    mobile_number = models.CharField('Mobile Number', max_length=15, null=True, blank=True)
    email = models.EmailField('Delivery Email', null=True, blank=True)
    house_number = models.CharField('House Number', max_length=20, null=True, blank=True)
    street = models.CharField('Street Address', max_length=250)
    city = models.CharField('City', max_length=100)
    state = models.CharField('State', max_length=100)
    zip_code = models.CharField('Zip Code', max_length=10)
    country = models.CharField('Country', default="India", max_length=50)
    is_default = models.BooleanField('Is Default', default=False)

    def __str__(self):
        """
        Returns the user and address for the user address.
        """
        return "{} {}, {}, {} - {}, {}".format(self.house_number, self.street, self.city, self.state, self.zip_code, self.country)
    
    @property
    def full_address(self):
        return  "{} {}, {}, {}, {}".format(self.house_number, self.street, self.city, self.state, self.country)
    
    class Meta:
        verbose_name = _("User Address")
        verbose_name_plural = _("User Addresses")



class Category(BaseModel):
    """
    A model representing a product category.
    """
    name = models.CharField("Name", max_length=100)
    description = models.TextField('Description', blank=True, null=True)
    image = models.ImageField(upload_to='category/', default="product-default.jpg")

    def __str__(self):
        return self.name



class Product(BaseModel):
    """
    A model representing a product.
    """
    STATUS_CHOICES = (
        ("IN STOCK", "IN STOCK"),
        ("NOT IN STOCK", "NOT IN STOCK"),
        ("UPCOMMING", "UPCOMMING"),
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, verbose_name='Category',
        related_name="products", null=True, blank=True
    )
    name = models.CharField(_('Product Name'), max_length=100)
    sub_name = models.CharField(
        _('Product Sub Name'), max_length=250,
        help_text="Product's short description or tagline"
    )
    description = models.TextField(_("Description"), null=True, blank=True)
    price = models.FloatField(_('Sell Price'))
    discount_price = models.FloatField(
        _('Given Discount Price'), default=0
    )
    is_featured = models.BooleanField(_('Is Featured?'), default=False)
    stock = models.PositiveIntegerField(_('Stock Count'), default=0)
    image1 = models.ImageField(_("Product Image 1"), upload_to='products/', default='product-default.jpg')
    image2 = models.ImageField(_("Product Image 2"), upload_to='products/', default='product-default.jpg')
    image3 = models.ImageField(_("Product Image 3"), upload_to='products/', default='product-default.jpg')
    image4 = models.ImageField(_("Product Image 4"), upload_to='products/', default='product-default.jpg')
    image5 = models.ImageField(_("Product Image 5"), upload_to='products/', default='product-default.jpg')
    benefits = CKEditor5Field('Benefits', config_name='default', null=True, blank=True)
    cons = CKEditor5Field('Cons', config_name='default', null=True, blank=True)
    how_to_use = CKEditor5Field('How To Use', config_name='default', null=True, blank=True)
    availability = models.CharField(
        'Availability', max_length=14, choices=STATUS_CHOICES, default="IN STOCK"
    )
    status = models.BooleanField(
        _('Active Status'), default=True,
        help_text=_('If it is not active, the product will be hidden from the site.')
    )

    class Meta:
        """
        Meta options for the Product model.
        """
        ordering = ['-created_at']
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        """
        Returns the name of the product.
        """
        return f"{self.name} ({self.price}) - {self.category.name}"

    @property
    def list_price(self):
        return self.price + self.discount_price
    
    @property
    def rating(self):
        """
        Average rating of this product
        """
        rating = self.reviews.aggregate(
            models.Avg('rating'))['rating__avg']
        if not rating:
            return 0
        return round(rating, 2)



class ProductFAQ(BaseModel):
    """
    A model representing a frequently asked question (FAQ) for a product.
    """
    product = models.ForeignKey(
        Product, related_name='faqs', on_delete=models.CASCADE
    )
    question = models.CharField('Question', max_length=150)
    answer = models.TextField('Answer')
    status = models.BooleanField('Status', default=True)

    def __str__(self):
        """
        Returns the question of the FAQ.
        """
        return self.question



class ProductReview(BaseModel):
    """
    A model representing a product review.
    """
    PRODUCT_RATING_CHOICES = (
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    )
    product = models.ForeignKey(
        Product, related_name='reviews', on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(_('Rating'), choices=PRODUCT_RATING_CHOICES)
    review = models.TextField('Review', null=True, blank=True)
    status = models.BooleanField('Status', default=True)

    def __str__(self):
        """
        Returns the user and product for the review.
        """
        return f'{self.user} - {self.product}'



class Cart(BaseModel):
    """
    A model representing a product cart.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Cart Items"

    def __str__(self):
        """
        Returns the user, product, and quantity for the product cart.
        """
        return f'{self.user} - {self.product} ({self.quantity})'



class Order(BaseModel):
    """
    A model representing a product order.
    """
    ORDER_STATUS_CHOICES = (
        ("PENDING", "PENDING"),
        ("ORDERED", "ORDERED"),
        ("IN-PROGRESS", "IN-PROGRESS"),
        ("DELIVERED", "DELIVERED"),
        ("FAILED", "FAILED"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.FloatField(default=0)
    status = models.CharField(max_length=12, choices=ORDER_STATUS_CHOICES, default="PENDING")
    delivery_address = models.CharField(_("Delivery Address"), max_length=250, null=True, blank=True)
    delivery_zip_code = models.CharField(_("Delivery ZIP Code"), max_length=10, null=True, blank=True)

    def __str__(self):
        """
        Returns the user and order date for the order.
        """
        return f'{self.user} - {self.created_at}'
    
    @property
    def order_id(self):
        """
        This is an id to show only
        """
        return f"#{str(self.pk).zfill(3)}"
    


class OrderProduct(BaseModel):
    """
    A model representing the relationship between an order and a product.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_products')
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField()

    class Meta:
        verbose_name = "Order Product"
        verbose_name_plural = "Order Products"
        unique_together = ('order', 'product',)

    def __str__(self):
        """
        Returns the order, product, and quantity for the order product.
        """
        return f'{self.order} - {self.product} ({self.quantity})'



class Transaction(BaseModel):
    """
    A model representing a financial transaction.
    """
    TRANSACTION_STATUS_CHOICES = (
        ("PENDING", "PENDING"),
        ("SUCCESS", "SUCCESS"),
        ("FAILED", "FAILED"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transactions')
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=TRANSACTION_STATUS_CHOICES, default="PENDING")
    mode = models.CharField(
        _("Transaction Mode"),
        max_length=10,
        choices=(
            ("CASH", 'CASH'),
            ("ONLINE", 'ONLINE'),
            ),
        default="CASH")
    
    # Bank Transaction  Details
    tracking_id = models.CharField(
        _("Bank Tracking/UTR Number"),
        max_length=100,
        null = True, blank=True
    )

    def __str__(self):
        """
        Returns the user, order, and status for the transaction.
        """
        return f'{self.user} - {self.order} - {self.status}'
