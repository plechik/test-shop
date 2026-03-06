from django.contrib import admin
from .models import Category, Subcategory, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']
    ordering = ['name']

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'category', 'price', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'id_1c', 'description', 'category')
        }),
        ('Цена и изображение', {
            'fields': ('price', 'opt_price', 'image')
        }),
    )