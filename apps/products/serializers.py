from decimal import Decimal, InvalidOperation

from rest_framework import serializers

from .models import Category, Order, OrderTracking, Product


class CategorySerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'icon', 'description', 'count']

    def get_count(self, obj):
        return obj.product_set.filter(status='onsale').count()


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    seller_name = serializers.CharField(source='seller.username', read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'category', 'category_name',
            'specifications', 'image', 'image_url', 'stock', 'status', 'seller', 'seller_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'seller', 'created_at', 'updated_at']

    def to_internal_value(self, data):
        data = data.copy()
        if 'price' in data:
            data['price'] = str(data['price']).replace(',', '').replace('NT$', '').strip()
        if 'category' in data:
            category = str(data['category']).strip()
            if not category:
                data.pop('category')
            elif not category.isdigit():
                obj, _created = Category.objects.get_or_create(
                    name=category,
                    defaults={'description': '', 'icon': '📦'},
                )
                data['category'] = obj.pk
        return super().to_internal_value(data)

    def get_image_url(self, obj):
        if not obj.image:
            return None
        request = self.context.get('request')
        url = obj.image.url
        return request.build_absolute_uri(url) if request else url

    def validate_price(self, value):
        try:
            price = Decimal(str(value).replace(',', '').replace('NT$', '').strip())
        except (InvalidOperation, AttributeError):
            raise serializers.ValidationError('Enter a valid price.')
        if price < 0:
            raise serializers.ValidationError('Price cannot be negative.')
        return price.quantize(Decimal('0.01'))


class OrderTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTracking
        fields = ['id', 'title', 'description', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class OrderDetailSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    tracking = OrderTrackingSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'buyer', 'product', 'product_name', 'quantity',
            'selected_specification', 'total_price', 'shipping_fee', 'recipient_name', 'recipient_phone',
            'recipient_address', 'status', 'payment_method', 'tracking',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'order_number', 'buyer', 'created_at', 'updated_at']


class OrderListSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_icon = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'product', 'product_name', 'product_icon',
            'quantity', 'selected_specification', 'total_price', 'status', 'payment_method', 'created_at'
        ]
        read_only_fields = ['id', 'order_number', 'created_at']

    def get_product_icon(self, obj):
        if obj.product and obj.product.category:
            return obj.product.category.icon
        return ''
