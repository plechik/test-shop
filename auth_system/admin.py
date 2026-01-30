from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Добавляем твои поля в список и в формы редактирования
    list_display = ('username', 'is_staff', 'is_client_opt')
    
    # Добавляем поле телефона в карточку пользователя в админке
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('is_client_opt', 'is_simple_client', 'bio')}),
    )
    # Поля для создания пользователя
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительно', {'fields': ('first_name', 'last_name')}),
    )

admin.site.register(User, CustomUserAdmin)