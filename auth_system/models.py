from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Поле username здесь НЕ пишем, оно наследуется автоматически
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="Номер телефона")

    is_staff = models.BooleanField(default=False, verbose_name='Сотрудник')
    is_client_opt = models.BooleanField(default=False, verbose_name='Оптовик')
    is_simple_client = models.BooleanField(default=True, verbose_name='Покупатель')
    bio = models.TextField(max_length=100, blank=True)

    # REQUIRED_FIELDS для обычной модели — это список полей, 
    # которые запросят ПРИДОБАВОК к username, email и password.
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.username} ({self.first_name})"
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"