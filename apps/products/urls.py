from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'products'

# 創建路由器
router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'orders', views.OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('', views.ProductListView.as_view(), name='list'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='detail'),
]
