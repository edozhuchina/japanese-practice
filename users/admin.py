from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'nickname', 'japanese_level', 'learning_goal', 'date_joined')
    list_filter = ('japanese_level', 'learning_goal')
    search_fields = ('username', 'nickname', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('nickname', 'avatar', 'email', 'japanese_level', 'learning_goal')}),
        ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('重要日期', {'fields': ('date_joined', 'last_login')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
