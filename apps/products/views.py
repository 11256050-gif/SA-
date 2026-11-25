from datetime import datetime
import random
import re

from django.shortcuts import render
from django.views import View
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Category, Order, OrderTracking, Product
from .serializers import (
    CategorySerializer,
    OrderDetailSerializer,
    OrderListSerializer,
    OrderTrackingSerializer,
    ProductSerializer,
)


SPECIFICATION_SEPARATOR_RE = re.compile('[\n,\uFF0C\u3001;\uFF1B]+')


def normalize_specification(value):
    return re.sub(r'\s+', ' ', str(value or '')).strip()


def product_specification_options(product):
    return [
        normalize_specification(item)
        for item in SPECIFICATION_SEPARATOR_RE.split(product.specifications or '')
        if normalize_specification(item)
    ]


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            if not self.request.user.is_authenticated:
                return Product.objects.none()
            return Product.objects.filter(seller=self.request.user)

        queryset = Product.objects.filter(status='onsale', stock__gt=0)
        category = self.request.query_params.get('category')
        if category and category != 'all':
            queryset = queryset.filter(category__name=category)

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search) | queryset.filter(
                description__icontains=search
            )
        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_products(self, request):
        queryset = Product.objects.filter(seller=request.user).order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        return OrderDetailSerializer

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def create_order(self, request):
        try:
            data = request.data
            product = Product.objects.get(id=data.get('product_id'), status='onsale')
            quantity = int(data.get('quantity', 1))
            selected_specification = normalize_specification(data.get('selected_specification', ''))

            if product.stock < quantity:
                return Response(
                    {'success': False, 'message': 'Not enough stock.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            specification_options = product_specification_options(product)
            if specification_options:
                if not selected_specification and len(specification_options) == 1:
                    selected_specification = specification_options[0]
                else:
                    selected_match = next(
                        (
                            option
                            for option in specification_options
                            if normalize_specification(option) == selected_specification
                        ),
                        None,
                    )
                    if not selected_match:
                        return Response(
                            {'success': False, 'message': 'Please select a valid product specification.'},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    selected_specification = selected_match

            order_number = f"EB-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
            total_price = product.price * quantity + 60

            order = Order.objects.create(
                order_number=order_number,
                buyer=request.user,
                product=product,
                quantity=quantity,
                selected_specification=selected_specification,
                total_price=total_price,
                recipient_name=data.get('recipient_name'),
                recipient_phone=data.get('recipient_phone'),
                recipient_address=data.get('recipient_address'),
                payment_method=data.get('payment_method', 'cod'),
                status='pending',
            )

            OrderTracking.objects.create(
                order=order,
                title='Order created',
                description='Your order has been created.',
                is_active=True,
            )

            product.stock -= quantity
            product.save()

            return Response({
                'success': True,
                'message': 'Order created.',
                'order_id': order.id,
                'order_number': order_number,
            }, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response(
                {'success': False, 'message': 'Product not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as exc:
            return Response(
                {'success': False, 'message': str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=['get'])
    def tracking(self, request, pk=None):
        order = self.get_object()
        tracking = OrderTracking.objects.filter(order=order).order_by('created_at')
        serializer = OrderTrackingSerializer(tracking, many=True)
        return Response(serializer.data)


class ProductListView(View):
    def get(self, request):
        products = Product.objects.filter(status='onsale')
        return render(request, 'products/list.html', {'products': products})


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'products/detail.html', {'product': product})
