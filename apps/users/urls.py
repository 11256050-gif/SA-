from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'users'

# 創建路由器
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('api/register/', views.register_api, name='api_register'),
    path('api/login/', views.login_api, name='api_login'),
    path('api/logout/', views.logout_api, name='api_logout'),
    path('api/me/', views.get_user_info, name='api_me'),
]
