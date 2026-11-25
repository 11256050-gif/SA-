from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Order, OrderTracking


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('icon_display', 'name', 'product_count', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',)
    
    def icon_display(self, obj):
        return format_html(f'<span style="font-size: 20px;">{obj.icon}</span>')
    icon_display.short_description = '圖標'
    
    def product_count(self, obj):
        count = obj.product_set.filter(status='onsale').count()
        return format_html(f'<span style="color: green; font-weight: bold;">{count}</span>')
    product_count.short_description = '上架商品'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price_display', 'stock_display', 'status_display', 'seller', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'description', 'image', 'category')
        }),
        ('商業信息', {
            'fields': ('price', 'stock', 'status', 'seller')
        }),
        ('時間戳', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def price_display(self, obj):
        return format_html(f'<span style="color: #e28743; font-weight: bold;">NT${obj.price}</span>')
    price_display.short_description = '價格'
    
    def stock_display(self, obj):
        color = 'green' if obj.stock > 0 else 'red'
        return format_html(f'<span style="color: {color}; font-weight: bold;">{obj.stock}</span>')
    stock_display.short_description = '庫存'
    
    def status_display(self, obj):
        colors = {'onsale': 'green', 'offsale': 'red'}
        status_text = {'onsale': '上架', 'offsale': '下架'}
        color = colors.get(obj.status, 'gray')
        text = status_text.get(obj.status, obj.status)
        return format_html(f'<span style="color: {color}; font-weight: bold;">{text}</span>')
    status_display.short_description = '狀態'


class OrderTrackingInline(admin.TabularInline):
    model = OrderTracking
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'buyer', 'product', 'total_price_display', 'status_display', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('order_number', 'buyer__username', 'recipient_name')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    inlines = [OrderTrackingInline]
    fieldsets = (
        ('訂單基本', {
            'fields': ('order_number', 'buyer', 'product', 'quantity')
        }),
        ('價格信息', {
            'fields': ('total_price', 'shipping_fee')
        }),
        ('收件信息', {
            'fields': ('recipient_name', 'recipient_phone', 'recipient_address')
        }),
        ('訂單狀態', {
            'fields': ('status', 'payment_method')
        }),
        ('時間戳', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def total_price_display(self, obj):
        return format_html(f'<span style="color: #e28743; font-weight: bold;">NT${obj.total_price}</span>')
    total_price_display.short_description = '總金額'
    
    def status_display(self, obj):
        status_colors = {
            'pending': 'orange',
            'confirmed': 'blue',
            'shipped': 'purple',
            'delivered': 'green',
            'cancelled': 'red'
        }
        status_text = {
            'pending': '待確認',
            'confirmed': '已確認',
            'shipped': '已出貨',
            'delivered': '已送達',
            'cancelled': '已取消'
        }
        color = status_colors.get(obj.status, 'gray')
        text = status_text.get(obj.status, obj.status)
        return format_html(f'<span style="color: {color}; font-weight: bold;">{text}</span>')
    status_display.short_description = '狀態'
