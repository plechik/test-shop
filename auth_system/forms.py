from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        label='Номер телефона',
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Имя пользователя',
    )
    email = forms.EmailField(
        required=True,
        label='Email'
    )   
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='Имя',
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label='Фамилия',
    )

    password1 = forms.CharField(
        label='Пароль',
    )
    password2 = forms.CharField(
        label='Подтвердите пароль',
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone_number", "email", "username")

class CustomLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")