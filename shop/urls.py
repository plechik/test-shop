from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('products/<int:pk>/delete-image/', views.delete_product_image, name='delete_product_image'),
    
    # Info pages
    path('payment/', views.payment_view, name='payment'),
    path('delivery/', views.delivery_view, name='delivery'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('news/', views.news_view, name='news'),
    path('price/', views.price_view, name='price'),
    
    # User pages
    path('cart/', views.cart_view, name='cart'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('profile/', views.profile_view, name='profile'),
    
    # Product detail (keep last due to slug patterns)
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
]
