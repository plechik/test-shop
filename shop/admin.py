from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']
    ordering = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'category', 'price', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'category')
        }),
        ('Цена и изображение', {
            'fields': ('price', 'image')
        }),
    )