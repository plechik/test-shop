import os
import uuid
from django.db import models
from django.urls import reverse
from django.utils import timezone
import re
from transliterate import slugify

def get_transliterated_path(instance, filename):
    name, ext = os.path.splitext(filename)
    short_name = name.split('-')[0][:50]
    print(short_name)
    new_name = slugify(short_name)
    # Возвращаем полный путь: папка/имя.расширение
    return os.path.join("products", f"{new_name}{ext}")

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    slug = models.SlugField(unique=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        # Категория ссылается на саму себя, убираем .category
        # Добавляем 'shop:' перед именем пути
        return reverse('shop:product_list') + f'?category={self.id}'
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название товара")
    description = models.TextField(verbose_name="Описание", blank=True)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        verbose_name="Категория",
        related_name='products'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена (руб.)")
    opt_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена опт (руб.)")
    id_1c = models.IntegerField(unique=True, verbose_name="ID в 1С")
    image = models.ImageField(
        upload_to=get_transliterated_path,
        max_length = 500,
        verbose_name="Изображение товара",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={
            'category_slug': self.category.slug,
            'product_slug': self.slug
        })

    def get_image_url(self):
        """Получить URL изображения или заглушку"""
        if self.image and hasattr(self.image, 'url') and self.image.url:
            return self.image.url
        return '/static/images/no-image.jpg'
    
    def __str__(self):
        return f"{self.name} ({self.category})"
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']