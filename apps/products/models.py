from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Category name')
    description = models.TextField(blank=True, verbose_name='Description')
    icon = models.CharField(max_length=2, default='📦', verbose_name='Icon')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_CHOICES = [
        ('onsale', 'On sale'),
        ('offsale', 'Off sale'),
    ]

    name = models.CharField(max_length=200, verbose_name='Product name')
    description = models.TextField(blank=True, verbose_name='Description')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Category',
    )
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Price')
    specifications = models.TextField(
        blank=True,
        verbose_name='Specifications',
        help_text='One option per line or comma-separated, e.g. lipstick shades.',
    )
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Image')
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name='Stock')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='onsale',
        verbose_name='Status',
    )
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Seller',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_METHODS = [
        ('cod', 'Cash on delivery'),
        ('credit_card', 'Credit card'),
        ('line_pay', 'LINE Pay'),
    ]

    order_number = models.CharField(max_length=50, unique=True, verbose_name='Order number')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='Buyer')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='Product')
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)], verbose_name='Quantity')
    selected_specification = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Selected specification',
    )
    total_price = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='Total price')
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=60, verbose_name='Shipping fee')
    recipient_name = models.CharField(max_length=100, verbose_name='Recipient name')
    recipient_phone = models.CharField(max_length=20, verbose_name='Recipient phone')
    recipient_address = models.TextField(verbose_name='Recipient address')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Status')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, verbose_name='Payment method')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order_number} - {self.buyer.username}"


class OrderTracking(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tracking', verbose_name='Order')
    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    is_active = models.BooleanField(default=False, verbose_name='Is active')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')

    class Meta:
        verbose_name = 'Order tracking'
        verbose_name_plural = 'Order tracking'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.order.order_number} - {self.title}"
