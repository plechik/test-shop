from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Что видим в списке
    list_display = ('username', 'email', 'is_staff', 'is_client_opt', 'is_active')
    list_filter = ('is_staff', 'is_client_opt', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

    # Карточка редактирования
    fieldsets = (
        ('Аккаунт', {
            'fields': ('username', 'password')
        }),
        ('Личные данные', {
            'fields': ('first_name', 'last_name', 'email', 'bio')
        }),
        ('Статусы и доступы', { # Объединяем всё важное здесь
            'fields': (
                'is_staff', 
                'is_client_opt', 
                'is_simple_client', 
                'is_active'
            )
        }),
        ('Даты', {
            'classes': ('collapse',),
            'fields': ('last_login', 'date_joined'),
        }),
        ('Расширенные права', {
            'classes': ('collapse',), # Скрываем суперпользователя и группы
            'fields': ('is_superuser', 'groups', 'user_permissions'),
        }),
    )

    # Поля при создании (через кнопку "Добавить")
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'phone_number', 'email', 'password', 'is_staff', 'is_client_opt'),
        }),
    )

    readonly_fields = ('last_login', 'date_joined')