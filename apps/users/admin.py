from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('個人信息', {'fields': ('first_name', 'last_name', 'email', 'phone', 'address', 'bio', 'profile_picture')}),
        ('用戶類型', {'fields': ('user_type', 'store_name', 'is_verified')}),
        ('權限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('重要日期', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    list_display = ('username', 'email', 'user_type_display', 'is_verified_display', 'is_staff', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'user_type', 'is_verified', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'store_name')
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'date_joined')
    
    def user_type_display(self, obj):
        type_colors = {'buyer': 'blue', 'seller': 'green', 'both': 'purple'}
        type_text = {'buyer': '買家', 'seller': '賣家', 'both': '買賣家'}
        color = type_colors.get(obj.user_type, 'gray')
        text = type_text.get(obj.user_type, obj.user_type)
        return format_html(f'<span style="color: {color}; font-weight: bold;">{text}</span>')
    user_type_display.short_description = '用戶類型'
    
    def is_verified_display(self, obj):
        if obj.is_verified:
            return format_html('<span style="color: green; font-weight: bold;">✓ 已認證</span>')
        else:
            return format_html('<span style="color: gray;">未認證</span>')
    is_verified_display.short_description = '認證狀態'
