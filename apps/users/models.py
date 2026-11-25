from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """自訂用戶模型"""
    USER_TYPE_CHOICES = [
        ('buyer', '買家'),
        ('seller', '賣家'),
        ('both', '買家兼賣家'),
    ]
    
    phone = models.CharField(max_length=20, blank=True, verbose_name='電話')
    address = models.TextField(blank=True, verbose_name='地址')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name='頭像')
    bio = models.TextField(max_length=500, blank=True, verbose_name='個人簡介')
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='buyer', verbose_name='用戶類型')
    store_name = models.CharField(max_length=100, blank=True, verbose_name='店鋪名稱')
    is_verified = models.BooleanField(default=False, verbose_name='是否已驗證')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')

    class Meta:
        verbose_name = '用戶'
        verbose_name_plural = '用戶'
        ordering = ['-created_at']

    def __str__(self):
        return self.username
