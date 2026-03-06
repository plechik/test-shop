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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ""
        self.fields['password2'].help_text = ""
        
        self.fields['password1'].widget = forms.PasswordInput()
        self.fields['password2'].widget = forms.PasswordInput()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone_number", "email", "username")

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        required=True,
        widget=forms.PasswordInput() # Скрывает вводимые символы
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].help_text = ""