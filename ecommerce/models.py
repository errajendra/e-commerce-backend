from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from user.models import BaseModel, CustomUser as User, _



class Category(BaseModel):
    """
    A model representing a product category.
    """
    name = models.CharField("Name", max_length=100)
    description = models.TextField('Description', blank=True, null=True)

    def __str__(self):
        """
        Returns the name of the category.
        """
        return self.name



class Product(BaseModel):
    """
    A model representing a product.
    """
    STATUS_CHOICES = (
        ("AVAILABLE", "AVAILABLE"),
        ("NOT AVAILABLE", "NOT AVAILABLE"),
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
    price = models.DecimalField(_('Price'), decimal_places=2, max_digits=8)
    discount_price = models.DecimalField(
        _('Given Discount Price'), decimal_places=2, max_digits=8, default=0
    )
    is_featured = models.BooleanField(_('Is Featured?'), default=False)
    stock = models.PositiveIntegerField(_('Stock Count'), default=0)
    image1 = models.ImageField(_("Product Image 1"), upload_to='products/', default='product-default.jpg')
    image2 = models.ImageField(_("Product Image 2"), upload_to='products/', default='product-default.jpg')
    image3 = models.ImageField(_("Product Image 3"), upload_to='products/', default='product-default.jpg')
    image4 = models.ImageField(_("Product Image 4"), upload_to='products/', default='product-default.jpg')
    image5 = models.ImageField(_("Product Image 5"), upload_to='products/', default='product-default.jpg')
    benefits = CKEditor5Field('Benefits', config_name='default', null=True, blank=True)
    how_to_use = CKEditor5Field('How To Use', config_name='default', null=True, blank=True)
    availability = models.CharField(
        'Availability', max_length=14, choices=STATUS_CHOICES, default="AVAILABLE"
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
        return self.name

    @property
    def list_price(self):
        return self.price + self.discount_price
    
    @property
    def rating(self):
        rating = self.reviews.aggregate(
            models.Avg('rating'))['rating__avg']
        if not rating:
            return 0
        return rating



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
    review = models.TextField('Review')
    status = models.BooleanField('Status', default=True)

    def __str__(self):
        """
        Returns the user and product for the review.
        """
        return f'{self.user} - {self.product}'
