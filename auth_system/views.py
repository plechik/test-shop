from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomLoginForm

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect("shop:home")
        else:
            messages.error(request, "Исправьте ошибки в форме.")
    else:
        form = CustomUserCreationForm()

    return render(request, "auth_system/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            # AuthenticationForm проверяет данные сама в методе is_valid
            user = form.get_user() 
            login(request, user)
            return redirect("shop:home")
        else:
            messages.error(request, "Неправильный номер телефона или пароль")
    else:
        form = CustomLoginForm()

    return render(request, "auth_system/login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.success(request, "Вы вышли из аккаунта")
    return redirect("shop:home")