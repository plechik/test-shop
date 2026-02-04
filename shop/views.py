import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, Category
from .forms import ProductForm

def home_view(request):
    """Главная страница"""
    try:
        latest_products = Product.objects.select_related('category').order_by('-created_at')[:4]
        categories = Category.objects.all()[:6]
    except Exception as e:
        # Если произошла ошибка (например, таблицы не созданы)
        print(f"Ошибка при загрузке товаров: {e}")
        latest_products = []
        categories = []
    
    context = {
        'latest_products': latest_products,
        'categories': categories,
        'title': 'Главная страница'
    }
    return render(request, 'shop/home.html', context)

def product_list(request):
    """Полный список товаров"""
    products = Product.objects.select_related('category').all().order_by('-created_at')
    categories = Category.objects.all()
    
    # Фильтрация по категории
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'title': 'Все товары'
    }
    return render(request, 'shop/list.html', context)

def product_create(request):
    """Создание нового товара"""
    # Проверяем, есть ли категории
    categories = Category.objects.all()
    
    if not categories.exists():
        messages.warning(
            request, 
            'Сначала создайте категории через админ-панель (/admin/)'
        )
        return redirect('shop:home')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                product = form.save()
                messages.success(request, f'✅ Товар "{product.name}" успешно создан!')
                return redirect('shop:home')
            except Exception as e:
                messages.error(request, f'❌ Ошибка при сохранении товара: {e}')
        else:
            messages.error(request, '❌ Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'categories': categories,
        'title': 'Создание товара'
    }
    return render(request, 'shop/product_create.html', context)
def product_detail(request, category_slug, product_slug):
    """Детальная страница товара"""
    product = get_object_or_404(
        Product, 
        slug=product_slug,
        category__slug=category_slug
    )
    context = {
        'product': product,
        'title': product.name
    }
    return render(request, 'shop/product_detail.html', context)

def product_delete(request, pk):
    """Удаление товара"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        next_url = request.GET.get('next', 'shop:home')
        product_name = product.name
        if product.image:
            if os.path.isfile(product.image.path):
                os.remove(product.image.path)
        product.delete()
        messages.success(request, f'Товар "{product_name}" успешно удален!')
        return redirect(next_url)
    
    # Если зашли через GET (просто по ссылке), ничего не удаляем
    return redirect('shop:product_detail', category_slug=product.category.slug, product_slug=product.slug)

def delete_product_image(request, pk):
    """Удаление изображения товара"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        if product.image:
            # Удаляем файл изображения
            product.image.delete(save=False)
            product.image = None
            product.save()
            messages.success(request, 'Изображение товара успешно удалено!')
        else:
            messages.warning(request, 'У товара нет изображения для удаления.')
    
    return redirect('shop:product_update', pk=product.pk)

def product_update(request, pk):
    """Редактирование товара"""
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()
    
    if not categories.exists():
        messages.warning(request, 'Нет доступных категорий. Создайте их через админ-панель.')
        return redirect('shop:home')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            try:
                # Если загружено новое изображение, удаляем старое
                if 'image' in request.FILES and product.image:
                    product.image.delete(save=False)
                
                product = form.save()
                
                # Обработка дополнительных действий
                if 'save_and_continue' in request.POST:
                    messages.success(request, f'Товар "{product.name}" обновлен!')
                    return redirect('shop:product_update', pk=product.pk)
                elif 'save_and_add' in request.POST:
                    messages.success(request, f'Товар "{product.name}" обновлен!')
                    return redirect('shop:product_create')
                else:
                    messages.success(request, f'Товар "{product.name}" успешно обновлен!')
                    return redirect('shop:product_detail', category_slug=product.category.slug, product_slug=product.slug)
                    
            except Exception as e:
                messages.error(request, f'Ошибка при сохранении: {e}')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
        'categories': categories,
        'title': f'Редактирование: {product.name}'
    }
    return render(request, 'shop/product_update.html', context)

# ==================== INFO PAGES ====================

def payment_view(request):
    """Страница оплаты"""
    return render(request, 'partials/info/payment.html', {'title': 'Способы оплаты'})

def delivery_view(request):
    """Страница доставки"""
    return render(request, 'partials/info/delivery.html', {'title': 'Доставка'})

def contacts_view(request):
    """Страница контактов"""
    return render(request, 'partials/info/contacts.html', {'title': 'Контакты'})

def news_view(request):
    """Страница новостей"""
    return render(request, 'partials/info/news.html', {'title': 'Новости'})

def price_view(request):
    """Страница прайс-листа"""
    categories = Category.objects.all()
    return render(request, 'partials/info/price.html', {'title': 'Прайс-лист', 'categories': categories})


# ==================== USER PAGES ====================

def cart_view(request):
    """Страница корзины"""
    # Пока корзина пустая - для демонстрации
    context = {
        'title': 'Корзина',
        'cart_items': [],
        'cart_count': 0,
        'cart_subtotal': 0,
        'cart_total': 0,
    }
    return render(request, 'shop/cart.html', context)

def favorites_view(request):
    """Страница избранного"""
    # Пока избранное пустое - для демонстрации
    context = {
        'title': 'Избранное',
        'favorites': [],
    }
    return render(request, 'shop/favorites.html', context)

def profile_view(request):
    """Страница личного кабинета"""
    return render(request, 'partials/profile.html', {'title': 'Личный кабинет'})